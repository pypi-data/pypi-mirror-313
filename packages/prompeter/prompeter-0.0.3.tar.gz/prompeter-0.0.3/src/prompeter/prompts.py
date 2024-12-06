from pathlib import Path
import markdown_strings as md
from ruamel.yaml import YAML

from pydantic import BaseModel, model_validator, Field
from pydantic_core import core_schema as cs
from pydantic import GetJsonSchemaHandler, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from enum import Enum, EnumMeta
from typing import List, Union, Optional, Any
import warnings
from pprint import pprint

yaml = YAML(typ='rt')


# see https://github.com/pydantic/pydantic/issues/7161#issuecomment-2154496296
class OptionalNotNullableModel(BaseModel):

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Remove nullablity from optional fields."""
        _json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(_json_schema)
        if 'properties' not in json_schema:
            return _json_schema
        required = json_schema.get('required', [])
        changed = False
        for key, prop in json_schema['properties'].items():
            if prop.get('default','') is None:
                if key in required:
                    continue
                # remove nullablilty
                changed = True
                del prop['default']
                if not (prop.get('anyOf') is None):
                    non_nullable = [ t for t in prop['anyOf'] if t.get('type') != 'null']
                    if len(non_nullable) == 1:
                        del prop['anyOf']
                        prop.update(non_nullable[0])
                    else:
                        prop['anyOf'] = non_nullable
            else:
                # This is needed for "required" properties (no default value set), when setting a field description to '
                # avoid having an "allOf" list of one object with the #ref as only entry.
                if prop.get('allOf') is None:
                    continue
                changed = True
                non_nullable = [t for t in prop['allOf'] if t.get('type') != 'null']
                if len(non_nullable) == 1:
                    del prop['allOf']
                    prop.update(non_nullable[0])
                else:
                    prop['allOf'] = non_nullable
        return json_schema if changed else _json_schema


# Define sets of keywords specifying classes/types of prompts
class EnumMetaWithContain(EnumMeta):
    def __contains__(self, item):
        return item in self.__members__.keys()

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema['enum'] = list(set(json_schema['enum']))
        return json_schema


class PromptTask(str, Enum, metaclass=EnumMetaWithContain):
    """
    The PromptTask Enum class specify the type of task the prompt template is intended for

    NOTE: Currently only question_answer is supported.
    """
    question_answer = 'question_answer'
    # Aliases for question_answer
    QnA = 'question_answer'
    qna = 'question_answer'
    QA = 'question_answer'
    qa = 'question_answer'

    summarization = 'summarization'
    # Aliases for summarization
    sum = 'summarization'

    # Done in the metaclass instead to affect all enum classes
    #@classmethod
    #def __get_pydantic_json_schema__(
    #        cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    #) -> JsonSchemaValue:
    #    json_schema = handler(core_schema)
    #    json_schema = handler.resolve_ref_schema(json_schema)
    #    json_schema['enum'] = list(set(json_schema['enum']))
    #    return json_schema


class PromptMethod(str, Enum, metaclass=EnumMetaWithContain):
    """
    The PromptMethod Enum class specify which methods the prompt template uses
    """
    zero_shot = 'zero_shot'
    # aliases
    zeroshot = 'zero_shot'

    few_shot = 'few_shot'
    # aliases
    fewshot = 'few_shot'

    RAG = 'RAG'
    # aliases
    rag = 'RAG'
    retrival_argumented_generation = 'RAG'


class PromptStyle(str, Enum, metaclass=EnumMetaWithContain):
    """
    The style of the prompt template, indicates which model type the prompt
    template is intended for. Whether continuation models, instruction finetuned
    models or dialogue finetuned models
    """
    continuation = 'continuation'
    instruct = 'instruct'
    dialog = 'dialog'
    chat = 'dialog'


class Language(str, Enum, metaclass=EnumMetaWithContain):
    """
    The Language Enum class specify the language of the text in the prompt template
    """
    danish = 'danish'
    # aliases
    da = 'danish'

    english = 'english'
    # aliases
    en = 'english'


#@dataclass
class PromptCategory(BaseModel):
    """
    A dataclass for the prompt template to hold metadata categorising the template
    """
    task: PromptTask
    style: PromptStyle
    methods: List[PromptMethod]
    language: Language

    # When pydantic validate enum values, it is possible to supply a string. This is accepted if the string represent 
    # an enum value (but not a member), and enum aliases are formed by adding more members with the same value.
    # To exploit the aliases one needs to use the __getitem__ method of the enum class (instead of __call__), thus 
    # using EnumClass[<member>] instead of EnumClass(<value>)
    @model_validator(mode='before')
    @classmethod
    def get_enum_attr(cls, data: Any) -> Any:
        category_members = {'task': PromptTask, 'style': PromptStyle, 'language': Language}
        if isinstance(data, dict):
            for member_name, member_enum in category_members.items():
                if member_name in data:
                    if isinstance(data[member_name], str):
                        if data[member_name] in member_enum:
                            data[member_name] = member_enum[data[member_name]]
            if 'methods' in data:
                if isinstance(data['methods'], list):
                    validated_methods = []
                    for method in data['methods']:
                        if isinstance(method, str):
                            if method in PromptMethod:
                                validated_methods.append(PromptMethod[method])
                                continue
                        validated_methods.append(method)
                    data['methods'] = validated_methods
        return data


# Helper classes and methods
class Markup(str, Enum):
    """
    The Markup Enum class list the possible markup that can be applied to various input sections in the prompt template.

    NOTE: Currently the markup will be formatted with Markdown syntax
    """
    unordered_list = 'unordered_list'
    quote = 'quote'
    bold = 'bold'
    italics = 'italics'


def markdown(text: str, markup: Markup | None = None) -> str:
    """markdown formats a given text with the requested markup according to the Markdown syntax

    :param text: string to apply markup on
    :param markup: Type of markup to apply
    :return: string formatted with Markdown syntax
    """
    if markup is None:
        return text

    if markup == Markup.unordered_list:
        return md.unordered_list([text])

    if markup == Markup.quote:
        return md.blockquote(text)

    if markup == Markup.bold:
        return md.bold(text)

    if markup == Markup.italics:
        return md.italics(text)


# Classes for input to prompt templates
##@dataclass
#class PromptInput:
class PromptInput(BaseModel):
    """
    PromptInput is a basic class for inputs to a prompt template which have some associate metadata. 
    It could e.g. be retrived snippets of context for a RAG solution
    """
    text: str
    metadata: Optional[dict] = Field(default_factory=dict)


class QnAPromptInput(BaseModel):
    """
    QnAPromptInput is a class for Question and Answer examples for few shot learning in prompt templates.
    It collects two basic PromptInput, the user instruction and the assistent answer and then an optional
    list of context or background PromptInput

    Note: For now it is named specifically for few shot question-answers examples, but it might be applicable for any
    few shot examples.
    """
    question: Union[PromptInput, dict, str]
    answer: Union[PromptInput, dict, str]
    context: Optional[List[Union[PromptInput, dict, str]]] = None


# Parts of a prompt template
class PromptTextSnippet(BaseModel):
    """
    Basic prompt template building block. Represent a text snippet in a prompt template.
    It might be the system prompt, or it might be a part of a prompt section.
    The PromptTextSnippet basically consist of a text which can holds a number of variables in the form {var}, if the
    variables are related to counting of an inputted text (e.g. example 2 of 3 examples) then they are handled explicitly
    by the boolean numbered and counted, respectively, and the variable name is stored in num_var and count_var,
    respectively. These variables will be handled automatically by the prompt template, whereas other metadata variables
    needs to be provided together with an accompaning prompt input adhering to the PromptInput class.
    """
    text: str = Field(description='Template text snippet with optional variables in the form {var}.')
    seperator: str = Field(default='\n', description='Separator to be used between text snippet and inputted text when the text snippet is part of a prompt section.')
    numbered: bool = Field(default=False, description='Indicate if a variable represents a count eg \"example nr {#} of a total of 3 examples\"')
    num_var: str = Field(default='#', description='The variable to be counted')
    counted: bool = Field(default=False, description='Indicate if a variable represents a total count eg \"example nr 2 of a total of {tot} examples\"')
    count_var: str = Field(default='tot', description='The variable to be substituted for the total count')
    meta_data_vars: List[str] = Field(default_factory=list, description='The variables used in the template snippet, they will have to be supplied as metadata for prompt input')

    # TODO: Delete, if not used
    # To allow for text as a positional argument
    #def __init__(self, text: str, **the_other_arguments: Any) -> None:
    #    super(PromptTextSnippet, self).__init__(text=text, **the_other_arguments)

    @model_validator(mode='after')
    def check_variables_in_text(self: 'PromptTextSnippet') -> 'PromptTextSnippet':
        # Nb according to https://docs.pydantic.dev/latest/concepts/validators/#model-validators
        # the assert statements are disabled if python is run with optimization - maybe it needs to
        # be replaced by if not -> raise and then a fitting exception
        if self.numbered:
            assert f'{{{self.num_var}}}' in self.text, f'The text does not contain reference to a number eventhough it is reported to be numbered.\nText: {self.text}\nnum var: {self.num_var}'
        if self.counted:
            assert f'{{{self.count_var}}}' in self.text, f'The text does not contain reference to a total count, eventhough it is reported to that it should be counted.\nText: {self.text}\nCount var: {self.count_var}'
        for meta_var in self.meta_data_vars:
            assert f'{{{meta_var}}}' in self.text, f'The text does not contain reference to {meta_var}, eventhough it is listed as a meta data variable'
        return self

    @model_validator(mode='after')
    def ensure_no_additional_newlines(self: 'PromptTextSnippet') -> 'PromptTextSnippet':
        """When the text of a snippet is left empty (in prompt developing) ensure that the default seperation newline 
        is also removed"""
        if len(self.text) == 0:
            self.seperator = ''
        return self
            
    
    def get_text(self, number: Union[int, None] = None, total_count: Union[int, None] = None, **metadata) -> str:
        """
        Class method to return the class text with the variables substituted

        :param number: possible integer to substitute for the class num_var variable
        :param total_count: possible integer to substitute for the class count_var variable
        :param metadata: possible extra keyword arguments with keywords being the variable names to substitute with the
                         values (strings) provided
        :return: text with the variables substituted
        """
        prepared_text = self.text
        if self.numbered:
            if number is None:
                raise ValueError('a number must be provided')
            prepared_text = prepared_text.replace(f'{{{self.num_var}}}', str(number))
        if self.counted:
            if total_count is None:
                raise ValueError('a total count must be provided')
            prepared_text = prepared_text.replace(f'{{{self.count_var}}}', str(total_count))
        for meta_var in self.meta_data_vars:
            if meta_var not in metadata.keys():
                raise ValueError(f'{meta_var} and a value for it, must be provided')
            prepared_text = prepared_text.replace(
                f'{{{meta_var}}}',
                metadata[meta_var] if metadata[meta_var] is not None else f'{{{meta_var}:<None>}}'
            )
        return prepared_text


#class PromptSection(BaseModel):
class PromptSection(OptionalNotNullableModel):
    """
    PromptSection class gives a section of the prompt template, which can take a prompt input and pre or append a
    prompt template text snippet, which will optionally be formatted with a markup.
    """
    text_before: Optional[PromptTextSnippet] = Field(default=None, description='Optional text introducing an section')
    text_after: Optional[PromptTextSnippet] = Field(default=None, description='Optional text ending an section')
    prompt_text_markup: Markup | None = Field(default=None, description='Optional formatting of an section')

    # Handle receiving strings instead of PomptTextSnippets (or dicts with corresponding fields), by catching this 
    # before the input is validated
    @model_validator(mode='before')
    @classmethod
    def cast_str_to_prompt_text_snippets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for key in ['text_before', 'text_after']:
                if key in data:
                    if isinstance(data[key], str):
                        data[key] = PromptTextSnippet(text=data[key])
        return data

    def get_text(self, prompt_text: Union[PromptInput, str], number: Union[int, None] = None, total_count: Union[int, None] = None, **metadata) -> str:
        """
        Class method to return a prompt input with prepended and appended text snippets, where variables have been substituted

        :param prompt_text: Prompt input to be inserted into the prompt template
        :param number: Optional integer to substitute for the num_var variable in the prompt template snippets 
                       "text before" and "text after". This will most often be used internally when constructing
                       the prompt template when using the RepeatablePromptSection og QnAFewShotPromptSection class.
        :param total_count: Optional integer to substitute for the count_var variable in the prompt template snippets 
                            "text before" and "text after". This will most often be used internally when constructing
                            the prompt template when using the RepeatablePromptSection og QnAFewShotPromptSection class.
        :param metadata: Addtional keyword argument to be added to the prompt input metadata
        :return: A section for the final prompt with the templated filled according to the prompt input
        """
        if type(prompt_text) is PromptInput:
            # Split the promptInput
            metadata = prompt_text.metadata | metadata
            text = prompt_text.text
        else:
            text = prompt_text
        prepared_text = markdown(text, self.prompt_text_markup)
        if self.text_before is not None:
            prepared_text = self.text_before.get_text(number=number, total_count=total_count, **metadata) + self.text_before.seperator + prepared_text
        if self.text_after is not None:
            prepared_text = prepared_text + self.text_after.seperator + self.text_after.get_text(number=number, total_count=total_count, **metadata)
        return prepared_text


class RepeatablePromptSection(PromptSection):
    """
    RepeatablePromptSection class gives a section of the prompt template like the PromptSection, but in addition to a 
    text before and a text after, it also contains a main text section, which in itself is also a promptSection. 
    The main text will be repeated when a prompt is constructed the number of times needed based on the length of the
    list of prompt input supplied to the class method get_text.
    """
    # Inherited
    # text_before: PromptTextSnippet
    # text_after: PromptTextSnippet
    main_text: PromptSection = Field(description='Template for a section of the prompt that will be repeated as many times as needed depending on the input supplied for template.')
    seperator: str = Field(default='\n', description='Seperator between the repeated sections')

    def get_text(self, prompt_texts: List[Union[PromptInput, dict, str]], **metadata) -> str:
        """
        Class method to construct a prompt section from a list of prompt input which will be prepended and appended 
        with the text snippets indicated by the main_text class variable. This repeated block will be pre- and appended 
        with the text snippets indicated given in the text_before and text_after, respectively.
        :param prompt_texts: List of prompt inputs
        :param metadata: any extra keyword arguments provided which will be added to the prompt input metadata
        :return: A section for the final prompt with the templated filled according to the prompt input
        """
        num_texts = len(prompt_texts)
        prepared_texts = []
        for i, prompt_text in enumerate(prompt_texts):
            if type(prompt_text) is dict:
                prompt_text = PromptInput.model_validate(prompt_text)
            prepared_texts.append(
                self.main_text.get_text(prompt_text=prompt_text, number=i + 1, total_count=num_texts, **metadata))

        return super().get_text(prompt_text=self.seperator.join(prepared_texts), total_count=num_texts, **metadata)


class QnAFewShotPromptSection(PromptSection):
    """
    QnAFewShotPromptSection class gives a section of the prompt template like the RepeatablePromptSection, but instead
    of a single main text section, it contains two prompt sections (question_text and answer_text) and an optional
    RepeatablePromptSection (context_text), where these two are three prompt sections are concatenated and then repeated
    the number of times needed based on the length of the list of prompt input supplied to the class method get_text.
    """
    # Inherited
    # text_before: PromptTextSnippet
    # text_after: PromptTextSnippet
    text_before_set: Optional[PromptTextSnippet] = Field(default=None, description='Optional text preceding each example')
    text_after_set: Optional[PromptTextSnippet] = Field(default=None, description='Optional text succeding each example')
    # Todo: consider removing _text from question, answer and context
    question_text: PromptSection = Field(description='Prompt template specification for the question text of the few shot examples')
    answer_text: PromptSection = Field(description='Prompt template specification for the answer text of the few shot examples')
    context_text: Optional[RepeatablePromptSection] = Field(default=None, description='Optional prompt template specification for the context text of the few shot examples')
    inner_seperator: str = Field(default='\n\n', description='Seperator between the elements of an example - (context), question and answer')
    outer_seperator: str = Field(default='\n\n---\n\n', description='Seperator between the examples')

    def get_text(self, prompt_texts: List[Union[QnAPromptInput, dict, str]], **metadata) -> str:
        """
        Class method to construct a prompt section from a list of prompt input which will be prepended and appended 
        with the text snippets indicated by the main_text class variable. This repeated block will be pre- and appended 
        with the text snippets indicated given in the text_before and text_after, respectively.
        :param prompt_texts: List of QnAPrompt inputs
        :param metadata: any extra keyword arguments provided which will be added to the prompt input metadata
        :return: A section for the final prompt with the templated filled according to the prompt input
        """
        num_texts = len(prompt_texts)
        prepared_texts = []
        # If context is given to the qna pairs then we might need to update numbering
        if self.context_text is not None:
            context_metadata = metadata
            context_numbering_vars = set()
            context_counting_vars = set()
            if self.context_text.text_before is not None:
                if self.context_text.text_before.numbered:
                    # then this will relate to the outer numbering and we must move it to metadata
                    outer_num_var = '_outer_' + self.context_text.text_before.num_var
                    context_numbering_vars.add(outer_num_var)
                    self.context_text.text_before.text = self.context_text.text_before.text.replace(
                        f'{{{self.context_text.text_before.num_var}}}', f'{{{outer_num_var}}}')
                    self.context_text.text_before.meta_data_vars.append(outer_num_var)
                    self.context_text.text_before.numbered = False
                if self.context_text.text_before.counted:
                    # then this will relate to the outer numbering and we must move it to metadata
                    outer_count_var = '_outer_' + self.context_text.text_before.count_var
                    context_counting_vars.add(outer_count_var)
                    self.context_text.text_before.text = self.context_text.text_before.text.replace(
                        f'{{{self.context_text.text_before.count_var}}}', f'{{{outer_count_var}}}')
                    self.context_text.text_before.meta_data_vars.append(outer_count_var)
                    self.context_text.text_before.counted = False
            if self.context_text.text_after is not None:
                if self.context_text.text_after.numbered:
                    # then this will relate to the other numbering and we must move it to metadata
                    outer_num_var = '_outer_' + self.context_text.text_after.num_var
                    context_numbering_vars.add(outer_num_var)
                    self.context_text.text_after.text = self.context_text.text_after.text.replace(
                        f'{{{self.context_text.text_after.num_var}}}', f'{{{outer_num_var}}}')
                    self.context_text.text_after.meta_data_vars.append(outer_num_var)
                    self.context_text.text_after.numbered = False
                if self.context_text.text_after.counted:
                    # then this will relate to the other numbering and we must move it to metadata
                    outer_count_var = '_outer_' + self.context_text.text_after.count_var
                    context_counting_vars.add(outer_count_var)
                    self.context_text.text_after.text = self.context_text.text_after.text.replace(
                        f'{{{self.context_text.text_after.count_var}}}', f'{{{outer_count_var}}}')
                    self.context_text.text_after.meta_data_vars.append(outer_count_var)
                    self.context_text.text_after.counted = False
        for i, prompt_text in enumerate(prompt_texts):
            if type(prompt_text) is dict:
                prompt_text = QnAPromptInput.model_validate(prompt_text)

            qna_section_text = []

            # Handle any text that is repeated before each of the qna sets
            if self.text_before_set is not None:
                qna_section_text.append(self.text_before_set.get_text(number=i + 1, total_count=num_texts, **metadata))

            # Handle context for the qna
            if (self.context_text is not None) and (prompt_text.context is not None):
                for outer_num_var in context_numbering_vars:
                    context_metadata = context_metadata | {outer_num_var: str(i + 1)}
                for outer_count_var in context_counting_vars:
                    context_metadata = context_metadata | {outer_count_var: str(num_texts)}
                qna_section_text.append(self.context_text.get_text(prompt_texts=prompt_text.context, **context_metadata))

            # Handle question (required)
            qna_section_text.append(
                self.question_text.get_text(prompt_text=prompt_text.question, number=i + 1, total_count=num_texts, **metadata))

            # Handle answer (required)
            qna_section_text.append(
                self.answer_text.get_text(prompt_text=prompt_text.answer, number=i + 1, total_count=num_texts,
                                            **metadata))

            # Handle any text that appear after each of the qna sets
            if self.text_after_set is not None:
                qna_section_text.append(self.text_after_set.get_text(number=i + 1, total_count=num_texts, **metadata))

            # Concatenate text before a set, the sets context, question, answer and the text after the set
            prepared_texts.append(self.inner_seperator.join(qna_section_text))

        # Concatenate all the qna sets and handle text starting and ending the section
        return super().get_text(prompt_text=self.outer_seperator.join(prepared_texts), total_count=num_texts, **metadata)
    
    def get_dialog_messages(self, prompt_texts: List[Union[QnAPromptInput, dict, str]], **metadata) -> List[dict]:
        """
        Class method to construct a list of prompt message-dicts from a list of prompt input which will be prepended and appended 
        with the text snippets indicated by the main_text class variable. 
        As opposed to the get_text method this repeated block will NOT be pre- and appended 
        with the text snippets indicated given in the text_before_set and text_after_set nor will the entire section be 
        pre- or appended with the text_before or text_after since this should follow from the message dialogue format.
        :param prompt_texts: List of QnAPrompt inputs
        :param metadata: any extra keyword arguments provided which will be added to the prompt input metadata
        :return: A section for the final prompt with the templated filled according to the prompt input
        """
        if (self.text_before is not None) or (self.text_after is not None) or (self.text_before_set is not None) or (self.text_after_set is not None):
            warnings.warn('Notice that no prepending or appending of text is applied, eventhough it have explicitly been provided')
        dialogue = []
        for prompt_text in prompt_texts:
            if type(prompt_text) is dict:
                prompt_text = QnAPromptInput.model_validate(prompt_text)

            user_message = ''

            # Handle context for the qna
            if (self.context_text is not None) and (prompt_text.context is not None):
                user_message = self.context_text.get_text(prompt_texts=prompt_text.context, **metadata) + self.inner_seperator

            # Handle question (required)
            user_message = user_message + self.question_text.get_text(prompt_text=prompt_text.question, **metadata)
            dialogue.append({
                "role": "user",
                "content": user_message
            })
            # Handle answer (required)
            dialogue.append({
                "role": "assistant",
                "content": self.answer_text.get_text(prompt_text=prompt_text.answer, **metadata)
            })

        return dialogue


#@dataclass
#class PromptTemplate(BaseModel):
class PromptTemplate(OptionalNotNullableModel):
    keywords: Optional[List[str]] = Field(default=None, description='List of keywords that determines the category of the template')
    category: PromptCategory | None = Field(default=None, description='Category object, classifies the template. Required unless keywords have been supplied')
    system: PromptTextSnippet = Field(default=PromptTextSnippet(text='',seperator=''), description='System part of the prompt')
    examples: Optional[QnAFewShotPromptSection] = Field(default=None, description='Prompt template section for Few shot examples. Required if specified in category/keywords') 
    context: Optional[RepeatablePromptSection] = Field(default=None, description='Prompt template section for retrieved context. Required if specified in category/keywords')
    question: PromptSection = Field(default=PromptSection(text_before=PromptTextSnippet(text='',seperator=''),text_after=PromptTextSnippet(text='',seperator='')), description='Prompt template for the user question')
    seperator: str = '\n\n'

    # Handle receiving strings instead of PomptTextSnippets (or dicts with corresponding fields), by catching this
    # before the input is validated
    @model_validator(mode='before')
    @classmethod
    def cast_str_to_prompt_text_snippets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for key in ['system']:
                if key in data:
                    if isinstance(data[key], str):
                        data[key] = PromptTextSnippet(text=data[key])
        return data

    @model_validator(mode='after')
    def validate_category(self: 'PromptTemplate') -> 'PromptTemplate':
        if self.category is None:
            if self.keywords is None:
                raise KeyError('Either a list of keywords or a category dict/class must be provided')
            # Handle task category
            task = None
            for keyword in self.keywords:
                if keyword in PromptTask:
                    task = PromptTask[keyword]
                    self.keywords.remove(keyword)
            if task is None:
                raise KeyError(f'Among the keywords must be one that specify the task of the prompt template. The following keywords were provided: {", ".join(self.keywords)}. One of {", ".join([task.name for task in PromptTask])}')
            # Handle the style category
            style = None
            for keyword in self.keywords:
                if keyword in PromptStyle:
                    style = PromptStyle[keyword]
                    self.keywords.remove(keyword)
            if style is None:
                raise KeyError(f'Among the keywords must be one that specify the style of the prompt template and thus the indended model type. The following keywords were provided: {", ".join(self.keywords)}. One of {", ".join([style.name for style in PromptStyle])}')
            # Handle method category
            methods = []
            for keyword in self.keywords:
                if keyword in PromptMethod:
                    methods.append(PromptMethod[keyword])
                    self.keywords.remove(keyword)
            # Handle Language
            language = None
            for keyword in self.keywords:
                if keyword in Language:
                    language = Language[keyword]
                    self.keywords.remove(keyword)
            if language is None:
                raise KeyError(f'The language should be specified in among the keywords. Provided keywords: {", ".join(self.keywords)}. Available languages {", ".join([lang.name for lang in Language])}')
            self.category = PromptCategory(task=task, style=style, methods=methods, language=language)
        if PromptMethod.RAG in self.category.methods:
            if self.context is None:
                raise KeyError('A context section is missing, but RAG is listed as a prompt method')
        if PromptMethod.few_shot in self.category.methods:
            if self.examples is None:
                raise KeyError('An examples section is missing, but few_shot is listed as a prompt method')
        return self

    def construct_prompt(self,
                         user_prompt: Union[PromptInput, dict, str],
                         example_texts: Optional[List[Union[QnAPromptInput, dict, str]]] = None, 
                         context_texts: Optional[List[Union[PromptInput, dict, str]]] = None, 
                         **metadata
                         ) -> str:
        texts_to_join = [self.system.get_text(**metadata)]
        if example_texts is None:
            if self.examples is not None:
                raise KeyError('Missing argument "example_texts"')
        else:
            texts_to_join.append(self.examples.get_text(prompt_texts=example_texts, **metadata))
        if context_texts is None:
            if self.context is not None:
                raise KeyError('Missing argument "context_texts"')
        else:
            texts_to_join.append(self.context.get_text(prompt_texts=context_texts, **metadata))
        texts_to_join.append(self.question.get_text(prompt_text=user_prompt, **metadata))
        prompt = self.seperator.join(texts_to_join)
        return prompt

    def construct_messages(self,
                           user_prompt: Union[PromptInput, dict, str],
                           example_texts: Optional[List[Union[QnAPromptInput, dict, str]]]=None,
                           context_texts: Optional[List[Union[PromptInput, dict, str]]]=None,
                           **metadata
                           ) -> list[dict]:
        if self.category.style is PromptStyle('dialog'):
            messages = [
                {
                    "role": "system",
                    "content": self.system.get_text(**metadata)
                }]
            if example_texts is None:
                if self.examples is not None:
                    raise KeyError('Missing argument "example_texts"')
            else:
                messages.append(self.examples.get_dialog_messages(prompt_texts=example_texts, **metadata))
            texts_to_join = []
            if context_texts is None:
                if self.context is not None:
                    raise KeyError('Missing argument "context_texts"')
            else:
                texts_to_join.append(self.context.get_text(prompt_texts=context_texts, **metadata))
            texts_to_join.append(self.question.get_text(prompt_text=user_prompt, **metadata))
            messages.append([{
                    "role": "user",
                    "content": self.seperator.join(texts_to_join)
                }
            ])
            return messages
        else:
            if self.category.style is PromptStyle('continuation'):
                warnings.warn('The prompt template style is indicated to be intended for a continuation model, thus providing the model with message formatted input will probably not work as expected. The provided messages are intended for instruction type models')
            # Default to instruction formatted message output
            texts_to_join = [self.system.get_text(**metadata)]
            if example_texts is None:
                if self.examples is not None:
                    raise KeyError('Missing argument "example_texts"')
            else:
                texts_to_join.append(self.examples.get_text(prompt_texts=example_texts, **metadata))
            if context_texts is None:
                if self.context is not None:
                    raise KeyError('Missing argument "context_texts"')
            else:
                texts_to_join.append(self.context.get_text(prompt_texts=context_texts, **metadata))
            messages = [
               {
                   "role": "system",
                   "content": self.seperator.join(texts_to_join)
               },
               {
                   "role": "user",
                   "content": self.question.get_text(prompt_text=user_prompt, **metadata),
               }
            ]
            return messages

    # TODO: Add a pre_construct_prompt method, that sets the few_shot_examples and maybe some metadata


def get_prompt_template(path_prompt_template: Path | str) -> PromptTemplate:
    if isinstance(path_prompt_template, str):
        path_prompt_template = Path(path_prompt_template)

    if path_prompt_template.suffix == '.json':
        template = prompt_template_from_json(path_prompt_template)
    elif path_prompt_template.suffix == '.yaml':
        template = prompt_template_from_yaml(path_prompt_template)
    else:
        raise FileNotFoundError(f'{path_prompt_template.suffix} is not a supported file type')
    return template


def prompt_template_from_json(path_prompt_template: Path) -> PromptTemplate:
    with open(path_prompt_template, 'r', encoding='utf-8') as fp:
        template = PromptTemplate.model_validate_json(fp.read())

    return template


def remove_leafless_branches_from_dict(a_dict: dict) -> dict:
    new_dict = {}
    for k, v in a_dict.items():
        if isinstance(v, dict):
            v = remove_leafless_branches_from_dict(v)
        if v is not None:
            new_dict[k] = v
    return new_dict or None


def prompt_template_from_yaml(path_prompt_template: Path) -> PromptTemplate:
    with open(path_prompt_template, 'r', encoding='utf-8') as fp:
        prompt_template_data = yaml.load(fp)
    prompt_template_data = remove_leafless_branches_from_dict(prompt_template_data)
    template = PromptTemplate.model_validate(prompt_template_data)
    return template

def print_template_with_placeholders(
        prompt_template: PromptTemplate, 
        question_placeholder:str = '<user_question>', 
        context_placeholder:str = '<context>', 
        number_context:int = 2, 
        ex_question_placeholder:str = '<example_question>',
        ex_answer_placeholder:str = '<example_answer>',
        number_examples:int = 2
) -> str:
    args = {}
    # Add metadata vars for systemprompt
    args = args | {var: '{' + var + '}' for var in prompt_template.system.meta_data_vars}
    # metadata for user prompt
    user_prompt_meta = {var: '{' + var + '}' for var in get_meta_data_variable_set(prompt_template.question)}
    # Add the user prompt
    args = args | {'user_prompt': PromptInput(text=question_placeholder, metadata=user_prompt_meta)}
    # If prompt template has context:
    if prompt_template.context is not None:
        # prepare placeholder metadata for context 
        context_meta = {var: '{' + var + '}' for var in get_meta_data_variable_set(prompt_template.context)}
        # add context arg
        args = args | {'context_texts': number_context*[PromptInput(text=context_placeholder, metadata=context_meta)]}
    if prompt_template.examples is not None:
        # prepare placeholder metadata for example question and answer 
        ex_question_meta = {var: '{' + var + '}' for var in get_meta_data_variable_set(prompt_template.examples.question_text)}
        ex_answer_meta = {var: '{' + var + '}' for var in get_meta_data_variable_set(prompt_template.examples.answer_text)}
        # Add additional possible metadata to general args
        args = args | {var: '{' + var + '}' for var in get_meta_data_variable_set(prompt_template.examples)}
        qna_prompt_input = {
            'question': PromptInput(text=ex_question_placeholder, metadata=ex_question_meta), 
            'answer': PromptInput(text=ex_answer_placeholder, metadata=ex_answer_meta)
        }
        if prompt_template.examples.context_text is not None:
            context_meta = {var: '{' + var + '}' for var in get_meta_data_variable_set(prompt_template.examples.context_text)}
            qna_prompt_input = qna_prompt_input | {'context': number_context*[PromptInput(text=context_placeholder, metadata=context_meta)]}
        args = args | {'example_texts': number_examples*[QnAPromptInput(**qna_prompt_input)]}
    
    if prompt_template.category.style is PromptStyle('continuation'):
        return prompt_template.construct_prompt(**args)
    else:
        # either prompt_template.category.style is PromptStyle('instruct'):
        # or prompt_template.category.style is PromptStyle('dialog'):
        messages = prompt_template.construct_messages(**args)
        return print_messages(messages)
    
        
def get_meta_data_variable_set(prompt_block: Union[PromptSection, RepeatablePromptSection, QnAFewShotPromptSection]) -> set:
    meta_var_set = set()
    if isinstance(prompt_block, RepeatablePromptSection):
        meta_var_set = get_meta_data_variable_set(prompt_block.main_text)
    for prompt_snippet in ['text_before', 'text_after', 'text_before_set', 'text_after_set']:
        if hasattr(prompt_block, prompt_snippet):
            if getattr(prompt_block, prompt_snippet) is not None:
                meta_var_set = meta_var_set | set(getattr(prompt_block, prompt_snippet).meta_data_vars)
    return meta_var_set

def print_messages(messages: list[dict]) -> str:
    """Prints a llama-style-like text prompt from a ollama style list of payload messages
    
    NB: the llama-style is from out of my memory. It should only serve for illustrative purposes
    
    NB: a starting assistent-token (or tag) will not be added
    """
    output_str = ''
    for message in messages:
        if message['role'] == 'system':
            output_str = output_str + '<system>\n' + message['content'] + '\n</system>\n'
        elif message['role'] == 'user':
            output_str = output_str + '<user>\n' + message['content'] + '\n</user>\n'
        elif message['role'] == 'assistant':
            output_str = output_str + '<assistant>\n' + message['content'] + '\n</assistant>\n'
    if output_str[-1] == '\n':
        output_str = output_str[:-1]
    return output_str

from prompeter.prompts import PromptTemplate
import json
from pprint import pprint

from pydantic.json_schema import GenerateJsonSchema

class MyGenerateJsonSchema(GenerateJsonSchema):
    def generate(self, schema, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        # Reorder schema
        #json_schema['$defs'] = json_schema.pop('$defs')
        preferred_entry_order = ['title', "description", "type", "$ref", "required", "additionalProperties", "enum", "items", "properties"]
        new_order = [key for key in preferred_entry_order if key in json_schema.keys()]
        json_schema = {key: json_schema.pop(key) for key in new_order} | json_schema
        preferred_ref_order = ['PromptTextSnippet', 'PromptSection', 'RepeatablePromptSection', 'QnAFewShotPromptSection', 'PromptMethod', 'PromptStyle', 'PromptTask', 'Language', 'PromptCategory', 'Markup']
        new_ref_order = [key for key in preferred_ref_order if key in json_schema['$defs'].keys()]
        json_schema['$defs'] = {key: json_schema['$defs'].pop(key) for key in new_ref_order} | json_schema['$defs']
        return json_schema


print(json.dumps(PromptTemplate.model_json_schema(schema_generator=MyGenerateJsonSchema), indent=2))

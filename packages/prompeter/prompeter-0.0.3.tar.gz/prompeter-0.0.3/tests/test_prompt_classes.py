import pytest
import json
from pydantic import ValidationError
import src.prompeter.prompts as prompts

def test_PromptCategory():
    prompt_cat = prompts.PromptCategory(task='question_answer', style='instruct', methods=['zero_shot', 'rag'], language='danish')
    assert prompt_cat.task == 'question_answer'
    assert isinstance(prompt_cat.task, prompts.PromptTask)
    assert prompt_cat.style == 'instruct'
    assert isinstance(prompt_cat.style, prompts.PromptStyle)
    assert prompt_cat.language == 'danish'
    assert isinstance(prompt_cat.language, prompts.Language)
    assert 'few_shot' not in prompt_cat.methods
    for method in prompt_cat.methods:
        assert isinstance(method, prompts.PromptMethod)

def test_PromptCategory_validation_err():
    with pytest.raises(ValidationError) as except_info:
        prompt_cat = prompts.PromptCategory(task='ner', methods=['few_shot'], language='danish')
    assert except_info.type == ValidationError


def test_PromptText_Basic():
    system_prompt_text = '''Du er en AI-assistent der benyttes af sundhedsfagligt personale i en kommune. Din bruger vil stille spørgsmål til 
    eller efterspørge oplysninger om korrekte procedurer inden for sit professionelle felt, der handler om at levere 
    effektiv og målrettet pleje og omsorg for borgere i kommunen med høj standard og kvalitet.

    Du skal besvare brugerens spørgsmål kort, fagligt præcist og i en professionel tone.

    Efter hver sætning i dit svar skal du om muligt henvise til kilden hvorpå dit svar er baseret i formen 
    ”Kilde: ’henvisning’, ’side’”, hvor ’henvisning’ og ’side’ er baseret på de oplysninger, der er gjort tilgængelige 
    for dig i de informationer og den kontekst, som om lidt gøres tilgængelig for dig under KONTEKST.'''
    prompt_text = prompts.PromptTextSnippet(text=system_prompt_text)
    assert prompt_text.text == system_prompt_text
    assert prompt_text.get_text() == system_prompt_text
    assert not prompt_text.numbered
    assert not prompt_text.counted
    assert not prompt_text.meta_data_vars, "List of metadata variables should be empty"


def test_PromptText():
    examples_text_before = 'Herunder er {total} eksempler på gode svar på en brugers spørgsmål'
    prompt_text = prompts.PromptTextSnippet(text=examples_text_before, counted=True, count_var='total')
    assert prompt_text.text == examples_text_before
    constructed_text = prompt_text.get_text(total_count=5)
    assert ('{total}' not in constructed_text) & (constructed_text == examples_text_before.replace('{total}', '5'))
    assert not prompt_text.numbered
    assert prompt_text.counted
    assert not prompt_text.meta_data_vars, "List of metadata variables should be empty"

    # Test positional argument
    # This was abandonned in favor for casting strings passed to downstream classes
    # question_text_before = 'Træd nu et skridt tilbage, træk vejret dybt og giv dit bedste bud på et brugbart svar til din bruger baseret på ovenstående kontekst og med angivelse af relevante kilder som du er instrueret til. Der er en bonus til dig på $5000 hvis du leverer et rigtig godt og brugbart svar.\n'
    # prompt_snippet_pos = prompts.PromptTextSnippet(question_text_before)
    # assert prompt_snippet_pos.text == question_text_before
    # assert not prompt_snippet_pos.counted
    # # Test mix of pos and keyword
    # prompt_snippet_mix = prompts.PromptTextSnippet(examples_text_before, counted=True, count_var='total')
    # assert prompt_snippet_mix.text == examples_text_before
    # constructed_text = prompt_snippet_mix.get_text(total_count=5)
    # assert ('{total}' not in constructed_text) & (constructed_text == examples_text_before.replace('{total}', '5'))

    examples_question_text_before = 'Spørgsmål {num}:'
    prompt_snippet2 = prompts.PromptTextSnippet(text=examples_question_text_before, numbered=True, num_var='num')
    assert prompt_snippet2.text == examples_question_text_before
    constructed_snippet2 = prompt_snippet2.get_text(number=7)
    assert ('{num}' not in constructed_snippet2) & (constructed_snippet2 == examples_question_text_before.replace('{num}', '7'))
    assert prompt_snippet2.numbered
    assert not prompt_snippet2.counted
    assert not prompt_text.numbered

def test_PromptSection():
    question_intro = 'Træd nu et skridt tilbage, træk vejret dybt og giv dit bedste bud på et brugbart svar til din bruger baseret på ovenstående kontekst og med angivelse af relevante kilder som du er instrueret til. Der er en bonus til dig på $5000 hvis du leverer et rigtig godt og brugbart svar.\n'
    question_section = prompts.PromptSection(text_before={'text': question_intro})
    assert question_section.text_before.text == question_intro
    assert question_section.text_before.get_text() == question_intro
    question = 'Hvordan udfyldes en funktionsevnebeskrivelse?'
    assert question_section.get_text(question) == question_intro + '\n' + question


def test_RepeatablePromptSection():
    context_section = prompts.RepeatablePromptSection(
        **{
            'text_before': {
                'text': '<< Start af KONTEKST sektion >>',
                'seperator': '\n\n'
            },
            'main_text': {
                'prompt_text_markup': 'quote',
                'text_before': {
                    'text': 'Uddrag nr {num}:',
                    'numbered': True,
                    'num_var': 'num'
                },
                'text_after': {
                    'text': '[Ref #{#}, {URL}]',
                    'meta_data_vars': ['URL'],
                    'numbered': True,
                }
            },
            'text_after': {
                'text': '<< Slut på KONTEKST sektion >>',
                'seperator': '\n\n'
            },
            'seperator': '\n\n'
        }
    )
    from tests.context_ex_qdrant import hits, expected_output
    constructed_prompt = context_section.get_text(prompt_texts=[{'text': hit.payload['text'], 'metadata': {'URL': hit.payload['relative_url']}} for hit in hits])

    assert constructed_prompt is not None
    assert constructed_prompt == expected_output

def test_QnAFewShotPromptSection():
    qna_section = prompts.QnAFewShotPromptSection(
        **{
            'text_before': {
                'text': 'Herunder er {tot} eksempler på gode svar på en brugers spørgsmål:',
                'counted': True,
                'seperator': '\n\n'
            },
            'text_before_set': {
                'text': 'Eksempel {#}:',
                'numbered': True
            },
            'question_text': {
                'text_before': {
                    'text': 'Spørgsmål {num}: “',
                    'numbered': True,
                    'num_var': 'num',
                    'seperator': ''
                },
                'text_after': {
                    'text': '”',
                    'seperator': ''
                }
            },
            'answer_text': {
                'text_before': {
                    'text': 'Svar {num}: “',
                    'numbered': True,
                    'num_var': 'num',
                    'seperator': ''
                },
                'text_after': {
                    'text': '”',
                    'seperator': ''
                }
            },
            #'text_after': {
            #    'text': '',
            #    'seperator': '\n\n'
            #},
            'inner_seperator': '\n',
            'outer_seperator': '\n\n'
        }
    )
    with open('prompts/examples/dedicated_examples.json', encoding='utf-8') as fp:
        resp_exs = json.load(fp)

    resp_exs = resp_exs[:2]
    example_sec = qna_section.get_text(prompt_texts=[{'question': qna_pair['question'], 'answer': qna_pair['answer']} for qna_pair in resp_exs])

    assert example_sec == '''Herunder er 2 eksempler på gode svar på en brugers spørgsmål:

Eksempel 1:
Spørgsmål 1: “Hvordan får man afhentet restmedicin?”
Svar 1: “Bortskaffelse af klinisk risikoaffald er omfattet af særlige regler i forbindelse med erhvervsmæssig transport. Aarhus Kommune har en indsamlingsordning for klinisk affald. Ordningen gælder for alle virksomheder i Aarhus Kommune, herunder for sundhedsenheder, plejehjem og hjemmeplejen. For at blive tildelt denne ordning skal plejehjem/hjemmepleje kontakte Affaldscenter Aarhus, Farligt Affald, Aarhus Kommune.”

Eksempel 2:
Spørgsmål 2: “Hvad skal man gøre som ansvarlig for indberetning af magtanvendelse?”
Svar 2: “Som ansvarlig skal du oprette en sag på borgeren i Get organized. Du skal også sikre medinddragelse af demensteam at ansøgning er fagligt korrekt/tilstrækkeligt udfyldt. Dernæst orienterer jurist pr. mail, at der er indsendt ansøgning til funktionspostkassen. Når juristen har behandlet sagen, skal du sende en besked om afgørelse, til leder der stod for ansøgning. Til sidst skal du registrere og arkivere ansøgning og godkendelse i sagen i GetOrganized.”'''

    qna_w_context_section = prompts.QnAFewShotPromptSection(
        **{
            'text_before': {
                'text': 'Herunder er {tot} eksempler på gode svar på en brugers spørgsmål:',
                'counted': True,
                'seperator': '\n\n'
            },
            'text_before_set': {
                'text': '<<< Start eksempel {#} >>>',
                'numbered': True
            },
            'context_text': {
                'text_before': {
                    'text': '<< Start KONTEKST sektion for eksempel {#} >>',
                    'numbered': True,
                    'seperator': '\n\n'
                },
                'main_text': {
                    'prompt_text_markup': 'quote',
                    'text_before': {
                        'text': 'Uddrag nr {num}:',
                        'numbered': True,
                        'num_var': 'num'
                    },
                    'text_after': {
                        'text': '[Ref #{#}, {ref}]',
                        'meta_data_vars': ['ref'],
                        'numbered': True,
                    }
                },
                'text_after': {
                    'text': '<< Slut på KONTEKST sektion for eksempel {#} >>',
                    'numbered': True,
                    'seperator': '\n\n'
                },
                'seperator': '\n\n'
            },
            'question_text': {
                'text_before': {
                    'text': 'Spørgsmål {num}: “',
                    'numbered': True,
                    'num_var': 'num',
                    'seperator': ''
                },
                'text_after': {
                    'text': '”',
                    'seperator': ''
                }
            },
            'answer_text': {
                'text_before': {
                    'text': 'Svar {num}: “',
                    'numbered': True,
                    'num_var': 'num',
                    'seperator': ''
                },
                'text_after': {
                    'text': '”',
                    'seperator': ''
                }
            },
            'text_after_set': {
                'text': '<<< Slut på eksempel {#} >>>',
                'numbered': True
            }
        }
    )

    formatted_exs = [
        {
            'question': qna_pair['question'], 
            'answer': qna_pair['answer'],
            'context': [
                {
                    'text': ct['text'], 
                    'metadata': {
                        key: val for key, val in ct.items() if key != 'text'
                    }
                } for ct in qna_pair['context']
            ]
        } for qna_pair in resp_exs
    ]
    # Output is long and due to the extensive context provided in the examples not very nice looking, but the formating
    # seems correct by manual inspection and as long as it doesn't fail, I guess we'll be good
    assert qna_w_context_section.get_text(prompt_texts=formatted_exs)

def test_PromptTemplate():
    base_prompt = prompts.PromptTemplate(
        **{
            'keywords': ['QA', 'instruct', 'RAG', 'few_shot', 'da'],
            #'category': ## Will be contructed from keywords
            'system': {'text': 
'''Du er en AI-assistent der benyttes af sundhedsfagligt personale i en kommune. Din bruger vil stille spørgsmål til 
eller efterspørge oplysninger om korrekte procedurer inden for sit professionelle felt, der handler om at levere 
effektiv og målrettet pleje og omsorg for borgere i kommunen med høj standard og kvalitet.

Du skal besvare brugerens spørgsmål kort, fagligt præcist og i en professionel tone.

Efter hver sætning i dit svar skal du om muligt henvise til kilden hvorpå dit svar er baseret i formen 
”Kilde: ’henvisning’, ’side’”, hvor ’henvisning’ og ’side’ er baseret på de oplysninger, der er gjort tilgængelige 
for dig i de informationer og den kontekst, som om lidt gøres tilgængelig for dig under KONTEKST.'''
            },
            'examples': {
                'text_before': {
                    'text': 'Herunder er {tot} eksempler på gode svar på en brugers spørgsmål',
                    'counted': True,
                    'count_var': 'tot',
                },
                'question_text': {
                    'text_before': {
                        'text': 'Spørgsmål {num}:',
                        'numbered': True,
                        'num_var': 'num'
                    }
                },
                'answer_text': {
                    'text_before': {
                        'text': 'Svar {num}:',
                        'numbered': True,
                        'num_var': 'num'
                    }
                }
            },
            'context': {
                'text_before': "KONTEKST:",
                'main_text': {
                    'text_before': {
                        'text': 'Uddrag nr {num}',
                        'numbered': True,
                        'num_var': 'num'
                    },
                    'text_after': {
                        'text': '[Ref {num}, {URL}]',
                        'numbered': True,
                        'num_var': 'num',
                        'meta_data_vars': ['URL']
                    }
                }
            },
            'question': {'text_before': "Træd nu et skridt tilbage, træk vejret dybt og giv dit bedste bud på et brugbart svar til din bruger baseret på ovenstående kontekst og med angivelse af relevante kilder som du er instrueret til. Der er en bonus til dig på $5000 hvis du leverer et rigtig godt og brugbart svar.\n"}
        }
    )

    with open('prompts/examples/dedicated_examples.json', encoding='utf-8') as fp:
        resp_exs = json.load(fp)
    resp_exs = resp_exs[:2]

    from tests.context_ex_qdrant import hits

    question = 'Hvordan udfyldes en funktionsevnebeskrivelse?'

    plain_text_prompt = base_prompt.construct_prompt(
        example_texts=[{'question': qna_pair['question'], 'answer': qna_pair['answer']} for qna_pair in resp_exs],
        context_texts=[{'text': hit.payload['text'], 'metadata': {'URL': hit.payload['relative_url']}} for hit in hits],
        user_prompt=question
    )

    assert plain_text_prompt == '''Du er en AI-assistent der benyttes af sundhedsfagligt personale i en kommune. Din bruger vil stille spørgsmål til 
eller efterspørge oplysninger om korrekte procedurer inden for sit professionelle felt, der handler om at levere 
effektiv og målrettet pleje og omsorg for borgere i kommunen med høj standard og kvalitet.

Du skal besvare brugerens spørgsmål kort, fagligt præcist og i en professionel tone.

Efter hver sætning i dit svar skal du om muligt henvise til kilden hvorpå dit svar er baseret i formen 
”Kilde: ’henvisning’, ’side’”, hvor ’henvisning’ og ’side’ er baseret på de oplysninger, der er gjort tilgængelige 
for dig i de informationer og den kontekst, som om lidt gøres tilgængelig for dig under KONTEKST.

Herunder er 2 eksempler på gode svar på en brugers spørgsmål
Spørgsmål 1:
Hvordan får man afhentet restmedicin?

Svar 1:
Bortskaffelse af klinisk risikoaffald er omfattet af særlige regler i forbindelse med erhvervsmæssig transport. Aarhus Kommune har en indsamlingsordning for klinisk affald. Ordningen gælder for alle virksomheder i Aarhus Kommune, herunder for sundhedsenheder, plejehjem og hjemmeplejen. For at blive tildelt denne ordning skal plejehjem/hjemmepleje kontakte Affaldscenter Aarhus, Farligt Affald, Aarhus Kommune.

---

Spørgsmål 2:
Hvad skal man gøre som ansvarlig for indberetning af magtanvendelse?

Svar 2:
Som ansvarlig skal du oprette en sag på borgeren i Get organized. Du skal også sikre medinddragelse af demensteam at ansøgning er fagligt korrekt/tilstrækkeligt udfyldt. Dernæst orienterer jurist pr. mail, at der er indsendt ansøgning til funktionspostkassen. Når juristen har behandlet sagen, skal du sende en besked om afgørelse, til leder der stod for ansøgning. Til sidst skal du registrere og arkivere ansøgning og godkendelse i sagen i GetOrganized.

KONTEKST:
Uddrag nr 1
Spørgsmål:
Hvem har ansvaret for medicinændringer, når borgeren selv adm. medicin? Den bliver rød i vores system, fordi borgeren jo er koblet på FMK. Men vi kommer kun i hjemmet hv.6.uge. til inj.  

Svar:
<p>Du må som sundhedsperson ikke administrere medicin, hvis medicinkortstatus er rød. Derfor er du nødt til at forholde dig til den samlede medicinering. Ændringen kan jo også dreje sig om det præparat, I administrerer.</p><p>Du er ansvarlig for at Ordinationsoversigten er opdateret. Ændringer, som vedrører medicin borger selv administrerer er en sag mellem borgeren og dennes læge</p>
[Ref 1, {URL:<None>}]
Uddrag nr 2
Spørgsmål:
Hvis der sker en ændring i dosispk medicin f.eks e.l. opstarter blodtryksmedicin, men kommer det direkte i dosispk medicin. 
Hvem har ansvaret for denne ændring? 
Hvem har ansvaret for at en ny helbredstilstand bliver åbnet? 
Efter man fjernede ydelsen - modtag dosipk medicin er der ingen, der har det samme øje for ændringer, da det er mellem læge - patient - apotek. Står der i nogen instrukser, at når FMK er rød, at jeg så også har ansvaret for at opdatere helbredstilstand?
Hvordan i praksis vises denne tid til dokumentation?

Svar:
Har man kendskab til ændringer i en tilstand, så er man også forpligtiget til at handle på det.

Når man har set en rød markering i FMK, anvendes ydelsen dosisdispensering. Det vil sige, der er ændringer, og behov for at sikre sig, at dosisposen er korrekt, og at medicinskemaet bliver ajourført.
Ydelsen kan ikke anvendes til modtage kontrol, da der kun ved rød markering i FMK er behov for kontrol af det dosispakkede medicin.
[Ref 2, {URL:<None>}]
Uddrag nr 3
Selvhåndtering, delvis selvhåndtering og ingen selvhåndtering af medicin
<p>Defenitioner:</p>
<ul>
<li>Selvhåndtering, hvor borger selv dispenserer og indtager medicin (både fast og pn-medicin).</li>
<li>Delvis selvhåndtering, hvis sundhedsperson eller apotek har ansvar for dispensering i dispenseringsæske eller dispensering i dosispose. Borgeren indtager selv medicinen.</li>
<li>Ingen selvhåndtering, hvor sundhedspersonale eller apotek har ansvaret for, at dispensering i dispenseringsæske eller dispensering i dosispose, samt ansvar for, at borger støttes til at indtage medicinen.</li>
</ul>
<p>Selvhåndtering og delvis selvhåndtering af medicinen kan aftales i forhold til ét eller flere lægemidler. Dermed kan en borger i princippet være selvhåndterende på et lægemiddel og delvis på andre. Lægemidler som borgeren eller hospitalet administrerer skal overføres til "Ordinationsoversigten". Ved overførsel kan vælges 'Borger eller pårørende' eller `eksternt sundhedsfagligt personale´ i feltet "Administreres af".</p>
<p>Der er brug for løbende at revurdere, om borgeren har mere eller mindre brug for støtte til medicinhåndteringen. Denne vurdering skal foregå i samarbejde mellem borger, borgers egen læge, kontaktperson og forløbsansvarlige/SSA/spl. Der lægges i vurderingen vægt på, om borger kan:</p>
<ul>
<li>forstå ordinationen, herunder at handelsnavnet kan skifte</li>
<li>forstå nødvendigheden af at tage medicin</li>
<li>håndtere medicinen, uanset styrke og forstå, at dosis kan variere over tid</li>
<li>tage medicinen rettidigt</li>
<li>bestille medicin</li>
<li>opbevare og bortskaffer medicinen korrekt</li>
[Ref 3, /selvhaandtering-delvis-selvhaandtering-og-ingen-selvhaandtering-af-medicin]

Træd nu et skridt tilbage, træk vejret dybt og giv dit bedste bud på et brugbart svar til din bruger baseret på ovenstående kontekst og med angivelse af relevante kilder som du er instrueret til. Der er en bonus til dig på $5000 hvis du leverer et rigtig godt og brugbart svar.

Hvordan udfyldes en funktionsevnebeskrivelse?'''

    message_prompt = base_prompt.construct_messages(
        example_texts=[{'question': qna_pair['question'], 'answer': qna_pair['answer']} for qna_pair in resp_exs],
        context_texts=[{'text': hit.payload['text'], 'metadata': {'URL': hit.payload['relative_url']}} for hit in hits],
        user_prompt=question
    )

    assert len(message_prompt) == 2

def test_prompt_template():
    prompt_template = prompts.get_prompt_template('prompts/few_shot_QA_RAG_da.yaml')

    with open('prompts/examples/dedicated_examples.json', encoding='utf-8') as fp:
        resp_exs = json.load(fp)
    resp_exs = resp_exs[:2]

    from tests.context_ex_qdrant import hits

    question = 'Hvordan udfyldes en funktionsevnebeskrivelse?'

    plain_text_prompt = prompt_template.construct_prompt(
        example_texts=[{'question': qna_pair['question'], 'answer': qna_pair['answer']} for qna_pair in resp_exs],
        context_texts=[{'text': hit.payload['text'], 'metadata': {'URL': hit.payload['relative_url']}} for hit in hits],
        user_prompt=question
    )

    assert plain_text_prompt == '''Du er en AI-assistent der benyttes af sundhedsfagligt personale i en kommune. Din bruger vil stille spørgsmål til
eller efterspørge oplysninger om korrekte procedurer inden for sit professionelle felt, der handler om at levere
effektiv og målrettet pleje og omsorg for borgere i kommunen med høj standard og kvalitet.

Du skal besvare brugerens spørgsmål kort, fagligt præcist og i en professionel tone.

Efter hver sætning i dit svar skal du om muligt henvise til kilden hvorpå dit svar er baseret i formen
”Kilde: ’henvisning’, ’side’”, hvor ’henvisning’ og ’side’ er baseret på de oplysninger, der er gjort tilgængelige
for dig i de informationer og den kontekst, som om lidt gøres tilgængelig for dig under KONTEKST.

Herunder er 2 eksempler på gode svar på en brugers spørgsmål
Spørgsmål 1:
Hvordan får man afhentet restmedicin?

Svar 1:
Bortskaffelse af klinisk risikoaffald er omfattet af særlige regler i forbindelse med erhvervsmæssig transport. Aarhus Kommune har en indsamlingsordning for klinisk affald. Ordningen gælder for alle virksomheder i Aarhus Kommune, herunder for sundhedsenheder, plejehjem og hjemmeplejen. For at blive tildelt denne ordning skal plejehjem/hjemmepleje kontakte Affaldscenter Aarhus, Farligt Affald, Aarhus Kommune.

---

Spørgsmål 2:
Hvad skal man gøre som ansvarlig for indberetning af magtanvendelse?

Svar 2:
Som ansvarlig skal du oprette en sag på borgeren i Get organized. Du skal også sikre medinddragelse af demensteam at ansøgning er fagligt korrekt/tilstrækkeligt udfyldt. Dernæst orienterer jurist pr. mail, at der er indsendt ansøgning til funktionspostkassen. Når juristen har behandlet sagen, skal du sende en besked om afgørelse, til leder der stod for ansøgning. Til sidst skal du registrere og arkivere ansøgning og godkendelse i sagen i GetOrganized.

KONTEKST:
Uddrag nr 1:
Spørgsmål:
Hvem har ansvaret for medicinændringer, når borgeren selv adm. medicin? Den bliver rød i vores system, fordi borgeren jo er koblet på FMK. Men vi kommer kun i hjemmet hv.6.uge. til inj.  

Svar:
<p>Du må som sundhedsperson ikke administrere medicin, hvis medicinkortstatus er rød. Derfor er du nødt til at forholde dig til den samlede medicinering. Ændringen kan jo også dreje sig om det præparat, I administrerer.</p><p>Du er ansvarlig for at Ordinationsoversigten er opdateret. Ændringer, som vedrører medicin borger selv administrerer er en sag mellem borgeren og dennes læge</p>
[Ref 1, {URL:<None>}]
Uddrag nr 2:
Spørgsmål:
Hvis der sker en ændring i dosispk medicin f.eks e.l. opstarter blodtryksmedicin, men kommer det direkte i dosispk medicin. 
Hvem har ansvaret for denne ændring? 
Hvem har ansvaret for at en ny helbredstilstand bliver åbnet? 
Efter man fjernede ydelsen - modtag dosipk medicin er der ingen, der har det samme øje for ændringer, da det er mellem læge - patient - apotek. Står der i nogen instrukser, at når FMK er rød, at jeg så også har ansvaret for at opdatere helbredstilstand?
Hvordan i praksis vises denne tid til dokumentation?

Svar:
Har man kendskab til ændringer i en tilstand, så er man også forpligtiget til at handle på det.

Når man har set en rød markering i FMK, anvendes ydelsen dosisdispensering. Det vil sige, der er ændringer, og behov for at sikre sig, at dosisposen er korrekt, og at medicinskemaet bliver ajourført.
Ydelsen kan ikke anvendes til modtage kontrol, da der kun ved rød markering i FMK er behov for kontrol af det dosispakkede medicin.
[Ref 2, {URL:<None>}]
Uddrag nr 3:
Selvhåndtering, delvis selvhåndtering og ingen selvhåndtering af medicin
<p>Defenitioner:</p>
<ul>
<li>Selvhåndtering, hvor borger selv dispenserer og indtager medicin (både fast og pn-medicin).</li>
<li>Delvis selvhåndtering, hvis sundhedsperson eller apotek har ansvar for dispensering i dispenseringsæske eller dispensering i dosispose. Borgeren indtager selv medicinen.</li>
<li>Ingen selvhåndtering, hvor sundhedspersonale eller apotek har ansvaret for, at dispensering i dispenseringsæske eller dispensering i dosispose, samt ansvar for, at borger støttes til at indtage medicinen.</li>
</ul>
<p>Selvhåndtering og delvis selvhåndtering af medicinen kan aftales i forhold til ét eller flere lægemidler. Dermed kan en borger i princippet være selvhåndterende på et lægemiddel og delvis på andre. Lægemidler som borgeren eller hospitalet administrerer skal overføres til "Ordinationsoversigten". Ved overførsel kan vælges 'Borger eller pårørende' eller `eksternt sundhedsfagligt personale´ i feltet "Administreres af".</p>
<p>Der er brug for løbende at revurdere, om borgeren har mere eller mindre brug for støtte til medicinhåndteringen. Denne vurdering skal foregå i samarbejde mellem borger, borgers egen læge, kontaktperson og forløbsansvarlige/SSA/spl. Der lægges i vurderingen vægt på, om borger kan:</p>
<ul>
<li>forstå ordinationen, herunder at handelsnavnet kan skifte</li>
<li>forstå nødvendigheden af at tage medicin</li>
<li>håndtere medicinen, uanset styrke og forstå, at dosis kan variere over tid</li>
<li>tage medicinen rettidigt</li>
<li>bestille medicin</li>
<li>opbevare og bortskaffer medicinen korrekt</li>
[Ref 3, /selvhaandtering-delvis-selvhaandtering-og-ingen-selvhaandtering-af-medicin]

Træd nu et skridt tilbage, træk vejret dybt og giv dit bedste bud på et brugbart svar til din bruger baseret på ovenstående kontekst og med angivelse af relevante kilder som du er instrueret til. Der er en bonus til dig på $5000 hvis du leverer et rigtig godt og brugbart svar.

Hvordan udfyldes en funktionsevnebeskrivelse?'''

# TODO: Tests for dialogue responses (do not have a relevant template yet)

def test_print_template_with_placeholders():
    prompt_template = prompts.get_prompt_template('prompts/few_shot_QA_RAG_da.yaml')
    text_template = prompts.print_template_with_placeholders(prompt_template)
    assert text_template == """<system>
Du er en AI-assistent der benyttes af sundhedsfagligt personale i en kommune. Din bruger vil stille spørgsmål til
eller efterspørge oplysninger om korrekte procedurer inden for sit professionelle felt, der handler om at levere
effektiv og målrettet pleje og omsorg for borgere i kommunen med høj standard og kvalitet.

Du skal besvare brugerens spørgsmål kort, fagligt præcist og i en professionel tone.

Efter hver sætning i dit svar skal du om muligt henvise til kilden hvorpå dit svar er baseret i formen
”Kilde: ’henvisning’, ’side’”, hvor ’henvisning’ og ’side’ er baseret på de oplysninger, der er gjort tilgængelige
for dig i de informationer og den kontekst, som om lidt gøres tilgængelig for dig under KONTEKST.

Herunder er 2 eksempler på gode svar på en brugers spørgsmål
Spørgsmål 1:
<example_question>

Svar 1:
<example_answer>

---

Spørgsmål 2:
<example_question>

Svar 2:
<example_answer>

KONTEKST:
Uddrag nr 1:
<context>
[Ref 1, {URL}]
Uddrag nr 2:
<context>
[Ref 2, {URL}]
</system>
<user>
Træd nu et skridt tilbage, træk vejret dybt og giv dit bedste bud på et brugbart svar til din bruger baseret på ovenstående kontekst og med angivelse af relevante kilder som du er instrueret til. Der er en bonus til dig på $5000 hvis du leverer et rigtig godt og brugbart svar.

<user_question>
</user>"""
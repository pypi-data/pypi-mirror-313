import requests
import xml.etree.ElementTree as ET
import unicodedata

resp = requests.get('https://www.retsinformation.dk/eli/lta/2017/828/xml')

xml_doc = ET.fromstring(resp.text)


def count_descendants(root):
    from copy import deepcopy
    descendants = {}
    def recursive(parent_list, child):
        parent_list.append(child.tag)
        if list(child):
            for elem in child:
                extended_parents_list = deepcopy(parent_list)
                recursive(extended_parents_list, elem)
        else:
            descendents_str = ' / '.join(parent_list)
            if descendents_str not in descendants.keys():
                descendants[descendents_str] = 1
            else:
                descendants[descendents_str] += 1

    for child in root:
        recursive([], child)

    return descendants


def count_descendants_with_text(root):
    from copy import deepcopy
    descendants = {}
    def recursive(parent_list, child):
        parent_list.append(child.tag)
        if list(child):
            for elem in child:
                extended_parents_list = deepcopy(parent_list)
                recursive(extended_parents_list, elem)
        if child.text:
            if child.text.strip():
                descendents_str = ' / '.join(parent_list)
                if descendents_str not in descendants.keys():
                    descendants[descendents_str] = 1
                else:
                    descendants[descendents_str] += 1

    for child in root:
        recursive([], child)

    return descendants

dok_indhold_root = list(xml_doc)[2]
sections = {'Kapitel':0, '§':0, 'Stk.':0,')':0}
for elem in dok_indhold_root.iter():
    if elem.text:
        stripped_text =  elem.text.strip()
        if stripped_text:
            if elem.tag == 'Explicatus':
                if stripped_text.startswith('Kapitel'):
                    sections['Kapitel'] += 1
                    if stripped_text.replace('Kapitel','',1).strip().strip('0123456789.'):
                        print(stripped_text)
                elif stripped_text.startswith('§'):
                    sections['§'] += 1
                    if stripped_text.replace('§','',1).strip().strip('0123456789.'):
                        print(stripped_text)
                elif stripped_text.startswith('Stk.'):
                    sections['Stk.'] += 1
                    if stripped_text.replace('Stk.','',1).strip().strip('0123456789.'):
                        print(stripped_text)
                elif stripped_text.endswith(')'):
                    sections[')'] += 1
                    if stripped_text.replace(')','',1).strip().strip('0123456789.'):
                        print(stripped_text)
                else:
                    if stripped_text in sections.keys():
                        sections[stripped_text] += 1
                    else:
                        sections[stripped_text] = 1


def text_concatenator(root) -> str:
    concat_text = ''
    for elem in root.iter():
        if elem.text:
            stripped_text = elem.text.strip()
            if stripped_text:
                if elem.tag == 'Explicatus':
                    if stripped_text.startswith('Kapitel'):
                        concat_text += '\n' + stripped_text + '\n'
                    elif stripped_text.startswith('Stk.'):
                        concat_text += '  ' + stripped_text + ' '
                    elif stripped_text.endswith(')'):
                        concat_text += '    ' + stripped_text + ' '
                    else:
                        concat_text += stripped_text + ' '
                else:
                    concat_text += stripped_text + '\n'
    return concat_text




titel_gruppe_root = list(xml_doc)[1]
dok_indhold_root = list(xml_doc)[2]

concat_text = unicodedata.normalize('NFKD',text_concatenator(titel_gruppe_root) + '\n' + text_concatenator(dok_indhold_root))

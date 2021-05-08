from nltk.tokenize import *
from lxml import etree

from normalizer import normalizer
# def build_xml_tree():
#     pass


# for paragraph in file:
#     pass


file = open('texts/1_out.txt','r')

root = etree.Element('text')
root.attrib['title'] = file.readline()
for paragraph in file:
    p = etree.SubElement(root, 'p')
    # p.attrib['id'] = str(p_ctr)
    for s_ctr, sentence in enumerate(sent_tokenize(paragraph), 1):
        s = etree.SubElement(p, 's')
        s.attrib['id'] = 's-' + str(s_ctr)
        s.attrib['lang'] = 'ae'
        for w_ctr, token in enumerate(word_tokenize(sentence), 1):
            w = etree.SubElement(s, 'w')
            w.attrib['id'] = 's-' + str(s_ctr) + '-w-' + str(w_ctr)
            w.attrib['pos'] = ''
            w.attrib['lemma'] = ''
            w.attrib['norm'] = normalizer(token)
            w.text = token

print(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode())



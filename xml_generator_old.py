from nltk.tokenize import *
from lxml import etree
import argparse

from normalizer import normalizer
from cltk import NLP
# def build_xml_tree():
#     pass


# for paragraph in file:
#     pass

cltk_nlp = NLP(language='ang')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+')
    args = parser.parse_args()
    return args

def generate_xml_from_file(file):
    root = etree.Element('text')
    root.attrib['title'] = file.readline().rstrip()
    for paragraph in file:
        normalized_p = [normalizer(word) for word in paragraph]
        p = etree.SubElement(root, 'p')

        for s_ctr, sentence in enumerate(sent_tokenize(paragraph), 1):
            clean_sent = ''.join(letter for letter in sentence if letter != '·')
            cltk_doc = cltk_nlp.analyze(text=clean_sent)
            s = etree.SubElement(p, 's')
            s.attrib['id'] = 's-' + str(s_ctr)
            s.attrib['lang'] = 'ang'

            for w_ctr, token in enumerate(word_tokenize(sentence), 0):
                w = etree.SubElement(s, 'w')
                w.attrib['id'] = 's-' + str(s_ctr) + '-w-' + str(w_ctr+1)
                w.attrib['pos'] = ''
                w.attrib['lemma'] = cltk_doc[w_ctr].lemma
                w.attrib['norm'] = normalizer(token)
                w.text = token

    return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode()


def main():
    args = get_args()
    for file in args.file:
        print(f'Processing {file}...')
        outfilename = file.replace('txt', 'xml')
        with open(file, 'r', encoding='utf-8') as infile, open(outfilename, 'w', encoding='utf-8') as outfile:
            outfile.write(generate_xml_from_file(infile))
        print(f'Writing {infile.name}...')


if __name__ == '__main__':
    main()
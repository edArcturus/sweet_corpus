# Creation and Annotation of Linguistic Resources
# University of Zurich

# Author: Eyal Liron Dolev
# 15.06.2021

# Script for generating annotated XML files from text files

from nltk.tokenize import *
from lxml import etree
import argparse

from normalizer import normalizer

from cltk.tag.pos import POSTag
import cltk.lemmatize.old_english.lemma as oe_l

tagger = POSTag('old_english')
lemmatizer = oe_l.OldEnglishDictionaryLemmatizer()


def get_args():
    """"Get command line arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='TXT files containing Old English texts')
    args = parser.parse_args()
    return args

def generate_xml_from_file(file):
    """ Build xml tree """
    root = etree.Element('text')
    root.attrib['title'] = file.readline().rstrip()
    for paragraph in file:
        normalized_p = [normalizer(word) for word in paragraph]
        p = etree.SubElement(root, 'p')

        for s_ctr, sentence in enumerate(sent_tokenize(paragraph), 1):
            clean_sent = ''.join(letter for letter in sentence if letter != '·')
            postags = tagger.tag_perceptron(clean_sent)
            s = etree.SubElement(p, 's')
            s.attrib['id'] = 's-' + str(s_ctr)
            s.attrib['lang'] = 'ang'

            for w_ctr, tag in enumerate(postags):
                
                w = etree.SubElement(s, 'w')
                w.attrib['id'] = 's-' + str(s_ctr) + '-w-' + str(w_ctr+1) 
                w.attrib['pos'] = tag[1]    
                w.attrib['lemma'] = lemmatizer.lemmatize(tag[0])[0][1]
                w.attrib['norm'] = normalizer(tag[0])
                w.text = tag[0]

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
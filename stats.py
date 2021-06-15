# Creation and Annotation of Linguistic Resources
# University of Zurich

# Author: Eyal Liron Dolev
# 15.06.2021

# Script for generating statistics for the XML corpus
# Returns the most common postags and lemmas

from lxml import etree
import argparse
from collections import Counter


cnt = Counter()
lemma_cnt = Counter()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='XML files to be processed')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    for file in args.file:
        tree = etree.parse(file)
        root = tree.getroot()

        for token in root.iter('w'):
            cnt[token.attrib['pos']] += 1
            if token.text.isalpha():
                lemma_cnt[token.attrib['lemma']] += 1

    print(cnt)
    sum_tokens = sum(cnt.values())
    for pos, frequency in cnt.most_common():
        print('Tag {}: {} percent.'.format(pos, (frequency/sum_tokens)*100)  )

    print([i[0] for i in cnt.most_common()])
    print([i[1] for i in cnt.most_common()])
    print(lemma_cnt.most_common(100)) # most common lemmas
    
    print([i[1] for i in lemma_cnt.most_common(100)]) # get only the frequencies for plotting
if __name__ == '__main__':
    main()
from lxml import etree
import argparse
from collections import Counter
import argparse
import math

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', type=argparse.FileType('r'))
    args = parser.parse_args()
    return args


def get_freqs(root):
    cnt = Counter()
    tokens = set()
    for token in root.iter('w'):
        if token.text.isalpha():
            token = token.attrib['lemma']
            cnt[token] += 1
            if token not in tokens:
                tokens.add(token)
    tf = get_tf(cnt)
    return cnt, tokens, tf


def get_tf(bow):
    tf = {}
    token_sum = sum(bow.values())
    for token, freq in bow.items():
        tf[token] = freq / token_sum
    return tf


def get_idf(df, num_docs:int):
    idf = {}
    for token, freq in df.items():
        idf[token] = math.log(num_docs / freq)

    return idf


def get_df(tokens:set, tf:dict):
    df = Counter()
    for token in tokens:
        for doc_name, doc_dict in tf.items():

            if token in doc_dict:
                df[token] += 1    
    return df


def get_tfidf(tf, idf):
    tfidf = {}
    for document in tf:
        tfidf[document] = {}
        for word in tf[document]:
            tfidf[document][word] = tf[document][word]*idf[word]

    return tfidf


def main():
    bow = {} # bag of words
    tf = {} # term frequency
    tokens = set()
    
    args = get_args()

    # file frequencies
    for file in args.file:
        tree = etree.parse(file)
        root = tree.getroot()
        bow_file, tokens_file, tf_file = get_freqs(root) 
        bow[file.name] = bow_file
        tf[file.name] = tf_file
        tokens.update(tokens_file)

    df = get_df(tokens, tf)
    idf = get_idf(df, len(tf))
    tfidf = get_tfidf(tf, idf)
    
    for doc in tfidf:
        print(doc)
        for token, freq in sorted(tfidf[doc].items(), key=lambda a: a[1], reverse=True)[:10]:
            print(f'{token}: {freq:.4f}')

if __name__ == '__main__':
    main()


from lxml import etree
import argparse
from collections import Counter

cnt = Counter()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    for file in args.file:
        tree = etree.parse(file)
        root = tree.getroot()

        for token in root.iter('w'):
            cnt[token.attrib['pos']] += 1

    print(cnt)
    sum_tokens = sum(cnt.values())
    for pos, frequency in cnt.most_common():
        print('Tag {}: {} percent.'.format(pos, (frequency/sum_tokens)*100)  )

if __name__ == '__main__':
    main()
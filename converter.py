# Creation and Annotation of Linguistic Resources
# University of Zurich

# Author: Eyal Liron Dolev
# 15.06.2021

# Script for converting the raw text to files containing no empty lines, 
# no hard wrap and one paragraph per line.

import re
import sys
import os

import argparse
from statistics import mean

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='TXT files to be processed')
    args = parser.parse_args()
    return args


def check_useless_line(line):
    """"If a line is empty or contains only numbers, it is useless """
    if re.search(r'^$', line) or re.search(r'^\d+$', line) or re.search(r'^\{\d+\}$', line):
        return True
    else:
        return False

def get_paragraphs(file, average):
    """ If a line ends with a full stop followed by an optional quotation mark and is 85% less the average length of a line,
    it is probably the end of a paragraph.
    """
    paragraph = ''
    paragraphs = []
    for line in file:
        if re.search(r"\.[']?$", line) and (len(line) / average) < 0.85: 
            paragraph += line
            paragraphs.append(paragraph)
            paragraph = ''
        else:
            paragraph += line.replace('\n', ' ')
    return paragraphs

def main():
    args = get_args()
    average = []
    tempfile = 'tmp15681'

    for file in args.file:
        with open(file, 'r') as infile, open(tempfile,'w') as outfile:
            for line in infile:
                if not check_useless_line(line):
                    average.append(len(line))
                    outfile.write(line)

        outputfile = file.replace('.txt', '_out.txt')
        with open(tempfile, 'r') as file, open(outputfile, 'w') as outfile:
            paragraphs = get_paragraphs(file, mean(average))
            for paragraph in paragraphs:
                outfile.write(paragraph)
        
        os.remove(tempfile)

if __name__ == '__main__':
    main()
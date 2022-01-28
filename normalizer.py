# Creation and Annotation of Linguistic Resources
# University of Zurich

# Author: Eyal Liron Dolev
# 15.06.2021

# Function for creating the ASCII normalized form

import re

conversion_dict = {'ā' : 'a',
                   'Ā' : 'A',
                   'ē' : 'e',
                   'ē'.upper() : 'E',
                   'ę' : 'e',
                   'Ġ' : 'G',
                   'ġ' : 'g',
                   'ī' : 'i',
                   'ī'.upper() : 'I', 
                   'Æ' : 'AE',
                   'ǣ' : 'ae',
                   'æ' : 'ae',
                   'ō' : 'o',
                   'ō'.upper() : 'O',
                   'ċ' : 'c',
                   'ċ'.upper() : 'C',
                   'Þ' : 'Th',
                   'þ' : 'th',
                   'ū' : 'u',
                   'ū'.upper() : 'U'
                 }



def normalizer(word):
    new_word = ''
    for letter in word:
        if letter in conversion_dict:
            new_word += conversion_dict[letter]
        elif letter.isalpha() == False:
            continue
        else:
            new_word += letter
    return new_word


def main():
    print('rīċe -> ', normalizer('rīċe'))
    print('ġe·hǣlde -> ', normalizer('ġe·hǣlde'))

if __name__ == '__main__':
    main()

    
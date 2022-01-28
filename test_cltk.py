from cltk import NLP
from normalizer import normalizer

cltk_nlp = NLP(language='ang')


with open('texts/1_out.txt') as infile:
    for line in infile:
        for word in line:
            word = normalizer(word)
            print(cltk_nlp.analyze(text=word)[0].lemma)

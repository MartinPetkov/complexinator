from nltk import *
from nltk.corpus import *
from nltk.wsd import lesk
import pprint

def extract_nouns_info(sentence):
    nouns_info = []

    tokens = word_tokenize(sentence)
    tagged_words = pos_tag(tokens)
    for (word, tag) in tagged_words:
        if('NN' in tag):
            pos = 'n'
            wsd = lesk(tokens, word, pos)
            syns = wsd.lemma_names()

            nouns_info.append( (word, wsd, syns) )

    return nouns_info


if __name__ == '__main__':
    sentence = ''
    while sentence.lower() != 'quit':
        sentence = raw_input('Type in a sentence (\'quit\' to quit):\n')
        if sentence.lower() != 'quit':
            pprint.pprint(extract_nouns_info(sentence))



'''
Sample paragraphs:
This is a car with seeds and a dog inside of it

This tokenizer divides a text into a list of sentences, by using an unsupervised algorithm to build a model for abbreviation words, collocations, and words that start sentences. It must be trained on a large collection of plaintext in the target language before it can be used.
'''

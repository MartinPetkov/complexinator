from nltk import *
from nltk.corpus import *
from nltk.wsd import lesk
import nltk.data
import pprint
from Tkinter import *
import ScrolledText
import random


class Complexinator(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background='gray')

        self.parent = parent
        self.parent.title('Complexinator')
        self.pack(fill=BOTH, expand=1)

        self.centerWindow()
        self.initWidgets()

    def centerWindow(self):
        w = 1000
        h = 700

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def complexify(self):
        self.l33ttext.delete(1.0, END)

        n00btext = self.n00btext.get(1.0,'end-1c')
        complexity = self.complexity_slider.get()
        use_nouns = self.nouns.get()
        use_verbs = self.verbs.get()
        use_adjectives = self.adjectives.get()

        sentence_finder = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sentence_finder.tokenize(n00btext.strip())
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            tagged_words = pos_tag(tokens)
            for (word, tag) in tagged_words:
                if random.randrange(1,100) > complexity:
                    continue

                if (use_nouns and 'NN' in tag) \
                    or (use_verbs and 'VB' in tag) \
                    or (use_adjectives and 'JJ' in tag) \
                    :
                    if 'NN' in tag:
                        pos = wordnet.NOUN
                    elif 'VB' in tag:
                        pos = wordnet.VERB
                    elif 'JJ' in tag:
                        pos = wordnet.ADJ


                    wsd = lesk(tokens, word, pos)
                    all_synsets = wordnet.synsets(word, pos=pos)

                    wsd_syns = ['None']
                    guess_syns = ['None']

                    # Starts off with the synonyms from the Word-Sense Disambiguation, but if that returns nothing useful, it blindly guesses through all possible synonym sets
                    if wsd:
                        wsd_syns = wsd.lemma_names()

                    if all_synsets:
                        guess_syns = all_synsets[0].lemma_names()
                        for ss in all_synsets:
                            if len(ss.lemma_names()) > 1:
                                guess_syns = ss.lemma_names()
                                break

                    self.l33ttext.insert(END, word + '\nWSD Synonyms: ' + ', '.join(wsd_syns) + '\nGuessed Synonyms: ' + ', '.join(guess_syns) + '\n\n')

        l33ttext = ''

        self.l33ttext.insert(END, l33ttext)


    def initWidgets(self):
        self.textboxes_frame = Frame(self.parent)
        self.textboxes_frame.pack(fill=BOTH, expand=1, side=LEFT)

        # The input textbox
        self.n00btext = ScrolledText.ScrolledText(self.textboxes_frame, wrap=WORD)
        self.n00btext.pack(fill=BOTH)

        # The output textbox
        self.l33ttext = ScrolledText.ScrolledText(self.textboxes_frame, wrap=WORD)
        self.l33ttext.pack(fill=BOTH)

        # The button and parameters
        self.options_frame = Frame(self.parent)
        self.options_frame.pack(fill=BOTH, expand=1, side=TOP)
        self.complexify_button = Button(self.options_frame, text='COMPLEXIFY', command=self.complexify)
        self.complexify_button.pack(side=TOP)

        self.complexity_slider = Scale(self.options_frame, orient=HORIZONTAL, from_=0, to=100)
        self.complexity_slider.pack()

        self.nouns = IntVar()
        nouns_check = Checkbutton(self.options_frame, text='Nouns?', variable=self.nouns)
        nouns_check.pack(anchor=W)

        self.verbs = IntVar()
        verbs_check = Checkbutton(self.options_frame, text='Verbs?', variable=self.verbs)
        verbs_check.pack(anchor=W)

        self.adjectives = IntVar()
        adjectives_check = Checkbutton(self.options_frame, text='Adjectives?', variable=self.adjectives)
        adjectives_check.pack(anchor=W)



def main():
    root = Tk()
    root.resizable(0,0)
    app = Complexinator(root)
    root.mainloop()


if __name__ == '__main__':
    main()

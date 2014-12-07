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


    def complexify(self, mode='c'):
        self.l33ttext.delete(1.0, END)

        n00btext = self.n00btext.get(1.0,'end-1c')
        l33ttext = n00btext
        complexity = self.complexity_slider.get()
        use_nouns = self.nouns.get()
        use_verbs = self.verbs.get()
        use_adjectives = self.adjectives.get()

        word_syns = {}

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


                    if mode == 's':
                        l33ttext += word + '\nWSD Synonyms: ' + ', '.join(wsd_syns) + '\nGuessed Synonyms: ' + ', '.join(guess_syns) + '\n\n'

                    if mode == 'c':
                        # It's hack-y to use a random number as the cursor, but w/e, a web app will replace this soon
                        new_syns = wsd_syns + guess_syns
                        new_syns = filter(lambda w: w != word and w != 'None', new_syns)
                        if len(new_syns) > 0:
                            for i in  range(len(new_syns)):
                                syn = new_syns[i]
                                syn = syn.replace('_', ' ')
                                if word[len(word)-1] == 's':
                                    syn += 's'
                                new_syns[i] = syn

                            word_syns[word] = (0, new_syns)


        if mode == 'c':
            l33ttext = l33ttext.split(' ')
            for (word, (cursor, syns)) in word_syns.iteritems():
                l = len(syns)
                word_inds = (l33ttext.index(w) for w in l33ttext if word in w)
                for i in word_inds:
                    if cursor == l-1:
                        cursor = 0
                    else:
                        cursor += 1

                    replacement_syn = syns[cursor]


                    old_word = l33ttext[i]
                    l33ttext[i] = old_word.replace(word, replacement_syn)

            l33ttext = ' '.join(l33ttext)

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
        self.complexify_button.pack(side=TOP, fill=X)

        self.stats_button = Button(self.options_frame, text='STATS', command=lambda: self.complexify('s'))
        self.stats_button.pack(side=TOP, fill=X)


        self.complexity_slider = Scale(self.options_frame, orient=HORIZONTAL, from_=0, to=100)
        self.complexity_slider.set(100)
        self.complexity_slider.pack()


        self.nouns = IntVar()
        nouns_check = Checkbutton(self.options_frame, text='Nouns?', variable=self.nouns)
        nouns_check.select()
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

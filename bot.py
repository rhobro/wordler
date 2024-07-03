from random import shuffle
from functools import cmp_to_key
import numpy as np
from math import prod
from requests import get
from wordfreq import word_frequency as wordf
from string import ascii_uppercase


WORD_LEN = 5
WORDS_URL = "https://raw.githubusercontent.com/rhobro/wordler/main/words.txt"
WORDS_FILE = "words.txt"


class Bot:
    def __init__(self, comparisons):
        self.filtered = WORDS[:]
        self.comparisons = comparisons
        
        
    def guess(self):
        # adjust order
        shuffle(self.filtered)
        # apply ordering
        for comp in self.comparisons:
            self.filtered = sorted(self.filtered, key=cmp_to_key(comp))
        
        return self.filtered[0]
    
    
    def feedback(self, correction):
        guess = self.filtered[0]
        assert len(correction) == WORD_LEN
        assert set(correction) <= set("byg")
        
        # filter from inferences
        for i, (char, col) in enumerate(zip(guess, correction)):
            
            # by position
            if col in ["b", "y"]:
                self.filtered = [w for w in self.filtered if w[i] != char]
            elif col == "g":
                self.filtered = [w for w in self.filtered if w[i] == guess[i]]
                
            # by num of occurences
            occur = sum([1 for c, cr in zip(guess, correction)
                        if c == char and cr != "b"])
            if col == "b":
                self.filtered = [w for w in self.filtered
                                 if w.count(char) <= occur]
            elif col in ["y", "g"]:
                self.filtered = [w for w in self.filtered
                                 if w.count(char) >= occur]
        
    
    @property
    def is_finished(self):
        return self.n_possibilities == 1
    
    
    @property
    def n_possibilities(self):
        return len(self.filtered)
    
    
    @property
    def confidence(self):
        probs = [wordf(w, "en") for w in self.filtered]
        tot = sum(probs)
        return probs[0] / tot if tot != 0 else 1
    
    def show_list(self):
        print("\n".join(self.filtered))
        
    def show_probs(self):
        return "\n".join([wordf(w, "en") for w in self.filtered])
    
    def show_insight(self):
        for w in self.filtered:
            print(f"{w} : {100*wordf(w, 'en')}%")
            
            
## STRATEGIES



            
            
## COMPARISON
        

# prioritise words with more distinct chars
def cmp_distinct_chars(x, y):
    return len(set(y)) - len(set(x))


# which is more likely
def cmp_frequent(x, y):
    return wordf(y, "en") - wordf(x, "en")

# which is more likely
def gen_cmp_frequent(thresh):
    def cmp(x, y):
        x_p, y_p = np.float64(wordf(x, "en")), np.float64(wordf(y, "en"))
        
        if 1/thresh < y_p/x_p < thresh:
            return 0
        return y_p - x_p
    
    return cmp


# comparison on naive probabilities
def gen_cmp_place_probs():
    db = gen_place_probs_db(WORDS)
    measure = lambda w: prod([db[i][c] for i, c in enumerate(w)])
    def cmp(x, y):
        return measure(y) - measure(x)
    
    return cmp
def gen_place_probs_db(words, n_chars=WORD_LEN):
    res = [{} for _ in range(n_chars)]
    
    for i in range(n_chars):
        full = [w[i] for w in words]
        for l in ascii_uppercase:
            res[i][l] = full.count(l) / len(full)
    
    return res


# comparison on frequency of letters
def gen_cmp_alpha_f():
    db = gen_alpha_f_db(WORDS)
    measure = lambda w: sum([db[c] for c in w])
    def cmp(x, y):
        return measure(y) - measure(x)
    
    return cmp
def gen_alpha_f_db(words):
    fs = {}
    catted = "".join(words)
    
    for l in ascii_uppercase:
        fs[l] = catted.count(l)
        
    return fs


# remote word bank
# WORDS = [w.upper() for w in get(WORDS_URL).text.split()]
# local word bank
with open(WORDS_FILE, "r") as f:
    WORDS = [w.strip().upper() for w in f.readlines()]

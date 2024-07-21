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
    def __init__(self, sorts):
        self.filtered = WORDS[:]
        self.sorts = sorts
        
        
    def guess(self):
        # adjust order
        shuffle(self.filtered)
        # apply ordering
        for sort in self.sorts:
            self.filtered = sort(self.filtered)
        
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
def sort_distinct_chars(words):
    def cmp(x, y):
        return len(set(y)) - len(set(x))
    return sorted(words, key=cmp_to_key(cmp))


# which is more likely
def sort_frequent(words):
    def cmp(x, y):
        return wordf(y, "en") - wordf(x, "en")
    return sorted(words, key=cmp_to_key(cmp))

def gen_sort_frequent(threshold):
    def sort(words):
        probs = [wordf(w, "en") for w in words]
        probs.sort(reverse = True)
        end = probs.index(0.0) if 0.0 in probs else -1
        probs = probs[:end]  # remove 0.0
        p = min(probs)
        
        above = [w for w in words if wordf(w, "en") > threshold*p]
        above = sort_frequent(above)
        below = [w for w in words if wordf(w, "en") <= threshold*p]
        below = sort_frequent(below)
        return above + below
    return sort


# comparison on naive probabilities
def gen_sort_place_probs():
    db = gen_place_probs_db(WORDS)
    measure = lambda w: prod([db[i][c] for i, c in enumerate(w)])
    def cmp(x, y):
        return measure(y) - measure(x)
    
    return lambda words: sorted(words, key=cmp_to_key(cmp))
def gen_place_probs_db(words, n_chars=WORD_LEN):
    res = [{} for _ in range(n_chars)]
    
    for i in range(n_chars):
        full = [w[i] for w in words]
        for l in ascii_uppercase:
            res[i][l] = full.count(l) / len(full)
    
    return res


# comparison on frequency of letters
def gen_sort_alpha_f():
    db = gen_alpha_f_db(WORDS)
    measure = lambda w: sum([db[c] for c in w])
    def cmp(x, y):
        return measure(y) - measure(x)
    
    return lambda words: sorted(words, key=cmp_to_key(cmp))

def gen_alpha_f_db(words):
    fs = {}
    catted = "".join(words)
    
    for l in ascii_uppercase:
        fs[l] = catted.count(l)
        
    return fs


def from_t(f, n_skip):
    i = 0
    def sort(words):
        nonlocal i
        i += 1
        if i <= n_skip:
            return words
        return f(words)
    
    return sort

def until_t(f, n_skip):
    i = 0
    def sort(words):
        nonlocal i
        i += 1
        if i <= n_skip:
            return f(words)
        return words
    
    return sort

# remote word bank
# WORDS = [w.upper() for w in get(WORDS_URL).text.split()]
# local word bank
with open(WORDS_FILE, "r") as f:
    WORDS = [w.strip().upper() for w in f.readlines()]

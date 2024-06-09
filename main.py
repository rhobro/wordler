from functools import cmp_to_key
from random import shuffle
import requests as rq
from string import ascii_uppercase
from math import prod
from wordfreq import word_frequency as freq


WORDS_URL = "https://raw.githubusercontent.com/rhobro/wordler/main/words.txt"


def main():
    # get word list
    rsp = rq.get(WORDS_URL)
    filtered = [w.upper() for w in rsp.text.split()]
    probs_db = gen_probs(filtered)
    
    while True:
        # sort for distinct characters
        shuffle(filtered)
        filtered = sorted(filtered, key=cmp_to_key(cmp_distinct_chars))
        # filtered = sorted(filtered, key=cmp_to_key(gen_cmp_probs(probs_db)))
        filtered = sorted(filtered, key=cmp_to_key(cmp_more_frequent))

        # guess
        guess = filtered[0]
        print(f"{guess} - {len(filtered)} words left")
        if len(filtered) == 1:  # found
            break
        
        # get correction colours
        correction = input("Feedback colours (b/y/g): ").lower()[:5]
        if correction == "ggggg":
            break
        
        # filter based on colours
        for i, c in enumerate(correction):
            if c == "b":
                # not in word
                filtered = [w for w in filtered if guess[i] not in w]
            elif c == "y":
                # not in that place
                filtered = [w for w in filtered if w[i] != guess[i] and guess[i] in w]
            elif c == "g":
                # in right place
                filtered = [w for w in filtered if w[i] == guess[i]]
                
                
def gen_probs(words, n_chars=5):
    res = [{} for _ in range(n_chars)]
    
    for i in range(n_chars):
        full = [w[i] for w in words]
        for l in ascii_uppercase:
            res[i][l] = full.count(l) / len(full)
    
    return res
        

# prioritise words with more distinct chars
def cmp_distinct_chars(x, y):
    return len(set(y)) - len(set(x))


def cmp_more_frequent(x, y):
    return freq(y, "en") - freq(x, "en")


def gen_cmp_probs(db):
    measure = lambda w: prod([db[i][c] for i, c in enumerate(w)])
    def cmp(x, y):
        return measure(y) - measure(x)
    
    return cmp
    

if __name__ == "__main__":
    main()
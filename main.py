from functools import cmp_to_key
from random import shuffle
import requests as rq


WORDS_URL = "https://raw.githubusercontent.com/rhobro/wordler/main/words.txt"


def main():
    # get word list
    rsp = rq.get(WORDS_URL)
    filtered = [w.upper() for w in rsp.text.split()]
    
    while True:
        # sort for distinct characters
        shuffle(filtered)
        filtered = sorted(filtered, key=cmp_to_key(cmp_distinct_chars))
        
        # guess
        guess = filtered[0]
        print(f"{guess} - {len(filtered)} words left")
        if len(filtered) == 1:  # found
            break
        
        # get correction colours
        correction = input("Feedback colours (b/y/g): ").lower()
        
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
        

# prioritise words with more distinct chars
def cmp_distinct_chars(x, y):
    return len(set(y)) - len(set(x))


if __name__ == "__main__":
    main()
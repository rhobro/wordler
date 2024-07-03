from bot import *


def main():
    bot = Bot(comparisons=STRATEGY_ALPHA)
    
    while True:
        
        # guess
        guess = bot.guess()
        print(f"\n{guess} - from {bot.n_possibilities} words ({bot.confidence * 100:.2f}%)")
        if bot.is_finished:
            break
        
        # get correction colours
        correction = input("Feedback colours (b/y/g): ").lower()
        # check commands
        if correction[0] == "/":
            if correction == "/list":
                bot.show_list()
            elif correction == "/probs":
                bot.show_probs()
            elif correction == "/insight":
                bot.show_insight()
            elif correction == "/q":
                print("Ending session")
                break
            continue
        
        # feedback
        bot.feedback(correction)
        
        
STRATEGY_FREQUENT_LETTERS = [
    gen_cmp_alpha_f(),
    cmp_distinct_chars,
]

STRATEGY_PLACE_PROBS = [
    gen_cmp_place_probs(),
    cmp_distinct_chars,
]

STRATEGY_FREQUENT = [
    cmp_frequent,
    cmp_distinct_chars,
]

STRATEGY_ALPHA = [
    gen_cmp_alpha_f(),
    cmp_distinct_chars,
    # gen_cmp_frequent(10),
]
    

if __name__ == "__main__":
    main()
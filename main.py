from bot import *


def main():
    bot = Bot(STRATEGY_ALPHA)
    
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
        

STRATEGY_ALPHA = [
    gen_sort_alpha_f(),
    until_t(sort_distinct_chars, 2),
    from_t(gen_sort_frequent(100), 1),
]
    

if __name__ == "__main__":
    main()
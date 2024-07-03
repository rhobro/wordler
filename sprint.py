from game import Game
from bot import Bot
from time import sleep


def main():
    game = Game()
    
    while True:
        bot = Bot()
        # wait to load
        while not game.is_ready:
            continue
        sleep(0.1)
        
        while True:
            # guess 
            game.guess(bot.guess())
            # wait for feedback
            while not game.has_processed:
                continue
            sleep(0.05)
            
            print(game.is_finished or bot.is_finished)
            if game.is_finished or bot.is_finished:
                break
            
            # return feedback
            bot.feedback(game.get_colours()[-5:])
        
        game.refresh()


if __name__ == "__main__":
    main()

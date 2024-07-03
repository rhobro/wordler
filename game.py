from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Safari


URL = "https://wordly.org/"


class Game:
    def __init__(self) -> None:
        self.browser = Safari()
        self.refresh()
        
    
    def get_colours(self):
        colours = self.browser \
            .find_elements(By.CSS_SELECTOR, "div.Row-letter")
        colours = [l.get_attribute("class") for l in colours]
        colours = [class_to_colour(c) for c in colours]
        colours = "".join(colours)
        
        return colours
    
    
    def get_letters(self):
        letters = self.browser \
            .find_elements(By.CSS_SELECTOR, "div.Row-letter")
        letters = [l.text[0] if len(l.text) > 0 else "" for l in letters]
        letters = "".join(letters)
        
        return letters
    
    
    def guess(self, word):
        self.browser \
            .find_element(By.CSS_SELECTOR, "body") \
            .send_keys(word + Keys.ENTER)
        
        
    def refresh(self):
        self.browser.get(URL)
        
        
    def get_alert(self):
        return self.browser.find_element(By.CSS_SELECTOR, "div.alert").text
        
    
    @property
    def has_processed(self):
        return len(self.get_colours()) == len(self.get_letters())
    
    
    @property
    def is_ready(self):
        return self.get_alert() != "Guess the first word!"
        
        
    @property
    def is_finished(self):
        cols = self.get_colours()
        letters = self.get_letters()
        return cols[-5:] == "ggggg" or len(letters) == 30 if len(cols) > 0 else False
        
        
def class_to_colour(categories):
    if "letter-absent" in categories:
        return "b"
    elif "letter-elsewhere" in categories:
        return "y"
    elif "letter-correct" in categories:
        return "g"
    return ""
        
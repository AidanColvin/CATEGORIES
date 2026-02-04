# Connections Word Game

A Python-based word puzzle game inspired by the popular Connections game. Players must identify groups of four related words from a grid of 16 words across total of 16 words 4 words in each category 4 categories in total

## Rules

# Categories
Categories - There are 4 categories, each category has a different level of difficulty (easy, medium, hard, expert)
Category should be related to the words in other categories (e.g. if the category is "animals", the other categories could be "colors", "fruits", "countries", etc.)
Categories should not be related to spelling or grammar (e.g. "verbs", "nouns", "adjectives", etc.)
Categories should not be related to root of words or adding a letter to the end or beginning of a word (e.g. "cat", "cats", "catty", etc.)

# Words
Words should be atleast 3 letters long
Words should be related to each other in some way (e.g. they could all be animals, or they could all be colors, etc.)
Words should be related to the category they are in (e.g. if the category is "animals", the words should be related to animals)
Words should be unique and not repeated in other categories (e.g. if the word "cat" is in the "animals" category, it should not be in the "colors" category)
Words should not be over 3 syllables long
Words should be common words that are easily recognizable and not obscure or technical terms (e.g. "cat", "dog", "red", "blue", etc.)

# User Interface
Words should be displayed in a random order each time the program is run, and the categories should also be displayed in a random order each time the program is run
Each Word should be displayed in its own single box with a border around it
Boxs should be displayed in a grid format with 4 boxes in each row and 4 rows in total

User should be able to click on a box to select the word inside, and the box should change color when clicked
Users should be able to click on a box again to deselect the word inside, and the box should change back to its original color when clicked again
When a user clicks on a box, the word inside should be added to a list of selected words, and when a user clicks on a box again to deselect it, the word should be removed from the list of selected words
When the user has selected 4 words, and presses submit buttom or the return button the program should check if the selected words are all in the same category, and if they are, the program should display the name of the category and all boxs should be changed to the categories color 
The category should be displayed above the boxes in a larger font size.     
If the selected words are not all in the same category, the program should display a message saying # of words off if 3 are corect say one off if 2 correct say 2 off otherwise say try again
Users should be able to reset the game at any time by pressing a reset button, which will clear the list of selected words, reset the colors of all boxes to their original color, and display a new set of words and categories in a random order.
Users should be able to shuffle the words at any time by pressing a shuffle button, which will display a new order of the same words and categories in a random order without resetting the game or clearing the list of selected words.
Users are able to have for submiting their answer by pressing the return button on their keyboard or clicking the submit button.

## Master Category Bank
How to grow the bank: This creates a "Chain" where DATE, LIME, and SILVER act as the connectors that confuse the player.
- Start with a Seed: FRUIT (Apple, Date, Lime, Kiwi)
- Find a Red Herring: CALENDAR (Date, Month, Year, Week)
- Find a Tricky: COLORS (Lime, Orange, Rose, Silver)
- Find an Expert: METALS (Silver, Gold, Iron, Tin)




""""
Rules

Categories - There are 4 categories, each category has a different level of difficulty (easy, medium, hard, expert)
Category should be related to the words in other categories (e.g. if the category is "animals", the other categories could be "colors", "fruits", "countries", etc.)
Categories should not be related to spelling or grammar (e.g. "verbs", "nouns", "adjectives", etc.)
Categories should not be related to root of words or adding a letter to the end or beginning of a word (e.g. "cat", "cats", "catty", etc.)

Words should be atleast 3 letters long
Words should be related to each other in some way (e.g. they could all be animals, or they could all be colors, etc.)
Words should be related to the category they are in (e.g. if the category is "animals", the words should be related to animals)
Words should be unique and not repeated in other categories (e.g. if the word "cat" is in the "animals" category, it should not be in the "colors" category)
Words should not be over 3 syllables long
Words should be common words that are easily recognizable and not obscure or technical terms (e.g. "cat", "dog", "red", "blue", etc.)

Total of 16 words
4 words in each category
4 categories in total


Words should be displayed in a random order each time the program is run, and the categories should also be displayed in a random order each time the program is run
Each Word should be displayed in its own single box with a border around it
Boxs should be displayed in a grid format with 4 boxes in each row and 4 rows in total

User should be able to click on a box to select the word inside, and the box should change color when clicked
Users should be able to click on a box again to deselect the word inside, and the box should change back to its original color when clicked again
When a user clicks on a box, the word inside should be added to a list of selected words, and when a user clicks on a box again to deselect it, the word should be removed from the list of selected words
When the user has selected 4 words, and presses submit buttom or the return button the program should check if the selected words are all in the same category, and if they are, the program should display the name of the category and all boxs should be changed to the categories color 
The category should be displayed above the boxes in a larger font size.     
If the selected words are not all in the same category, the program should display a message saying # of words off if 3 are corect say one off if 2 correct say 2 off otherwise say try again

Users should be able to reset the game at any time by pressing a reset button, which will clear the list of selected words, reset the colors of all boxes to their original color, and display a new set of words and categories in a random order.
Users should be able to shuffle the words at any time by pressing a shuffle button, which will display a new order of the same words and categories in a random order without resetting the game or clearing the list of selected words.
Users are able to have for submiting their answer by pressing the return button on their keyboard or clicking the submit button.

"""

# Category 1 - Easy (LIGHT SOFT GREEN)
# Genarate a series of 4 words, each word should be 3 letters long, and the words should be related to each other in some way. 

# Category 2 - Medium (LIGHT SOFT BLUE)
# Genarate a series of 4 words, each word should be 3 letters long, and the words should be related to each other in some way. 

# Category 3 - Hard (LIGHT SOFT YELLOW)
# Genarate a series of 4 words, each word should be 3 letters long, and the words should be related to each other in some way.

# Category 4 - Expert (LIGHT SOFT RED)
# Genarate a series of 4 words, each word should be 3 letters long, and the words should be related to each other in some way.


import json
import random
import tkinter as tk
from tkinter import messagebox

class ConnectionsEngine:
    """
    Logic engine for selecting and assembling tricky word puzzles.
    
    Attributes:
        bank (list): A list of dictionaries containing category names and words.
    """

    def __init__(self, json_path):
        """
        Initializes the engine by loading the master category bank.

        Args:
            json_path (str): Path to the master_category_bank.json file.
        """
        with open(json_path, 'r') as f:
            data = json.load(f)
            # Flattens the nested 'batches' structure into a single list
            self.bank = []
            for batch in data['batches'].values():
                self.bank.extend(batch)

    def get_overlap_count(self, cat1_words, cat2_words):
        """
        Calculates the number of shared words between two lists.

        Args:
            cat1_words (list): List of strings (words).
            cat2_words (list): List of strings (words).

        Returns:
            int: The count of overlapping words.
        """
        return len(set(cat1_words).intersection(set(cat2_words)))

    def find_category_with_overlap(self, target_words, required_overlap, exclude_names):
        """
        Searches the bank for a category with a specific overlap count.

        Args:
            target_words (list): All words currently on the board.
            required_overlap (int): Exact number of words that must overlap.
            exclude_names (set): Names of categories already in the puzzle.

        Returns:
            dict: A category dictionary or None if no match is found.
        """
        candidates = []
        for cat in self.bank:
            if cat['name'] in exclude_names:
                continue
            
            overlap = self.get_overlap_count(target_words, cat['words'])
            if overlap == required_overlap:
                candidates.append(cat)
        
        return random.choice(candidates) if candidates else None

    def build_puzzle(self):
        """
        Assembles a 4-category puzzle using overlap logic for difficulty.

        The logic creates 'red herrings' by ensuring subsequent categories 
        share words with previous ones.

        Returns:
            list: A list of 4 category dictionaries.
        """
        # 1. Start with a random Seed (any category can be a seed)
        seed_cat = random.choice(self.bank)
        puzzle = [seed_cat]
        exclude = {seed_cat['name']}
        board_words = list(seed_cat['words'])

        # 2. Find Tricky (Target: 3 word overlap)
        tricky = self.find_category_with_overlap(board_words, 3, exclude)
        if not tricky: tricky = random.choice(self.bank) # Fallback
        puzzle.append(tricky)
        exclude.add(tricky['name'])
        board_words.extend(tricky['words'])

        # 3. Find Hard (Target: 3 word overlap)
        hard = self.find_category_with_overlap(board_words, 3, exclude)
        if not hard: hard = random.choice(self.bank)
        puzzle.append(hard)
        exclude.add(hard['name'])
        board_words.extend(hard['words'])

        # 4. Find Expert (Target: 2 word overlap)
        expert = self.find_category_with_overlap(board_words, 2, exclude)
        if not expert: expert = random.choice(self.bank)
        puzzle.append(expert)

        return puzzle

---

**Note**: This is an educational project and is not affiliated with or endorsed by The New York Times.

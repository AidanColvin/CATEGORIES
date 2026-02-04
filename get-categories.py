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

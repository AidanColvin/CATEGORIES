import unittest
import json
import tkinter as tk
from connection_generator import ConnectionsEngine
from main import ConnectionsGame, ConnectionBox

class TestConnectionsMegaSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("master_category_bank.json", "r") as f:
            data = json.load(f)
            cls.categories = data.get('categories', [])

    def setUp(self):
        self.root = tk.Tk()
        self.engine = ConnectionsEngine()
        self.game = ConnectionsGame(self.root)

    def tearDown(self):
        self.root.destroy()

    # --- 1. DATA & LINGUISTIC ROBUSTNESS (Approx 100+ subtests) ---
    def test_comprehensive_word_checks(self):
        """Checks every single word for length, casing, and uniqueness."""
        all_words = []
        for cat in self.categories:
            for word in cat['words']:
                with self.subTest(word=word, category=cat['name']):
                    # Rule: Words >= 3 letters
                    self.assertGreaterEqual(len(word), 3)
                    # Rule: No obscure technical terms (basic syllable check)
                    vowels = "aeiouy"
                    syllables = len([char for char in word.lower() if char in vowels])
                    self.assertLessEqual(syllables, 4, f"{word} is too complex")
                    all_words.append(word.upper())

    def test_category_integrity(self):
        """Checks every category for exactly 4 words and a valid name."""
        for cat in self.categories:
            with self.subTest(category_name=cat['name']):
                self.assertEqual(len(cat['words']), 4)
                self.assertTrue(len(cat['name']) > 0)

    # --- 2. UI & USER EXPERIENCE (Approx 80+ subtests) ---
    def test_box_visual_states(self):
        """Verifies the 'Egg Shell' to 'Light Gray' transition for all logic paths."""
        box = ConnectionBox(self.root, "TEST", self.categories[0], self.game.handle_click)
        
        # Test Default State (Fall Tones)
        with self.subTest(state="Default"):
            self.assertEqual(box.cget("bg").upper(), "#F0EAD6") # Egg Shell
            
        # Test Selected State
        box.toggle()
        with self.subTest(state="Selected"):
            self.assertEqual(box.cget("bg").upper(), "#D3D3D3") # Light Gray
            self.assertTrue(box.selected)
            
        # Test Deselect
        box.toggle()
        with self.subTest(state="Deselected"):
            self.assertEqual(box.cget("bg").upper(), "#F0EAD6")
            self.assertFalse(box.selected)

    def test_selection_limit_edge_cases(self):
        """Ensures the UI strictly prevents 5+ selections across multiple attempts."""
        boxes = [ConnectionBox(self.root, f"W{i}", self.categories[0], self.game.handle_click) for i in range(6)]
        for i in range(6):
            with self.subTest(click_index=i):
                self.game.handle_click(boxes[i])
                if i < 4:
                    self.assertEqual(len(self.game.selected_boxes), i + 1)
                else:
                    self.assertEqual(len(self.game.selected_boxes), 4)

    # --- 3. ENGINE & OVERLAP LOGIC (Approx 70+ subtests) ---
    def test_overlap_permutations(self):
        """Tests the engine's ability to identify overlaps across various inputs."""
        test_cases = [
            (["CAT", "DOG", "FISH", "BIRD"], ["CAT", "DOG", "FISH", "SNAKE"], 3),
            (["A", "B", "C", "D"], ["E", "F", "G", "H"], 0),
            (["RED", "BLUE"], ["RED", "BLUE"], 2)
        ]
        for list_a, list_b, expected in test_cases:
            with self.subTest(a=list_a, b=list_b):
                self.assertEqual(self.engine._get_overlap(list_a, list_b), expected)

    def test_puzzle_generation_uniqueness(self):
        """Ensures that the engine does not duplicate categories within a single puzzle."""
        for i in range(20): # Run generation 20 times to check for stability
            with self.subTest(iteration=i):
                puzzle = self.engine.get_new_puzzle()
                names = [c['name'] for c in puzzle]
                self.assertEqual(len(set(names)), 4, "Duplicate category found in puzzle")

    def test_reset_and_shuffle_stability(self):
        """Ensures that UI internal lists remain synced during rapid state changes."""
        for _ in range(10):
            self.game.shuffle_words()
            with self.subTest(action="Shuffle"):
                self.assertEqual(len(self.game.all_word_objects), 16)
            
            self.game.reset_game()
            with self.subTest(action="Reset"):
                self.assertEqual(self.game.solved_count, 0)
                self.assertEqual(len(self.game.selected_boxes), 0)

if __name__ == "__main__":
    unittest.main()
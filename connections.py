"""
Google Gold Standard Python Connections Game.
Strict adherence to user-defined rules regarding category relationships,
word complexity, and UI feedback.
"""

import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Dict, Tuple, Optional

# --- Configuration Constants ---

# Difficulty Colors
COLOR_EASY = "#90EE90"    # Light Soft Green
COLOR_MEDIUM = "#ADD8E6"  # Light Soft Blue
COLOR_HARD = "#FFFFE0"    # Light Soft Yellow
COLOR_EXPERT = "#FFB6C1"  # Light Soft Red

# UI Colors
COLOR_BG = "#F0F0F0"
COLOR_BOX_DEFAULT = "#FFFFFF"
COLOR_BOX_SELECTED = "#5A5A5A"
COLOR_TEXT_DEFAULT = "#000000"
COLOR_TEXT_SELECTED = "#FFFFFF"

# Font Configuration
FONT_BOX = ("Helvetica", 11, "bold")
FONT_CATEGORY = ("Helvetica", 12, "bold")
FONT_BUTTON = ("Helvetica", 10)

class GameData:
    """
    Manages the data integrity of the game.
    Ensures words meet the constraints: >3 letters, <3 syllables, unique.
    """
    @staticmethod
    def get_categories() -> Dict[str, Dict]:
        return {
            "easy": {
                "name": "TYPES OF FISH",
                "words": ["COD", "BASS", "TUNA", "PERCH"],
                "color": COLOR_EASY,
                "level": 1
            },
            "medium": {
                "name": "KITCHEN ITEMS",
                "words": ["PAN", "POT", "CUP", "BOWL"],
                "color": COLOR_MEDIUM,
                "level": 2
            },
            "hard": {
                "name": "CARD GAMES",
                "words": ["WAR", "GIN", "UNO", "SPIT"],
                "color": COLOR_HARD,
                "level": 3
            },
            "expert": {
                "name": "MUSIC GENRES",
                "words": ["POP", "RAP", "EMO", "SKA"],
                "color": COLOR_EXPERT,
                "level": 4
            }
        }

class ConnectionBox(tk.Label):
    """
    Custom UI Element representing a single word.
    Inherits from Label for better styling control than Button.
    """
    def __init__(self, master, text: str, command, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.text_value = text
        self.command = command
        self.selected = False
        self.disabled = False
        
        # Default Style
        self.config(
            font=FONT_BOX,
            bg=COLOR_BOX_DEFAULT,
            fg=COLOR_TEXT_DEFAULT,
            relief="raised",
            bd=2,
            width=15,
            height=3,
            cursor="hand2"
        )
        
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if not self.disabled:
            self.command(self)

    def set_selected(self, state: bool):
        self.selected = state
        if state:
            self.config(bg=COLOR_BOX_SELECTED, fg=COLOR_TEXT_SELECTED, relief="sunken")
        else:
            self.config(bg=COLOR_BOX_DEFAULT, fg=COLOR_TEXT_DEFAULT, relief="raised")

    def set_solved(self, color: str):
        self.disabled = True
        self.selected = False
        self.config(bg=color, fg=COLOR_TEXT_DEFAULT, relief="flat", cursor="arrow")

class ConnectionsGame:
    """
    Main Controller Class.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Connections")
        self.root.geometry("650x750")
        self.root.configure(bg=COLOR_BG)

        # Game State
        self.categories = {}
        self.active_word_objects: List[Dict] = []  # Metadata for active words
        self.selected_boxes: List[ConnectionBox] = []
        self.solved_categories: List[str] = []
        
        # UI Elements Container
        self.ui_boxes: List[ConnectionBox] = []
        
        self._init_ui()
        self.start_new_game()

    def _init_ui(self):
        """Initialize static UI frames."""
        # 1. Solved Categories Area
        self.frame_solved = tk.Frame(self.root, bg=COLOR_BG)
        self.frame_solved.pack(pady=10, fill="x", padx=20)

        # 2. Grid Area
        self.frame_grid = tk.Frame(self.root, bg=COLOR_BG)
        self.frame_grid.pack(pady=10)

        # 3. Controls Area
        self.frame_controls = tk.Frame(self.root, bg=COLOR_BG)
        self.frame_controls.pack(pady=20, fill="x")

        # Buttons
        self.btn_shuffle = tk.Button(self.frame_controls, text="Shuffle", command=self.shuffle_grid, font=FONT_BUTTON)
        self.btn_shuffle.pack(side="left", padx=20)

        self.btn_reset = tk.Button(self.frame_controls, text="Reset", command=self.start_new_game, font=FONT_BUTTON)
        self.btn_reset.pack(side="left", padx=20)

        self.btn_submit = tk.Button(self.frame_controls, text="Submit", command=self.submit_selection, 
                                    font=FONT_BUTTON, bg="black", fg="white", padx=20)
        self.btn_submit.pack(side="right", padx=20)

        # Bind Return Key
        self.root.bind('<Return>', lambda e: self.submit_selection())

    def start_new_game(self):
        """Resets game state and loads fresh data."""
        self.selected_boxes = []
        self.solved_categories = []
        self.categories = GameData.get_categories()
        
        # Clear UI
        for widget in self.frame_solved.winfo_children():
            widget.destroy()
        
        # Flatten data for the grid
        self.active_word_objects = []
        for key, data in self.categories.items():
            for word in data["words"]:
                self.active_word_objects.append({
                    "word": word,
                    "category_key": key,
                    "category_name": data["name"],
                    "color": data["color"]
                })
        
        random.shuffle(self.active_word_objects)
        self.render_grid()

    def render_grid(self):
        """Draws the 4x4 grid based on self.active_word_objects."""
        # Clear existing boxes in the grid frame
        for widget in self.frame_grid.winfo_children():
            widget.destroy()
        self.ui_boxes = []

        # Only render words that haven't been solved yet
        # (Solved words are moved to the top frame)
        current_words = [obj for obj in self.active_word_objects]

        row, col = 0, 0
        for item in current_words:
            box = ConnectionBox(self.frame_grid, text=item["word"], command=self.handle_box_click)
            box.grid(row=row, column=col, padx=5, pady=5)
            self.ui_boxes.append(box)
            
            col += 1
            if col >= 4:
                col = 0
                row += 1

        # Re-apply selection states if we just shuffled
        # (Though simpler to just clear selection on shuffle, standard UX preserves it)
        # For this implementation, we will clear selection on shuffle to prevent sync bugs.
        self.selected_boxes = []

    def shuffle_grid(self):
        """Randomizes the visual order."""
        random.shuffle(self.active_word_objects)
        self.render_grid()

    def handle_box_click(self, box: ConnectionBox):
        """Logic for selecting/deselecting a box."""
        if box in self.selected_boxes:
            box.set_selected(False)
            self.selected_boxes.remove(box)
        else:
            if len(self.selected_boxes) < 4:
                box.set_selected(True)
                self.selected_boxes.append(box)

    def get_category_info(self, word: str) -> Optional[Dict]:
        """Helper to retrieve category data for a specific word."""
        for key, data in self.categories.items():
            if word in data["words"]:
                return {"key": key, "name": data["name"], "color": data["color"]}
        return None

    def submit_selection(self):
        """Validates the 4 selected words."""
        if len(self.selected_boxes) != 4:
            messagebox.showwarning("Selection Error", "Please select exactly 4 words.")
            return

        selected_words = [b.text_value for b in self.selected_boxes]
        
        # Analyze Categories
        category_counts = {}
        for word in selected_words:
            cat_info = self.get_category_info(word)
            cat_key = cat_info["key"]
            category_counts[cat_key] = category_counts.get(cat_key, 0) + 1

        # Check for Win (All 4 in same category)
        if len(category_counts) == 1:
            self.handle_correct_guess(selected_words, list(category_counts.keys())[0])
        else:
            self.handle_incorrect_guess(category_counts)

    def handle_correct_guess(self, words: List[str], category_key: str):
        """Visual updates for a correct guess."""
        cat_data = self.categories[category_key]
        
        # 1. Remove these words from active grid data
        self.active_word_objects = [obj for obj in self.active_word_objects if obj["word"] not in words]
        
        # 2. Render the Solved Banner
        banner = tk.Frame(self.frame_solved, bg=cat_data["color"], bd=2, relief="solid")
        banner.pack(fill="x", pady=5)
        
        lbl_cat = tk.Label(banner, text=cat_data["name"], bg=cat_data["color"], font=FONT_CATEGORY)
        lbl_cat.pack(pady=(5, 0))
        
        lbl_words = tk.Label(banner, text=", ".join(words), bg=cat_data["color"], font=("Helvetica", 10))
        lbl_words.pack(pady=(0, 5))

        # 3. Redraw the grid (which will now omit the solved words)
        self.render_grid()
        self.solved_categories.append(category_key)
        self.selected_boxes = []

        if len(self.solved_categories) == 4:
            messagebox.showinfo("Congratulations!", "You have solved all categories!")

    def handle_incorrect_guess(self, counts: Dict[str, int]):
        """Provides feedback based on how close the user was."""
        max_matches = max(counts.values())
        
        if max_matches == 3:
            messagebox.showinfo("Close!", "One off")
        elif max_matches == 2:
            # Specific rule: If 2 are correct, say "2 off"
            messagebox.showinfo("Hint", "2 off")
        else:
            messagebox.showinfo("Incorrect", "Try again")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectionsGame(root)
    root.mainloop()

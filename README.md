A category puzzle using overlap logic for difficulty

# Categories

# Category 1 - Seed (LIGHT SOFT GREEN)
Definition: The most "obvious" group, but still compromised.
The Rule: Must have a 2-word overlap.
Effect: Even the easiest category has 50% of its words "stolen" by other more complex categories.
COLOR_SEED = "#90EE90"    # Light Soft Green

# Category 2 - Red Herring (LIGHT SOFT BLUE)
Definition: The primary distractor.
The Rule: Must have a 3-word overlap with the Seed or Tricky groups.
Effect: This specifically targets the "obvious" connections, making the player second-guess the simplest category.
COLOR_RED_HERRING = "#ADD8E6"  # Light Soft Blue

# Category 3 - Tricky (LIGHT SOFT YELLOW)
Definition: A high-interference group.
The Rule: Must have a 3-word overlap with the rest of the board.
Effect: This creates a "Red Herring" situation where the player sees a nearly complete set of 4, but one word is actually part of the Expert or Seed group.
COLOR_TRICKY = "#FFFFE0"    # Light Soft Yellow

# Category 4 - Expert (LIGHT SOFT RED)
Definition: This is the hardest category to solve because it doesn't exist in isolation.
The Rule: It must have an overlap of at least 4 words across the other three categories.
Effect: Every single word in the Expert category could "logically" fit somewhere else, forcing the player to solve the other three groups first to find what's left over.
COLOR_Expert = "#FFB6C1"  # Light Soft Red

# Categories Rules
There are four categories, each category has a different level of difficulty (hard, tricky, red herring, seed) 
Categories should be related to the words in other categories (e.g. if the category is "animals", the other categories could be "colors", "fruits", "countries", etc.) 
Categories should not be related to spelling or grammar (e.g. "verbs", "nouns", "adjectives", etc.) 
Categories should not be related to root of words or adding a letter to the end or beginning of a word (e.g. "cat", "cats", "catty", etc.)

# Knowlage Generator
master_category_bank.json


# Funtion Flow
Import master_category_bank.json 
Find overlap count
Category overlap
Select seed
Select red hair
Select Tricky
Hard

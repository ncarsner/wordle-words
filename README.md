# wordle-words
App to generate an array of 5-letter words all with unique letters, to propose efficient narrowing of qualifying words for Wordle game.

## Word List Management

This project includes command-line utilities to examine and modify the word list in `words.py`.

### Usage

Run the utility from the project root directory:

```bash
python utils/utils.py [command] [options]
```

### Available Commands

#### `stats` - Show Word List Statistics
Display comprehensive statistics about the current word list:
```bash
python utils/utils.py stats
```
**Output includes:**
- Total word count
- Number of unique words
- Number of duplicates
- Whether the list is alphabetically sorted

#### `scarce-letters` - Find Least Common Letters
Identify the least frequently used letters in the word list:
```bash
# Find 3 least common letters (default)
python utils/utils.py scarce-letters

# Find 5 least common letters
python utils/utils.py scarce-letters --num 5
```
**Use case:** Helpful for Wordle strategy - these letters appear less frequently in the word list.

#### `remove-duplicates` - Clean Duplicate Words
Remove duplicate entries from the word list and update `words.py`:
```bash
python utils/utils.py remove-duplicates
```
**⚠️ Note:** This modifies the `words.py` file in place.

#### `sort` - Alphabetically Sort Word List
Sort the word list alphabetically and update `words.py`:
```bash
python utils/utils.py sort
```
**⚠️ Note:** This modifies the `words.py` file in place.

### Examples

```bash
# Check current status
python utils/utils.py stats

# Clean up the word list
python utils/utils.py remove-duplicates
python utils/utils.py sort

# Analyze letter frequency for Wordle strategy
python utils/utils.py scarce-letters --num 10
```

### Help

For detailed command options:
```bash
python utils/utils.py --help
```

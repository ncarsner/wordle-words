# wordle-words
App to generate an array of 5-letter words all with unique letters, to propose efficient narrowing of qualifying words for Wordle game.

## Main Word Generator

The core functionality is in `src/main.py` - it generates sets of 5-letter words where **no letter appears in multiple words**. This is perfect for Wordle strategy as it maximizes letter coverage.

### Usage

Run from the project root directory:

```bash
# Generate default number of words (attempts 5, but may find fewer)
python -m src.main

# Generate specific number of words
python -m src.main 3
python -m src.main 4
python -m src.main 10
```

### Examples

```bash
$ python -m src.main 3
Selected words: ['clack', 'biter', 'found']
Used letters: ABCDEF__I_KL_NO__R_TU_____

$ python -m src.main 4
Selected words: ['squad', 'glory', 'mimic', 'theft']
Used letters: A_CDEFGHI__LM_O_QRSTU___Y_

$ python -m src.main
Selected words: ['regal', 'couch', 'ditty']
Used letters: A_CDE_GHI__L__O__R_TU___Y_
```

### How It Works

1. **Shuffles** the word list randomly for variety
2. **Selects words** with no overlapping letters
3. **Stops** when the requested number is reached or no more qualifying words exist
4. **Displays** the selected words and all unique letters used (sorted a-z)

### Wordle Strategy Benefits

- **Maximum letter coverage** - Each word uses completely different letters
- **Efficient elimination** - Quickly narrow down possible answers
- **Alphabet scanning** - Sorted letter output shows coverage gaps

## Word List Management

This project includes command-line utilities to examine and modify the word list in `words.py`.

### Usage

Run the utility from the project root directory:

```bash
python -m src.main [command] [options]
```

### Available Commands

#### `stats` - Show Word List Statistics
Display comprehensive statistics about the current word list:
```bash
python -m src.main stats
```
**Output includes:**
- Total word count
- Number of unique words
- Number of duplicates
- Whether the list is alphabetically sorted

#### `find-scarce` - Find Least Common Letters
Identify the least frequently used letters in the word list:
```bash
# Find 3 least common letters (default)
python -m src.main find-scarce

# Find 5 least common letters
python -m src.main find-scarce --num 5
```
**Use case:** Helpful for Wordle strategy - these letters appear less frequently in the word list.

#### `dedup` - Clean Duplicate Words
Remove duplicate entries from the word list and update `words.py`:
```bash
python -m src.main dedup
```
**⚠️ Note:** This modifies the `words.py` file in place.

#### `sort` - Alphabetically Sort Word List
Sort the word list alphabetically and update `words.py`:
```bash
python -m src.main sort
```
**⚠️ Note:** This modifies the `words.py` file in place.

### Examples

```bash
# Check current status
python -m src.main stats

# Clean up the word list
python -m src.main clean
python -m src.main dedup
python -m src.main sort

# Analyze letter frequency for Wordle strategy
python -m src.main find-scarce --num 10
```

### Help

For detailed command options:
```bash
python -m src.main --help
```

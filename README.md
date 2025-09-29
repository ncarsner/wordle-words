# wordle-words
App to generate an array of 5-letter words all with unique letters, to propose efficient narrowing of qualifying words for Wordle game.

## Main Word Generator

The core functionality is in `src/main.py` - it generates sets of 5-letter words where **no letter appears in multiple words**. This is perfect for Wordle strategy as it maximizes letter coverage.

### Usage

Run from the project root directory:

```bash
# Generate default number of words (attempts 5, but may find fewer)
python src/main.py

# Generate specific number of words
python src/main.py 3
python src/main.py 4
python src/main.py 10
```

### Examples

```bash
$ python src/main.py 3
Selected words: ['shuck', 'eagle', 'dizzy']
Used letters: acdeghiklsuyz

$ python src/main.py 4
Selected words: ['jazzy', 'quill', 'detox']
Used letters: adeilloqtuxy

$ python src/main.py
Selected words: ['adept', 'frown', 'silly']
Used letters: adefilnoprstwy
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

#### `find-scarce` - Find Least Common Letters
Identify the least frequently used letters in the word list:
```bash
# Find 3 least common letters (default)
python utils/utils.py find-scarce

# Find 5 least common letters
python utils/utils.py find-scarce --num 5
```
**Use case:** Helpful for Wordle strategy - these letters appear less frequently in the word list.

#### `dedup` - Clean Duplicate Words
Remove duplicate entries from the word list and update `words.py`:
```bash
python utils/utils.py dedup
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
python utils/utils.py dedup
python utils/utils.py sort

# Analyze letter frequency for Wordle strategy
python utils/utils.py find-scarce --num 10
```

### Help

For detailed command options:
```bash
python utils/utils.py --help
```

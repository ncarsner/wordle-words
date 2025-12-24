# wordle-words
App to generate an array of 5-letter words all with unique letters, to propose efficient narrowing of qualifying words for Wordle game.

## Main Word Generator

The core functionality generates sets of 5-letter words where **no letter appears in multiple words**. This is perfect for Wordle strategy as it maximizes letter coverage.

### Usage

Run from the project root directory:

```bash
# Generate default number of words (attempts 3, but may find fewer)
ww

# Generate specific number of words
ww 2
ww 4
ww 5

# Generate words with no repeating letters
ww 3 -u
ww -u
```

### Examples

```bash
$ ww 3
Selected words: ['clack', 'biter', 'found']
Used letters: ABCDEF__I_KL_NO__R_TU_____

$ ww 4
Selected words: ['squad', 'glory', 'mimic', 'theft']
Used letters: A_CDEFGHI__LM_O_QRSTU___Y_

$ ww
Selected words: ['regal', 'couch', 'ditty']
Used letters: A_CDE_GHI__L__O__R_TU___Y_

$ ww 4 -u
Selected words: ['frail', 'wench', 'judgy', 'stomp']
Used letters: A_CDEFGHIJ_LMNOP_RSTU_W_Y_

$ ww 2 -u
Selected words: ['mango', 'build']
Used letters: AB_D__G_I__LMNO_____U_____

$ ww -u
Selected words: ['clean', 'ivory', 'thump']
Used letters: A_C_E__HI__LMNOP_R_TUV__Y_
```

### How It Works

1. **Samples** the word list randomly for variety
2. **Selects words** with no overlapping letters
3. **Stops** when the requested number is reached or no more qualifying words exist
4. **Displays** the selected words and all unique letters used (sorted a-z)

### Wordle Strategy Benefits

- **Maximum letter coverage** - Each word introduces different letters
- **Efficient elimination** - Quickly narrow down possible answers
- **Alphabet scanning** - Sorted letter output shows coverage gaps

## Word List Management

This project includes command-line utilities to examine and modify the word list in `words.py`.

### Usage

Run the utility from the project root directory:

```bash
ww [command] [options]
```

### Available Commands

#### `stats` - Show Word List Statistics
Display comprehensive statistics about the current word list:
```bash
ww stats
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
ww find-scarce

# Find 5 least common letters
ww find-scarce --num 5
```
**Use case:** Helpful for Wordle strategy - these letters appear less frequently in the word list.

#### `dedup` - Clean Duplicate Words
Remove duplicate entries from the word list and update `words.py`:
```bash
ww dedup
```
**⚠️ Note:** This modifies the `words.py` file in place.

#### `sort` - Alphabetically Sort Word List
Sort the word list alphabetically and update `words.py`:
```bash
ww sort
```
**⚠️ Note:** This modifies the `words.py` file in place.

### Examples

```bash
# Check current status
ww stats

# Clean up the word list
ww clean
ww dedup
ww sort

# Analyze letter frequency for Wordle strategy
ww find-scarce --num 10
```

### Help

For detailed command options:
```bash
ww --help
```

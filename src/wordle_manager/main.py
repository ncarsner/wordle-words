import sys
import random
from string import ascii_lowercase

from .cli import parse_args
from .utils import WordListManager, has_repeating_letters
from .words import word_list


def run(num_words=3, unique_letters=None):
    used_letters = set()
    selected_words = []
    
    # Filter word list if unique letters flag is set
    available_words = word_list
    if unique_letters is not None:
        available_words = [word for word in word_list if not has_repeating_letters(word)]
    for word in random.sample(available_words, len(available_words)):
        if not any(letter in used_letters for letter in word):
            selected_words.append(word)
            used_letters.update(word)

        if len(selected_words) == num_words:
            break

    used_letters = "".join(
        letter if letter in used_letters else "_" for letter in ascii_lowercase
    )

    print("Selected words:", selected_words)
    print("Used letters:", used_letters.upper())


def main():
    # Handle special case: positional number argument before flags
    # Transform 'ww 3 -u' into 'ww -n 3 -u' for argparse
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        num = sys.argv[1]
        sys.argv = [sys.argv[0]] + ['-n', num] + sys.argv[2:]
    
    args = parse_args()
    
    # If no action specified, run word selection
    if not args.action:
        num_words = args.num_words
        run(num_words, unique_letters=args.u)
        return
    
    # Handle management actions
    manager = WordListManager()
    
    match args.action:
        case "stats":
            manager.show_stats()
        case "find-scarce":
            manager.find_scarce_letters(args.num)
        case "dedup":
            manager.remove_duplicates()
        case "sort":
            manager.sort_words()
        case "add":
            if not args.word:
                print("Error: No word provided to add.")
                sys.exit(1)
            manager.add_word(args.word)
        case "clean":
            manager.remove_invalid_words()
            print("Clean operation completed")
        case _:
            num_words = args.num_words
            run(num_words)

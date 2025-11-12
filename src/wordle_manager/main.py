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
    if unique_letters:
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
    # Handle simple cases and word generation with flags
    # Check if we have numeric arguments or flags that indicate word generation
    has_flag = '-u' in sys.argv
    has_numeric = any(arg.isdigit() for arg in sys.argv[1:])
    has_action = any(arg in ['stats', 'dedup', 'sort', 'clean', 'find-scarce', 'add'] for arg in sys.argv[1:])
    
    # If no action command and either has flags or numeric args, handle as word generation
    if not has_action and (has_flag or has_numeric or len(sys.argv) == 1):
        # Parse for word generation mode
        # Handle legacy simple numeric argument
        if len(sys.argv) <= 2 and (len(sys.argv) == 1 or sys.argv[1].isdigit()):
            num_words = int(sys.argv[1]) if len(sys.argv) == 2 else 3
            run(num_words)
            sys.exit(0)
        
        # Handle cases with flags like 'ww 3 -u' or 'ww -u'
        unique_flag = '-u' in sys.argv
        num_words = 3  # default
        
        # Extract numeric argument if present
        for arg in sys.argv[1:]:
            if arg.isdigit():
                num_words = int(arg)
                break
        
        run(num_words, unique_letters=unique_flag)
        sys.exit(0)

    # For other cases, use the full argument parser
    args = parse_args()
    manager = WordListManager()
    
    # Handle actions that use WordListManager
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
            # Default behavior: word selection with potential flags
            num_words = args.num_words
            run(num_words, unique_letters=args.u)

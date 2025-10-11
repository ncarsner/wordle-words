import sys
import random
import argparse

from .utils import WordListManager
from .words import word_list


def main(num_words=5):
    used_letters = set()
    selected_words = []

    for word in random.sample(word_list, len(word_list)):
        if not any(letter in used_letters for letter in word):
            selected_words.append(word)
            used_letters.update(word)

        if len(selected_words) == num_words:
            break

    print("Selected words:", selected_words)
    print("Used letters:", "".join(sorted(used_letters)))


if __name__ == "__main__": # pragma: no cover
    # Default behavior
    if len(sys.argv) <= 2 and (len(sys.argv) == 1 or sys.argv[1].isdigit()):
        num_words = int(sys.argv[1]) if len(sys.argv) == 2 else None
        main(num_words or 5)
        sys.exit(0)

    # Handle action commands and other arguments
    parser = argparse.ArgumentParser(
        description="Examine and modify the Wordle word list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "action",
        nargs="?",  # Optional
        choices=["find-scarce", "dedup", "sort", "stats", "add", "clean"],
        help="Action to perform on the word list"
    )
    parser.add_argument(
        "--num",
        type=int,
        default=3,
        help="Number of scarce letters to find (default: 3)"
    )
    parser.add_argument(
        "word", 
        nargs="?", 
        help="Word to add (required for 'add' action)"
    )

    args = parser.parse_args()

    # If no action provided, generate words
    if not args.action:
        if args.word and args.word.isdigit():
            main(int(args.word))
        else:
            main()
    else:
        manager = WordListManager()

        if args.action == "stats":
            manager.show_stats()
        elif args.action == "find-scarce":
            manager.find_scarce_letters(args.num)
        elif args.action == "dedup":
            manager.remove_duplicates()
        elif args.action == "sort":
            manager.sort_words()
        elif args.action == "add":
            if not args.word:
                print("Error: 'add' action requires a word argument")
                print("Usage: python -m src.main add <word>")
            else:
                manager.add_word(args.word)
        elif args.action == "clean":
            manager.remove_invalid_words()

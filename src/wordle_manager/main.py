import sys
import random
from string import ascii_lowercase

from .cli import parse_args
from .utils import WordListManager
from .words import word_list


def run(num_words=3):  # pragma: no cover
    used_letters = set()
    selected_words = []

    for word in random.sample(word_list, len(word_list)):
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
    if len(sys.argv) <= 2 and (len(sys.argv) == 1 or sys.argv[1].isdigit()):
        num_words = int(sys.argv[1]) if len(sys.argv) == 2 else None
        run(num_words or 3)
        sys.exit(0)

    manager = WordListManager()
    args = parse_args()
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
            word_arg = getattr(args, "word", None)
            run(int(word_arg)) if word_arg and str(word_arg).isdigit() else run()

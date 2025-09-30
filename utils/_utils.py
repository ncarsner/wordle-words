import argparse
import sys
from collections import Counter
from pathlib import Path

# Add parent directory to sys.path to import words module
sys.path.append(str(Path(__file__).parent.parent))

try:
    from words import word_list
except ImportError:
    print("Error: Cannot find words.py module")
    sys.exit(1)


def remove_invalid_words():
    vowels = set("aeiouy")
    original_count = len(word_list)
    valid_words = [
        word for word in word_list
        if len(word) == 5 and word.isalpha() and any(char in vowels for char in word)
    ]
    removed_count = original_count - len(valid_words)

    if removed_count > 0:
        print(f"Removed {removed_count} invalid words")
        word_list[:] = valid_words
        write_word_list_to_file()
    else:
        print("No invalid words found")


def add_words(new_words):
    """Add single or comma-separated words to the word list"""
    words_to_add = [
        word.strip().lower() for word in new_words.split(",") if word.strip()
    ]
    word_list.extend(words_to_add)
    print(f"Added {len(words_to_add)} words to the word list")

    remove_duplicate_words()
    sort_word_list()


def find_scarce_letters(num=3):
    """Find the least common letters in the word list"""
    letters_counts = Counter("".join(word_list))
    least_used_letters = letters_counts.most_common()[: -num - 1 : -1]
    print(f"The {num} least common letters:")
    for letter, count in least_used_letters:
        print(f"  {letter.upper()}: {count} occurrences")
    return least_used_letters


def remove_duplicate_words():
    original_count = len(word_list)
    word_list[:] = list(set(word_list))
    removed_count = original_count - len(word_list)
    print(f"Removed {removed_count} duplicates")
    print(f"Word list: {len(word_list)} unique words")

    sort_word_list()


def sort_word_list():
    word_list.sort()

    write_word_list_to_file()


def write_word_list_to_file():
    """Write the current word_list back to words.py"""
    words_file = Path(__file__).parent.parent / "words.py"

    with open(words_file, "w") as f:
        f.write("word_list = [\n")
        for i, word in enumerate(word_list):
            if i % 10 == 0 and i > 0:
                f.write("\n")
            f.write(f" '{word}',")
        f.write("\n]\n")

    print(f"Updated {words_file}")


def show_stats():
    """Show statistics about the word list"""
    print("Word list statistics:")
    print(f"  Total words:  {len(word_list):>5}")
    print(f"  Unique words: {len(set(word_list)):>5}")
    print(f"  Duplicates:   {len(word_list) - len(set(word_list)):>5}")
    print(f"  List sorted:  {'Yes' if word_list == sorted(word_list) else 'No':>5}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Examine and modify the Wordle word list"
    )
    parser.add_argument(
        "action",
        choices=["find-scarce", "dedup", "sort", "stats", "add", "clean"],
        help="Action to perform on the word list",
    )
    parser.add_argument(
        "--num",
        type=int,
        default=3,
        help="Number of scarce letters to find (default: 3)",
    )

    args = parser.parse_args()

    print(f"Current word list has {len(word_list)} words")
    print("-" * 50)

    if args.action == "find-scarce":
        find_scarce_letters(args.num)
    elif args.action == "dedup":
        remove_duplicate_words()
    elif args.action == "sort":
        sort_word_list()
    elif args.action == "stats":
        show_stats()
    elif args.action == "clean":
        remove_invalid_words()
    elif args.action == "add":
        new_words = input("Enter words to add (comma-separated): ")
        add_words(new_words)

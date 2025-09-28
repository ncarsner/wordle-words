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


def find_scarce_letters(num=3):
    """Find the least common letters in the word list"""
    letters_counts = Counter("".join(word_list))
    least_used_letters = letters_counts.most_common()[:-num-1:-1]
    print(f"The {num} least common letters:")
    for letter, count in least_used_letters:
        print(f"  {letter}: {count} occurrences")
    return least_used_letters


def remove_duplicate_words():
    """Remove duplicate words from the word list in place"""
    original_count = len(word_list)
    unique_words = list(set(word_list))
    word_list[:] = unique_words
    removed_count = original_count - len(word_list)
    print(f"Removed {removed_count} duplicate words")
    print(f"Word list now has {len(word_list)} unique words")
    
    # Write changes back to words.py
    write_word_list_to_file()


def sort_word_list():
    """Sort the word list alphabetically in place"""
    original_first_word = word_list[0] if word_list else None
    word_list.sort()
    new_first_word = word_list[0] if word_list else None
    
    if original_first_word != new_first_word:
        print("Word list sorted alphabetically")
        print(f"First word changed from '{original_first_word}' to '{new_first_word}'")
    else:
        print("Word list was already sorted")
    
    # Write changes back to words.py
    write_word_list_to_file()


def write_word_list_to_file():
    """Write the current word_list back to words.py"""
    words_file = Path(__file__).parent.parent / "words.py"
    
    with open(words_file, 'w') as f:
        f.write("word_list = [\n")
        for i, word in enumerate(word_list):
            if i % 8 == 0 and i > 0:
                f.write("\n")
            f.write(f"    '{word}',")
        f.write("\n]\n\n# print(sorted(words))\n\n")
    
    print(f"Updated {words_file}")


def show_stats():
    """Show statistics about the word list"""
    print("Word list statistics:")
    print(f"  Total words: {len(word_list)}")
    print(f"  Unique words: {len(set(word_list))}")
    print(f"  Duplicates: {len(word_list) - len(set(word_list))}")
    print(f"  Alphabetically sorted: {'Yes' if word_list == sorted(word_list) else 'No'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Examine and modify the Wordle word list")
    parser.add_argument("action", choices=[
        "scarce-letters", 
        "remove-duplicates", 
        "sort", 
        "stats"
    ], help="Action to perform on the word list")
    parser.add_argument("--num", type=int, default=3, 
                       help="Number of scarce letters to find (default: 3)")
    
    args = parser.parse_args()
    
    print(f"Current word list has {len(word_list)} words")
    print("-" * 50)
    
    if args.action == "scarce-letters":
        find_scarce_letters(args.num)
    elif args.action == "remove-duplicates":
        remove_duplicate_words()
    elif args.action == "sort":
        sort_word_list()
    elif args.action == "stats":
        show_stats()
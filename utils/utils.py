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
        print(f"  {letter.upper()}: {count} occurrences")
    return least_used_letters


def remove_duplicate_words():
    original_count = len(word_list)
    seen = set()
    unique_words = []
    
    for word in word_list:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    
    word_list[:] = unique_words
    removed_count = original_count - len(word_list)
    print(f"Removed {removed_count} duplicates")
    print(f"Word list: {len(word_list)} unique words")
    
    write_word_list_to_file()


def sort_word_list():
    word_list.sort()
    
    write_word_list_to_file()


def write_word_list_to_file():
    """Write the current word_list back to words.py"""
    words_file = Path(__file__).parent.parent / "words.py"
    
    with open(words_file, 'w') as f:
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
    print(f"  Total words: {len(word_list)}")
    print(f"  Unique words: {len(set(word_list))}")
    print(f"  Duplicates: {len(word_list) - len(set(word_list))}")
    print(f"  Alphabetically sorted: {'Yes' if word_list == sorted(word_list) else 'No'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Examine and modify the Wordle word list")
    parser.add_argument("action", choices=[
        "find-scarce", 
        "dedup", 
        "sort", 
        "stats"
    ], help="Action to perform on the word list")
    parser.add_argument("--num", type=int, default=3, 
                       help="Number of scarce letters to find (default: 3)")
    
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
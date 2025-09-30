import os
import argparse
from collections import Counter

from . import words


class WordListManager:
    def remove_invalid_words(self):
        vowels = set("aeiouy")
        original_count = len(words.word_list)
        valid_words = [
            word
            for word in words.word_list
            if len(word) == 5
            and word.isalpha()
            and any(char in vowels for char in word)
        ]
        removed_count = original_count - len(valid_words)

        if removed_count > 0:
            print(f"Removed {removed_count} invalid words")
            words.word_list[:] = valid_words
            self.save_to_file()

        else:
            print("No invalid words found")

    def find_scarce_letters(self, num=3):
        letters_counts = Counter("".join(words.word_list))
        least_used_letters = letters_counts.most_common()[: -num - 1 : -1]
        for letter, count in least_used_letters:
            print(f"  {letter.upper()}: {count} occurrences")
        # return least_used_letters

    def remove_duplicates(self):
        original_count = len(words.word_list)
        words.word_list = list(set(words.word_list))
        removed_count = original_count - len(words.word_list)
        print(f"Removed {removed_count} duplicate words")
        print(f"Word list: {len(words.word_list)} unique words")

        self.sort_words()

    def sort_words(self):
        was_sorted = words.word_list == sorted(words.word_list)
        words.word_list.sort()

        if not was_sorted:
            print("Word list sorted")
        else:
            print("Word list was already sorted")

        # Save after operation
        self.save_to_file()

    def add_word(self, word):
        if word not in words.word_list:
            words.word_list.append(word)
            print(f"Added '{word}' to word list")
            self.save_to_file()
            return True
        else:
            print(f"'{word}' already exists in word list")
            return False

    def save_to_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_file = os.path.join(script_dir, "words.py")

        with open(words_file, "w") as f:
            f.write("word_list = [\n")
            for i, word in enumerate(words.word_list):
                if i % 10 == 0 and i > 0:
                    f.write("\n")
                f.write(f" '{word}',")
            f.write("\n]\n")

        print(f"Updated {words_file}")

    def show_stats(self):
        """Show statistics about the word list"""
        print("Word list statistics:")
        print(f"  Total words:  {len(words.word_list):>5}")
        print(f"  Unique words: {len(set(words.word_list)):>5}")
        print(f"  Duplicates:   {len(words.word_list) - len(set(words.word_list)):>5}")
        print(f"  List sorted:  {'Yes' if words.word_list == sorted(words.word_list) else 'No':>5}")


def main():
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
    parser.add_argument(
        "word", nargs="?", help="Word to add (required for 'add' action)"
    )

    args = parser.parse_args()

    # Create word list manager instance
    manager = WordListManager()

    # Execute the requested action
    if args.action == "stats":
        manager.show_stats()
    elif args.action == "find-scarce":
        manager.find_scarce_letters(args.num)
    elif args.action == "dedup":
        manager.remove_duplicates()
    elif args.action == "sort":
        manager.sort_words()
    elif args.action == "add":
        if args.word:
            manager.add_word(args.word)
        else:
            print("Error: 'add' action requires a word argument\n")
    elif args.action == "clean":
        manager.remove_invalid_words()
        print("Clean operation completed\n")


if __name__ == "__main__":
    main()

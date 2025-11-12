import os
from collections import Counter

from . import words

def has_repeating_letters(word):
    return len(set(word)) != len(word)

class WordListManager:
    def __init__(
        self, word_list: list[str] | None = None, save_on_change: bool = True
    ) -> None:
        if word_list is None:
            self.word_list = words.word_list
        else:
            self.word_list = word_list
        self.save_on_change = save_on_change
        self._initial_state = None

    def __enter__(self):
        """Context manager entry - save initial state"""
        self._initial_state = self.word_list.copy()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - save changes if any were made"""
        if self.save_on_change:
            if self._initial_state != self.word_list:
                self.save_to_file()
                print("Changes saved automatically")
        return False

    @classmethod
    def for_testing(cls, test_word_list=None):
        """Create manager for testing that doesn't modify the original file"""
        if test_word_list is None:
            test_word_list = words.word_list.copy()
        return cls(word_list=test_word_list, save_on_change=False)

    def remove_invalid_words(self):
        VOWELS = set("aeiouy")
        original_count = len(self.word_list)
        valid_words = [
            word
            for word in self.word_list
            if len(word) == 5
            and word.isalpha()
            and any(char in VOWELS for char in word)
        ]
        removed_count = original_count - len(valid_words)

        if removed_count:
            print(f"Removed {removed_count} invalid words")
            self.word_list[:] = valid_words
            if self.save_on_change:
                self.save_to_file()
        else:
            print("No invalid words found")

    def find_scarce_letters(self, num=3):
        target_list = self.word_list
        letters_counts = Counter("".join(target_list))
        least_used_letters = letters_counts.most_common()[: -num - 1 : -1]
        for letter, count in least_used_letters:
            print(f"  {letter.upper()}: {count} occurrences")

    def remove_duplicates(self):
        target_list = self.word_list
        original_count = len(target_list)
        seen = set()
        target_list[:] = [
            word for word in target_list if not (word in seen or seen.add(word))
        ]
        removed_count = original_count - len(target_list)
        print(f"Removed {removed_count} duplicate words")
        print(f"Word list: {len(target_list)} unique words")
        if self.save_on_change:
            self.save_to_file()

    def sort_words(self):
        target_list = self.word_list
        target_list.sort()
        print("Word list sorted")
        if self.save_on_change:
            self.save_to_file()

    def add_word(self, word):
        target_list = self.word_list
        if word not in target_list:
            target_list.append(word)
            print(f"Added '{word}' to word list")
            if self.save_on_change:
                self.save_to_file()
            return True
        else:
            print(f"'{word}' already exists in word list")
            return False

    def save_to_file(self):  # pragma: no cover
        if not self.save_on_change:
            return
        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_file = os.path.join(script_dir, "words.py")

        with open(words_file, "w") as f:
            f.write("word_list = [\n")
            for i, word in enumerate(words.word_list):
                if i % 10 == 0 and i > 0:
                    f.write("\n")
                f.write(f" '{word}',")
            f.write("\n]\n")

    def show_stats(self):
        target_list = self.word_list
        print("Word list statistics:")
        print(f"  Total words:    {len(target_list):>5,}")
        print(f"  Unique words:   {len(set(target_list)):>5,}")
        print(f"  Duplicates:     {len(target_list) - len(set(target_list)):>5,}")
        print(
            f"  List sorted:    {'Yes' if target_list == sorted(target_list) else 'No':>5}"
        )

import os
from collections import Counter

from . import words


class WordListManager:
    def remove_invalid_words(self):
        VOWELS = set("aeiouy")
        original_count = len(words.word_list)
        valid_words = [
            word
            for word in words.word_list
            if len(word) == 5
            and word.isalpha()
            and any(char in VOWELS for char in word)
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
        least_used_letters = letters_counts.most_common()[:-num-1:-1]
        for letter, count in least_used_letters:
            print(f"  {letter.upper()}: {count} occurrences")

    def remove_duplicates(self):
        original_count = len(words.word_list)
        words.word_list = list(set(words.word_list))
        removed_count = original_count - len(words.word_list)
        print(f"Removed {removed_count} duplicate words")
        print(f"Word list: {len(words.word_list)} unique words")
        self.sort_words()

    def sort_words(self):
        words.word_list.sort()
        print("Word list sorted")
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

    def show_stats(self):
        print("Word list statistics:")
        print(f"  Total words:    {len(words.word_list):>5,}")
        print(f"  Unique words:   {len(set(words.word_list)):>5,}")
        print(f"  Duplicates:     {len(words.word_list) - len(set(words.word_list)):>5,}")
        print(f"  List sorted:    {'Yes' if words.word_list == sorted(words.word_list) else 'No':>5}")

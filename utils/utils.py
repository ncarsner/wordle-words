from pathlib import Path
import argparse
import importlib.util
from collections import Counter

class WordListManager:
    def __init__(self, words_file_path=None):
        if words_file_path is None:
            words_file_path = Path(__file__).parent.parent / "words.py"
        
        self.words_file = Path(words_file_path)
        self.word_list = self._load_word_list()
    
    def _load_word_list(self):
        """Load word list from words.py file"""
        try:
            # Dynamic import to get word_list from words.py
            spec = importlib.util.spec_from_file_location("words", self.words_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module from {self.words_file}")
            
            words_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(words_module)
            
            if not hasattr(words_module, 'word_list'):
                raise AttributeError("No 'word_list' found in words.py")
                
            return words_module.word_list.copy()  # Make a copy to avoid mutations
        except (ImportError, FileNotFoundError, AttributeError) as e:
            print(f"Warning: Could not load word list from {self.words_file}: {e}")
            return []
    
    def find_scarce_letters(self, num=3):
        letters_counts = Counter("".join(self.word_list))
        least_used_letters = letters_counts.most_common()[:-num-1:-1]
        for letter, count in least_used_letters:
            print(f"  {letter.upper()}: {count} occurrences")
        return least_used_letters
    
    def remove_duplicates(self):
        original_count = len(self.word_list)
        self.word_list = list(set(self.word_list))
        removed_count = original_count - len(self.word_list)
        print(f"Removed {removed_count} duplicate words")
        return removed_count
    
    def sort_words(self):
        self.word_list.sort()
        print("Word list sorted")
    
    def add_word(self, word):
        if word not in self.word_list:
            self.word_list.append(word)
            print(f"Added '{word}' to word list")
            return True
        else:
            print(f"'{word}' already exists in word list")
            return False
    
    def save_to_file(self):
        """Write the current word_list back to words.py"""
        with open(self.words_file, "w") as f:
            f.write("word_list = [\n")
            for i, word in enumerate(self.word_list):
                if i % 10 == 0 and i > 0:
                    f.write("\n")
                f.write(f" '{word}',")
            f.write("\n]\n")
        
        print(f"Updated {self.words_file}")
    
    def show_stats(self):
        """Show statistics about the word list"""
        print("Word list statistics:")
        print(f"  Total words:  {len(self.word_list):>5}")
        print(f"  Unique words: {len(set(self.word_list)):>5}")
        print(f"  Duplicates:   {len(self.word_list) - len(set(self.word_list)):>5}")
        print(f"  List sorted:  {'Yes' if self.word_list == sorted(self.word_list) else 'No':>5}")


def main():
    parser = argparse.ArgumentParser(
        description="Examine and modify the Wordle word list"
    )
    parser.add_argument(
        "action",
        choices=["find-scarce", "dedup", "sort", "stats", "add", "clean"],
        help="Action to perform on the word list"
    )
    parser.add_argument(
        "word", 
        nargs="?", 
        help="Word to add (required for 'add' action)"
    )
    
    args = parser.parse_args()
    
    # Create word list manager instance
    manager = WordListManager()
    
    # Execute the requested action
    if args.action == "stats":
        manager.show_stats()
    elif args.action == "find-scarce":
        scarce_letters = manager.find_scarce_letters()
        print("Scarce letters:", scarce_letters)
    elif args.action == "dedup":
        manager.remove_duplicates()
        manager.save_to_file()
    elif args.action == "sort":
        manager.sort_words()
        manager.save_to_file()
    elif args.action == "add":
        if args.word:
            manager.add_word(args.word)
            manager.save_to_file()
        else:
            print("Error: 'add' action requires a word argument")
    elif args.action == "clean":
        manager.remove_duplicates()
        manager.sort_words()
        manager.save_to_file()


if __name__ == "__main__":
    main()
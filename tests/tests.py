from src.words import word_list
from src.utils import WordListManager

word_list_copy = word_list.copy()
a = WordListManager(word_list=word_list_copy, save_on_change=False)

# add pytest fixtures

def test_all_words_five_letters():
    assert all(len(word) == 5 for word in word_list)


def test_no_duplicate_words():
    assert len(word_list) == len(set(word_list))


def test_word_list_alphabetical():
    assert word_list == sorted(word_list)


def test_copy():
    a.add_word("abcde")
    assert "abcde" not in word_list
    assert "abcde" in a.word_list


def test_add_word():
    a.add_word("bugaboo")
    assert "bugaboo" in a.word_list


def test_add_existing_word():
    result = a.add_word("apple")
    assert result is False


def test_remove_invalid_words():
    a.remove_invalid_words()
    assert all(len(word) == 5 for word in a.word_list)
    assert all(word.isalpha() for word in a.word_list)
    assert all(any(char in "aeiouy" for char in word) for word in a.word_list)

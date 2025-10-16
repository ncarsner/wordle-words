from src.wordle_manager.words import word_list
from src.wordle_manager.utils import WordListManager
import pytest


@pytest.fixture
def word_list_manager():
    word_list_copy = word_list.copy()
    return WordListManager(word_list=word_list_copy, save_on_change=False)


def test_all_words_five_letters():
    assert all(len(word) == 5 for word in word_list)


def test_no_duplicate_words():
    assert len(word_list) == len(set(word_list))


def test_word_list_alphabetical():
    assert word_list == sorted(word_list)


def test_copy(word_list_manager):
    word_list_manager.add_word("abcde")
    assert "abcde" not in word_list
    assert "abcde" in word_list_manager.word_list


def test_add_word(word_list_manager):
    word_list_manager.add_word("bugaboo")
    assert "bugaboo" in word_list_manager.word_list


def test_add_existing_word(word_list_manager):
    result = word_list_manager.add_word("apple")
    assert result is False


def test_remove_invalid_words(word_list_manager):
    word_list_manager.remove_invalid_words()
    assert all(len(word) == 5 for word in word_list_manager.word_list)
    assert all(word.isalpha() for word in word_list_manager.word_list)
    assert all(any(char in "aeiouy" for char in word) for word in word_list_manager.word_list)

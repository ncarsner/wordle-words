import pytest
from unittest.mock import patch

from src.wordle_manager.utils import WordListManager
from src.wordle_manager import words


@pytest.fixture(autouse=True)
def safe_testing_environment():
    # Store the original word list
    original_words = words.word_list.copy()
    original_id = id(words.word_list)

    # Mock the save_to_file method to prevent any file writes
    with patch.object(WordListManager, "save_to_file", return_value=None) as mock_save:
        try:
            yield mock_save
        finally:
            # Restore to the original state
            if id(words.word_list) != original_id:
                words.word_list = original_words
            else:
                words.word_list[:] = original_words


class TestContextManagerExitAdditional:
    def test_exit_with_initial_state_none(self):
        # Arrange
        manager = WordListManager()
        manager._initial_state = None  # This could happen if __enter__ wasn't called

        # Act
        result = manager.__exit__(None, None, None)

        # Assert - handles None gracefully
        assert result is False

    def test_exit_exception_propagation(self):
        # Arrange
        manager = WordListManager()
        manager._initial_state = words.word_list.copy()

        # Act & Assert - __exit__ returns False, so exceptions should propagate
        with pytest.raises(ValueError):
            with manager:
                raise ValueError("This should not be suppressed")


class TestForTestingAdditionalCoverage:
    def test_empty_words_list(self):
        # Arrange
        words.word_list[:] = []

        # Act
        manager = WordListManager.for_testing()

        # Assert
        assert manager.word_list == []
        assert manager.word_list is not words.word_list
        assert isinstance(manager.word_list, list)


class TestFindScarceLetters:
    def test_find_scarce_letters_production_vs_test_mode(self, capsys):
        # Test mode case
        test_words = ["test", "mode"]
        test_manager = WordListManager.for_testing(test_words)
        test_manager.find_scarce_letters(num=1)
        test_output = capsys.readouterr().out

        # Production mode case - should use words.word_list
        prod_manager = WordListManager()
        prod_manager.find_scarce_letters(num=1)
        prod_output = capsys.readouterr().out

        # Outputs should be different, produce output, and do not crash
        assert test_output.strip() != ""
        assert prod_output.strip() != ""


class TestRemoveDuplicates:
    def test_remove_duplicates_production_vs_test_mode(self):
        # Arrange - add duplicates for production test
        words.word_list.extend(["test_dup", "test_dup"])

        # Test production mode - line 65: target_list = words.word_list (when not test_mode)
        prod_manager = WordListManager()
        original_prod_length = len(words.word_list)
        prod_manager.remove_duplicates()

        # Should have removed the duplicate 'test_dup'
        assert len(words.word_list) < original_prod_length

        # Test test mode - line 65: target_list = self.word_list (when test_mode)
        test_words = ["test_a", "test_a", "test_b"]
        test_manager = WordListManager.for_testing(test_words)
        test_manager.remove_duplicates()

        # Should only affect test_manager.word_list, not words.word_list
        assert test_manager.word_list == ["test_a", "test_b"]


class TestFileSafetyVerification:
    def test_save_to_file_mocked_no_actual_file_writes(self, safe_testing_environment):
        mock_save = safe_testing_environment

        # Arrange
        manager = WordListManager()
        words.word_list[:] = ["test", "data"]

        # Act - call a method that triggers save_to_file
        manager.sort_words()

        # Assert - save_to_file was called but mocked
        assert mock_save.called, "save_to_file should have been called"

    def test_add_word_in_production_mode_mocked(self, safe_testing_environment):
        mock_save = safe_testing_environment

        # Arrange - save_on_change=True by default
        manager = WordListManager()
        unique_word = "safetestword123"

        # Ensure word doesn't exist
        if unique_word in words.word_list:
            words.word_list.remove(unique_word)

        # Act
        result = manager.add_word(unique_word)

        # Assert
        assert result is True
        assert unique_word in words.word_list
        assert mock_save.called, "save_to_file should have been called but was mocked"


class TestShowStatsFormatting:
    def test_show_stats_total_words_formatting(self, capsys):
        # Arrange
        test_words = ["word1", "word2", "word3", "word4", "word5"]
        manager = WordListManager.for_testing(test_words)

        # Act
        manager.show_stats()

        # Assert formatting
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        total_line = [line for line in lines if "Total words:" in line][0]

        # Right-aligned number with comma formatting
        assert "    5" in total_line
        assert "Total words:" in total_line


class TestRemoveInvalidWords:
    def test_remove_invalid_words_conditional_save_production_mode(self):
        # Arrange - production mode with mocked save_to_file
        words.word_list[:] = [
            "house",
            "inv@l",
            "xyz",
        ]
        with patch.object(WordListManager, "save_to_file"):
            manager = WordListManager()

            # Act
            manager.remove_invalid_words()

            # Assert - condition should be True
            assert manager.word_list == words.word_list

            # Verify invalid words were removed
            assert "inv@l" not in words.word_list  # Invalid: special character
            assert "xyz" not in words.word_list  # Invalid: no vowels
            assert "house" in words.word_list  # Valid: 5 letters, alpha, has vowels

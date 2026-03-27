import pytest
from src.preprocessing import clean_text


class TestCleanTextLowercase:
    def test_converts_uppercase_to_lowercase(self):
        assert clean_text("HELLO SPAM") == "hello spam"

    def test_converts_mixed_case(self):
        assert clean_text("FREE Money!!!") == "free money"

    def test_already_lowercase_unchanged(self):
        assert clean_text("hello world") == "hello world"


class TestCleanTextPunctuation:
    def test_removes_exclamation_marks(self):
        assert clean_text("win!!!") == "win"

    def test_removes_question_marks(self):
        assert clean_text("win???") == "win"

    def test_removes_mixed_punctuation(self):
        assert clean_text("call now!!!???...") == "call now"

    def test_preserves_spaces_between_words(self):
        result = clean_text("call now")
        assert result == "call now"
        assert "  " not in result  # sem espaços duplos


class TestCleanTextEdgeCases:
    def test_empty_string_returns_empty(self):
        assert clean_text("") == ""

    def test_only_punctuation_returns_empty(self):
        assert clean_text("!!!???...") == ""

    def test_strips_leading_trailing_whitespace(self):
        assert clean_text("  hello  ") == "hello"

    def test_collapses_internal_whitespace(self):
        assert clean_text("hello   world") == "hello world"

    def test_numbers_are_preserved(self):
        assert clean_text("win 1000 dollars") == "win 1000 dollars"

    def test_idempotent(self):
        """Aplicar clean_text duas vezes deve dar o mesmo resultado."""
        text = "FREE Prize!!! Call NOW"
        assert clean_text(clean_text(text)) == clean_text(text)

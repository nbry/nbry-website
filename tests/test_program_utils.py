"""Tests for program utility functions."""

import pytest

from nbry_website.sites.lifting.lib.program_utils import (
    format_sets_display,
    get_display_name,
)


class TestFormatSetsDisplay:
    def test_simple_sets_with_rep_range(self):
        exercise = {"sets": 3, "rep_range": [8, 12]}
        assert format_sets_display(exercise) == "3 × 8–12"

    def test_simple_sets_no_rep_range(self):
        exercise = {"sets": 3}
        assert format_sets_display(exercise) == "3 sets"

    def test_detailed_sets_identical(self):
        exercise = {"sets": [{"reps": 5, "tune": 0.72}] * 5}
        assert format_sets_display(exercise) == "5×5"

    def test_detailed_sets_single(self):
        exercise = {"sets": [{"reps": 8, "tune": 0.9}]}
        assert format_sets_display(exercise) == "1×8"

    def test_detailed_sets_varying_tune_same_reps(self):
        # OHP: warmup set + working sets, all same reps
        exercise = {
            "sets": [
                {"reps": 5, "tune": 1.0},
                {"reps": 5, "tune": 0.9},
                {"reps": 5, "tune": 0.9},
                {"reps": 5, "tune": 0.9},
            ]
        }
        assert format_sets_display(exercise) == "4×5"

    def test_simple_sets_rep_range_single_set(self):
        exercise = {"sets": 1, "rep_range": [10, 15]}
        assert format_sets_display(exercise) == "1 × 10–15"


class TestGetDisplayName:
    def test_key_with_display_name(self):
        config = {"ohp": {"display_name": "OHP", "tier": "secondary"}}
        assert get_display_name("ohp", config) == "OHP"

    def test_key_without_display_name_falls_back_to_title_case(self):
        config = {"squat": {"tier": "primary"}}
        assert get_display_name("squat", config) == "Squat"

    def test_key_not_in_config_falls_back_to_title_case(self):
        assert get_display_name("barbell_row", {}) == "Barbell Row"

    def test_multi_word_snake_case_title_fallback(self):
        assert get_display_name("incline_barbell_bench", {}) == "Incline Barbell Bench"

    def test_empty_display_name_falls_back(self):
        config = {"squat": {"display_name": "", "tier": "primary"}}
        assert get_display_name("squat", config) == "Squat"

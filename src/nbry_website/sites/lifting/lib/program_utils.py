"""Utility functions for formatting program display data."""

from typing import Any


def format_sets_display(exercise: dict[str, Any]) -> str:
    """Format an exercise's sets as 'N×M' or 'N × min–max'."""
    sets = exercise.get("sets")
    if isinstance(sets, int):
        rep_range = exercise.get("rep_range", [])
        if len(rep_range) == 2:
            return f"{sets} × {rep_range[0]}–{rep_range[1]}"
        return f"{sets} sets"
    reps = sets[0]["reps"]
    return f"{len(sets)}×{reps}"


def get_display_name(exercise_key: str, exercises_config: dict[str, Any]) -> str:
    """Return display name from exercises config, falling back to title-cased key."""
    exercise = exercises_config.get(exercise_key, {})
    if display_name := exercise.get("display_name"):
        return display_name
    return exercise_key.replace("_", " ").title()

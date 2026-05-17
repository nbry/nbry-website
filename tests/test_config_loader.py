"""Tests for ConfigLoader."""

import tomllib
from pathlib import Path

import pytest

from nbry_lifting_website.lib.config_loader import ConfigLoader


class TestConfigLoaderInit:
    """Tests for ConfigLoader initialization."""

    def test_init_with_valid_directory(self):
        """ConfigLoader initializes with valid directory path."""
        config_dir = Path("src/nbry_lifting_website/configs")
        loader = ConfigLoader(config_dir)
        assert loader.config_dir == config_dir

    def test_init_with_string_path(self):
        """ConfigLoader accepts string path and converts to Path."""
        loader = ConfigLoader("src/nbry_lifting_website/configs")
        assert isinstance(loader.config_dir, Path)
        assert loader.config_dir == Path("src/nbry_lifting_website/configs")

    def test_init_with_nonexistent_directory(self):
        """ConfigLoader raises FileNotFoundError for nonexistent directory."""
        with pytest.raises(FileNotFoundError, match="Config directory not found"):
            ConfigLoader("nonexistent/directory")

    def test_init_with_file_instead_of_directory(self, tmp_path):
        """ConfigLoader raises NotADirectoryError when path is a file."""
        file_path = tmp_path / "not_a_dir.txt"
        file_path.touch()

        with pytest.raises(NotADirectoryError, match="not a directory"):
            ConfigLoader(file_path)


class TestConfigLoaderLoad:
    """Tests for ConfigLoader.load() method."""

    @pytest.fixture
    def loader(self):
        """Fixture providing ConfigLoader with actual config directory."""
        return ConfigLoader("src/nbry_lifting_website/configs")

    def test_load_program_toml(self, loader):
        """Load program.toml and verify structure."""
        data = loader.load("program.toml")

        assert "program" in data
        assert data["program"]["id"] == "pillar_v1"
        assert data["program"]["name"] == "Pillar"
        assert data["program"]["duration_weeks"] == 5
        assert data["program"]["days_per_week"] == 4

    def test_load_program_has_block_references(self, loader):
        """program.toml contains block references."""
        data = loader.load("program.toml")

        blocks = data["program"]["blocks"]
        assert len(blocks) == 3
        assert blocks[0]["name"] == "accumulation"
        assert blocks[0]["file"] == "blocks/accumulation.toml"
        assert blocks[0]["weeks"] == [1, 2]

    def test_load_nested_block_file(self, loader):
        """Load nested block file from blocks/ subdirectory."""
        data = loader.load("blocks/accumulation.toml")

        assert "name" in data
        assert data["name"] == "Accumulation"
        assert "days" in data
        assert len(data["days"]) > 0

    def test_load_exercises_catalog(self, loader):
        """Load exercises.toml and verify structure."""
        data = loader.load("exercises.toml")

        assert "squat" in data
        assert data["squat"]["tier"] == "primary"
        assert data["squat"]["calculation_mode"] == "training_max"
        assert "bench" in data
        assert "deadlift" in data

    def test_load_nonexistent_file(self, loader):
        """Loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            loader.load("nonexistent.toml")

    def test_load_invalid_toml(self, tmp_path):
        """Loading invalid TOML raises TOMLDecodeError."""
        # Create temp config dir with invalid TOML
        config_dir = tmp_path / "configs"
        config_dir.mkdir()

        bad_toml = config_dir / "bad.toml"
        bad_toml.write_text("this is not valid = = = toml")

        loader = ConfigLoader(config_dir)
        with pytest.raises(tomllib.TOMLDecodeError):
            loader.load("bad.toml")

    def test_load_returns_dict(self, loader):
        """load() returns a dictionary."""
        data = loader.load("program.toml")
        assert isinstance(data, dict)


class TestConfigLoaderDataStructure:
    """Tests verifying the structure of loaded config data."""

    @pytest.fixture
    def loader(self):
        """Fixture providing ConfigLoader."""
        return ConfigLoader("src/nbry_lifting_website/configs")

    def test_block_contains_days_with_exercises(self, loader):
        """Block files contain days with exercises."""
        data = loader.load("blocks/accumulation.toml")

        first_day = data["days"][0]
        assert "name" in first_day
        assert "exercises" in first_day
        assert len(first_day["exercises"]) > 0

    def test_exercise_has_sets_and_reps(self, loader):
        """Exercises in blocks have sets and reps data."""
        data = loader.load("blocks/accumulation.toml")

        first_exercise = data["days"][0]["exercises"][0]
        assert "exercise" in first_exercise

        # Exercises can have either detailed sets or shorthand notation
        assert "sets" in first_exercise or "reps" in first_exercise

    def test_detailed_sets_have_reps_and_tune(self, loader):
        """Detailed set definitions have reps and tune values."""
        data = loader.load("blocks/accumulation.toml")

        # First exercise (squat) uses detailed sets with tune values
        squat = data["days"][0]["exercises"][0]
        assert squat["exercise"] == "squat"

        sets = squat["sets"]
        assert isinstance(sets, list)
        assert len(sets) > 0

        first_set = sets[0]
        assert "reps" in first_set
        assert "tune" in first_set
        assert first_set["tune"] == 0.72  # 72% of training max

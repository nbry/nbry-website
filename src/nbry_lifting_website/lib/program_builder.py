"""Program configuration loader and builder."""

import tomllib
from pathlib import Path
from typing import Any

from .models import (
    BlockDefinition,
    CalculationRule,
    ExerciseDefinition,
    Milestones,
    ProgramDefinition,
    ProgressionRules,
    RestRules,
    RoundingRules,
)


class ProgramBuilder:
    """Loads and validates modular program configs."""

    def __init__(self, config_dir: Path | str = "configs"):
        """Initialize with config directory path.

        Args:
            config_dir: Path to configs directory. If relative, resolved from package root.
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.is_absolute():
            # Make relative to package directory (parent of lib/)
            package_dir = Path(__file__).parent.parent
            self.config_dir = package_dir / config_dir

    def load_program(self, program_file: str = "program.toml") -> ProgramDefinition:
        """Load the root program config and validate.

        Args:
            program_file: Name of program config file.

        Returns:
            Validated ProgramDefinition model.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If config doesn't match schema.
        """
        program_path = self.config_dir / program_file
        with open(program_path, "rb") as f:
            data = tomllib.load(f)
        return ProgramDefinition(**data["program"])

    def load_exercises(self, exercises_file: str) -> dict[str, ExerciseDefinition]:
        """Load exercise catalog.

        Args:
            exercises_file: Name of exercises config file.

        Returns:
            Dict mapping exercise IDs to ExerciseDefinition models.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If exercises don't match schema.
        """
        exercises_path = self.config_dir / exercises_file
        with open(exercises_path, "rb") as f:
            data = tomllib.load(f)
        return {
            exercise_id: ExerciseDefinition(**exercise_data)
            for exercise_id, exercise_data in data.items()
        }

    def load_block(self, block_file: str) -> BlockDefinition:
        """Load a single block definition.

        Args:
            block_file: Path to block config file (e.g., 'blocks/accumulation.toml').

        Returns:
            Validated BlockDefinition model.

        Raises:
            FileNotFoundError: If block file doesn't exist.
            ValidationError: If block doesn't match schema.
        """
        block_path = self.config_dir / block_file
        with open(block_path, "rb") as f:
            data = tomllib.load(f)
        return BlockDefinition(**data)

    def load_progression_rules(self, progression_file: str) -> ProgressionRules:
        """Load progression rules.

        Args:
            progression_file: Name of progression config file.

        Returns:
            Validated ProgressionRules model.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If rules don't match schema.
        """
        progression_path = self.config_dir / progression_file
        with open(progression_path, "rb") as f:
            data = tomllib.load(f)
        return ProgressionRules(**data)

    def load_calculation_rules(
        self, calculation_file: str
    ) -> dict[str, CalculationRule]:
        """Load calculation formulas.

        Args:
            calculation_file: Name of calculation config file.

        Returns:
            Dict mapping calculation modes to CalculationRule models.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If rules don't match schema.
        """
        calculation_path = self.config_dir / calculation_file
        with open(calculation_path, "rb") as f:
            data = tomllib.load(f)
        return {mode: CalculationRule(**rule_data) for mode, rule_data in data.items()}

    def load_rounding_rules(self, rounding_file: str) -> RoundingRules:
        """Load rounding rules.

        Args:
            rounding_file: Name of rounding config file.

        Returns:
            Validated RoundingRules model.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If rules don't match schema.
        """
        rounding_path = self.config_dir / rounding_file
        with open(rounding_path, "rb") as f:
            data = tomllib.load(f)
        return RoundingRules(**data["equipment"])

    def load_rest_rules(self, rest_file: str) -> RestRules:
        """Load rest time rules.

        Args:
            rest_file: Name of rest config file.

        Returns:
            Validated RestRules model.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If rules don't match schema.
        """
        rest_path = self.config_dir / rest_file
        with open(rest_path, "rb") as f:
            data = tomllib.load(f)
        return RestRules(**data["by_type"])

    def load_milestones(self, milestones_file: str) -> Milestones:
        """Load milestone definitions.

        Args:
            milestones_file: Name of milestones config file.

        Returns:
            Validated Milestones model.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValidationError: If milestones don't match schema.
        """
        milestones_path = self.config_dir / milestones_file
        with open(milestones_path, "rb") as f:
            data = tomllib.load(f)
        return Milestones(**data)

    def load_full_program(self) -> dict[str, Any]:
        """Load entire program with all dependencies.

        Returns:
            Dict containing all loaded and validated configs:
                - program: ProgramDefinition
                - exercises: dict[str, ExerciseDefinition]
                - blocks: list[BlockDefinition]
                - progression: ProgressionRules
                - calculation: dict[str, CalculationRule]
                - rounding: RoundingRules
                - rest: RestRules
                - milestones: Milestones

        Raises:
            FileNotFoundError: If any config file doesn't exist.
            ValidationError: If any config doesn't match schema.
        """
        program = self.load_program()

        return {
            "program": program,
            "exercises": self.load_exercises(program.exercise_catalog),
            "blocks": [self.load_block(block_ref.file) for block_ref in program.blocks],
            "progression": self.load_progression_rules(program.progression_rules),
            "calculation": self.load_calculation_rules(program.calculation_rules),
            "rounding": self.load_rounding_rules(program.rounding_rules),
            "rest": self.load_rest_rules(program.rest_rules),
            "milestones": self.load_milestones(program.milestones),
        }

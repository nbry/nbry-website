"""Pydantic models for lifting program configuration."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class ExerciseDefinition(BaseModel):
    """Exercise definition in the catalog."""

    tier: Literal["primary", "secondary", "tertiary"]
    movement: str
    equipment: str
    focus: Literal["strength", "hypertrophy"]
    calculation_mode: Literal["training_max", "reference", "static"]
    enabled: bool = True

    # Optional fields depending on calculation_mode
    increment: Optional[float] = None  # Not required for reference exercises
    reference_exercise: Optional[str] = None
    rep_range: Optional[list[int]] = None
    target_reps: Optional[int] = None
    target_weight: Optional[float] = None


class SetDefinition(BaseModel):
    """Individual set definition with reps and tune."""

    reps: int
    tune: Optional[float] = None


class ExerciseInWorkout(BaseModel):
    """Exercise reference in a workout day."""

    exercise: str  # ID reference to exercise catalog
    sets: Optional[list[SetDefinition] | int] = None  # List of sets or int count
    reps: Optional[int] = None  # For shorthand notation (reps per set)


class DayDefinition(BaseModel):
    """Single workout day definition."""

    name: str
    exercises: list[ExerciseInWorkout]


class BlockDefinition(BaseModel):
    """Training block definition."""

    name: str
    days: list[DayDefinition]


class BlockReference(BaseModel):
    """Reference to a block file in program definition."""

    name: str
    file: str
    weeks: list[int]


class RoundingRules(BaseModel):
    """Rounding rules by equipment type."""

    barbell: float
    dumbbell: float
    plate: float
    bodyweight: float


class RestRules(BaseModel):
    """Rest time rules by exercise type (in seconds)."""

    primary_strength: int
    secondary_strength: int
    secondary_hypertrophy: int
    tertiary_hypertrophy: int
    core: int


class CalculationRule(BaseModel):
    """Calculation formula definition."""

    description: str
    formula: str


class ProgressionFailurePolicy(BaseModel):
    """Failure policy for progression rules."""

    repeat_cycle_on_failure: bool
    allow_manual_override: bool


class PrimaryProgressionRule(BaseModel):
    """Progression rules for primary exercises."""

    progress_if: str
    increase_training_max_by_increment: bool
    failure_policy: ProgressionFailurePolicy


class SecondaryProgressionBranch(BaseModel):
    """Branch logic for secondary progression."""

    increase_weight_by_increment: Optional[bool] = None
    reset_reps_to_rep_range_minimum: Optional[bool] = None
    increase_target_reps_by: Optional[int] = None


class SecondaryProgressionRule(BaseModel):
    """Progression rules for secondary exercises."""

    progress_if: str
    if_top_of_rep_range: SecondaryProgressionBranch
    otherwise: SecondaryProgressionBranch


class TertiaryProgressionRule(BaseModel):
    """Progression rules for tertiary exercises."""

    progress_if: str
    if_top_of_rep_range: SecondaryProgressionBranch
    otherwise: SecondaryProgressionBranch


class ProgressionRules(BaseModel):
    """All progression rules."""

    primary: PrimaryProgressionRule
    secondary: SecondaryProgressionRule
    tertiary: TertiaryProgressionRule


class PlateMilestone(BaseModel):
    """Individual plate milestone."""

    weight: int
    label: str


class Milestones(BaseModel):
    """Milestone definitions for imperial and metric."""

    plate_milestones: dict[str, list[PlateMilestone]]
    total_milestones: dict[str, list[int]]


class ProgramDefinition(BaseModel):
    """Root program configuration."""

    id: str
    name: str
    description: str
    duration_weeks: int
    days_per_week: int
    unit_system: Literal["imperial", "metric"]

    # File references
    exercise_catalog: str
    progression_rules: str
    calculation_rules: str
    rounding_rules: str
    rest_rules: str
    milestones: str
    blocks: list[BlockReference]

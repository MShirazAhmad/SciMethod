import math
import os
import numpy as np
from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# === Base Model for Timestamps ===
class TimestampedModel(models.Model):
    """
    Abstract base model that provides self-updating 'created_at' and 'updated_at' fields.
    """
    # Timestamp when the record was created
    created_at = models.DateTimeField(default=timezone.now)
    # Timestamp when the record was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# === Scientific Method Core Models ===

class ResearchProblem(TimestampedModel):
    """
    Represents a research problem being studied, containing its background and goal.
    """
    # Title of the research problem
    title = models.CharField(max_length=255)

    # Markdown field for background information
    background = MDTextField()

    # Markdown field for the main research goal
    goal = MDTextField()

    def __str__(self):
        return self.title

class ResearchQuestion(TimestampedModel):
    """
    Represents a specific research question derived from a research problem.
    """
    # Foreign key linking to the parent research problem
    research_problem = models.ForeignKey(ResearchProblem, on_delete=models.CASCADE, related_name='questions')

    # Markdown field containing the question text
    question_text = MDTextField()

    # Optional markdown field explaining the rationale behind the question
    rationale = MDTextField(null=True, blank=True)

    def __str__(self):
        return self.question_text

class Hypothesis(TimestampedModel):
    """
    Represents a hypothesis related to a research question, including its type and status.
    """
    # Foreign key linking to the associated research question
    research_question = models.ForeignKey(ResearchQuestion, on_delete=models.CASCADE, related_name='hypotheses')

    # Optional self-referential foreign key to a parent hypothesis for hierarchical hypotheses
    parent_hypothesis = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_hypotheses')

    # Markdown field containing the hypothesis statement
    statement = MDTextField()

    # Type of hypothesis: Null or Alternative
    hypothesis_type = models.CharField(
        max_length=20,
        choices=[
            ('Null', 'Null Hypothesis (H₀)'),
            ('Alternative', 'Alternative Hypothesis (H₁)')
        ]
    )

    # Optional markdown field describing the scientific basis for the hypothesis
    scientific_basis = MDTextField(null=True, blank=True)

    # Optional markdown field describing the expected outcome if hypothesis is true
    expected_outcome = MDTextField(null=True, blank=True)

    # Current testing status of the hypothesis
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending Testing'),
            ('Supported', 'Supported by Data'),
            ('Refuted', 'Refuted by Data'),
            ('Modified', 'Modified after Results')
        ],
        default='Pending'
    )

    # Optional markdown notes about any modifications to the hypothesis
    modification_notes = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_hypothesis_type_display()}: {self.statement[:60]}..."

class HypothesisRevision(TimestampedModel):
    """
    Represents a revision made to an original hypothesis, including rationale and observational basis.
    """
    # Foreign key to the original hypothesis being revised
    original_hypothesis = models.ForeignKey(Hypothesis, on_delete=models.CASCADE, related_name='revisions')

    # One-to-one link to the new hypothesis created from this revision
    new_hypothesis = models.OneToOneField(Hypothesis, on_delete=models.CASCADE, related_name='created_from_revision')

    # Markdown field explaining the rationale for the change
    rationale_for_change = MDTextField()

    # Optional foreign key to an observation that motivated this revision
    based_on_observation = models.ForeignKey('Observation', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Revision of Hypothesis {self.original_hypothesis.id}"

class ExperimentalPlan(TimestampedModel):
    """
    Represents the experimental design and methods planned to test a hypothesis.
    """
    # Foreign key linking to the hypothesis this plan is designed for
    hypothesis = models.ForeignKey(Hypothesis, on_delete=models.CASCADE, related_name='experimental_plans')

    # Type of experimental design used
    design_type = models.CharField(
        max_length=50,
        choices=[
            ('CRD', 'Completely Randomized Design'),
            ('RBD', 'Randomized Block Design'),
            ('LSD', 'Latin Square Design'),
            ('Other', 'Other Design')
        ]
    )

    # Markdown field describing independent variables in the experiment
    independent_variables = MDTextField()

    # Markdown field describing dependent variables measured in the experiment
    dependent_variables = MDTextField()

    # Markdown field describing control variables held constant
    control_variables = MDTextField()

    # Markdown field describing the planned experimental methods
    planned_methods = MDTextField()

    # Optional markdown notes related to the experimental plan
    notes = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"Plan for {self.hypothesis}"

class Experiment(TimestampedModel):
    """
    Represents an actual experiment conducted according to an experimental plan.
    """
    # Foreign key linking to the experimental plan followed
    experimental_plan = models.ForeignKey(ExperimentalPlan, on_delete=models.CASCADE, related_name='experiments')

    # Title or name of the experiment
    title = models.CharField(max_length=255)

    # Optional start date of the experiment
    start_date = models.DateField(null=True, blank=True)

    # Optional end date of the experiment
    end_date = models.DateField(null=True, blank=True)

    # Current status of the experiment
    status = models.CharField(
        max_length=20,
        choices=[
            ('Planned', 'Planned'),
            ('Running', 'Running'),
            ('Completed', 'Completed Successfully'),
            ('Failed', 'Failed')
        ],
        default='Planned'
    )

    # Optional markdown field describing reason for failure if experiment failed
    failure_reason = MDTextField(null=True, blank=True)

    # Optional field indicating the stage at which failure occurred
    failure_stage = models.CharField(
        max_length=50,
        choices=[
            ('Setup', 'Setup Failure'),
            ('Execution', 'Execution Failure'),
            ('Data Collection', 'Data Collection Failure'),
            ('Post Processing', 'Post Processing Failure'),
            ('Unknown', 'Unknown/Multiple Stages')
        ],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

class FailureLog(TimestampedModel):
    """
    Logs details about failures encountered during experiments.
    """
    # Foreign key linking to the experiment where failure occurred
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='failure_logs')

    # Markdown field describing the failure in detail
    description = MDTextField()

    # Stage of the experiment during which failure happened
    stage = models.CharField(
        max_length=50,
        choices=[
            ('Setup', 'Setup Failure'),
            ('Execution', 'Execution Failure'),
            ('Data Collection', 'Data Collection Failure'),
            ('Post Processing', 'Post Processing Failure'),
            ('Unknown', 'Unknown/Multiple Stages')
        ]
    )

    # Optional markdown field describing corrective actions taken
    corrective_action = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"Failure during {self.stage} in {self.experiment.title}"

class Variable(TimestampedModel):
    """
    Represents a variable involved in an experiment, including its type and measurement unit.
    """
    # Foreign key linking to the experiment where the variable is used
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='variables')

    # Name of the variable
    name = models.CharField(max_length=255)

    # Type of variable: Independent, Dependent, or Confounding
    variable_type = models.CharField(
        max_length=50,
        choices=[
            ('Independent', 'Independent Variable'),
            ('Dependent', 'Dependent Variable'),
            ('Confounding', 'Confounding Variable')
        ]
    )

    # Optional unit of measurement for the variable
    measurement_unit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.variable_type})"

class Observation(TimestampedModel):
    """
    Represents an observation or measurement recorded during an experiment.
    """
    # Foreign key linking to the experiment where observation was made
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='observations')

    # Foreign key linking to the variable observed
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, related_name='observations')

    # Numeric value recorded for the observation
    value = models.FloatField()

    # Optional date when the observation was made
    observation_date = models.DateField(null=True, blank=True)

    # Optional foreign key to the hypothesis tested by this observation
    hypothesis_tested = models.ForeignKey(Hypothesis, on_delete=models.SET_NULL, null=True, blank=True, related_name='observations')

    # Result interpretation indicating support or refutation of hypothesis
    result_support = models.CharField(
        max_length=20,
        choices=[
            ('Support', 'Supports Hypothesis'),
            ('Refute', 'Refutes Hypothesis'),
            ('Inconclusive', 'Inconclusive Result')
        ],
        default='Inconclusive'
    )

    # Optional markdown notes about the observation
    notes = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"Observation {self.variable.name} on {self.observation_date}"

class EditHistory(TimestampedModel):
    """
    Tracks edits made to model instances, including field changes and reasons.
    """
    # Name of the model where the edit occurred
    model_name = models.CharField(max_length=255)

    # ID of the object that was edited
    object_id = models.PositiveIntegerField()

    # Name of the field that was changed
    field_name = models.CharField(max_length=255)

    # Optional markdown field storing the old value before edit
    old_value = MDTextField(null=True, blank=True)

    # Optional markdown field storing the new value after edit
    new_value = MDTextField(null=True, blank=True)

    # Optional markdown field explaining the reason for the change
    change_reason = MDTextField(null=True, blank=True)

    # Optional name or identifier of the person who made the edit
    edited_by = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Edit in {self.model_name} ({self.field_name}) at {self.created_at}"

# === Version Tracking Model ===
class VersionHistory(models.Model):
    """
    Generic model to track version history of any model instance's field changes.
    """
    # Content type of the tracked model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # ID of the tracked object
    object_id = models.PositiveIntegerField()

    # Generic foreign key to the tracked object
    content_object = GenericForeignKey('content_type', 'object_id')

    # Name of the field that changed
    field_name = models.CharField(max_length=255)

    # Old value of the field before change
    old_value = models.TextField(null=True, blank=True)

    # New value of the field after change
    new_value = models.TextField(null=True, blank=True)

    # Optional name or identifier of the editor
    edited_by = models.CharField(max_length=255, null=True, blank=True)

    # Timestamp of when the change was made
    timestamp = models.DateTimeField(default=timezone.now)

    # Optional text explaining the reason for the change
    change_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.content_type.model} #{self.object_id} – {self.field_name} changed at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

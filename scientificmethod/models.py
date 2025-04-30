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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# === Scientific Method Core Models ===

class ResearchProblem(TimestampedModel):
    title = models.CharField(max_length=255)
    background = MDTextField()
    goal = MDTextField()

    def __str__(self):
        return self.title

class ResearchQuestion(TimestampedModel):
    research_problem = models.ForeignKey(ResearchProblem, on_delete=models.CASCADE, related_name='questions')
    question_text = MDTextField()
    rationale = MDTextField(null=True, blank=True)

    def __str__(self):
        return self.question_text

class Hypothesis(TimestampedModel):
    research_question = models.ForeignKey(ResearchQuestion, on_delete=models.CASCADE, related_name='hypotheses')
    parent_hypothesis = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_hypotheses')
    statement = MDTextField()
    hypothesis_type = models.CharField(
        max_length=20,
        choices=[
            ('Null', 'Null Hypothesis (H₀)'),
            ('Alternative', 'Alternative Hypothesis (H₁)')
        ]
    )
    scientific_basis = MDTextField(null=True, blank=True)
    expected_outcome = MDTextField(null=True, blank=True)
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
    modification_notes = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_hypothesis_type_display()}: {self.statement[:60]}..."

class HypothesisRevision(TimestampedModel):
    original_hypothesis = models.ForeignKey(Hypothesis, on_delete=models.CASCADE, related_name='revisions')
    new_hypothesis = models.OneToOneField(Hypothesis, on_delete=models.CASCADE, related_name='created_from_revision')
    rationale_for_change = MDTextField()
    based_on_observation = models.ForeignKey('Observation', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Revision of Hypothesis {self.original_hypothesis.id}"

class ExperimentalPlan(TimestampedModel):
    hypothesis = models.ForeignKey(Hypothesis, on_delete=models.CASCADE, related_name='experimental_plans')
    design_type = models.CharField(
        max_length=50,
        choices=[
            ('CRD', 'Completely Randomized Design'),
            ('RBD', 'Randomized Block Design'),
            ('LSD', 'Latin Square Design'),
            ('Other', 'Other Design')
        ]
    )
    independent_variables = MDTextField()
    dependent_variables = MDTextField()
    control_variables = MDTextField()
    planned_methods = MDTextField()
    notes = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"Plan for {self.hypothesis}"

class Experiment(TimestampedModel):
    experimental_plan = models.ForeignKey(ExperimentalPlan, on_delete=models.CASCADE, related_name='experiments')
    title = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
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
    failure_reason = MDTextField(null=True, blank=True)
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
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='failure_logs')
    description = MDTextField()
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
    corrective_action = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"Failure during {self.stage} in {self.experiment.title}"

class Variable(TimestampedModel):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='variables')
    name = models.CharField(max_length=255)
    variable_type = models.CharField(
        max_length=50,
        choices=[
            ('Independent', 'Independent Variable'),
            ('Dependent', 'Dependent Variable'),
            ('Confounding', 'Confounding Variable')
        ]
    )
    measurement_unit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.variable_type})"

class Observation(TimestampedModel):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='observations')
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, related_name='observations')
    value = models.FloatField()
    observation_date = models.DateField(null=True, blank=True)
    hypothesis_tested = models.ForeignKey(Hypothesis, on_delete=models.SET_NULL, null=True, blank=True, related_name='observations')
    result_support = models.CharField(
        max_length=20,
        choices=[
            ('Support', 'Supports Hypothesis'),
            ('Refute', 'Refutes Hypothesis'),
            ('Inconclusive', 'Inconclusive Result')
        ],
        default='Inconclusive'
    )
    notes = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"Observation {self.variable.name} on {self.observation_date}"

class EditHistory(TimestampedModel):
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    field_name = models.CharField(max_length=255)
    old_value = MDTextField(null=True, blank=True)
    new_value = MDTextField(null=True, blank=True)
    change_reason = MDTextField(null=True, blank=True)
    edited_by = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Edit in {self.model_name} ({self.field_name}) at {self.created_at}"

# === Version Tracking Model ===
class VersionHistory(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    field_name = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    edited_by = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    change_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.content_type.model} #{self.object_id} – {self.field_name} changed at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

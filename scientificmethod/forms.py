from django import forms
from .models import (
    ResearchProblem, ResearchQuestion, Hypothesis, HypothesisRevision,
    ExperimentalPlan, Experiment, Variable, Observation, FailureLog
)
from mdeditor.widgets import MDEditorWidget

class ResearchProblemForm(forms.ModelForm):
    class Meta:
        model = ResearchProblem
        fields = ['title', 'background', 'goal']
        widgets = {
            'background': MDEditorWidget(),
            'goal': MDEditorWidget(),
        }

class ResearchQuestionForm(forms.ModelForm):
    class Meta:
        model = ResearchQuestion
        fields = ['research_problem', 'question_text', 'rationale']
        widgets = {
            'rationale': MDEditorWidget(),
        }

class HypothesisForm(forms.ModelForm):
    class Meta:
        model = Hypothesis
        fields = ['research_question', 'parent_hypothesis', 'statement', 'hypothesis_type', 'scientific_basis', 'expected_outcome', 'status', 'modification_notes']
        widgets = {
            'statement': MDEditorWidget(),
            'scientific_basis': MDEditorWidget(),
            'expected_outcome': MDEditorWidget(),
            'modification_notes': MDEditorWidget(),
        }

class HypothesisRevisionForm(forms.ModelForm):
    class Meta:
        model = HypothesisRevision
        fields = ['original_hypothesis', 'new_hypothesis', 'rationale_for_change', 'based_on_observation']
        widgets = {
            'rationale_for_change': MDEditorWidget(),
        }

class ExperimentalPlanForm(forms.ModelForm):
    class Meta:
        model = ExperimentalPlan
        fields = ['hypothesis', 'design_type', 'independent_variables', 'dependent_variables', 'control_variables', 'planned_methods', 'notes']
        widgets = {
            'independent_variables': MDEditorWidget(),
            'dependent_variables': MDEditorWidget(),
            'control_variables': MDEditorWidget(),
            'planned_methods': MDEditorWidget(),
            'notes': MDEditorWidget(),
        }

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['experimental_plan', 'title', 'start_date', 'end_date', 'status', 'failure_reason', 'failure_stage']
        widgets = {
            'failure_reason': MDEditorWidget(),
        }

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ['experiment', 'name', 'variable_type', 'measurement_unit']

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['experiment', 'variable', 'value', 'observation_date', 'hypothesis_tested', 'result_support', 'notes']
        widgets = {
            'notes': MDEditorWidget(),
        }

class FailureLogForm(forms.ModelForm):
    class Meta:
        model = FailureLog
        fields = ['experiment', 'description', 'stage', 'corrective_action']
        widgets = {
            'description': MDEditorWidget(),
            'corrective_action': MDEditorWidget(),
        }

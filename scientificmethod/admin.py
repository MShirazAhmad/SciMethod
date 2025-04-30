from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ResearchProblem, ResearchQuestion, Hypothesis, HypothesisRevision,
    ExperimentalPlan, Experiment, Variable, Observation,
    FailureLog, EditHistory
)

# === Inline Admin Classes ===

class ResearchQuestionInline(admin.TabularInline):
    model = ResearchQuestion
    extra = 1

class HypothesisInline(admin.TabularInline):
    model = Hypothesis
    extra = 1

class HypothesisRevisionInline(admin.TabularInline):
    model = HypothesisRevision
    fk_name = 'original_hypothesis'  # Important: specify which ForeignKey
    extra = 1

class ExperimentalPlanInline(admin.TabularInline):
    model = ExperimentalPlan
    extra = 1

class ExperimentInline(admin.TabularInline):
    model = Experiment
    extra = 1

class VariableInline(admin.TabularInline):
    model = Variable
    extra = 1

class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 1

class FailureLogInline(admin.TabularInline):
    model = FailureLog
    extra = 1

# === Admin Model Registrations ===

@admin.register(ResearchProblem)
class ResearchProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [ResearchQuestionInline]

@admin.register(ResearchQuestion)
class ResearchQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'research_problem', 'created_at')
    ordering = ('-created_at',)
    inlines = [HypothesisInline]

@admin.register(Hypothesis)
class HypothesisAdmin(admin.ModelAdmin):
    list_display = ('statement', 'research_question', 'hypothesis_type', 'status', 'created_at')
    list_filter = ('hypothesis_type', 'status')
    ordering = ('-created_at',)
    inlines = [HypothesisRevisionInline, ExperimentalPlanInline]

@admin.register(ExperimentalPlan)
class ExperimentalPlanAdmin(admin.ModelAdmin):
    list_display = ('hypothesis', 'design_type', 'created_at')
    ordering = ('-created_at',)
    inlines = [ExperimentInline]

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'experimental_plan', 'status', 'failure_stage', 'start_date', 'end_date', 'failure_summary')
    list_filter = ('status', 'failure_stage')
    search_fields = ('title',)
    ordering = ('-start_date',)
    inlines = [VariableInline, ObservationInline, FailureLogInline]

    def failure_summary(self, obj):
        """Show summarized failure reason, highlighted in red if failed."""
        if obj.status == 'Failed':
            if obj.failure_reason:
                return format_html("<span style='color: red;'>{}</span>", obj.failure_reason[:50] + "...")
            return "Failure reason not documented"
        return "-"
    failure_summary.short_description = "Failure Summary"

@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ('name', 'experiment', 'variable_type')
    list_filter = ('variable_type',)
    ordering = ('name',)

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('variable', 'experiment', 'value', 'result_support')
    list_filter = ('result_support',)
    ordering = ('observation_date',)

@admin.register(FailureLog)
class FailureLogAdmin(admin.ModelAdmin):
    list_display = ('experiment', 'stage', 'description', 'created_at')
    list_filter = ('stage',)
    ordering = ('-created_at',)

@admin.register(EditHistory)
class EditHistoryAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'object_id', 'field_name', 'created_at')
    list_filter = ('model_name',)
    ordering = ('-created_at',)

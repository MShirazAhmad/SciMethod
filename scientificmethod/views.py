from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from .models import (
    ResearchProblem, ResearchQuestion, Hypothesis, ExperimentalPlan,
    Experiment, Variable, Observation, FailureLog, EditHistory
)

# === Home Page ===
from django.shortcuts import render
from .models import ResearchProblem, ResearchQuestion, Hypothesis, Experiment, Variable, Observation, FailureLog

def home(request):
    problems_count = ResearchProblem.objects.count()
    questions_count = ResearchQuestion.objects.count()
    hypotheses = Hypothesis.objects.all()
    supported_count = hypotheses.filter(status='Supported').count()
    refuted_count = hypotheses.filter(status='Refuted').count()
    pending_count = hypotheses.exclude(status__in=['Supported', 'Refuted']).count()

    experiments = Experiment.objects.all()
    running_count = experiments.filter(status='Running').count()
    completed_count = experiments.filter(status='Completed').count()
    failed_count = experiments.filter(status='Failed').count()

    variables_count = Variable.objects.count()
    observations_count = Observation.objects.count()
    failures_count = FailureLog.objects.count()

    return render(request, 'scientificmethod/home.html', {
        'problems_count': problems_count,
        'questions_count': questions_count,
        'supported_count': supported_count,
        'refuted_count': refuted_count,
        'pending_count': pending_count,
        'running_count': running_count,
        'completed_count': completed_count,
        'failed_count': failed_count,
        'variables_count': variables_count,
        'observations_count': observations_count,
        'failures_count': failures_count,
    })

# === Research Problem Views ===
class ResearchProblemListView(generic.ListView):
    model = ResearchProblem
    template_name = 'scientificmethod/researchproblem_list.html'
    context_object_name = 'researchproblems'

class ResearchProblemDetailView(generic.DetailView):
    model = ResearchProblem
    template_name = 'scientificmethod/researchproblem_detail.html'
    context_object_name = 'researchproblem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version_history'] = EditHistory.objects.filter(model_name='ResearchProblem', object_id=self.object.pk).order_by('-created_at')
        return context

class ResearchProblemCreateView(generic.CreateView):
    model = ResearchProblem
    fields = ['title', 'background', 'goal']
    template_name = 'scientificmethod/researchproblem_form.html'
    success_url = reverse_lazy('researchproblem_list')

class ResearchProblemUpdateView(generic.UpdateView):
    model = ResearchProblem
    fields = ['title', 'background', 'goal']
    template_name = 'scientificmethod/researchproblem_form.html'
    success_url = reverse_lazy('researchproblem_list')

class ResearchProblemDeleteView(generic.DeleteView):
    model = ResearchProblem
    template_name = 'scientificmethod/researchproblem_confirm_delete.html'
    success_url = reverse_lazy('researchproblem_list')

# === Research Question Views ===
class ResearchQuestionCreateView(generic.CreateView):
    model = ResearchQuestion
    fields = ['question_text', 'rationale']
    template_name = 'scientificmethod/researchquestion_form.html'

    def form_valid(self, form):
        research_problem = get_object_or_404(ResearchProblem, pk=self.kwargs['researchproblem_id'])
        form.instance.research_problem = research_problem
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_detail', kwargs={'pk': self.object.research_problem.id})

class ResearchQuestionUpdateView(generic.UpdateView):
    model = ResearchQuestion
    fields = ['question_text', 'rationale']
    template_name = 'scientificmethod/researchquestion_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_detail', kwargs={'pk': self.object.research_problem.id})

# === Hypothesis Views ===
class HypothesisCreateView(generic.CreateView):
    model = Hypothesis
    fields = ['statement', 'hypothesis_type', 'scientific_basis', 'expected_outcome']
    template_name = 'scientificmethod/hypothesis_form.html'

    def form_valid(self, form):
        research_question = get_object_or_404(ResearchQuestion, pk=self.kwargs['researchquestion_id'])
        form.instance.research_question = research_question
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

class HypothesisDetailView(generic.DetailView):
    model = Hypothesis
    template_name = 'scientificmethod/hypothesis_detail.html'
    context_object_name = 'hypothesis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version_history'] = EditHistory.objects.filter(model_name='Hypothesis', object_id=self.object.pk).order_by('-created_at')
        return context

class HypothesisUpdateView(generic.UpdateView):
    model = Hypothesis
    fields = ['statement', 'hypothesis_type', 'scientific_basis', 'expected_outcome', 'status', 'modification_notes']
    template_name = 'scientificmethod/hypothesis_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

# === Experimental Plan Views ===
class ExperimentalPlanCreateView(generic.CreateView):
    model = ExperimentalPlan
    fields = ['design_type', 'independent_variables', 'dependent_variables', 'control_variables', 'planned_methods', 'notes']
    template_name = 'scientificmethod/experimentalplan_form.html'

    def form_valid(self, form):
        hypothesis = get_object_or_404(Hypothesis, pk=self.kwargs['hypothesis_id'])
        form.instance.hypothesis = hypothesis
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

# === Experiment Views ===
class ExperimentCreateView(generic.CreateView):
    model = Experiment
    fields = ['title', 'start_date', 'end_date', 'status', 'failure_reason', 'failure_stage']
    template_name = 'scientificmethod/experiment_form.html'

    def form_valid(self, form):
        plan = get_object_or_404(ExperimentalPlan, pk=self.kwargs['experimentalplan_id'])
        form.instance.experimental_plan = plan
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

class ExperimentDetailView(generic.DetailView):
    model = Experiment
    template_name = 'scientificmethod/experiment_detail.html'
    context_object_name = 'experiment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version_history'] = EditHistory.objects.filter(model_name='Experiment', object_id=self.object.pk).order_by('-created_at')
        return context

class ExperimentUpdateView(generic.UpdateView):
    model = Experiment
    fields = ['title', 'start_date', 'end_date', 'status', 'failure_reason', 'failure_stage']
    template_name = 'scientificmethod/experiment_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

# === Variable Views ===
class VariableCreateView(generic.CreateView):
    model = Variable
    fields = ['name', 'variable_type', 'measurement_unit']
    template_name = 'scientificmethod/variable_form.html'

    def form_valid(self, form):
        experiment = get_object_or_404(Experiment, pk=self.kwargs['experiment_id'])
        form.instance.experiment = experiment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

# === Observation Views ===
class ObservationCreateView(generic.CreateView):
    model = Observation
    fields = ['variable', 'value', 'observation_date', 'hypothesis_tested', 'result_support', 'notes']
    template_name = 'scientificmethod/observation_form.html'

    def form_valid(self, form):
        experiment = get_object_or_404(Experiment, pk=self.kwargs['experiment_id'])
        form.instance.experiment = experiment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

# === FailureLog Views ===
class FailureLogCreateView(generic.CreateView):
    model = FailureLog
    fields = ['description', 'stage', 'corrective_action']
    template_name = 'scientificmethod/failurelog_form.html'

    def form_valid(self, form):
        experiment = get_object_or_404(Experiment, pk=self.kwargs['experiment_id'])
        form.instance.experiment = experiment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


class ScientificTreeView(generic.TemplateView):
    template_name = 'scientificmethod/treeview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problems = ResearchProblem.objects.prefetch_related('questions__hypotheses__experimental_plans__experiments')
        context['problems'] = problems
        return context


from django.urls import reverse_lazy
from django.views import generic
from .models import (
    ResearchProblem, ResearchQuestion, Hypothesis, ExperimentalPlan,
    Experiment, Variable, Observation, FailureLog
)


# --- Already existing ---
# ResearchProblemListView, ResearchProblemDetailView, ResearchProblemCreateView, etc.

# === ResearchQuestion Delete ===
class ResearchQuestionDeleteView(generic.DeleteView):
    model = ResearchQuestion
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_detail', kwargs={'pk': self.object.research_problem.id})


# === Hypothesis Delete ===
class HypothesisDeleteView(generic.DeleteView):
    model = Hypothesis
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


# === ExperimentalPlan Update/Delete ===
class ExperimentalPlanUpdateView(generic.UpdateView):
    model = ExperimentalPlan
    fields = ['design_type', 'independent_variables', 'dependent_variables', 'control_variables', 'planned_methods',
              'notes']
    template_name = 'scientificmethod/experimentalplan_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


class ExperimentalPlanDeleteView(generic.DeleteView):
    model = ExperimentalPlan
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


# === Experiment Delete ===
class ExperimentDeleteView(generic.DeleteView):
    model = Experiment
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


# === Variable Update/Delete ===
class VariableUpdateView(generic.UpdateView):
    model = Variable
    fields = ['name', 'variable_type', 'measurement_unit']
    template_name = 'scientificmethod/variable_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


class VariableDeleteView(generic.DeleteView):
    model = Variable
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


# === Observation Update/Delete ===
class ObservationUpdateView(generic.UpdateView):
    model = Observation
    fields = ['variable', 'value', 'observation_date', 'hypothesis_tested', 'result_support', 'notes']
    template_name = 'scientificmethod/observation_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


class ObservationDeleteView(generic.DeleteView):
    model = Observation
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


# === FailureLog Update/Delete ===
class FailureLogUpdateView(generic.UpdateView):
    model = FailureLog
    fields = ['description', 'stage', 'corrective_action']
    template_name = 'scientificmethod/failurelog_form.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')


class FailureLogDeleteView(generic.DeleteView):
    model = FailureLog
    template_name = 'scientificmethod/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('researchproblem_list')

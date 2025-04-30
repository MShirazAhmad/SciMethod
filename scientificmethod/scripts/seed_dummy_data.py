import random
from django.utils import timezone
from django.contrib.auth import get_user_model
from myapp.models import (
    ResearchProblem,
    ResearchQuestion,
    Hypothesis,
    ExperimentalPlan,
    Experiment,
    Variable,
    Observation,
    FailureLog,
    EditHistory,
)
from mdeditor.fields import MDTextField

def run():
    # Clear existing data
    # Helper functions to create safe test markdown content
    def get_test_markdown(title):
        return f"# {title}\n\nThis is a **test** markdown content for {title}.\n\n- Item 1\n- Item 2\n"

    # Create a dummy user for ownership if needed
    User = get_user_model()
    user, created = User.objects.get_or_create(username="seeduser", defaults={"email":"seeduser@example.com"})
    if created:
        user.set_password("password")
        user.save()

    # Create Research Problems
    problems = []
    for i in range(3):
        problem = ResearchProblem.objects.create(
            title=f"Research Problem {i+1}",
            description=get_test_markdown(f"Research Problem {i+1} Description"),
            created_by=user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        problems.append(problem)

    # Create Research Questions linked to Research Problems
    questions = []
    for problem in problems:
        for j in range(2):
            question = ResearchQuestion.objects.create(
                problem=problem,
                question_text=get_test_markdown(f"Research Question {j+1} for {problem.title}"),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            questions.append(question)

    # Create Hypotheses linked to Research Questions
    hypotheses = []
    for question in questions:
        for k in range(2):
            hypothesis = Hypothesis.objects.create(
                question=question,
                hypothesis_text=get_test_markdown(f"Hypothesis {k+1} for {question.question_text[:20]}"),
                status=random.choice(['proposed', 'tested', 'rejected']),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            hypotheses.append(hypothesis)

    # Create Experimental Plans linked to Hypotheses
    plans = []
    for hypothesis in hypotheses:
        for l in range(2):
            plan = ExperimentalPlan.objects.create(
                hypothesis=hypothesis,
                plan_description=get_test_markdown(f"Experimental Plan {l+1} for {hypothesis.hypothesis_text[:20]}"),
                status=random.choice(['draft', 'approved', 'completed']),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            plans.append(plan)

    # Create Experiments linked to Experimental Plans
    experiments = []
    for plan in plans:
        for m in range(2):
            experiment = Experiment.objects.create(
                plan=plan,
                experiment_name=f"Experiment {m+1} for Plan {plan.id}",
                description=get_test_markdown(f"Experiment {m+1} Description"),
                status=random.choice(['planned', 'running', 'finished']),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            experiments.append(experiment)

    # Create Variables linked to Experiments
    variables = []
    for experiment in experiments:
        for n in range(3):
            variable = Variable.objects.create(
                experiment=experiment,
                name=f"Variable {n+1} for Experiment {experiment.id}",
                var_type=random.choice(['independent', 'dependent', 'control']),
                description=get_test_markdown(f"Variable {n+1} Description"),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            variables.append(variable)

    # Create Observations linked to Variables
    observations = []
    for variable in variables:
        for o in range(2):
            observation = Observation.objects.create(
                variable=variable,
                observed_value=f"Value {random.uniform(0, 100):.2f}",
                notes=get_test_markdown(f"Observation notes for variable {variable.name}"),
                observed_at=timezone.now(),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            observations.append(observation)

    # Create Failure Logs linked to Experiments
    for experiment in experiments:
        for p in range(1):
            failure = FailureLog.objects.create(
                experiment=experiment,
                failure_reason="Simulated failure due to timeout.",
                failure_details=get_test_markdown(f"Failure details for experiment {experiment.id}"),
                logged_at=timezone.now(),
                created_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

    # Create Edit Histories linked to all above models randomly
    all_objs = problems + questions + hypotheses + plans + experiments + variables + observations
    for obj in all_objs:
        for q in range(1):
            EditHistory.objects.create(
                content_object=obj,
                edited_by=user,
                edit_summary="Initial seed edit",
                edit_notes=get_test_markdown(f"Edit notes for {obj}"),
                edited_at=timezone.now(),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

    print("Seeding complete.")

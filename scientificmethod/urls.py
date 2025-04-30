from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Tree
    path('tree/', views.ScientificTreeView.as_view(), name='scientific_tree'),

    # ResearchProblem
    path('problems/', views.ResearchProblemListView.as_view(), name='researchproblem_list'),
    path('problems/add/', views.ResearchProblemCreateView.as_view(), name='researchproblem_create'),
    path('problems/<int:pk>/', views.ResearchProblemDetailView.as_view(), name='researchproblem_detail'),
    path('problems/<int:pk>/edit/', views.ResearchProblemUpdateView.as_view(), name='researchproblem_update'),
    path('problems/<int:pk>/delete/', views.ResearchProblemDeleteView.as_view(), name='researchproblem_delete'),

    # ResearchQuestion
    path('questions/add/<int:researchproblem_id>/', views.ResearchQuestionCreateView.as_view(), name='researchquestion_create'),
    path('questions/<int:pk>/edit/', views.ResearchQuestionUpdateView.as_view(), name='researchquestion_update'),
    path('questions/<int:pk>/delete/', views.ResearchQuestionDeleteView.as_view(), name='researchquestion_delete'),  # NEW

    # Hypotheses
    path('hypotheses/add/<int:researchquestion_id>/', views.HypothesisCreateView.as_view(), name='hypothesis_create'),
    path('hypotheses/<int:pk>/', views.HypothesisDetailView.as_view(), name='hypothesis_detail'),
    path('hypotheses/<int:pk>/edit/', views.HypothesisUpdateView.as_view(), name='hypothesis_update'),
    path('hypotheses/<int:pk>/delete/', views.HypothesisDeleteView.as_view(), name='hypothesis_delete'),  # NEW

    # Experimental Plan
    path('plans/add/<int:hypothesis_id>/', views.ExperimentalPlanCreateView.as_view(), name='experimentalplan_create'),
    path('plans/<int:pk>/edit/', views.ExperimentalPlanUpdateView.as_view(), name='experimentalplan_update'),  # NEW
    path('plans/<int:pk>/delete/', views.ExperimentalPlanDeleteView.as_view(), name='experimentalplan_delete'),  # NEW

    # Experiments
    path('experiments/add/<int:experimentalplan_id>/', views.ExperimentCreateView.as_view(), name='experiment_create'),
    path('experiments/<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment_detail'),
    path('experiments/<int:pk>/edit/', views.ExperimentUpdateView.as_view(), name='experiment_update'),
    path('experiments/<int:pk>/delete/', views.ExperimentDeleteView.as_view(), name='experiment_delete'),  # NEW

    # Variables
    path('variables/add/<int:experiment_id>/', views.VariableCreateView.as_view(), name='variable_create'),
    path('variables/<int:pk>/edit/', views.VariableUpdateView.as_view(), name='variable_update'),  # NEW
    path('variables/<int:pk>/delete/', views.VariableDeleteView.as_view(), name='variable_delete'),  # NEW

    # Observations
    path('observations/add/<int:experiment_id>/', views.ObservationCreateView.as_view(), name='observation_create'),
    path('observations/<int:pk>/edit/', views.ObservationUpdateView.as_view(), name='observation_update'),  # NEW
    path('observations/<int:pk>/delete/', views.ObservationDeleteView.as_view(), name='observation_delete'),  # NEW

    # Failure Logs
    path('failures/add/<int:experiment_id>/', views.FailureLogCreateView.as_view(), name='failurelog_create'),
    path('failures/<int:pk>/edit/', views.FailureLogUpdateView.as_view(), name='failurelog_update'),  # NEW
    path('failures/<int:pk>/delete/', views.FailureLogDeleteView.as_view(), name='failurelog_delete'),  # NEW
]

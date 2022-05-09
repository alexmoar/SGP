from django.urls import path

from writer import views

app_name = 'writer'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('projects/list/', views.ProjectsListView.as_view(), name='list_projects'),
    path('projects/edit/<int:id>', views.ProjectsEditView.as_view(), name='edit_project'),
    path('projects/questions/<int:id>', views.ProjectQuestionsView.as_view(), name='get_questions_project'),
    path('projects/questions-detail/<int:id>', views.ProjectDescriptionQuestionView.as_view(),
         name='get_question_detail'),
    path('projects/add/', views.AddProjectView.as_view(), name='add_project'),
    path('projects/questions/add/', views.AddQuestionsProjectView.as_view(), name='add_questions'),
]

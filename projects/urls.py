from django.urls import path
from .views import ProjectsListView, ProjectsDetailView, CreateProjectView, pause_project, activate_project, complete_project

app_name = 'projects'

urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects_list'),
    path('<int:pk>/', ProjectsDetailView.as_view(), name='project_detail'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('<int:pk>/pause', pause_project, name='pause_project'),
    path('<int:pk>/activate',activate_project, name='activate_project'),
    path('<int:pk>/complete', complete_project, name='complete_project'),
]
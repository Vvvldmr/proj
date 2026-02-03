from django.urls import path
from .views import ProjectsListView, ProjectsDeteilView, CreateProjectView

app_name = 'projects'

urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects_list'),
    path('<int:pk>/', ProjectsDeteilView.as_view(), name='project_deteil'),
    path('create/', CreateProjectView.as_view(), name='create_project')
]
from django.urls import path
from .views import ProjectsList, ProjectsDeteil

urlpatterns = [
    path('', ProjectsList.as_view(), name='projects_list'),
    path('<int:pk>/', ProjectsDeteil.as_view(), name='project_deteil'),
]
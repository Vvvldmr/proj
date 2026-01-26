from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Projects, Tasks

class ProjectsList(LoginRequiredMixin, ListView):
    model = Projects
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        # Получаем только проекты текущего авторизованного пользователя
        return Projects.objects.filter(owner=self.request.user)


class ProjectsDeteil(LoginRequiredMixin, DetailView):
    model = Projects
    template_name = 'projects/projects_deteil.html'
    context_object_name = 'project'

    def get_queryset(self):
        # Получаем только проекты текущего авторизованного пользователя
        return Projects.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
    
        tasks = project.tasks.all()

        context['tasks'] = tasks

        return context
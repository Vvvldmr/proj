from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project, Task
from .forms import CreateProjectForm

def home(request):
    if request.user.is_authenticated:
        return redirect('projects:projects_list')
    return render(request, 'home.html')


class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        # Получаем только проекты текущего авторизованного пользователя
        return Project.objects.filter(owner=self.request.user)


class ProjectsDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/projects_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        # Получаем только проекты текущего авторизованного пользователя
        return Project.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
    
        tasks = project.tasks.all()

        context['tasks'] = tasks

        return context
    

class CreateProjectView(CreateView):
    model = Project
    template_name = 'projects/create_project.html'
    form_class = CreateProjectForm
    success_url = reverse_lazy('projects:projects_list')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        return super().form_valid(form)
    

def pause_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.status == 'active':
        project.status = 'on_hold'
        project.save()
        messages.success(request, f'Проект "{project.name}" поставлен на паузу')
    else:
        messages.warning(request, 'Проект уже на паузе или завершен')
    
    return redirect('projects:project_detail', pk=pk)


def activate_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.status == 'on_hold':
        project.status = 'active'
        project.save()
        messages.success(request, f'Проект "{project.name}" возобновлен')
    elif project.status == 'completed':
        messages.warning(request, 'Завершенный проект нельзя активировать')
    else:
        messages.info(request, 'Проект уже активен')
    
    return redirect('projects:project_detail', pk=pk)


def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.status != 'completed':
        project.status = 'completed'
        project.save()
        messages.success(request, f'Проект "{project.name}" завершен!')
    else:
        messages.info(request, 'Проект уже завершен')
    
    return redirect('projects:project_detail', pk=pk)

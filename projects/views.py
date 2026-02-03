from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
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


class ProjectsDeteilView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/projects_deteil.html'
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

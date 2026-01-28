from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('projects_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

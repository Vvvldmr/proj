from django import forms
from django.utils import timezone
from .models import Project


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'deadline']
        labels = {
            'name': 'Название проекта',
            'decription': 'Описание'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для стилизации
        self.fields['deadline'].widget.attrs.update({
            'class': 'form-control datetimepicker',
            'placeholder': 'Выберите дату и время'
        })
        
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError('Дедлайн не может быть в прошлом')
        return deadline
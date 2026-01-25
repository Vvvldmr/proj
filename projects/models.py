from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', ('Active')
        COMPLETED = 'completed', ('Completed')
        ON_HOLD = 'on_hold', ('On Hold')

    name = models.CharField(('Название'), max_length=50)
    description = models.CharField(('Описание'), max_length=200)
    status = models.CharField(
        ('Статус'),
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    deadline = models.DateTimeField(('Дедлайн'))
    created_at = models.DateTimeField(('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(('Обновлен'), auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name=('Владелец')
    )

    class Meta:
        verbose_name = ('Проект')
        verbose_name_plural = ('Проекты')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Tasks(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', ('To Do')
        IN_PROGRESS = 'in_progress', ('In Progress')
        DONE = 'done', ('Done')
    
    class Priority(models.TextChoices):
        LOW = 'low', ('Low')
        MEDIUM = 'medium', ('Medium')
        HIGH = 'high', ('High')
    
    name = models.CharField(('Название'), max_length=100)
    description = models.CharField(('Описание'), max_length=500)
    status = models.CharField(
        ('Статус'),
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )
    deadline = models.DateTimeField(('Дедлайн'))
    priority = models.CharField(
        ('Приоритет'),
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=('Проект')
    )
    created_at = models.DateTimeField(('Создана'), auto_now_add=True)
    updated_at = models.DateTimeField(('Обновлена'), auto_now=True)
    # Связь с пользователем (исполнитель задачи)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=('Исполнитель')
    )
    
    # Связь с пользователем (создатель задачи)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name=('Создатель')
    )
    
    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = ('Задачи')
        ordering = ['priority', 'deadline']
    
    def __str__(self):
        return f"{self.name} ({self.project.name})"


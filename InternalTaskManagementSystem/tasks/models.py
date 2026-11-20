from django.db import models
from  datetime import timezone
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('to do', 'To Do'), ('in progress', 'In Progress'), ('completed', 'Completed')])
    priority = models.CharField(max_length = 10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default = 'medium')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey('auth.User', on_delete = models.CASCADE, related_name = 'assigned_tasks')
    created_by = models.ForeignKey('auth.User', on_delete = models.CASCADE, related_name = 'created_tasks')
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

class Notes(models.Model):
    by_user = models.ForeignKey('auth.User', on_delete= models.CASCADE, related_name = 'user_notes')
    on_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name = 'task_notes')
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


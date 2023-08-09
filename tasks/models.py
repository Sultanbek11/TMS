from django.db import models


class Task(models.Model):
    Priority = (
        ('I', 'Low'),
        ('II', 'Medium'),
        ('III', 'High'),
    )
    title = models.CharField(max_length=45)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=Priority)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title

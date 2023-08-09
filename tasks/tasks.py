from celery import shared_task
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_notification(task_id):
    task = Task.objects.get(pk=task_id)
    subject = f'Task Reminder: {task.title}'
    message = f'Don\'t forget to complete your task: {task.title} by {task.due_date}'
    send_mail(subject, message, 'tms@example.com', [task.owner.email])


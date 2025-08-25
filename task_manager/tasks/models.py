from django.contrib.auth import get_user_model
from django.db import models

from task_manager.statuses.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=256, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Автор',
        related_name="tasks_author"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Исполнитель',
        related_name="tasks_executor",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        )

    def __str__(self):
        return self.name
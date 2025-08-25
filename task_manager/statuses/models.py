from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=256, 
        unique=True, 
        blank=False,
        verbose_name='Name',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
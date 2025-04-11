

# Create your models here.
from django.db import models # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Importance scale from 1 (lowest) to 10 (highest)"
    )
    estimated_hours = models.FloatField(validators=[MinValueValidator(0.1)])
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
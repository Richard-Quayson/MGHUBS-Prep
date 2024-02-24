from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account

class PriorityLevel(models.TextChoices):
    """
    defines the priority levels for a ToDo object
    """

    HIGH = 'high', _('high')
    MEDIUM = 'medium', _('medium')
    LOW = 'low', _('low')


class ToDo(models.Model):
    """
    defines attributes for a ToDo object

    Attributes:
        - user (ForeignKey): user who created the ToDo object
        - title (CharField): title of the ToDo object
        - description (TextField): description of the ToDo object
        - priority (CharField): priority level of the ToDo object
        - due date (DateField): date the ToDo object is due
        - time (TimeField): time the ToDo object is due
        - completed (BooleanField): status of the ToDo object
        - created_at (DateTimeField): date and time the ToDo object was created
        - updated_at (DateTimeField): date and time the ToDo object was last updated
    """

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=6, choices=PriorityLevel.choices, default=PriorityLevel.LOW)
    due_date = models.DateField()
    time = models.TimeField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"User: {self.user.firstname} {self.user.lastname}: {self.title}"
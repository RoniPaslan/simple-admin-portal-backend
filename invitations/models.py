from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

# Fungsi callable untuk default expired_at
def default_expired_at():
    return timezone.now() + timezone.timedelta(hours=72)

class Invitation(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("staff", "Staff"),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=default_expired_at)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def is_expired(self):
        return timezone.now() > self.expired_at

    def __str__(self):
        return f"{self.email} ({self.role})"

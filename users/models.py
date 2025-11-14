from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("superadmin", "SuperAdmin"),
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("staff", "Staff"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "superadmin"
        elif self.is_staff and self.role not in ["admin", "manager"]:
            self.role = "staff"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

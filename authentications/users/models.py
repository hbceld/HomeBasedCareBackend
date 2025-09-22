from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, user_id, full_name, role, password=None, **extra_fields):
        if not user_id:
            raise ValueError("The user must have a user_id")
        if not role:
            raise ValueError("The user must have a role (nurse/patient/admin)")

        user = self.model(
            user_id=user_id,
            full_name=full_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, full_name="Admin", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            user_id=user_id,
            full_name=full_name,
            role="admin",
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("nurse", "Nurse"),
        ("patient", "Patient"),
        ("admin", "Admin"),
    ]

    user_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["full_name", "role"]

    objects = UserManager()

    def __str__(self):
        return f"{self.user_id} ({self.role})"

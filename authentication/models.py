from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from core.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    ADMIN = "admin"
    EVALUATOR = "evaluator"
    WRITER = "writer"

    ROL = [
        (ADMIN, "Administrador"),
        (EVALUATOR, "Evaluador"),
        (WRITER, "Escritor"),
    ]

    username = models.CharField("Usuario", max_length=255, unique=True)
    first_name = models.CharField("Nombre(s)", max_length=255)
    last_name = models.CharField(verbose_name="Apellido(s)", max_length=255)
    identification = models.CharField(
        "Identificación", max_length=255, blank=True, null=True
    )
    cellphone = models.CharField("Teléfono", max_length=255)
    email = models.CharField(max_length=255, blank=True,
                             null=True, db_index=True)
    biography = models.TextField("Biografía")
    photo = models.CharField("Foto", max_length=255)
    role = models.CharField(
        max_length=9,
        choices=ROL
    )
    staff = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.id} | {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    full_name.fget.short_description = "Nombre"

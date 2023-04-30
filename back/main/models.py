from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MainUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    bonuses = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)

    objects = MainUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        return self.is_admin


class CreditCard(models.Model):
    MasterCard = 'MasterCard'
    Visa = 'Visa'

    CARD_TYPES = (
        (MasterCard, 'MasterCard'),
        (Visa, 'Visa'),
    )

    card_number = models.CharField(max_length=50)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    type = models.CharField(choices=CARD_TYPES, max_length=20)
    owner = models.ForeignKey(MainUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.card_number} - {self.type} - {self.owner}"

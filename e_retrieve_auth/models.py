from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid
from datetime import datetime

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):

        # creates a user with the parameters
        if username is None:
            raise ValueError('Registration number is required!')

        if name is None:
            raise ValueError('Full name is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            username=username.upper().strip(),
            name=name.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, name, password=None):
        # create a superuser with the above parameters

        user = self.create_user(
            username=username,
            name=name,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    username = models.CharField(max_length=100, db_index=True,
                                unique=True, verbose_name='reg number', blank=True)
    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)

    pics = models.ImageField(
        default='img/user.png', upload_to='uploads/', null=True)

    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("auth:profile", kwargs={
            'pk': self.user_id
        })

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'

class Session(models.Model):
    session_title = models.CharField(max_length=9, unique=True)
    session_description = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return self.session_title

    class Meta:
        db_table = 'Session'
        verbose_name_plural = 'Sessions'

class Semester(models.Model):
    semester_title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.semester_title

    class Meta:
        db_table = 'Semester'
        verbose_name_plural = 'Semesters'

class Department(models.Model):
    Department_title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Department_title

    class Meta:
        db_table = 'Department'
        verbose_name_plural = 'Departments'


class PastQuestion(models.Model):

    course_title = models.CharField(max_length=100)

    session = models.ForeignKey(
        to="Session", on_delete=models.CASCADE, blank=True, null=True, related_name="session")

    semester = models.ForeignKey(
        to="Semester", on_delete=models.CASCADE, blank=True, null=True, related_name="semester")

    department = models.ForeignKey(
        to="Department", on_delete=models.CASCADE, blank=True, null=True, related_name="department")

    past_question = models.FileField(upload_to='uploads/')

    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.semester} | {self.course_title}"

    class Meta:
        db_table = 'Past Question'
        verbose_name_plural = 'Past Questions'


"""
Databases Models.
"""
from django.conf import settings # noqa
from django.db import models # noqa
from django.utils.timezone import now # noqa
""" https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_username:~:text=Importing-,AbstractBaseUser,-AbstractBaseUser%20and%20BaseUserManager """ # noqa
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin ) # noqa


class UserManager(BaseUserManager):
    """ Manager for user."""

    def create_user(self, email, password=None, **extra_fields):
        """ Creatre, save and return a new user """
        if not email:
            raise ValueError('Users must have an email address.')
        """Pass normalised email to the email field. be4 saving the user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        """ This set_password will encrypt the password. """
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create and save a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


""" PermissionsMixin = Functioonality for the permiussions & fields. """


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    """ is_staff, Login with django admin """
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role_id = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        """Custom save method to update 'updated_at' automatically."""
        self.updated_at = now()
        super().save(*args, **kwargs)


class Role(models.Model):
    """Role model. """
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    """Course model."""
    title = models.CharField(max_length=255)
    image_link = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='instructor_courses'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    end_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Lesson model."""
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    content_type = models.CharField(max_length=50, choices=[('pdf', 'PDF'), ('video', 'Video'), ('doc', 'Doc')])
    description = models.TextField(null=True, blank=True)
    content_url = models.TextField(null=True, blank=True)
    order = models.SmallIntegerField()
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    """Enrollment model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('non-paid', 'Non-paid')])
    enrolled_at = models.DateTimeField(default=now)
    end_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} - {self.course.title}'


class Payment(models.Model):
    """Payment model."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('fail', 'Fail'), ('pending', 'Pending')])
    transaction_date = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.enrollment.user.email} - {self.enrollment.course.title} - {self.amount}'


class ListOfUserCourse(models.Model):
    """List of user course model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_courses'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='user_courses'
    )
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f'{self.user.email} - {self.course.title}'

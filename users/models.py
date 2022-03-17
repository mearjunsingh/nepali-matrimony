import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# path to upload profile photos
def UPLOAD_IMAGE_PATH(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return f'users/{filename}'


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

    # handles the user creation
    def create_user(self, phone_number, password, **kwargs):
        if not phone_number:
            raise ValueError(_('User must have a phone number.'))
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # handles the superuser creation
    def create_superuser(self, phone_number, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('full_name', 'Superuser')
        kwargs.setdefault('date_of_birth', '2000-01-01')
        kwargs.setdefault('gender', 'male')
        kwargs.setdefault('show', 'female')
        kwargs.setdefault('profile_photo', '/media/users/superuser.jpg')
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **kwargs)


class User(PermissionsMixin, AbstractBaseUser):
    """
    Custom User Model where phone number can be used to signup and login
    """
    id = models.UUIDField(primary_key=True, editable=False)

    # gender options
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )

    # hobby options
    HOBBIES = (
        ('music', 'Music'),
    )
    
    # user details
    phone_number = models.CharField(_('Phone Number'), max_length=15, unique=True)
    full_name = models.CharField(_('Full Name'), max_length=254)
    date_of_birth = models.DateField(_('Date of Birth'))
    gender = models.CharField(_('Gender'), max_length=7, choices=GENDERS)
    show = models.CharField(_('Show'), max_length=254, choices=GENDERS)
    profile_photo = models.ImageField(_('Profile Photo'), upload_to=UPLOAD_IMAGE_PATH)
    bio = models.TextField(_('Bio'), blank=True, null=True)
    hobbies = models.CharField(_('Hobbies'), max_length=254, choices=HOBBIES, blank=True, null=True)

    # user meta
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)

    # data meta
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('Last Login'), blank=True, null=True)
    user_created_ip = models.CharField(_('Created IP'), max_length=20, editable=False)

    # custom user manager
    objects = UserManager()

    # phone field as login credental
    USERNAME_FIELD = 'phone_number'

    # Display model instance as a readable string
    def __str__(self):
        return f'{self.full_name} - {self.phone_number}'
    
    # add ID once
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        return super().save(*args, **kwargs)

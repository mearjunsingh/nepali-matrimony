import datetime
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image


# path to upload profile photos
def UPLOAD_IMAGE_PATH(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return f"users/{filename}"


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

    # handles the user creation
    def create_user(self, phone_number, password, **kwargs):
        if not phone_number:
            raise ValueError(_("User must have a phone number."))
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # handles the superuser creation
    def create_superuser(self, phone_number, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_number, password, **kwargs)


class Hobby(models.Model):
    """
    Model that stores all hobbies
    """

    name = models.CharField(_("hobby title"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("hobbies")


class User(PermissionsMixin, AbstractBaseUser):
    """
    Custom User Model where phone number can be used to signup and login
    """

    id = models.UUIDField(primary_key=True, editable=False)

    # gender options
    GENDERS = (("male", "Male"), ("female", "Female"), ("other", "Other"))

    # user details
    phone_number = models.CharField(_("phone number"), max_length=10, unique=True)
    full_name = models.CharField(_("full name"), max_length=80)
    date_of_birth = models.DateField(_("date of birth"))
    gender = models.CharField(_("gender"), max_length=6, choices=GENDERS)
    show = models.CharField(_("show"), max_length=6, choices=GENDERS)
    profile_photo = models.ImageField(_("profile photo"), upload_to=UPLOAD_IMAGE_PATH)
    bio = models.TextField(_("bio"), blank=True, null=True)
    hobbies = models.ManyToManyField(Hobby, verbose_name=_("hobbies"))
    score = models.IntegerField(_("score"), default=0)

    # user meta
    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)

    # data meta
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last Login"), blank=True, null=True)

    # custom user manager
    objects = UserManager()

    # phone field as login credental
    USERNAME_FIELD = "phone_number"

    # must have fields for a user
    REQUIRED_FIELDS = ["full_name", "date_of_birth", "gender", "show", "profile_photo"]

    # Display model instance as a readable string
    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"

    # calculate age and use it as a property
    @property
    def age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

    # add ID once
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

        img = Image.open(self.profile_photo.path)
        width, height = img.size
        left = (width - 300) / 2
        top = (height - 300) / 2
        right = (width + 300) / 2
        bottom = (height + 300) / 2
        img = img.crop((left, top, right, bottom))
        img.save(self.profile_photo.path)

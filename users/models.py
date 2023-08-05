from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from library_app.utils import uuid4
from django.utils.text import slugify
import pyotp
import enum

class UserRole(enum.Enum):
    ADMINISTRATOR = ("A", _("Administrator"), _("Administrators"), "Administrators")
    EDITOR = ("E", _("Editor"), _("Editors"), "Editors")
    VIEWER = ("V", _("Viewer"), _("Viewers"), "Viewers")


    def __init__(self, code: str, display: str, display_plural: str, group_name: str):
        self.code = code
        self.display = display
        self.display_plural = display_plural
        self.group_name = group_name


    @classmethod
    def from_code(cls, code: str):
        for role in cls:
            if role.code == code:
                return role
        return None


    @classmethod
    def from_group(cls, group: Group):
        for role in cls:
            if role.group == group:
                return role
        return None

    @cached_property
    def group(self):
        """
        The auth group which defines the permissions for this role
        """
        return Group.objects.get(name=self.group_name)


    @cached_property
    def permissions(self) -> set:
        perms = self.group.permissions.select_related("content_type")
        return {f"{p.content_type.app_label}.{p.codename}" for p in perms}

    def has_perm(self, permission: str) -> bool:
        """
        Returns whether this role has the given permission
        """
        return permission in self.permissions


class UserManager(BaseUserManager):

  def _create_user(self,email,password,**extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.password = make_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    extra_fields.setdefault('is_active', False)  # Set is_active to False by default
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email,password,**extra_fields)

  def create_superuser(self,email,password,**extra_fields):
    extra_fields.setdefault('is_active', True)  # Set is_active to False by default
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('user_type', 'ADMIN')
    user=self._create_user(email,password,**extra_fields)
    return user


class User(AbstractUser):
    USER_TYPE_CHOICES = (("ADMIN", "ADMIN"),("STAFF", "STAFF"),("STUDENT", "STUDENT"))
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    username = None
    email = models.EmailField(max_length=254, unique=True)
    user_type = models.CharField(max_length=100,choices=USER_TYPE_CHOICES)
    role_code = models.CharField(max_length=100,default=UserRole.ADMINISTRATOR)
    school_id = models.CharField(max_length=225,null=True,blank=True) # Staff ID OR Student ID
    national_id = models.CharField(max_length=225,null=True,blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic",null=True)
    otp_secret = models.CharField(max_length=100, default=pyotp.random_base32)
    two_factor_enabled = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=100,null=True)
    phone_type = models.CharField(max_length=225,null=True,blank=True)
    phone_number = models.CharField(max_length=225,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    bio = models.TextField(null = True, blank = True)
    last_otp_verified = models.DateTimeField(null=True)
    is_otp_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    @property
    def name(self):
        return self.get_full_name()

class Attendance(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    item = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ('-created_at',)

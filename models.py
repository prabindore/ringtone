from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from django.utils import timezone
from django.db import models






class State(models.Model):
    name = models.CharField(max_length=30)
    country_id = models.IntegerField(default=101,null=True,blank=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'states' 
        ordering = ['name'] 
        

class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities' 
        ordering = ['name'] 


class Ringtone_Language(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    language_name = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ringtone_language'

    def __str__(self):
        return self.language_name
    

class Ringtone(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    AUDIO_TYPE_CHOICES = [
        ('file', 'File Upload'),
        ('url', 'URL'),
    ]

    ringtone_language = models.ForeignKey(Ringtone_Language, on_delete=models.CASCADE, related_name='ringtones')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    ringtone_title = models.CharField(max_length=255)
    ringtone_year = models.CharField(max_length=10)

    def ringtone_upload_path(instance, filename):
        return f'ringtones/{filename}'

    # Separate fields for file and URL
    ringtone_file = models.FileField(upload_to=ringtone_upload_path, null=True, blank=True)

    # Audio type choice to define whether it's a file or URL
    ringtone_url = models.URLField(max_length=500, null=True, blank=True)
    audio_type = models.CharField(max_length=10, choices=AUDIO_TYPE_CHOICES, default='file')

    is_hyped = models.BooleanField(default=False)
    is_all = models.BooleanField(default=False)
    play_times = models.IntegerField(default=0, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ringtone_title

    class Meta:
        db_table = 'ringtones'
        ordering = ['-created_at']
        


class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        # Ensure these fields are always set for a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, user_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]

    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    ringtone_language = models.ForeignKey(Ringtone_Language, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=60, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='User')
    user_phone = models.CharField(max_length=20)
    user_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    user_dob = models.DateField(null=True, blank=True)
    is_all = models.BooleanField(default=False,null=True,blank=True)
    profile_img = models.ImageField(upload_to='users_images/', null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add these two fields for superuser management
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.user_name




from django.contrib.auth import get_user_model
User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',null=True, blank=True)
    notification_title = models.CharField(max_length=255)
    notification_msg = models.CharField(max_length=255)
    notification_on = models.DateTimeField(default=timezone.now) 
    image = models.ImageField(upload_to='notification_images/', null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-notification_on']

    def __str__(self):
        return self.notification_title
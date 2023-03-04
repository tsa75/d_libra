from django import forms
from django.conf import settings
from django.db import models
from django.forms import ModelForm, PasswordInput
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


ROLES = (
    ('normaluser', 'normaluser'),
    ('editor', 'editor'),
)

VISIBILITY_STATUS = (
    ('public', 'Public'),
    ('member_only', 'Member Only'),
    ('editor_only', 'Editor Only'),
)


class User(models.Model):
    email = models.EmailField(max_length=255, default='')
    username = models.CharField(max_length=255, default='')
    password = models.TextField(default='')
    role = models.CharField(max_length=20, choices=ROLES, default='normaluser')
    icon = models.ImageField(upload_to='upload/user/icons/', blank=True, null=True)
    status = models.BooleanField(default=False)
    password_status = models.BooleanField(default=False)
    token = models.CharField(max_length=255, default='')
    token_status = models.BooleanField(default=False)
    token_tries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class UserForm(ModelForm):
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'icon']


class Category(MPTTModel):
    unique_identifier = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='upload/category/icons', blank=True, null=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='categories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.unique_identifier + ' ' + self.name


class Course(models.Model):
    unique_identifier = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='upload/course/icons', blank=True, null=True)
    cover_image = models.FileField(upload_to='upload/course/cover_images', blank=True, null=True)
    visibility_status = models.CharField(max_length=20, choices=VISIBILITY_STATUS, default='editor_only')
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unique_identifier + ' ' + self.name


class Chapter(models.Model):
    unique_identifier = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    visibility_status = models.CharField(max_length=20, choices=VISIBILITY_STATUS, default='editor_only')
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='chapters', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unique_identifier + ' ' + self.name


class Topic(models.Model):
    unique_identifier = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    main_figure = models.FileField(upload_to='upload/topic/main_figure', blank=True, null=True)
    description = models.TextField(default='')
    content = RichTextField()
    visibility_status = models.CharField(max_length=20, choices=VISIBILITY_STATUS, default='editor_only')
    chapter = models.ForeignKey(Chapter, related_name='topics', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unique_identifier + ' ' + self.name

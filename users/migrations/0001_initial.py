# Generated by Django 3.2.12 on 2022-03-16 15:48

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('country_code', models.CharField(max_length=3, verbose_name='Country Code')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='Phone Number')),
                ('full_name', models.CharField(max_length=254, verbose_name='Full Name')),
                ('date_of_birth', models.DateField(verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=7, verbose_name='Gender')),
                ('show', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=254, verbose_name='Show')),
                ('profile_photo', models.ImageField(upload_to=users.models.UPLOAD_IMAGE_PATH, verbose_name='Profile Photo')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('hobbies', models.CharField(blank=True, choices=[('music', 'Music')], max_length=254, null=True, verbose_name='Hobbies')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last Login')),
                ('user_created_ip', models.CharField(editable=False, max_length=20, verbose_name='Created IP')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

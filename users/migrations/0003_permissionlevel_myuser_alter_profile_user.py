# Generated by Django 4.2.6 on 2024-04-19 22:38

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion

def create_default_permission_level(apps, schema_editor):
    PermissionLevel = apps.get_model('users' , 'PermissionLevel')
    PermissionLevel.objects.create(name= 'Base', description='Default permission lv for new users')
    PermissionLevel.objects.create(name= 'Approver', description='base + can access an approval view that manages approving images')
    PermissionLevel.objects.create(name= 'Admin', description='admin, all')



class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0002_profile_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('permission_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.permissionlevel')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.myuser'),
        ),

        migrations.RunPython(create_default_permission_level),  
    ]

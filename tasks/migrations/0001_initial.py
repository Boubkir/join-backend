# Generated by Django 4.2.3 on 2023-07-06 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default=None, max_length=30)),
                ('title', models.CharField(default=None, max_length=200)),
                ('description', models.CharField(default=None, max_length=200)),
                ('priority', models.CharField(default=None, max_length=10)),
                ('status', models.CharField(default=None, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(default=None)),
                ('sub_tasks', models.JSONField(default=list, null=True)),
                ('assigned_to', models.ManyToManyField(related_name='todos', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

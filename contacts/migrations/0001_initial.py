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
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=30)),
                ('last_name', models.CharField(default=None, max_length=30)),
                ('email', models.CharField(default=None, max_length=50)),
                ('phone', models.CharField(default=None, max_length=20)),
                ('color', models.CharField(default=None, max_length=20)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
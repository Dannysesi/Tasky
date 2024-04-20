# Generated by Django 4.2.2 on 2024-04-01 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to='project.team'),
        ),
    ]
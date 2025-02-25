# Generated by Django 4.2.16 on 2025-02-25 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0023_remove_submit_ip_address_hash_submit_ip_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('deadline', models.DateTimeField()),
                ('publish_results', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('clazz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.class')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.JSONField(default=dict)),
                ('hash', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('root', models.CharField(default='quizzes', max_length=255)),
                ('src', models.CharField(max_length=255, unique=True, verbose_name='Directory')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.subject')),
            ],
        ),
        migrations.CreateModel(
            name='EnrolledQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField()),
                ('max_points', models.FloatField(default=0.0)),
                ('submit', models.JSONField(default=dict)),
                ('scoring', models.JSONField(default=dict)),
                ('submitted', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.assignedquiz')),
                ('scored_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scored_by', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.templatequiz')),
            ],
        ),
        migrations.AddField(
            model_name='assignedquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
    ]

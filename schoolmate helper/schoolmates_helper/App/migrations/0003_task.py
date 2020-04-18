# Generated by Django 2.0 on 2020-03-23 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32)),
                ('task_sketch', models.CharField(max_length=512)),
                ('task_file', models.FileField(upload_to='task_file/%Y/%m/%d/')),
                ('task_type', models.CharField(max_length=16)),
                ('task_date_year', models.IntegerField(default=0)),
                ('task_date_month', models.IntegerField(default=0)),
                ('task_date_day', models.IntegerField(default=0)),
                ('task_reward', models.IntegerField(default=0)),
                ('is_pickedup', models.BooleanField(default=False)),
                ('hunter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunter', to='App.User', verbose_name='委托人')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='App.User', verbose_name='发布人')),
            ],
        ),
    ]
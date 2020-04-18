# Generated by Django 2.0 on 2020-04-06 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_auto_20200406_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.SET_DEFAULT, to='App.TaskType'),
        ),
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(null=True, upload_to='icons/%Y/%m/%d/'),
        ),
    ]

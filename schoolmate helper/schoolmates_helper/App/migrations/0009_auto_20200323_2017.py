# Generated by Django 2.0 on 2020-03-23 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_auto_20200323_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='App.taskType'),
        ),
    ]

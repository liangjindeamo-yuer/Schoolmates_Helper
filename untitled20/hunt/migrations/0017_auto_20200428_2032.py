# Generated by Django 2.1.7 on 2020-04-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunt', '0016_auto_20200428_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_reward',
            field=models.IntegerField(default=0),
        ),
    ]

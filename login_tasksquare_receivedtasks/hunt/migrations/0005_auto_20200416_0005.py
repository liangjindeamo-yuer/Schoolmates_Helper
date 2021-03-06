# Generated by Django 2.0.13 on 2020-04-15 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hunt', '0004_auto_20200413_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(default=1)),
                ('typename', models.CharField(max_length=32)),
                ('typesort', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.SET_DEFAULT, to='hunt.TaskType'),
        ),
    ]

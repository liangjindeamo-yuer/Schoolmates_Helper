# Generated by Django 2.0.13 on 2020-04-10 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32)),
                ('task_sketch', models.CharField(max_length=512, null=True)),
                ('task_file', models.FileField(null=True, upload_to='task_file/%Y/%m/%d/')),
                ('task_date_year', models.IntegerField(default=2020, null=True)),
                ('task_date_month', models.IntegerField(default=0, null=True)),
                ('task_date_day', models.IntegerField(default=0, null=True)),
                ('task_reward', models.IntegerField(default=0, null=True)),
                ('is_pickedup', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(default=1)),
                ('typename', models.CharField(max_length=32)),
                ('typesort', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=64, unique=True)),
                ('icon', models.ImageField(upload_to='icons/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='hunter',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hunter', to='task_received.User', verbose_name='委托人'),
        ),
        migrations.AddField(
            model_name='task',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='task_received.User', verbose_name='发布人'),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.SET_DEFAULT, to='task_received.TaskType'),
        ),
    ]

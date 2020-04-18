# Generated by Django 2.0.5 on 2020-04-12 04:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_auto_20200412_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.RenameField(
            model_name='missioninfo',
            old_name='mission2',
            new_name='acp',
        ),
        migrations.RenameField(
            model_name='missioninfo',
            old_name='mission3',
            new_name='finish',
        ),
        migrations.RemoveField(
            model_name='missioninfo',
            name='mission4',
        ),
        migrations.RemoveField(
            model_name='missioninfo',
            name='pwd',
        ),
        migrations.RemoveField(
            model_name='missioninfo',
            name='user',
        ),
        migrations.AddField(
            model_name='missioninfo',
            name='reason',
            field=models.CharField(default="无", max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='missioninfo',
            name='m_user',
            field=models.ForeignKey(default=0, on_delete=None, to='App.UserInfo'),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.0.5 on 2020-04-12 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20200412_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment1', models.CharField(max_length=128)),
                ('m_mission', models.ForeignKey(on_delete=None, to='App.MissionInfo')),
            ],
        ),
    ]
# Generated by Django 2.0.5 on 2020-04-18 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_auto_20200418_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='missioninfo',
            name='m_money',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
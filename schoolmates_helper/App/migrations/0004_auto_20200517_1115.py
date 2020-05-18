# Generated by Django 2.1.7 on 2020-05-17 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_discuss_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='publisher',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='App.User', verbose_name='发布人'),
        ),
    ]
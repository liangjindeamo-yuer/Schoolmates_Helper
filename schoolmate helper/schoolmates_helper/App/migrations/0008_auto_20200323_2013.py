# Generated by Django 2.0 on 2020-03-23 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20200323_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='hunter',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hunter', to='App.User', verbose_name='委托人'),
        ),
    ]
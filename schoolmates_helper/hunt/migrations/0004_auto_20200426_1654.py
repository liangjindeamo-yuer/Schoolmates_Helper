# Generated by Django 2.0.5 on 2020-04-26 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunt', '0003_auto_20200420_1022'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comments',
        ),
    ]
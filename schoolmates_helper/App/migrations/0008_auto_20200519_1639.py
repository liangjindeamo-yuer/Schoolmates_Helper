# Generated by Django 2.1.7 on 2020-05-19 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_cancel_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(default='icons/haha.jpg', null=True, upload_to='icons/%Y/%m/%d/'),
        ),
    ]
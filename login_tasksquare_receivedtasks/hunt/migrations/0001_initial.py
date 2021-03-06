# Generated by Django 2.0.5 on 2020-04-11 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('code', models.CharField(default='0', max_length=20)),
                ('tel', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=30)),
                ('qq', models.CharField(blank=True, max_length=20, null=True)),
                ('wechat', models.CharField(blank=True, max_length=20, null=True)),
                ('other', models.CharField(blank=True, max_length=20, null=True)),
                ('star', models.PositiveIntegerField(default=5)),
            ],
        ),
    ]

# Generated by Django 3.2.5 on 2021-11-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20211029_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeyeCookieModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('updated_time', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(default='cookie name', max_length=64)),
                ('domain', models.CharField(default='', max_length=2048)),
                ('values', models.TextField()),
                ('status', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
                'db_table': 'geye_cookie',
            },
        ),
    ]

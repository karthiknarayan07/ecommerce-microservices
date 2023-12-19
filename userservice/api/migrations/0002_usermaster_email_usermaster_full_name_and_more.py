# Generated by Django 5.0 on 2023-12-19 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermaster',
            name='email',
            field=models.EmailField(default='abc@gmail.com', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermaster',
            name='full_name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermaster',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]

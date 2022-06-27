# Generated by Django 2.2.4 on 2022-06-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examApp', '0003_auto_20220625_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='grantedwish',
        ),
        migrations.AddField(
            model_name='wish',
            name='users_list',
            field=models.ManyToManyField(related_name='lists', to='examApp.User'),
        ),
        migrations.DeleteModel(
            name='grantedwish',
        ),
    ]
# Generated by Django 2.2.3 on 2019-10-01 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_loggeduser_emailid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='user',
        ),
    ]

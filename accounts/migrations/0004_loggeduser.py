# Generated by Django 2.2.3 on 2019-09-28 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_chatroom_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loggeduser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('emailid', models.EmailField(max_length=254)),
            ],
        ),
    ]
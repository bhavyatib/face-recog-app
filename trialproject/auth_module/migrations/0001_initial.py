# Generated by Django 4.0.4 on 2022-05-14 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('code', models.CharField(max_length=32)),
                ('account', models.CharField(choices=[('0', 'STUDENT'), ('1', 'PROFESSOR')], max_length=1)),
                ('status', models.CharField(choices=[('0', 'NOT_VERIFIED'), ('1', 'VERIFIED')], default='0', max_length=1)),
            ],
        ),
    ]
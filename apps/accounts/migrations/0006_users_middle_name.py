# Generated by Django 4.0.6 on 2023-07-29 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_users_college_users_department_users_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='middle_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
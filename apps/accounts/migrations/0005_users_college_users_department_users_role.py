# Generated by Django 4.0.6 on 2023-07-29 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('accounts', '0004_remove_users_college_remove_users_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.college'),
        ),
        migrations.AddField(
            model_name='users',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.department'),
        ),
        migrations.AddField(
            model_name='users',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.role'),
        ),
    ]

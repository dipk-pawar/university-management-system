# Generated by Django 4.0.6 on 2023-07-27 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_user_college'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.college'),
        ),
    ]
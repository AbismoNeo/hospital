# Generated by Django 4.0.6 on 2022-09-28 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitapp', '0011_alter_medical_staff_user_alter_patients_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alergies',
            name='user',
            field=models.IntegerField(verbose_name='id de Usuario'),
        ),
    ]

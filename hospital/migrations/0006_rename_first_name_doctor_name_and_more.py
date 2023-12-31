# Generated by Django 4.2.2 on 2023-07-02 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_rename_name_doctor_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='last_name',
        ),
    ]

# Generated by Django 3.2.8 on 2021-11-09 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoMedicalApp', '0002_rename_description_medicaldetails_detailsdescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='contact',
            new_name='contact_no',
        ),
    ]

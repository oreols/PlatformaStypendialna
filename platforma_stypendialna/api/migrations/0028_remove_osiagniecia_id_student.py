# Generated by Django 5.0.3 on 2024-05-04 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_remove_osiagniecia_typ_osiagniecia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='osiagniecia',
            name='id_student',
        ),
    ]
# Generated by Django 5.0.3 on 2024-05-04 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_osiagniecia_konkursy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='osiagniecia',
            name='id_konkursu',
        ),
    ]
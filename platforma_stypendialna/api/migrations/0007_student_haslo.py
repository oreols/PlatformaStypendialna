# Generated by Django 5.0.3 on 2024-04-04 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_student_haslo_alter_student_zalaczniki'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='haslo',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

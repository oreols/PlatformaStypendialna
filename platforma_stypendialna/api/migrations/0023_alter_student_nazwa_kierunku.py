# Generated by Django 5.0.3 on 2024-04-18 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_remove_student_kierunek_alter_student_nazwa_kierunku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='nazwa_kierunku',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.kierunek'),
            preserve_default=False,
        ),
    ]
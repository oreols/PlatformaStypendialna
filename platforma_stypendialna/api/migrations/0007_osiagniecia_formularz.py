# Generated by Django 5.0.3 on 2024-06-10 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_student_plec'),
    ]

    operations = [
        migrations.AddField(
            model_name='osiagniecia',
            name='formularz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.formularz'),
        ),
    ]

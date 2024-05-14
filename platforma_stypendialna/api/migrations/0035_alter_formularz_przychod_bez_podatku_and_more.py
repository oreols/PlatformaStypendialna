# Generated by Django 5.0.3 on 2024-05-14 13:15

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_alter_czlonekrodziny_imie_czlonka_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formularz',
            name='przychod_bez_podatku',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='imie',
            field=models.CharField(max_length=20, null=True, validators=[api.models.validate_string]),
        ),
        migrations.AlterField(
            model_name='student',
            name='nazwisko',
            field=models.CharField(max_length=35, null=True, validators=[api.models.validate_string]),
        ),
    ]
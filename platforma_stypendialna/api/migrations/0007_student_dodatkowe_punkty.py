# Generated by Django 5.0.3 on 2024-05-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_osiagniecia_id_osiagniecia'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='dodatkowe_punkty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

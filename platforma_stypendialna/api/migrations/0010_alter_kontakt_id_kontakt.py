# Generated by Django 5.0.3 on 2024-06-10 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_kontakt_id_kontakt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kontakt',
            name='id_kontakt',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

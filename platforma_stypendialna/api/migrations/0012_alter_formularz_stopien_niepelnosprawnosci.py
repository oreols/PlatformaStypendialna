# Generated by Django 5.0.3 on 2024-04-13 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_stopienniepelnosprawnosci'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formularz',
            name='stopien_niepelnosprawnosci',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.stopienniepelnosprawnosci'),
            preserve_default=False,
        ),
    ]

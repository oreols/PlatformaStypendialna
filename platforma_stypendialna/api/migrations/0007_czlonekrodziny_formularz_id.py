# Generated by Django 5.0.3 on 2024-05-17 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_osiagniecia_id_osiagniecia'),
    ]

    operations = [
        migrations.AddField(
            model_name='czlonekrodziny',
            name='formularz_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.formularz'),
            preserve_default=False,
        ),
    ]

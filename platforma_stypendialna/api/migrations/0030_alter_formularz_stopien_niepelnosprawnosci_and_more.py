# Generated by Django 5.0.3 on 2024-05-08 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_alter_osiagniecia_data_osiagniecia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formularz',
            name='stopien_niepelnosprawnosci',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.stopienniepelnosprawnosci'),
        ),
        migrations.AlterField(
            model_name='formularz',
            name='symbol_niepelnosprawnosci',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.symbolniepelnosprawnosci'),
        ),
    ]

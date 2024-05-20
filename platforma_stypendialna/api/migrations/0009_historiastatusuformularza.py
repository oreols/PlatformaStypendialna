# Generated by Django 5.0.3 on 2024-05-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_czlonekrodziny_formularz_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriaStatusuFormularza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formularz_id', models.IntegerField()),
                ('stary_status', models.CharField(max_length=255)),
                ('nowy_status', models.CharField(max_length=255)),
                ('zmiana_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'HistoriaStatusuFormularza',
            },
        ),
    ]

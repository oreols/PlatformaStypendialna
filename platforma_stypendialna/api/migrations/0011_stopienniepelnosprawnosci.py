# Generated by Django 5.0.3 on 2024-04-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_formularz_aktualny_semestr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StopienNiepelnosprawnosci',
            fields=[
                ('id_stopnia', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_stopnia', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
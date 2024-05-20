# Generated by Django 5.0.3 on 2024-05-15 13:48

import api.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id_admin', models.IntegerField(primary_key=True, serialize=False)),
                ('haslo', models.TextField(null=True)),
                ('login', models.TextField(null=True)),
                ('email', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id_log_admin', models.IntegerField(primary_key=True, serialize=False)),
                ('adres_ip', models.TextField(null=True)),
                ('login', models.TextField(null=True)),
                ('data_logowania', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AktualnySemestr',
            fields=[
                ('id_semestru', models.IntegerField(primary_key=True, serialize=False)),
                ('semestr', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DecyzjeStypendialne',
            fields=[
                ('id_decyzji', models.IntegerField(primary_key=True, serialize=False)),
                ('id_student', models.IntegerField(null=True)),
                ('decyzja', models.SmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kierunek',
            fields=[
                ('id_kierunku', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_kierunku', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SemestrStudenta',
            fields=[
                ('id_semestru', models.IntegerField(primary_key=True, serialize=False)),
                ('semestr', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StopienNiepelnosprawnosci',
            fields=[
                ('id_stopnia', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_stopnia', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SymbolNiepelnosprawnosci',
            fields=[
                ('id_symbolu', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_symbolu', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id_student', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=191, null=True, unique=True)),
                ('data_rejestracji', models.DateField(null=True)),
                ('ikonka', models.ImageField(blank=True, max_length=50, null=True, upload_to='dokumenty/ikonki')),
                ('pesel', models.CharField(max_length=11, null=True, unique=True, validators=[api.models.validate_digits_only])),
                ('imie', models.CharField(max_length=20, null=True)),
                ('nazwisko', models.CharField(max_length=35, null=True)),
                ('zalaczniki', models.FileField(blank=True, null=True, upload_to='dokumenty/zalaczniki')),
                ('numer_telefonu', models.CharField(max_length=9, null=True, unique=True, validators=[api.models.validate_digits_only])),
                ('semestr', models.CharField(max_length=1, null=True, validators=[api.models.validate_digits_only])),
                ('numer_albumu', models.CharField(max_length=5, null=True, validators=[api.models.validate_digits_only])),
                ('rok_studiow', models.CharField(max_length=1, null=True, validators=[api.models.validate_digits_only])),
                ('numer_konta_bankowego', models.CharField(max_length=26, null=True, validators=[api.models.validate_digits_only])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('nazwa_kierunku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.kierunek')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Aktualnosci',
            fields=[
                ('id_aktualnosci', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_aktualnosci', models.TextField(null=True)),
                ('tekst_aktualnosci', models.TextField(null=True)),
                ('data_opublikowania', models.DateField(null=True)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.admin')),
            ],
        ),
        migrations.CreateModel(
            name='CzlonekRodziny',
            fields=[
                ('id_czlonka', models.IntegerField(primary_key=True, serialize=False)),
                ('imie_czlonka', models.TextField(null=True)),
                ('nazwisko_czlonka', models.TextField(null=True)),
                ('stopien_pokrewienstwa', models.TextField(max_length=10, null=True)),
                ('data_urodzenia', models.DateField(null=True)),
                ('miejsce_pracy', models.TextField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DaneDziekanat',
            fields=[
                ('numer_albumu', models.IntegerField(primary_key=True, serialize=False)),
                ('imie', models.TextField(null=True)),
                ('nazwisko', models.TextField(null=True)),
                ('pesel', models.TextField(null=True)),
                ('srednia_ocen', models.FloatField(null=True)),
                ('id_przedmiot', models.IntegerField(null=True)),
                ('id_kierunku', models.IntegerField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Formularz',
            fields=[
                ('id_formularza', models.IntegerField(primary_key=True, serialize=False)),
                ('typ_stypendium', models.CharField(blank=True, max_length=30, null=True)),
                ('data_zlozenia', models.DateTimeField(blank=True, null=True)),
                ('przychod_bez_podatku', models.FloatField(blank=True, null=True)),
                ('srednia_przychod', models.FloatField(blank=True, null=True)),
                ('srednia_ocen', models.FloatField(blank=True, null=True)),
                ('dodatkowe_informacje', models.TextField(blank=True, null=True)),
                ('plik_orzeczenie', models.ImageField(blank=True, null=True, upload_to='dokumenty/orzeczenia')),
                ('id_osiagniecia', models.IntegerField(blank=True, null=True)),
                ('oswiadczenie_prawo_o_szkolnictwie', models.BooleanField(default=False)),
                ('oswiadczenie_gospodarstwo_domowe', models.BooleanField(default=False)),
                ('oswiadczenie_dochody', models.BooleanField(default=False)),
                ('zalacznik', models.FileField(blank=True, null=True, upload_to='dokumenty/zalaczniki')),
                ('charakter_stopnia_niepelnosprawnosci', models.TextField(blank=True, max_length=100, null=True)),
                ('data_rozpoczecia_orzeczenia', models.DateField(blank=True, null=True)),
                ('data_konca_orzeczenia', models.DateField(blank=True, null=True)),
                ('zalacznik_niepelnosprawnosc', models.FileField(blank=True, null=True, upload_to='dokumenty/zalaczniki_niepelnosprawnosci')),
                ('aktualny_semestr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.aktualnysemestr')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('semestr_studenta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.semestrstudenta')),
                ('stopien_niepelnosprawnosci', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.stopienniepelnosprawnosci')),
                ('symbol_niepelnosprawnosci', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.symbolniepelnosprawnosci')),
            ],
        ),
        migrations.CreateModel(
            name='InformacjeStypendialne',
            fields=[
                ('id_wersja', models.IntegerField(primary_key=True, serialize=False)),
                ('tekst', models.TextField(null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.admin')),
            ],
        ),
        migrations.CreateModel(
            name='Kontakt',
            fields=[
                ('id_kontakt', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.TextField(null=True)),
                ('numer_tel', models.IntegerField(null=True)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.admin')),
            ],
        ),
        migrations.CreateModel(
            name='Kryteria',
            fields=[
                ('rok_kryterium', models.IntegerField(primary_key=True, serialize=False)),
                ('srednia_ocen', models.FloatField(null=True)),
                ('przychod_bez_podatku', models.FloatField(null=True)),
                ('id_kierunku', models.IntegerField(null=True)),
                ('id_formularza', models.IntegerField(null=True)),
                ('wzor_stypendium', models.TextField(null=True)),
                ('formularz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.formularz')),
            ],
        ),
        migrations.CreateModel(
            name='KryteriaStrona',
            fields=[
                ('id_wersja', models.IntegerField(primary_key=True, serialize=False)),
                ('rok', models.TextField(null=True)),
                ('tekst', models.TextField(null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.admin')),
            ],
        ),
        migrations.CreateModel(
            name='Osiagniecia',
            fields=[
                ('id_osiagniecia', models.IntegerField(primary_key=True, serialize=False)),
                ('liczba_osiagniec', models.IntegerField(blank=True, null=True)),
                ('krotki_opis', models.TextField(blank=True, max_length=250, null=True)),
                ('data_osiagniecia', models.DateField(blank=True, null=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Powiadomienia',
            fields=[
                ('id_powiadomienia', models.IntegerField(primary_key=True, serialize=False)),
                ('tresc_powiadomienia', models.TextField(null=True)),
                ('naglowek_powiadomienia', models.TextField(null=True)),
                ('autor_powiadomienia', models.TextField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Przedmiot',
            fields=[
                ('id_przedmiot', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_przedmiotu', models.TextField(null=True)),
                ('id_kierunku', models.IntegerField(null=True)),
                ('semestr', models.IntegerField(null=True)),
                ('punkty_ects', models.IntegerField(null=True)),
                ('kierunek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.kierunek')),
            ],
        ),
        migrations.CreateModel(
            name='OcenaKoncowaDziekanat',
            fields=[
                ('id_ocena', models.IntegerField(primary_key=True, serialize=False)),
                ('numer_albumu', models.IntegerField(null=True)),
                ('ocena_koncowa', models.FloatField(null=True)),
                ('id_przedmiotu', models.IntegerField(null=True)),
                ('dane_dziekanat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.danedziekanat')),
                ('przedmiot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.przedmiot')),
            ],
        ),
        migrations.CreateModel(
            name='OcenaKoncowa',
            fields=[
                ('id_ocena', models.IntegerField(primary_key=True, serialize=False)),
                ('id_student', models.IntegerField(null=True)),
                ('ocena_koncowa', models.FloatField(null=True)),
                ('id_przedmiotu', models.IntegerField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('przedmiot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.przedmiot')),
            ],
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('numer_albumu', models.IntegerField(primary_key=True, serialize=False)),
                ('punkty_rankingu', models.CharField(max_length=45, null=True)),
                ('typ_stypendium', models.CharField(max_length=65, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentLog',
            fields=[
                ('id_log', models.IntegerField(primary_key=True, serialize=False)),
                ('adres_ip', models.CharField(max_length=45, null=True)),
                ('nazwa_uzytkownika', models.TextField(null=True)),
                ('data_logowania', models.DateTimeField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ustawienia',
            fields=[
                ('id_student', models.IntegerField(primary_key=True, serialize=False)),
                ('nowe_haslo', models.TextField(blank=True, null=True)),
                ('nowy_numer_konta_bankowego', models.TextField(blank=True, null=True)),
                ('nowy_email', models.TextField(blank=True, null=True)),
                ('nowe_imie', models.TextField(blank=True, null=True)),
                ('nowe_nazwisko', models.TextField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunSQL('''
            DELIMITER //
            CREATE PROCEDURE CountStudents()
            BEGIN
            DECLARE student_count INT;

            SELECT COUNT(*) INTO student_count FROM api_Student;

            SELECT student_count AS 'Liczba_studentow';
            END//
            DELIMITER ;
            '''),
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS HistoriaStatusuFormularza (
                id INT AUTO_INCREMENT PRIMARY KEY,
                formularz_id INT,
                stary_status VARCHAR(255),
                nowy_status VARCHAR(255),
                zmiana_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (formularz_id) REFERENCES api_formularz(id_formularza)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS HistoriaStatusuFormularza;"
        ),
        migrations.RunSQL(
            """
            DELIMITER //

            CREATE TRIGGER trg_status_update
            BEFORE UPDATE ON api_formularz
            FOR EACH ROW
            BEGIN
                IF NEW.status <> OLD.status THEN
                    INSERT INTO HistoriaStatusuFormularza (formularz_id, stary_status, nowy_status)
                    VALUES (OLD.id_formularza, OLD.status, NEW.status);
                END IF;
            END;
            //

            DELIMITER ;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS trg_status_update;"
        ),
    ]

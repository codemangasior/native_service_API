# Generated by Django 2.2.2 on 2019-06-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinalPricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_to_get_ready', models.DateField()),
                ('price', models.CharField(max_length=10)),
                ('comments', models.CharField(max_length=500)),
                ('secret_key', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='NativePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('REPREZENTOWANIE FIRM', 'REPREZENTOWANIE FIRM'), ('SPRAWY URZĘDOWE', 'SPRAWY URZĘDOWE'), ('PRACA MIESZKANIE AUTO', 'PRACA MIESZKANIE AUTO'), ('TŁUMACZENIA', 'TŁUMACZENIA')], max_length=50, verbose_name='Kategoria')),
                ('name', models.CharField(max_length=50, verbose_name='Imię')),
                ('last_name', models.CharField(max_length=50, verbose_name='Nazwisko')),
                ('title', models.CharField(max_length=200, verbose_name='Nazwa zlecenia')),
                ('priority', models.CharField(choices=[('WYSOKI', 'WYSOKI'), ('STANDARD', 'STANDARD'), ('NISKI', 'NISKI')], default='STANDARD', max_length=15, verbose_name='Priorytet')),
                ('email', models.CharField(max_length=100, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Numer Telefonu')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('date_to_be_done', models.DateField()),
                ('description', models.TextField(verbose_name='Opis zlecenia')),
                ('secret_key', models.SlugField(max_length=45)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]

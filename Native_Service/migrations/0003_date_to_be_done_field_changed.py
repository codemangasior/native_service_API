# Generated by Django 2.2.1 on 2019-06-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("Native_Service", "0002_auto_20190604_0731")]

    operations = [
        migrations.AlterField(
            model_name="nativepost",
            name="date",
            field=models.DateField(auto_now_add=True),
        )
    ]
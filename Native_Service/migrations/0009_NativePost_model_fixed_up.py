# Generated by Django 2.2.2 on 2019-06-13 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("Native_Service", "0008_datefield_swapped_with_datetimefiled")]

    operations = [
        migrations.CreateModel(
            name="FinalPricing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time_to_get_ready", models.DateField()),
                ("price", models.CharField(max_length=10)),
                ("comments", models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name="nativepost",
            name="date_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="nativepost", name="date_to_be_done", field=models.DateField()
        ),
    ]

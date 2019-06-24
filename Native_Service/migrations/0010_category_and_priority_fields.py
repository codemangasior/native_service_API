# Generated by Django 2.2.2 on 2019-06-24 14:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Native_Service', '0009_NativePost_model_fixed_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalpricing',
            name='secret_key',
            field=models.CharField(default=django.utils.timezone.now, max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nativepost',
            name='priority',
            field=models.CharField(choices=[('WYSOKI', 'WYSOKI'), ('STANDARD', 'STANDARD'), ('NISKI', 'NISKI')], default='STANDARD', max_length=15),
        ),
        migrations.AlterField(
            model_name='finalpricing',
            name='comments',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]

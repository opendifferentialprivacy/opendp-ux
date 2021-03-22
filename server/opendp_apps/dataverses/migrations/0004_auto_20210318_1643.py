# Generated by Django 3.1.2 on 2021-03-18 16:43

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataverses', '0003_dataversehandoff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifesttestparams',
            name='apiGeneralToken',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=255)),
        ),
        migrations.AlterField(
            model_name='manifesttestparams',
            name='apiSensitiveDataReadToken',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=255)),
        ),
        migrations.AlterField(
            model_name='manifesttestparams',
            name='datasetPid',
            field=models.CharField(help_text='Dataset DOI', max_length=255),
        ),
        migrations.AlterField(
            model_name='manifesttestparams',
            name='fileId',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='manifesttestparams',
            name='filePid',
            field=models.CharField(blank=True, help_text='File DOI', max_length=255),
        ),
        migrations.AlterField(
            model_name='manifesttestparams',
            name='siteUrl',
            field=models.CharField(max_length=255),
        ),
    ]

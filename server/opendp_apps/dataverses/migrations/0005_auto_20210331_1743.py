# Generated by Django 3.1.6 on 2021-03-31 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataverses', '0004_auto_20210318_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataversehandoff',
            name='fileId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='manifesttestparams',
            name='fileId',
            field=models.IntegerField(),
        ),
    ]
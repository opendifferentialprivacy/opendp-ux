# Generated by Django 3.1.2 on 2021-04-28 19:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('version', models.FloatField()),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Terms of Access',
                'verbose_name_plural': 'Terms of Access',
                'ordering': ('active', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TermsOfAccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('dataset_info', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataset.datasetinfo')),
                ('terms_of_access', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terms_of_access.termsofaccess')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

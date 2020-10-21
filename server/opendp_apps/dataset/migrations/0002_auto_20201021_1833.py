# Generated by Django 3.1.2 on 2020-10-21 18:33

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisPlan',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('is_complete', models.BooleanField(default=False)),
                ('user_step', models.CharField(choices=[('step_010', 'Step 10: Terms of Access'), ('step_020', 'Step 20: Custom Variables'), ('step_030', 'Step 30: Confirm Variable Types'), ('step_100', 'Step 100: Analysis ready!')], max_length=128)),
                ('variable_ranges', models.JSONField()),
                ('variable_categories', models.JSONField()),
                ('custom_variables', models.JSONField()),
                ('dp_statistics', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataSetInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('source', models.CharField(choices=[('upload', 'Upload'), ('dataverse', 'Dataverse')], max_length=128)),
                ('data_profile_key', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DatasetSource',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.CharField(choices=[('upload', 'Upload'), ('dataverse', 'Dataverse')], max_length=128)),
                ('dataset_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.datasetinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepositorSetupInfo',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('user_step', models.CharField(choices=[('step_10', 'Step 10: Terms of Access'), ('step_20', 'Step 20: Upload'), ('step_30', 'Step 30: Dataset Type')], max_length=128)),
                ('epsilon', models.FloatField()),
                ('dataset_questions', models.JSONField()),
                ('variable_ranges', models.JSONField()),
                ('variable_categories', models.JSONField()),
                ('dataset', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='dataset.datasetinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReleaseInfo',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('epsilon_used', models.FloatField()),
                ('dp_release', models.JSONField()),
                ('analysis_plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataset.analysisplan')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataset.datasetinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='DataverseFile',
        ),
        migrations.CreateModel(
            name='DataverseFileInfo',
            fields=[
                ('datasetinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dataset.datasetinfo')),
                ('dataverse_file_id', models.CharField(max_length=128)),
                ('doi', models.CharField(max_length=128)),
                ('installation_name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=('dataset.datasetinfo',),
        ),
        migrations.CreateModel(
            name='UploadFileInfo',
            fields=[
                ('datasetinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dataset.datasetinfo')),
                ('data_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/ramanprasad/Documents/github-rp/opendp-ux/server/test_setup/user_uploaded_data'), upload_to='user-files/%Y/%m/%d/', verbose_name='User uploaded files')),
            ],
            options={
                'abstract': False,
            },
            bases=('dataset.datasetinfo',),
        ),
    ]
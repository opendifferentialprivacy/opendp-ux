from django.db import models
from django.db.models import CASCADE
from polymorphic.models import PolymorphicModel

class DepositorSetupInfo(models.Model):
    """
    Metadata and aggregate data about potential release of Dataset
    """
    is_complete = models.BooleanField()
    user_step = models.CharField(max_length=128)
    epsilon = models.FloatField(null=False, blank=False)
    dataset_questions = models.JSONField()
    variable_ranges = models.JSONField()
    variable_categories = models.JSONField()

class BaseDataSetInfo(PolymorphicModel):
    """
    Base type for table that either holds DV data
    or a file upload
    """
    name = models.CharField(max_length=128)
    # Redis key to store potentially sensitive information
    # during analysis setup
    data_profile_key = models.CharField(max_length=128)
    depositor_setup_info = models.ForeignKey(DepositorSetupInfo, on_delete=CASCADE)

class DataverseFileInfo(BaseDataSetInfo):
    """
    Refers to a DV file from within a DV dataset
    """
    # TODO: This should have all fields from DV API response
    dataverse_file_id = models.CharField(max_length=128)
    doi = models.CharField(max_length=128)
    installation_name = models.CharField(max_length=128)


class UploadFileInfo(BaseDataSetInfo):
    """
    Refers to a file uploaded independently of DV
    """
    # TODO: What other fields are needed here?
    file_path = models.CharField(max_length=128)


class DatasetSource(models.Model):
    """
    Keeps track of where the data came from
    """
    class SourceChoices(models.TextChoices):
        # TODO: This should allow for all installation names?
        ONE = 'upload', 'Upload'
        TWO = 'dataverse', 'Dataverse'

    source = models.CharField(max_length=128, choices=SourceChoices.choices)
    dataset_info = models.ForeignKey(BaseDataSetInfo, on_delete=CASCADE)


class AnalysisPlan(models.Model):
    """
    Details of request for a differnetially private release
    """
    is_complete = models.BooleanField()
    user_step = models.CharField(max_length=128)
    variable_ranges = models.JSONField()
    variable_categories = models.JSONField()
    custom_variables = models.JSONField()
    dp_statistics = models.JSONField()

class ReleaseInfo(models.Model):
    """
    Release of differentially private result from Dataset
    """
    epsilon_used = models.FloatField(null=False, blank=False)
    dp_release = models.JSONField()

class TermsOfAccess(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    version = models.FloatField(null=False, blank=False)

class TermsOfAccessLog(models.Model):
    user = models.CharField(max_length=128)
    terms_of_access = models.ForeignKey(TermsOfAccess, on_delete=models.RESTRICT)
    dataset_info = models.ForeignKey(BaseDataSetInfo, on_delete=models.RESTRICT)
    timestamp = models.DateField()


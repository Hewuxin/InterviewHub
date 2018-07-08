"""
===== 
models.py 
===== 

"""

from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField, ArrayField
from django.utils import timezone


class QueryRequest(models.Model):
    """
    ==============

    ``QueryRequest``
    ----------

    .. py:class:: QueryRequest()
    Respective model for query requests.

    .. note::
    .. todo::
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    CHOICES = (
        ('AI', 'Arrange_interview'),
        ('GR', 'General_report'),
    )
    query_type = models.CharField(max_length=100, choices=CHOICES)
    request_date = models.DateTimeField(default=timezone.now)
    candidate = models.ForeignKey('CandidateModel', on_delete=models.CASCADE, blank=True) # models.CharField(max_length=300)
    interviewer = models.ForeignKey('InterviewerModel', on_delete=models.CASCADE, blank=True) # models.CharField(max_length=300)

    def add(self, **kwargs):
        """
        .. py:attribute:: add()
        Save model instances.

           :param query_type: the type ot query
           :type query_type: str
           :param candidate: candidate's username
           :type candidate: str
           :param interviewer: interviewer's username
           :type interviewer: str
           :param user: user object
           :type user: auth.User
        .. note::
        .. todo::
        """
        self.request_date = timezone.now()
        self.query_type = kwargs['query_type']
        self.candidate = kwargs['candidate']
        self.interviewer = kwargs['interviewer']
        self.user = kwargs['user']

class CandidateModel(models.Model):
    """
    ==============

    ``CandidateModel``
    ----------

    .. py:class:: CandidateModel()
    Candidate's model class. 

    .. note::
    .. todo::
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    available_dates = ArrayField(models.CharField(max_length=100), null=True, blank=True)

    class Meta:
        permissions = (
            ("candidate", "not an interviewer"),
        )
    def __str__(self):
        """
        .. py:attribute:: __str__()
        Respective string representation of the model fields.

        .. note::
        .. todo::
        """
        return str(self.user.username)


class InterviewerModel(models.Model):
    """
    ==============

    ``InterviewerModel``
    ----------

    .. py:class:: InterviewerModel()
    Interviewer's model class.

    .. note::
    .. todo::
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    available_dates = ArrayField(models.CharField(max_length=100),null=True, blank=True)
    

    def __str__(self):
        """
        .. py:attribute:: __str__()
        Respective string representation of the model fields.

        .. note::
        .. todo::
        """
        return str(self.user.username)
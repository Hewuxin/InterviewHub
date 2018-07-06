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
    candidate = models.ForeignKey('CandidateModel', on_delete=models.CASCADE) # models.CharField(max_length=300)
    interviewer = models.ForeignKey('InterviewerModel', on_delete=models.CASCADE) # models.CharField(max_length=300)

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


    .. note::
    .. todo::
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    available_dates = ArrayField(DateTimeRangeField(), null=True, blank=True)

    def __str__(self):
        """
        .. py:attribute:: __str__()


        .. note::
        .. todo::
        """
        return "{} {}".format(
            self.user.first_name,
            self.user.last_name
        ) 

class InterviewerModel(models.Model):
    """
    ==============

    ``InterviewerModel``
    ----------

    .. py:class:: InterviewerModel()


    .. note::
    .. todo::
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    available_dates = ArrayField(DateTimeRangeField(),null=True, blank=True)
    
    class Meta:
        permissions = (
            ("interviwer", "Permissions that a candidate shouldn't have."),
        )
    def __str__(self):
        """
        .. py:attribute:: __str__()

        .. note::
        .. todo::
        """
        return "{} {}".format(
            self.user.first_name,
            self.user.last_name
        ) 
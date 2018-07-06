from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField, ArrayField
from django.utils import timezone


class QueryRequest(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    CHOICES = (
        ('AI', 'Arrange_interview'),
        ('GR', 'General_report'),
    )
    query_type = models.CharField(max_length=100, choices=CHOICES)
    request_date = models.DateTimeField(default=timezone.now)
    candidate = models.CharField(max_length=300)
    interviewer = models.CharField(max_length=300)

    def add(self, **kwargs):
        self.request_date = timezone.now()
        self.query_type = kwargs['query_type']
        self.candidate = kwargs['candidate']
        self.interviewer = kwargs['interviewer']
        self.user = kwargs['user']

class CandidateModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    available_dates = ArrayField(DateTimeRangeField())

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}" 

class InterviewerModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    available_dates = ArrayField(DateTimeRangeField())
    
    class Meta:
        permissions = (
            ("interviwer", "Permissions that a candidate shouldn't have."),
        )
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

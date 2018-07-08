"""
===== 
analyzer.py 
===== 

This module contains all the necessary functions for analyzing
data and helpers for views. 
=================
"""

from calendarapp.models import CandidateModel, InterviewerModel
from collections import defaultdict
from functools import wraps
import tzlocal  # $ python3 -m pip install tzlocal
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime


def reformater(f):
    """
    ==============

    ``reformater``
    ----------

    .. py:function:: reformater(['f'])
    reformatting the names and date times
       :param f: function
       :type f: Function Onject
    .. note:: 
    .. todo:: Convert all the time zones to UTC
    """
    @wraps(f)
    def wrapper(*args):
        # Use local-timezone for more accuracy and preventing
        # the code from time conflicst.
        result = f(*args)
        # local_timezone = tzlocal.get_localzone()
        for (date, time), names in result.items():
            #s = datetime.fromtimestamp(float(s), local_timezone)
            #e = datetime.fromtimestamp(float(e), local_timezone)
            names = ','.join(names)
            yield {"date": date,"time": time, "names": names}
    return wrapper

class Analyzer:
    """
    ==============

    ``Analyzer``
    ----------

    .. py:class:: Analyzer()


    .. note::
    .. todo::
    """
    def __init__(self, *args, **kwargs):
        """
        .. py:attribute:: __init__()
        Constructor for Analyzer class

        .. note::
        .. todo::
        """
        pass
    
    @reformater
    def available_interviewers(self, candidate_email, interviewer):
        """
        .. py:attribute:: available_interviewers()
        This function accepts the candidates email and 
        returns a dictionary contains all the interviewers
        available for interviewing the given candidate.

           :param candidate_email: candidate's username
           :type candidate_email: string
        .. note::
        .. todo::
        """
        candidate = CandidateModel.objects.get(user__email=candidate_email)
        candidate_av_times =  self.time_formater(candidate.available_dates)
        interviewers = InterviewerModel.objects.all()
        interviewers_av_times = [(t.user.username,  self.time_formater(t.available_dates)) for t in interviewers]
        
        agg_result = defaultdict(list)
        for hours, date, _date, _time in candidate_av_times:
            for name, times in interviewers_av_times:
                if any((d == date) and h.intersection(hours) for h, d, *_ in times):
                    agg_result[(_date, _time)].append(name)
        return agg_result
    
    @reformater
    def available_candidates(self, candidate_email, interviewer):
        """
        .. py:attribute:: available_candidates()
        This function accepts the interviewer username and 
        returns a dictionary contains all the candidates
        available for interviewing by the given interviewer.
           :param interviewer: interviewer username
           :type interviewer: string
        .. note::
        .. todo::
        """
        interviewer = InterviewerModel.objects.get(username=interviewer)
        interviewer_av_times =  self.time_formater(interviewer.available_dates)
        candidates = CandidateModel.objects.all()
        candidates_av_times = [(t.username, self.time_formater(t.available_dates)) for t in candidates]
        
        agg_result = defaultdict(list)
        for hours, date, _date, _time in interviewer_av_times:
            for name, times in candidates_av_times:
                if any((d == date) and h.intersection(hours) for h, d, *_ in times):
                    agg_result[(_date, _time)].append(name)
        return agg_result
    
    def time_formater(self, times):
        for d in times:
            _date, _time = d.split('_')
            s, e = _time.split('-')
            date = datetime.strptime(_date, "%Y-%m-%d"),
            hours = set(range(int(s), int(e)))
            yield hours, date, _date, _time

"""
class FormCreator:
    def __init__(self, *args, **kwargs):
        _fields = [
            ('from_date_{}', forms.DateField(widget=AdminDateWidget())),
            ('to_date_{}', forms.DateField(widget=AdminDateWidget()))
        ]
        self.fields = [(name.format(i), filed) for i in kwargs['form_range'] for name, field in _fields]
    
    def create_interviewer_form(self):
        X = type('CandidateForm', (object, form.Form), self.fileds)
    
    def create_candidate_form(self):
        X = type('InterviewerForm', (object, form.Form), self.fileds)
"""    
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
    def wrapper(result):
        # Use local-timezone for more accuracy and preventing
        # the code from time conflicst.
        local_timezone = tzlocal.get_localzone()
        for (s, e), names in result.items():
            s = datetime.fromtimestamp(float(s), local_timezone)
            e = datetime.fromtimestamp(float(e), local_timezone)
            date = s.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)").split()[0]
            time = "{} to {}".format(s.hour, e.hour)
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
    def available_interviewers(candidate_email):
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
        candidate = CandidateModel.objects.get(email=candidate_email)
        candidate_av_times = candidate.available_times
        interviewers = InterviewerModel.objects.all()
        interviewers_av_times = [(t.username, t.available_times) for t in interviewers]
        
        agg_result = defaultdict(list)
        for s, e in candidate_av_times:
            for name, times in interviewers_av_times:
                if any(s > t[0] and e < t[1] for t in times):
                    agg_result[t].append(name)
        return agg_result
    
    @reformater
    def available_candidates(interviewer):
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
        interviewer_av_times = interviewer.available_times
        candidates = CandidateModel.objects.all()
        candidates_av_times = [(t.username, t.available_times) for t in candidates]
        
        agg_result = defaultdict(list)
        for s, e in interviewer_av_times:
            for name, times in candidates_av_times:
                if any(s > t[0] and e < t[1] for t in times):
                    agg_result[t].append(name)
        return agg_result

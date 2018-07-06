from calendarapp.models import CandidateModel, InterviewerModel
from collections import defaultdict
from functools import wraps

def reformater(f):
    @wraps(f)
    def wrapper(result):
        for (s, e), names in result.items():
            s = datetime.fromtimestamp(int(s))
            e = datetime.fromtimestamp(int(e))
            date = s.strftime('%Y-%m-%d %H:%M:%S').split()[0]
            time = "{} to {}".format(s.hour, e.hour)
            names = ','.join(names)
            yield {"date": date,"time": time, "names": names}
    return wrapper

class Analyzer:
    def __init__(self, *args, **kwargs):
        pass
    
    @reformater
    def available_interviewers(candidate_email):
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

from datetime import datetime, timedelta


query_th = [
    "date",
    "time",
    "interviewers"
]

RANGE_FRAME = 2 
ROW_NUMBER = 30

WEEKS = 2
TIME_RANGE = range(9, 16)
_date_range = [datetime.now() + timedelta(days=i) for i in range(WEEKS*7)]
DATES = [("{}-{}-{}".format(d.year, d.month, d.day), "{}-{}-{}".format(d.year, d.month, d.day)) for d in _date_range]
TIMES = [('{}-{}'.format(i, i + 1), '{}-{}'.format(i, i + 1)) for i in TIME_RANGE]
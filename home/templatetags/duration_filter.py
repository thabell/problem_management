from django import template
register = template.Library()

from datetime import timedelta

@register.filter
def duration_to_mins(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    # secs = timedeltaobj.total_seconds()
    # timetot = ""
    # if secs > 86400: # 60sec * 60min * 24hrs
    #     days = secs // 86400
    #     timetot += "{} days".format(int(days))
    #     secs = secs - days*86400

    # if secs > 3600:
    #     hrs = secs // 3600
    #     timetot += " {} hours".format(int(hrs))
    #     secs = secs - hrs*3600

    # if secs > 60:
    #     mins = secs // 60
    #     timetot += " {} minutes".format(int(mins))
    #     secs = secs - mins*60

    # if secs > 0:
    #     timetot += " {} seconds".format(int(secs))
    # return timetot
    # return secs
    answer = timedeltaobj
    if isinstance(timedeltaobj, timedelta):
        answer = int(timedeltaobj.total_seconds() // 60)
    else:
        answer = 0
    return answer
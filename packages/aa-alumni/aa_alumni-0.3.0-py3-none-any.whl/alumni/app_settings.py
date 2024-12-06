from django.conf import settings

ALUMNI_STATE_NAME = getattr(settings, 'ALUMNI_STATE_NAME', "Alumni")

ALUMNI_TASK_PRIORITY = getattr(settings, 'ALUMNI_TASK_PRIORITY', 7)

ALUMNI_CHARACTERCORPORATION_RATELIMIT = getattr(settings, 'ALUMNI_CHARACTERCORPORATION_RATELIMIT', '10/m')  # 10*10workers = 100/300 per min

ALUMNI_TASK_JITTER = getattr(settings, 'ALUMNI_TASK_PRIORITY', 600)

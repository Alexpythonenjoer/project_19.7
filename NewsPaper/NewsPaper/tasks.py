from celery import shared_task

from celery.schedules import crontab

from NewsPaper.NewsPaper.celery import app

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'action',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (agrs),
    },
}

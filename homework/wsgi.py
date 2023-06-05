"""
WSGI config for homework project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework.settings')

application = get_wsgi_application()

scheduler = BackgroundScheduler()


def clear_session_job():
    print('clear session data base')
    # 命令行执行python manage.py clearsessions,可以清除已经失效的session
    os.system('python manage.py clearsessions')


scheduler.add_job(clear_session_job, trigger='interval', hours=1)

scheduler.start()

"""
WSGI config for axemo_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import time
from threading import Thread
from .automations import luno_automation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axemo_project.settings')

application = get_wsgi_application()

error_retry = 0


def run_luno_auto():
    global error_retry
    while True:
        try:
            luno_automation.luno_sender()
        except Exception as e:
            print(e)
            print('retrying...')
            if error_retry < 3:
                time.sleep(5)
                error_retry += 1
                run_luno_auto()
            else:
                pass
        error_retry = 0
        print('Next round starting in 30 seconds.')
        time.sleep(30)


auto_thread_1 = Thread(target=run_luno_auto)
auto_thread_1.start()



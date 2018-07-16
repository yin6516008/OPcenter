import os
import sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()

from webmoni.models import Event_Type


def init_event_type():
    Event_Type_data = [
        {'id':3,'event_type':'Connection timed out'},
        {'id':4,'event_type':'Error Invalid Redirect'},
        {'id':5,'event_type':'Could not resolve'},
        {'id':7,'event_type':'Failed connect'},
        {'id':99,'event_type':'Unknown error'},
        {'id':100,'event_type':'OK'},
    ]

    for row in Event_Type_data:
        Event_Type.objects.create(**row)
    return True

if __name__ == '__main__':
    init_event_type()


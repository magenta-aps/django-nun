
import datetime
import django
import os
import re
import sys

from django.conf import settings

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
django.setup()
from nurseregister.models import NurseRegistration

INPUT_FILENAME = "autorisationer_per_2018-04-27.txt"

def text_to_state(text):
    if text == "Gyldig":
        return NurseRegistration.STATE_VALID
    raise Exception("Do not know how to handle state text %s" % text)

def parse_date(text):
    parts = text.split("-")
    return datetime.date(
        year=int(parts[2]), month=int(parts[1]), day=int(parts[0])
    )

def import_from_txt(filename):
    with open(filename, 'rb') as f:
        for line in f:
            m = re.match(
                r'^(\D+)\s+([-\d]+)\s+([-\d]+)\s+(.*)\s+([-\d]+)\s*$',
                line.decode("utf8")
            )
            if m is not None:
                item = {
                    "state": text_to_state(m.group(1)),
                    "date": parse_date(m.group(2)),
                    "number": m.group(3),
                    "name": m.group(4),
                    "birthday": parse_date(m.group(5)),
                }
                try:
                    NurseRegistration.objects.get(name=item["name"])
                except NurseRegistration.DoesNotExist:
                    obj = NurseRegistration(**item)
                    obj.save()

if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, INPUT_FILENAME)
    import_from_txt(filename)

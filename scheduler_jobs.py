import sys
from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from pytz import utc
from django.core import management
from django.core.management.commands import loaddata




####time date filter

def Hello():
    print("hello from cron job")
    management.call_command('send_queued_mail')

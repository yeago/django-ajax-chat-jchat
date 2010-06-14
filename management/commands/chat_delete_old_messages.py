'''
Delete old chat messages
'''
from django.core.management.base import BaseCommand, CommandError
from jchat.models import Room, Message
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Deletes old chat messages. Receives an optional integer parameter setting how old a message has to be to be deleted, if no parameter is passed 1 (one) hour is the default value, all messages older than this are deleted.'
    
    def handle(self, *args, **options):
        if len(args) != 1:
            hours = 1
        else:
            try:
                hours = int(args[0])
            except:
                raise CommandError('The parameter "' + args[0] + '" is not a valid amount of hours')
        delta = datetime.now() + timedelta(hours=hours)
        m = Message.objects.filter(timestamp__gt=delta)
        count = m.count()
        m.delete()
        if count:
            print "%d message(s) have been deleted" % count

from __future__ import print_function
import sys
from yaml import load
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'


class Category(object):
    def __init__(self, name, event_substr):
        self.name = name
        self.event_substr = event_substr
        self.counter = 0
        self.total_time = 0
        self.events = []


def analyze_calendar(categories=None, ignore_list=None):
    if not categories:
        categories = []

    if not ignore_list:
        ignore_list = []

    category_map = {c.event_substr: c for c in categories}

    # Track all events not in any categories
    others = Category('Others', None)

    # Track recurring events
    recurring = Category('Recurring Meetings', None)

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    last_week = datetime.utcnow() - timedelta(days=7)

    # 'Z' indicates UTC time
    last_week = last_week.isoformat() + 'Z'
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=last_week,
        timeMax=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
        print('No events found.')
        sys.exit(0)

    category_keys = category_map.keys()

    for event in events:
        skip = False

        # Skip any events in the ignore list
        for i in ignore_list:
            if i in event['summary']:
                skip = True
                break
        if skip:
            continue

        # Ignore all-day events
        d = event['start'].get('date')
        if d and len(d) <= 10:
            continue

        # Get event time in hours
        start_dt = datetime.strptime(event['start']['dateTime'],
                                     DATETIME_FORMAT)
        end_dt = datetime.strptime(event['end']['dateTime'], DATETIME_FORMAT)
        event_time = (end_dt - start_dt).total_seconds() / 60 / 60.0

        # Track recurring events
        if 'recurringEventId' in event:
            recurring.counter += 1
            recurring.total_time += event_time

        for k in category_keys:
            # Track metrics for each event mapped to a category
            if k in event['summary']:
                category_map[k].counter += 1
                category_map[k].total_time += event_time
                break
        else:
            # Everything else goes here
            others.counter += 1
            others.events.append(event)
            others.total_time += event_time

    print('Summary:')
    print(' - {0} recurring meetings took up {1:.1f} hours(s)'.format(
        recurring.counter, recurring.total_time
    ))

    for c in categories:
        print(' - {0}: {1} took up {2:.1f} hour(s)'.format(
            c.name, c.counter, c.total_time
        ))

    print(' - {0} other meetings took up {1:.1f} hours(s):'.format(
        others.counter, others.total_time
    ))
    for o in others.events:
        print('\t- {0}'.format(o['summary']))


if __name__ == '__main__':
    try:
        config = load(open('config.yaml', 'r').read())
    except:
        print('config.yaml is not found or not properly formatted.')
        sys.exit(1)

    categories = [Category(name, k) for k, name in config.items()
                  if k != 'Ignore']
    analyze_calendar(categories, ignore_list=config['Ignore'])

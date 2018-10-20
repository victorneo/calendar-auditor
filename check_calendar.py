from __future__ import print_function
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'


def analyze_calendar():
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
    print('Getting last week\'s events')
    events_result = service.events().list(
        calendarId='primary', timeMin=last_week,
        timeMax=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])

    counters = {
        'x Vix': {'name': '1-1s', 'counter': 0, 'total_time': 0},
        'Flight to': {'name': 'Flight(s)', 'counter': 0, 'total_time': 0},
        'Planning': {'name': 'Quiet Work', 'counter': 0, 'total_time': 0},
        'Interview': {'name': 'Interview(s)', 'counter': 0, 'total_time': 0},
        'SoS': {'name': 'Standup Meetings', 'counter': 0, 'total_time': 0},
        'Others': {
            'name': 'Others',
            'counter': 0,
            'events': [],
            'total_time': 0,
        }
    }

    recurring = {
        'counter': 0,
        'total_time': 0,
    }

    ignore = ['Avail. for Eng Folks Only']

    keys = counters.keys()

    if not events:
        print('No upcoming events found.')

    for event in events:
        if event['summary'] in ignore:
            continue

        d = event['start'].get('date')

        # Ignore all-day events
        if d and len(d) <= 10:
            continue

        # Get event time in minutes
        start_dt = datetime.strptime(event['start']['dateTime'],
                                     DATETIME_FORMAT)
        end_dt = datetime.strptime(event['end']['dateTime'], DATETIME_FORMAT)
        event_time = (end_dt - start_dt).total_seconds() / 60 / 60.0

        # Track recurring events
        if 'recurringEventId' in event.keys():
            recurring['counter'] += 1
            recurring['total_time'] += event_time

        for k in keys:
            if k in event['summary']:
                counters[k]['counter'] += 1
                counters[k]['total_time'] += event_time
                break
        else:
            counters['Others']['counter'] += 1
            counters['Others']['events'].append(event)
            counters['Others']['total_time'] += event_time

    print('Summary:')
    print('{0} recurring meetings took up {1:.1f} hours(s)'.format(
        recurring['counter'], recurring['total_time'])
    )

    for k in keys:
        print('{0}: {1} took up {2:.1f} hour(s)'.format(
            counters[k]['name'], counters[k]['counter'],
            counters[k]['total_time'])
        )

    print('List of other events:')
    for e in counters['Others']['events']:
        print('{0}: {1}'.format(e['start'], e['summary']))


if __name__ == '__main__':
    analyze_calendar()

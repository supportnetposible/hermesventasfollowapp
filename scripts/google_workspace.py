#!/usr/bin/env python3
"""
Google Workspace integration for FollowApp Sales (Tomas)
Uses Service Account with domain-wide delegation (admin@netposible.com)
Impersonates: martin.turra@netposible.com
"""

import json
import sys
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar']
SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.send']
USER_EMAIL = 'admin@netposible.com'
CREDS_FILE = '/root/.hermes/config/google-credentials.json'


def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDS_FILE, scopes=SCOPES_CALENDAR
    ).with_subject(USER_EMAIL)
    return build('calendar', 'v3', credentials=creds)


def get_gmail_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDS_FILE, scopes=SCOPES_GMAIL
    ).with_subject(USER_EMAIL)
    return build('gmail', 'v1', credentials=creds)


# ── CALENDAR ────────────────────────────────────────────────────────────────

def calendar_list(start=None, end=None, max_results=20):
    """List upcoming calendar events."""
    service = get_calendar_service()
    body = {
        'calendarId': 'primary',
        'maxResults': max_results,
        'orderBy': 'startTime',
        'singleEvents': True,
    }
    if start:
        body['timeMin'] = start
    if end:
        body['timeMax'] = end
    events = service.events().list(**body).execute()
    items = events.get('items', [])
    if not items:
        print(json.dumps({'status': 'ok', 'events': [], 'count': 0}))
        return
    result = []
    for e in items:
        result.append({
            'id': e.get('id'),
            'summary': e.get('summary', '(sin título)'),
            'start': e.get('start', {}).get('dateTime', e.get('start', {}).get('date')),
            'end': e.get('end', {}).get('dateTime', e.get('end', {}).get('date')),
            'location': e.get('location'),
            'attendees': [a.get('email') for a in e.get('attendees', []) if a.get('email')],
            'htmlLink': e.get('htmlLink'),
        })
    print(json.dumps({'status': 'ok', 'events': result, 'count': len(result)}))


def calendar_create(summary, start, end, description=None, location=None, attendees=None):
    """Create a calendar event.
    
    Args:
        summary: Event title
        start: ISO 8601 datetime (e.g. 2026-06-10T10:00:00-03:00)
        end: ISO 8601 datetime
        description: Event description text
        location: Location string
        attendees: Comma-separated email list
    """
    service = get_calendar_service()
    body = {
        'summary': summary,
        'start': {'dateTime': start},
        'end': {'dateTime': end},
    }
    if description:
        body['description'] = description
    if location:
        body['location'] = location
    if attendees:
        attendee_list = [{'email': e.strip()} for e in attendees.split(',') if e.strip()]
        if attendee_list:
            body['attendees'] = attendee_list
    event = service.events().insert(calendarId='primary', body=body).execute()
    print(json.dumps({
        'status': 'created',
        'id': event.get('id'),
        'summary': event.get('summary'),
        'htmlLink': event.get('htmlLink'),
    }))


def calendar_delete(event_id):
    """Delete a calendar event by ID."""
    service = get_calendar_service()
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print(json.dumps({'status': 'deleted', 'id': event_id}))


# ── GMAIL ─────────────────────────────────────────────────────────────────

def gmail_send(to, subject, body, cc=None):
    """Send an email.
    
    Args:
        to: Recipient email
        subject: Email subject
        body: Email body text
        cc: Optional CC email(s), comma-separated
    """
    service = get_gmail_service()
    
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import base64

    msg = MIMEMultipart()
    msg['to'] = to
    msg['subject'] = subject
    if cc:
        msg['cc'] = cc
    msg.attach(MIMEText(body, 'plain'))

    encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = service.users().messages().send(
        userId='me',
        body={'raw': encoded}
    ).execute()
    print(json.dumps({'status': 'sent', 'id': sent.get('id'), 'to': to}))


# ── MAIN ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Workspace for FollowApp Sales')
    sub = parser.add_subparsers(dest='cmd')

    # Calendar
    cal_list = sub.add_parser('calendar-list', help='List calendar events')
    cal_list.add_argument('--start', help='ISO start (timeMin)')
    cal_list.add_argument('--end', help='ISO end (timeMax)')
    cal_list.add_argument('--max', type=int, default=20, help='Max results')

    cal_create = sub.add_parser('calendar-create', help='Create calendar event')
    cal_create.add_argument('--summary', required=True, help='Event title')
    cal_create.add_argument('--start', required=True, help='ISO datetime start')
    cal_create.add_argument('--end', required=True, help='ISO datetime end')
    cal_create.add_argument('--description', help='Event description')
    cal_create.add_argument('--location', help='Location')
    cal_create.add_argument('--attendees', help='Comma-separated emails')

    cal_delete = sub.add_parser('calendar-delete', help='Delete calendar event')
    cal_delete.add_argument('--event-id', required=True)

    # Gmail
    mail = sub.add_parser('gmail-send', help='Send email')
    mail.add_argument('--to', required=True, help='Recipient')
    mail.add_argument('--subject', required=True, help='Subject')
    mail.add_argument('--body', required=True, help='Body text')
    mail.add_argument('--cc', help='CC recipients, comma-separated')

    args = parser.parse_args()

    if args.cmd == 'calendar-list':
        calendar_list(args.start, args.end, args.max)
    elif args.cmd == 'calendar-create':
        calendar_create(args.summary, args.start, args.end,
                       args.description, args.location, args.attendees)
    elif args.cmd == 'calendar-delete':
        calendar_delete(args.event_id)
    elif args.cmd == 'gmail-send':
        gmail_send(args.to, args.subject, args.body, args.cc)
    else:
        parser.print_help()

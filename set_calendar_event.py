import datetime
from googleapiclient.discovery import build

SAMPLE_SPREADSHEET_ID = '17-kJlVAcWF7q7hgC1z05kWnK7nipK_OrKkGzVlSZj8c'
SAMPLE_RANGE_NAME = 'Next-Actions!A2:H'

def set_calendar_event(creds):
    # Call the Sheets API
    sheet = build('sheets', 'v4', credentials=creds).spreadsheets()
    
    # Call the Calendar API
    calendar = build('calendar', 'v3', credentials=creds).events()

    # Get data from sheet range
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute().get('values', [])

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = calendar.list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


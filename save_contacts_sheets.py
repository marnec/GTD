from pprint import pprint
from googleapiclient.discovery import build

##################### SPREADSHEETS ###########################################

SAMPLE_SPREADSHEET_ID = '17-kJlVAcWF7q7hgC1z05kWnK7nipK_OrKkGzVlSZj8c'
SAMPLE_RANGE_NAME = 'Validations!F2:F'


def save_contacts_to_sheet(creds):
    # Call the Sheets API
    sheet = build('sheets', 'v4', credentials=creds).spreadsheets()
    
    # Call the People API
    contacts = build('people', 'v1', credentials=creds).people()

    # Get first 2000 voices in connections list
    connections = contacts.connections().list(
        resourceName='people/me',
        pageSize=2000,
        sortOrder="FIRST_NAME_ASCENDING",
        personFields='names,emailAddresses').execute().get('connections', [])

    # Transform GET result in list of strings 
    names = [[p.get("names", [])[0].get("displayName")] for p in connections if p.get("names", [])]

    # Prepare valueRange object for request body
    valuerange = {
        "range": "Validations!F2:F",
        "values": names
    }

    # Clear sheet from old names (eliminates trailing rows if new name list is shorter than old)
    response = sheet.values().clear(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME).execute()

    pprint(response)

    # Update sheet with new names
    response = sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME, 
        valueInputOption="RAW",
        body=valuerange).execute()

    pprint(response)


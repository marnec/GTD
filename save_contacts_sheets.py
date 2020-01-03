from pprint import pprint
from googleapiclient.discovery import build

##################### SPREADSHEETS ###########################################


# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1xrAiKF3AwJtLr2Y1GUeCaZ4AfgkeH8mfg-6WQyTdjco'

SAMPLE_SPREADSHEET_ID = '17-kJlVAcWF7q7hgC1z05kWnK7nipK_OrKkGzVlSZj8c'
SAMPLE_RANGE_NAME = 'Validations!F2:F'

"""Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""


service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()

values = result.get('values', [])
# print(values)


####################### CONTACTS #########################################


"""Shows basic usage of the People API.
Prints the name of the first 10 connections.
"""

service = build('people', 'v1', credentials=creds)

# Call the People API
results = service.people().connections().list(
    resourceName='people/me',
    pageSize=2000,
    sortOrder="FIRST_NAME_ASCENDING",
    personFields='names,emailAddresses').execute()

connections = results.get('connections', [])

for person in connections:
    names = person.get('names', [])
    if names:
        name = names[0].get('displayName')
        print(name)

names = [[p.get("names", [])[0].get("displayName")] for p in connections if p.get("names", [])]

print(names)
valuerange = {
    "range": "Validations!F2:F",
    "values": names
}
request = sheet.values().update(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    range=SAMPLE_RANGE_NAME, 
    valueInputOption="RAW",
    body=valuerange)

response = request.execute()
pprint(response)
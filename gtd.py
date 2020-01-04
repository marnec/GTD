from authenticate import authenticate
from save_contacts_sheets import save_contacts_to_sheet

creds = authenticate()
save_contacts_to_sheet(creds)

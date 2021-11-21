import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_last_entry_spreadsheet_symptoms():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('roche-hakaton-credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Simptomi')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    return records_data
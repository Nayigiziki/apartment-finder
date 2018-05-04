import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google_maps
import time

try:
    from private import *
except Exception:
    pass

GOOGLE_API_KEY_FILE = 'client_secret.json'

def open_sheet():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API_KEY_FILE, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(GOOGLE_SHEET_ID).worksheet('Scraped_Data')

def add_new_record(sheet, record_to_add):
    num_rows = sheet.row_count
    new_row = num_rows + 1
    row = [
            record_to_add['name'],
            record_to_add['link'],
            record_to_add['created'],
            record_to_add['lat'],
            record_to_add['lon'],
            record_to_add['price'],
            record_to_add['location'],
            record_to_add['tagged_location'],
            record_to_add['bedrooms'],
            record_to_add['bathrooms'],
            record_to_add['sq_ft'],
            record_to_add['amenities'],
            record_to_add['available_date'],
            # record_to_add['google_stop'],
            # record_to_add['google_dist'],
            # record_to_add['fb_stop'],
            # record_to_add['fb_dist'],
            record_to_add['should_include'],
            record_to_add['address'],
            record_to_add['adi_drivetime'],
            # record_to_add['google_walktime'],
            # record_to_add['fb_walktime']
            ]
    try:
        sheet.insert_row(row, new_row)
    except Exception as e:
        print e
        # try again just in case - sometimes Google tells you to wait 30 seconds and retry
        time.sleep(30)
        sheet.insert_row(row, new_row)
        #if we fail again, let it fail

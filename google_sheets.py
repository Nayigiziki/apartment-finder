import gspread
from oauth2client.service_account import ServiceAccountCredentials
GOOGLE_API_KEY_FILE = 'client_secret.json'
try:
    from private import *
except Exception:
    pass

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API_KEY_FILE, scope)
gc = gspread.authorize(credentials)

def open_sheet():
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
            record_to_add['google_stop'],
            record_to_add['google_dist'],
            record_to_add['fb_stop'],
            record_to_add['fb_dist'],
            record_to_add['should_include'],
            ]
    try:
        sheet.insert_row(row, new_row)
        sheet.update_cell(new_row, 19, '=hyperlink("https://www.google.com/maps/place/"&geoCodeLatLong(D%d,E%d), geoCodeLatLong(D%d,E%d))'%(new_row, new_row, new_row, new_row))
        sheet.update_cell(new_row, 20, '=importxml("http://maps.googleapis.com/maps/api/directions/xml?origin=" &D%d&","&E%d  & "&destination=555 California St, San Francisco, CA 94104&sensor=false&alternatives=false&departure_time=1493827772&mode=driving","//leg/duration/text")'%(new_row, new_row))
        sheet.update_cell(new_row, 21, '=importxml("http://maps.googleapis.com/maps/api/directions/xml?origin="&D%d&","&E%d&"&destination="&index(Shuttlses!$H$2:$H$30, match($N%d,Shuttlses!$G$2:$G$30, 0))&"&sensor=false&alternatives=false&departure_time=1493827772&mode=walking","//leg/duration/text")'%(new_row, new_row, new_row))
        sheet.update_cell(new_row, 22, '=importxml("http://maps.googleapis.com/maps/api/directions/xml?origin="&$D%d&","&$E%d&"&destination="&index(Shuttlses!$D$2:$D$18, match($P%d,Shuttlses!$C$2:$C$18, 0))&"&sensor=false&alternatives=false&departure_time=1493827772&mode=walking","//leg/duration/text")'%(new_row, new_row, new_row))
    except:
        try:
            sheet.insert_row(row, new_row)
            sheet.update_cell(new_row, 19, '=hyperlink("https://www.google.com/maps/place/"&geoCodeLatLong(D%d,E%d), geoCodeLatLong(D%d,E%d))'%(new_row, new_row, new_row, new_row))
            sheet.update_cell(new_row, 20, '=importxml("http://maps.googleapis.com/maps/api/directions/xml?origin=" &D%d&","&E%d  & "&destination=555 California St, San Francisco, CA 94104&sensor=false&alternatives=false&departure_time=1493827772&mode=driving","//leg/duration/text")'%(new_row, new_row))
            sheet.update_cell(new_row, 21, '=importxml("http://maps.googleapis.com/maps/api/directions/xml?origin="&D%d&","&E%d&"&destination="&index(Shuttlses!$H$2:$H$30, match($N%d,Shuttlses!$G$2:$G$30, 0))&"&sensor=false&alternatives=false&departure_time=1493827772&mode=walking","//leg/duration/text")'%(new_row, new_row, new_row))
            sheet.update_cell(new_row, 22, '=importxml("http://maps.googleapis.com/maps/api/directions/xml?origin="&$D%d&","&$E%d&"&destination="&index(Shuttlses!$D$2:$D$18, match($P%d,Shuttlses!$C$2:$C$18, 0))&"&sensor=false&alternatives=false&departure_time=1493827772&mode=walking","//leg/duration/text")'%(new_row, new_row, new_row))
        except:
            print 'error'

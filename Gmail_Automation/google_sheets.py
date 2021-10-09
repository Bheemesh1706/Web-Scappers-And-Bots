from datetime import date
import os.path
from re import S
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
import requests

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
URL = ''

def api_authentication():
   
    creds = None

    if os.path.exists('token_sheets.json'):
        creds = Credentials.from_authorized_user_file('token_sheets.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
      
        with open('token_sheets.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    return service

def Check_Sheet(service,name):
    try:
            file = open('sheetId.txt','r')
            count = 0

            for line in file:
                mySpreadsheets = service.spreadsheets().get(spreadsheetId=line.strip()).execute()
                if name == mySpreadsheets['properties']['title']:
                    count+=1

            file.close()

            return count

    except Exception as error:
        print(error)


def Send_Number(number, _name):
    try: 
        data = {
            'phone': number,
            'name': _name
        }
        response = requests.post(url = URL, data = data)
        print(response.text)
            
    except Exception as error:
        print(error)



def Create_Sheet(service,name):

    """ 
    dict_keys(['spreadsheetId','properties','sheets','spreadsheetUrl'])
    """

    """
    sheet property object to add values to th sheet like timezone,name
    Char set etc.
    """
    try:
            sheet_property ={
                'properties':{
                    'title': name,
                    'locale': 'en_US',
                }
            }

            if not Check_Sheet(service,name):
                    sheet=[]
                    sheet = service.spreadsheets().create(body=sheet_property).execute()

                    file = open('sheetId.txt','a')
                    file.write('\r\n')
                    file.write(sheet['spreadsheetId'])
                    file.close()

                    CELL_REFERENCE_POINT = 'A1'
                    
                    values = (
                    ('Date & Time', 'Sender', 'Page Name','URL','Varient',
                    'your_name','email','phone_number','ad_name','adset_name','campaign_name'),   
                )
                    VALUE_RANGE_BODY = {
                        'majorDimension': 'ROWS',
                        'values': values
                    }

                    service.spreadsheets().values().update(
                        spreadsheetId=sheet['spreadsheetId'],
                        valueInputOption='USER_ENTERED',
                        range= CELL_REFERENCE_POINT,
                        body=VALUE_RANGE_BODY
                    ).execute()
                    return sheet
            else:
                file = open('sheetId.txt','r')
                for line in file:
                    mySpreadsheets = service.spreadsheets().get(spreadsheetId=line.strip()).execute()
                    if name == mySpreadsheets['properties']['title']:
                        sheet= mySpreadsheets
            
                file.close()
                return sheet

    except errors.HttpError as error:
        print(error)
        

 
    
def Write_Data(service,sheet,data):

    try:
            CELL_REFERENCE_POINT = 'A1'
            
            values = (
            (data['Date'], data['Sender'],data['Page Name'],data['URL'],data['Varient'],data['your_name'],data['email'],
            data['phone_number'],data['ad_name'],data['adset_name'],data['campaign_name']),
            
        )
            VALUE_RANGE_BODY = {
                'majorDimension': 'ROWS',
                'values': values
            }

            service.spreadsheets().values().append(
                spreadsheetId=sheet['spreadsheetId'],
                valueInputOption='USER_ENTERED',
                range= CELL_REFERENCE_POINT,
                body=VALUE_RANGE_BODY
            ).execute()

            if len(data['phone_number']) > 10 :
                Send_Number(data['phone_number'], data['your_name'])

    except errors.HttpError as error:
        print(error)



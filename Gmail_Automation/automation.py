import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import email
import base64
from googleapiclient import errors
from google_sheets import api_authentication , Create_Sheet, Write_Data
import re
import sys
import getopt
import time



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def parse_message(message_string):
    
    DATE = ''
    SENDER= ''
    SUBJECT= ''
    PG=''
    URL=''
    VARIENT=''
    NAME=''
    EMAIL=''
    NUMBER=''
    AD=''
    ADSET=''
    CAMPAIGN=''

    splitted_message = message_string.split('Forwarded message')
    required_message=splitted_message.pop()
    parsed=required_message.split('\r\n')

    key_phrase =['Date:','From:','Subject:','Page Name','URL','Variant','your_name','email','phone_number','ad_name','adset_name','campaign_name']

    for x in parsed:
        if re.search(key_phrase[0],x):
            DATE= x.replace(key_phrase[0],"")
            DATE= DATE.replace(':',"")
            DATE= DATE.replace('=',"")
        elif re.search(key_phrase[1],x):
            SENDER= x.replace(key_phrase[1],"")
            SENDER= SENDER.replace(':',"")
            SENDER= SENDER.replace('=',"")
        elif re.search(key_phrase[2],x):
            SUBJECT= x.replace(key_phrase[2],"")
            SUBJECT= SUBJECT.replace(':',"")
            SUBJECT= SUBJECT.replace('=',"")
        elif re.search(key_phrase[3],x):
            PG= x.replace(key_phrase[3],"")
            PG= PG.replace(':',"")
            PG= PG.replace('=',"")
        elif re.search(key_phrase[4],x):
            URL= x.replace(key_phrase[4],"")
            URL= URL.replace(':',"")
            URL= URL.replace('=',"")
        elif re.search(key_phrase[5],x):
            VARIENT= x.replace(key_phrase[5],"")
            VARIENT= VARIENT.replace(':',"")
            VARIENT= VARIENT.replace('=',"")
        elif re.search(key_phrase[6],x):
            NAME= x.replace(key_phrase[6],"")
            NAME= NAME.replace(':',"")
            NAME= NAME.replace('=',"")
        elif re.search(key_phrase[7],x):
            EMAIL= x.replace(key_phrase[7],"")
            EMAIL= EMAIL.replace(':',"")
            EMAIL= EMAIL.replace('=',"")
        elif re.search(key_phrase[8],x):
            NUMBER= x.replace(key_phrase[8],"")
            NUMBER= NUMBER.replace(':',"")
            NUMBER= NUMBER.replace('=',"")
        elif re.search(key_phrase[9],x):
            AD= x.replace(key_phrase[9],"")
            AD= AD.replace(':',"")
            AD= AD.replace('=',"")
        elif re.search(key_phrase[10],x):
            ADSET= x.replace(key_phrase[10],"")
            ADSET= ADSET.replace(':',"")
            ADSET= ADSET.replace('=',"")
        elif re.search(key_phrase[11],x):
            CAMPAIGN= x.replace(key_phrase[11],"")
            CAMPAIGN= CAMPAIGN.replace(':',"")
            CAMPAIGN= CAMPAIGN.replace('=',"")
            
    message_object = {
        'Date': DATE,
        'Sender': SENDER,
        'Subject': SUBJECT,
        'Page Name': PG,
        'URL': URL,
        'Varient': VARIENT,
        'your_name': NAME,
        'email': EMAIL,
        'phone_number': NUMBER,
        'ad_name': AD,
        'adset_name': ADSET,
        'campaign_name': CAMPAIGN,
    }

    return message_object

def get_message(service, user_id,msg_id):

    try:
        message_list = service.users().messages().get(userId=user_id,id = msg_id,format="raw").execute()
        message_raw = base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))
        message_string = email.message_from_bytes(message_raw)

        if  message_string.get_content_maintype() == 'multipart':
            plain,html = message_string.get_payload()

            return plain.get_payload()
            
        else:
            return message_string.get_payload()

    except errors.HttpError as error:
        print(error)  



def search_messages(service,user_id, search_query):
    
    try:
        search_id = service.users().messages().list(userId=user_id,q=search_query).execute()
        total_results= search_id['resultSizeEstimate']
        id_list = []
        if total_results > 0 :
            message_ids = search_id['messages']
            for ids in message_ids:
                id_list.append(ids['id'])

            return id_list
        else :
            print('There were Zero Results for that query')
            return ""
    
    except errors.HttpError as error:
        print(error)

def authenticate_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_gmail.json'):
        creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_gmail.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service

def main():
    print('main')
    argv = sys.argv[1:]
    sheet_name= None

    try:
        opts, args = getopt.getopt(argv, "hn:")
    except Exception as e:
        print(e)
    
    if len(argv)>0:
        for opt, arg in opts:
            if opt in ['-n']:
                sheet_name = arg
                print(sheet_name)
            elif opt in ['-h']:
                print("python3 automation.py -n \"sheet_name\" ")
                sys.exit()
    else:
        print("python3 automation.py -n \"sheet_name\" ")
        sys.exit()

    #Authenticating Api Services
    gmail_service = authenticate_service()
    sheet_service = api_authentication()

    #Creates and Initializes the spreadsheet with column names
    sheet = Create_Sheet(sheet_service,sheet_name)

    while(True):
        total_rows = len(sheet_service.spreadsheets().values().get(
            spreadsheetId=sheet['spreadsheetId'],
            majorDimension='ROWS',
            range='A1:L').execute().get('values',[]))-1

        message_list = search_messages(gmail_service,'me','')

        if len(message_list) > total_rows :
            current_list= []
            for x in range(total_rows,len(message_list)):
                current = message_list.pop()
                current_list.append(current)

            for x in current_list:
                message = get_message(gmail_service,'me',x)
                message_object = parse_message(message)
                Write_Data(sheet_service,sheet,message_object)

            print(sheet['spreadsheetUrl'])
            print(sheet['spreadsheetId'])
            
        time.sleep(600)



    


if __name__ == '__main__':
    main()


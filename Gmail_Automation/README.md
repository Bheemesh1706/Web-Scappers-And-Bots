# **Gmail-Automation**

## GCP Setup :
   - First Create a [GCP account.](https://cloud.google.com/free/?utm_source=google&utm_medium=cpc&utm_campaign=japac-IN-all-en-dr-bkws-all-all-trial-e-dr-1009882&utm_content=text-ad-none-none-DEV_c-CRE_514666343194-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt%20~%20GCP%20~%20General_%20Core%20Brand-KWID_43700060584985724-kwd-26415313501-userloc_1007809&utm_term=KW_google%20cloud%20platform-ST_google%20cloud%20platform&gclsrc=ds&gclsrc=ds)
   - Activate account by [setting up the billing details](https://youtu.be/uINleRduCWM)
   - Create Api Keys for Google Sheets and Gmail.
   - Setup the OAuth and download the credentials_secrete.json file.
   - Rename the credentials_secrete.json as `credentials.json`.
   
## Developement Setup :
   - Run the [quickstart_gmail.py](Gmail-Automation/quickstart_gmail.py) as `python3 quickstart_gmail.py)`.
   - Run the [quickstart_sheets.py](Gmail-Automation/quickstart_sheets.py) as `python3 quickstart_sheets.py)`.
 

## Core Functions :

   ### There are 7 Core Functions which are divided into two files. The first one is [automation.py](Gmail-Automation/automation.py) and the second one is [google_sheets.py](Gmail-Automation/google_sheets.py)
   
   #### Functions in  [google_sheets.py](Gmail-Automation/google_sheets.py) 
   - `api_authentication()` It is a function to create service object for google sheets.
   - `Create_Sheet(service,name)` It creates an spreadsheet object by taking the service object and name of the sheet as parameters. It checks for the given sheet name if it exists it opens the existing file or else creates a new one. 
   - `Write_Data(service,sheet,data)` It writes data to the spreadsheet by taking the service object , spreadsheet object and data as parameters.
   
   #### Functions in  [automation.py](Gmail-Automation/automation.py)
   - `authenticate_service()` It is a function to create service object for gmail.
   - `search_messages(service,user_id,search_query)` It finds the emails from the gmail client and returns the message ID's as a list by taking gmail service object, user Id and search query as parameters.
   - `get_message(service,user_id,msg_id)` This functions gets the data from each message by taking in gmail service object, user Id and message Id as parameters.
   - `parse_message(message_string)` is used to clean the data from the message and restructure it as a proper key value pair based object for writting into the sheets.
   
   #### Usage
   `python3 automation.py -n [Name of the sheet]` For creating the new sheet
   
   `python3 automation.py -h` For help
   
        
        

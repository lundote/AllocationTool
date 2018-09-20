import csv
import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, date

class GoogleAPI:
    # argparse only relevant for command line - throws error in jupyter
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # If modifying these scopes, delete your previous saved credentials at
    # ~/.credentials/sheets.googleapis.com-python-gAPItest.json
    scopes = 'https://www.googleapis.com/auth/spreadsheets'
    #uses Oauth ID rather than service account
    client_secret_file = '/PATH/TO/CREDENTIALS'
    application_Name = 'Allocations'

    def get_credentials(self):
        """get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid, 
        the Oauth2 flow is completed to obtain new credentials

        Returns:
            Credentials, the obtained credentials.
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 
            'sheets.googleapis.com-python-gAPItest.json')#change for each project for different credentials


        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = self.application_Name
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:
                tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def import_data(self, PATH):
        print("Interacting w/ Google Sheets API")
        # Populates Google Sheets. Dependent on Pandas
        credentials = GoogleAPI().get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?', 
            'version=v4')
        service = discovery.build('sheets', 'v4', http=http)
        spreadsheetID = 'TAKE_FROM_URL' #taken from url; change for each project

        # Read csv files to be imported
        fgohFile = open(PATH + 'fgohGS.csv')
        fgohReader = csv.reader(fgohFile)
        fgohData = list(fgohReader)
        ordersFile = open(PATH + 'ordersGS.csv')
        ordersReader = csv.reader(ordersFile)
        ordersData = list(ordersReader)

        # Populate Google Sheets with csv data
        # Orders - sheet is named Invoices/SaiesOrders
        orderBody = {u'range': u'Invoices/SalesOrders!A1:H1500', 
                     u'values': ordersData, u'majorDimension': u'ROWS'}
        # clear sheet first to ensure no extra rows from last import
        result = service.spreadsheets().values().clear(spreadsheetId=spreadsheetID, 
                                                       range=orderBody['range'], 
                                                       body={}).execute()
        # import csv data to Google Sheet - Orders
        result = service.spreadsheets().values().update(spreadsheetId=spreadsheetID, 
                                                        range=orderBody['range'],
                                                        valueInputOption='USER_ENTERED', 
                                                        body=orderBody).execute()
        # FGOH - sheet is named FGOH
        fgohBody = {u'range': u'FGOH!A1:F1500', u'values': fgohData, 
                    u'majorDimension': u'ROWS'}
        # clear sheet first to ensure no extra rows from last import
        result = service.spreadsheets().values().clear(spreadsheetId=spreadsheetID, 
                                                       range=fgohBody['range'],
                                                       body={}).execute()
        # import csv data to Google Sheet - FGOH
        result = service.spreadsheets().values().update(spreadsheetId=spreadsheetID, 
                                                        range=fgohBody['range'],
                                                        valueInputOption='USER_ENTERED', 
                                                        body=fgohBody).execute()
        # # Insert last updated date
        today = [[str(datetime.today())]] #must be a list of lists
        updatedBody = {u'range': u'Dashboard!R1', u'values': today, 
                       u'majorDimension': u'ROWS'}
        # clear last updated cell
        result = service.spreadsheets().values().clear(spreadsheetId=spreadsheetID, 
                                                       range=updatedBody['range'],
                                                       body = {}).execute()
        # insert today's date
        result = service.spreadsheets().values().update(spreadsheetId=spreadsheetID, 
                                                        range=updatedBody['range'],
                                                        valueInputOption='USER_ENTERED', 
                                                        body=updatedBody).execute()
        return





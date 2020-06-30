import gspread 
from google.colab import auth
from oauth2client.client import GoogleCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pandas as pd

def getSpreadsheetAuth(): 
  auth.authenticate_user()
  spreadsheetAuth=gspread.authorize(GoogleCredentials.get_application_default())
  return spreadsheetAuth

def getCashFlowFrame(spreadsheetAuth,sheet_url,sheet_name):
  sheet=spreadsheetAuth.open_by_url(sheet_url)
  frame=get_as_dataframe(sheet.worksheet(sheet_name))
  frame=frame.dropna(how='all')
  frame=frame.dropna(axis='columns',how='all')
  frame['date'] = pd.to_datetime(frame['date'], format='%Y-%m-%d')
  return frame
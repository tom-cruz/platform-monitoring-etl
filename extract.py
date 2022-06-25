import os
from datetime import date
from dateutil.relativedelta import relativedelta
from simple_salesforce import Salesforce
import pandas as pd

#Datetime Filter Parameters
timeWindow_months = 6
today = date.today()
sixMonthsAgo_date = today - relativedelta(months=timeWindow_months)
date_format = '%Y-%m-%dT%H:%M:%S.000+0000'

#Queries
user_query = "SELECT Id, FederationIdentifier, name, username, GBS_User__c, IGF_User__c, USG_Federal_User__c, \
                    UK_Sensitive_Data__c, IsDachUser__c, isManager__c, IsActive, Non_Sales_Relationship__c, UserType FROM User"

loginHistory_query = "SELECT Id, UserId, LoginTime, LoginType, SourceIp, LoginUrl, NetworkId, AuthenticationServiceId, \
                        LoginGeoId, TlsProtocol, CipherSuite, OptionsIsGet, OptionsIsPost, Browser, Platform, Status, \
                        Application, ClientVersion, ApiType, ApiVersion, CountryIso, AuthMethodReference FROM LoginHistory \
                        WHERE LoginTime >= " + sixMonthsAgo_date.strftime(date_format)

# Settings
base_path = os.path.abspath(__file__ + "/../../")

# Source path where we want to save the data pulled from the Salesforce API
data_path = f"{base_path}/data/"


def create_folder_if_not_exists(path):
    """
    Create a new folder if it doesn't exists
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def api_get_data(objectName, query):
    """
    Call Salesforce API to query data from IBM Sales Cloud (ISC)
    """

    # Create destination folder
    create_folder_if_not_exists(data_path)
    
    # Instantiate login session with ISC
    sf = Salesforce(username='tom.cruz@ibm-isc.com.int',
                    password='',
                    security_token='',
                    domain='test')

    # Query data
    sf_data = sf.query_all(query)

    # Read data into pandas DataFrame and drop attributes metadata
    sf_df = pd.DataFrame(sf_data['records']).drop(['attributes'],axis=1)

    # Store data into csv in file dir
    sf_df.to_csv(data_path + objectName + '_' + today.strftime('%Y-%m-%d') + '.csv', index=False)

def main():
    print("[Extract] Start")
    
    print("[Extract] Downloading Login History")
    api_get_data("loginHistory",loginHistory_query)
    
    print("[Extract] Downloading Users")
    api_get_data("user",user_query)
    
    print(f"[Extract] End")
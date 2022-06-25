import os
import csv
from datetime import datetime

from common.tables import StgLoginHistory, StgUser
from common.base import session
from sqlalchemy import text

# Datetime file path
today = datetime.today()

# Settings
base_path = os.path.abspath(__file__ + "/../../")

# Source path where we want to extract the downloaded data from ISC
data_path = f"{base_path}/data/"

# File names to add to path
loginHistory_filename = 'loginHistory_' + today.strftime('%Y-%m-%d') + '.csv'
auditTrail_filename = 'auditTrail_' + today.strftime('%Y-%m-%d') + '.csv'
user_filename = 'user_' + today.strftime('%Y-%m-%d') + '.csv'


def convert_to_datetime(field):
    """
    Convert data type to datetime to apply to DataFrame column
    """
    date_format = '%Y-%m-%dT%H:%M:%S.000+0000'
    current_format = datetime.strptime(field, date_format)
    new_format = current_format.strftime(date_format)

    return new_format


def convert_to_bool(field):
    """
    Convert data type to boolean to apply to DataFrame column
    """
    field = bool([1 if x == 'true' else 0 for x in field])

    return field


def truncate_table(tablename):
    """
    Ensure that 'staging' table is always in empty state before running any transformations.
    """
    session.execute(
        text("TRUNCATE TABLE " + tablename + ";")
    )
    session.commit()


## CONSIDER transforming within dataframe as opposed to csv file
def transform_new_login_history_data(table,objectFilename):
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    with open(data_path + objectFilename, mode="r", encoding="windows-1252") as csv_file:
        # Read the new .csv snapshot ready to be processed
        reader = csv.DictReader(csv_file)
        # Initialize an empty list for objects
        table_objects = []
        for row in reader:
            # Apply transformations and save as object
            table_objects.append(
                table(
                    Id = row["Id"],
                    UserId = row["UserId"],
                    LoginTime = convert_to_datetime(row["LoginTime"]),
                    LoginType = row["LoginType"],
                    SourceIp = row["SourceIp"],
                    LoginUrl = row["LoginUrl"],
                    NetworkId = row["NetworkId"],
                    AuthenticationServiceId = row["AuthenticationServiceId"],
                    LoginGeoId = row["LoginGeoId"],
                    TlsProtocol = row["TlsProtocol"],
                    CipherSuite = row["CipherSuite"],
                    OptionsIsGet = convert_to_bool(row["OptionsIsGet"]),
                    OptionsIsPost = convert_to_bool(row["OptionsIsPost"]),
                    Browser = row["Browser"],
                    Platform = row["Platform"],
                    Status = row["Status"],
                    Application = row["Application"],
                    ClientVersion = row["ClientVersion"],
                    ApiType = row["ApiType"],
                    ApiVersion = row["ApiVersion"],
                    CountryIso = row["CountryIso"],
                    AuthMethodReference = row["AuthMethodReference"]
                )
            )
        # Bulk save all new processed objects and commit
        session.bulk_save_objects(table_objects)
        session.commit()


## CONSIDER transforming within dataframe as opposed to csv file
def transform_new_user_data(table,objectFilename):
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    with open(data_path + objectFilename, mode="r", encoding="cp850") as csv_file:
        # Read the new .csv snapshot ready to be processed
        reader = csv.DictReader(csv_file)
        # Initialize an empty list for objects
        table_objects = []
        for row in reader:
            # Apply transformations and save as object
            table_objects.append(
                table(
                    Id = row["Id"],
                    FederationIdentifier = row["FederationIdentifier"],
                    Name = row["Name"],
                    Username = row["Username"],
                    GBS_User__c = convert_to_bool(row["GBS_User__c"]),
                    IGF_User__c = convert_to_bool(row["IGF_User__c"]),
                    USG_Federal_User__c = convert_to_bool(row["USG_Federal_User__c"]),
                    UK_Sensitive_Data__c = convert_to_bool(row["UK_Sensitive_Data__c"]),
                    IsDachUser__c = convert_to_bool(row["IsDachUser__c"]),
                    isManager__c = convert_to_bool(row["isManager__c"]),
                    IsActive = convert_to_bool(row["IsActive"]),
                    Non_Sales_Relationship__c = row["Non_Sales_Relationship__c"],
                    UserType = row["UserType"]
                )
            )
        # Bulk save all new processed objects and commit
        session.bulk_save_objects(table_objects)
        session.commit()


def main():
    print("[Transform] Start")
    # User
    print("[Transform: User] Remove any old data from table")
    truncate_table('staging.tmp_user')
    print("[Transform: User] Transform new data in table")
    transform_new_user_data(StgUser,user_filename)
    
    # Login History
    print("[Transform: Login History] Remove any old data from table")
    truncate_table('staging.tmp_login_history')
    print("[Transform: Login History] Transform new data in table")
    transform_new_login_history_data(StgLoginHistory,loginHistory_filename)
    
    print("[Transform] End")
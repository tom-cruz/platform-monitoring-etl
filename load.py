from common.base import session
from common.tables import StgLoginHistory, PrdLoginHistory, StgUser, PrdUser

from sqlalchemy import cast, DateTime, Boolean
from sqlalchemy.dialects.postgresql import insert


def insert_user_transactions(table_stg, table_prd):
    """
    Insert operation: add new data
    """
    # Retrieve all the transaction ids from the clean table
    clean_transaction_ids = session.query(table_prd.transaction_id)

    # date_of_sale and price needs to be casted as their
    # datatype is not string but, respectively, Date and Integer
    transactions_to_insert = session.query(
        table_stg.Id,
        table_stg.FederationIdentifier,
        table_stg.Name,
        table_stg.Username,
        cast(table_stg.GBS_User__c, Boolean),
        cast(table_stg.IGF_User__c, Boolean),
        cast(table_stg.USG_Federal_User__c, Boolean),
        cast(table_stg.UK_Sensitive_Data__c, Boolean),
        cast(table_stg.IsDachUser__c, Boolean),
        cast(table_stg.isManager__c, Boolean),
        cast(table_stg.IsActive, Boolean),
        table_stg.Non_Sales_Relationship__c,
        table_stg.UserType
    ).filter(~table_stg.transaction_id.in_(clean_transaction_ids))
	
    # Print total number of transactions to insert
    print("Transactions to insert:", transactions_to_insert.count())
    
    # Insert the rows from the previously selected transactions
    stm = insert(table_prd).from_select(
        ["Id","FederationIdentifier","Name","Username","GBS_User__c","IGF_User__c","USG_Federal_User__c","UK_Sensitive_Data__c",\
        "IsDachUser__c","isManager__c","IsActive","Non_Sales_Relationship__c","UserType"],
        transactions_to_insert,
    )

    # Execute and commit the statement to make changes in the database.
    session.execute(stm)
    session.commit()


def insert_login_history_transactions(table_stg, table_prd):
    """
    Insert operation: add new data
    """
    # Retrieve all the transaction ids from the clean table
    clean_transaction_ids = session.query(table_prd.transaction_id)

    # date_of_sale and price needs to be casted as their
    # datatype is not string but, respectively, Date and Integer
    transactions_to_insert = session.query(
        table_stg.Id,
        table_stg.UserId,
        cast(table_stg.LoginTime, DateTime),
        table_stg.LoginType,
        table_stg.SourceIp,
        table_stg.LoginUrl,
        table_stg.NetworkId,
        table_stg.AuthenticationServiceId,
        table_stg.LoginGeoId,
        table_stg.TlsProtocol,
        table_stg.CipherSuite,
        cast(table_stg.OptionsIsGet, Boolean),
        cast(table_stg.OptionsIsPost,Boolean),
        table_stg.Browser,
        table_stg.Platform,
        table_stg.Status,
        table_stg.Application,
        table_stg.ClientVersion,
        table_stg.ApiType,
        table_stg.ApiVersion,
        table_stg.CountryIso,
        table_stg.AuthMethodReference
    ).filter(~table_stg.transaction_id.in_(clean_transaction_ids))
	
    # Print total number of transactions to insert
    print("Transactions to insert:", transactions_to_insert.count())
    
    # Insert the rows from the previously selected transactions
    stm = insert(table_prd).from_select(
        ["Id","UserId","LoginTime","LoginType","SourceIp","LoginUrl","NetworkId","AuthenticationServiceId",\
        "LoginGeoId","TlsProtocol","CipherSuite","OptionsIsGet","OptionsIsPost","Browser","Platform","Status", \
        "Application","ClientVersion","ApiType","ApiVersion","CountryIso","AuthMethodReference"],
        transactions_to_insert,
    )

    # Execute and commit the statement to make changes in the database.
    session.execute(stm)
    session.commit()


def delete_transactions(table_stg, table_prd):
    """
    Delete operation: delete any row not present in the last snapshot
    """
    # Get all ppr_raw_all transaction ids
    raw_transaction_ids = session.query(table_stg.transaction_id)

    # Filter all the prod table transactions that are not present in the staging table
    # and delete them.
    # Passing synchronize_session as argument for the delete method.
    transactions_to_delete = session.query(table_prd).filter(
        ~table_prd.transaction_id.in_(raw_transaction_ids)
    )
    
    # Print transactions to delete
    print("Transactions to delete:", transactions_to_delete.count())

    # Delete transactions
    transactions_to_delete.delete(synchronize_session=False)

    # Commit the session to make the changes in the database
    session.commit()


def main():
    print("[Load] Start")
    # User
    print("[Load: User] Inserting new rows")
    insert_user_transactions(StgUser, PrdUser)
    print("[Load: User] Deleting rows not available in the new transformed data")
    delete_transactions(StgUser, PrdUser)
    
    # Login History
    print("[Load: Login History] Inserting new rows")
    insert_login_history_transactions(StgLoginHistory, PrdLoginHistory)
    print("[Load: Login History] Deleting rows not available in the new transformed data")
    delete_transactions(StgLoginHistory, PrdLoginHistory)
    
    print("[Load] End")
# Platform Monitoring Dashboard

## Initiative
As a team that supports the integrity and stability of the ISC platform, we want to take a proactive approach in ensuring that ISC is operating in a secure and compliant fashion so that our users can effectively utilize the tool and deliver on IBM's strategic goals and initiatives.

## Description of Code

ETL pipeline for enabling Tableau CRM dashboards monitoring IBM Sales Cloud login activity, permission set assignments, and user activations

|**File Name**|**Description**|
|------|-----|
|base.py|Defines the credentials for the PostgreSQL database endpoint and creates a session for declaring operations on the tables|
|tables.py|Defines the schema for the tables in the PostgreSQL database, storing the data in the staging and production environments| 
|create_tables.py |Calls the *tables.py* file to create the defined schemas and tables|
|extract.py|Calls the Salesforce API, passing in the queries for the users and login history data|
|transform.py|Truncates tables of old data, stores data in staging schema, and makes data type conversions to the new extracted data|
|load.py|Loads transformed data into production schema|
|execute.py|Executes the ETL pipeline, calling the extract, transform, and load scripts|

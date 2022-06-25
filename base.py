from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

username = 'ibm_cloud_5d9d04e0_2e90_4a83_ad34_1d306e745505'
password = '990862829c69127cc7cb40586bbc76225c058996f005c02d78ff347845a47222'
host = 'be876916-7e43-4950-b2af-0cbe0ab35867.c7e0lq3d0hm8lbg600bg.databases.appdomain.cloud'
port = '31230'
database_name = 'ibmclouddb'

engine = create_engine("postgresql://" + username + ':' + password + '@' + host + ':' + port + '/' + database_name)
session = Session(engine)
Base = declarative_base()
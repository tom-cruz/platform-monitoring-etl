from sqlalchemy import Column, String, Boolean, DateTime
from common.base import Base
from sqlalchemy.orm import column_property


class StgLoginHistory(Base):
    __tablename__ = 'tmp_login_history'
    __table_args__ = {'schema': 'staging'}

    Id = Column(String(18), primary_key=True)
    UserId = Column(String(18))
    LoginTime = Column(String(19))
    LoginType = Column(String)
    SourceIp = Column(String(15))
    LoginUrl = Column(String)
    NetworkId = Column(String)
    AuthenticationServiceId = Column(String)
    LoginGeoId = Column(String)
    TlsProtocol = Column(String)
    CipherSuite = Column(String)
    OptionsIsGet = Column(Boolean)
    OptionsIsPost = Column(Boolean)
    Browser = Column(String)
    Platform = Column(String)
    Status = Column(String)
    Application = Column(String)
    ClientVersion = Column(String)
    ApiType = Column(String)
    ApiVersion = Column(String)
    CountryIso = Column(String(2))
    AuthMethodReference = Column(String)
    transaction_id = column_property(Id)


class PrdLoginHistory(Base):
    __tablename__ = 'login_history'
    __table_args__ = {'schema': 'public'}

    Id = Column(String(18), primary_key=True)
    UserId = Column(String(18))
    LoginTime = Column(DateTime)
    LoginType = Column(String)
    SourceIp = Column(String(15))
    LoginUrl = Column(String)
    NetworkId = Column(String)
    AuthenticationServiceId = Column(String)
    LoginGeoId = Column(String)
    TlsProtocol = Column(String)
    CipherSuite = Column(String)
    OptionsIsGet = Column(Boolean)
    OptionsIsPost = Column(Boolean)
    Browser = Column(String)
    Platform = Column(String)
    Status = Column(String)
    Application = Column(String)
    ClientVersion = Column(String)
    ApiType = Column(String)
    ApiVersion = Column(String)
    CountryIso = Column(String(2))
    AuthMethodReference = Column(String)
    transaction_id = column_property(Id)


class StgUser(Base):
    __tablename__ = "tmp_user"
    __table_args__ = {'schema': 'staging'}

    Id = Column(String(18), primary_key=True)
    FederationIdentifier = Column(String)
    Name = Column(String)
    Username = Column(String)
    GBS_User__c = Column(String)
    IGF_User__c = Column(String)
    USG_Federal_User__c = Column(String)
    UK_Sensitive_Data__c = Column(String)
    IsDachUser__c = Column(String)
    isManager__c = Column(String)
    IsActive = Column(String)
    Non_Sales_Relationship__c = Column(String)
    UserType = Column(String)
    transaction_id = column_property(Id + '_' + Username)


class PrdUser(Base):
    __tablename__ = "user"
    __table_args__ = {'schema': 'public'}

    Id = Column(String(18), primary_key=True)
    FederationIdentifier = Column(String)
    Name = Column(String)
    Username = Column(String)
    GBS_User__c = Column(Boolean)
    IGF_User__c = Column(Boolean)
    USG_Federal_User__c = Column(Boolean)
    UK_Sensitive_Data__c = Column(Boolean)
    IsDachUser__c = Column(Boolean)
    isManager__c = Column(Boolean)
    IsActive = Column(Boolean)
    Non_Sales_Relationship__c = Column(String)
    UserType = Column(String)
    transaction_id = column_property(Id + '_' + Username)
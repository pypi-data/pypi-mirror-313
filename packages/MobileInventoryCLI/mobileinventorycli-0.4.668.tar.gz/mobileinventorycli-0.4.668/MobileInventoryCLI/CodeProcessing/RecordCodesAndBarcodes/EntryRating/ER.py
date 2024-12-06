from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.RandomStringUtil import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.ReFormula import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from collections import namedtuple,OrderedDict
import nanoid
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar

class Properties(BASE,Template):
    __tablename__="Properties"
    Name=Column(String)
    Value=Column(String)
    Type_=Column(String)
    PID=Column(Integer,primary_key=True)

    def __init__(self,**kwargs):
        kwargs['__tablename__']=self.__tablename__
        self.init(**kwargs,)

Properties.metadata.create_all(ENGINE)

class EntryRating(BASE,Template):
    __tablename__="EntryRating"
    ERID=Column(Integer,primary_key=True)
    EntryId=Column(Integer)
    EntryBarcode=Column(String)
    EntryCode=Column(String)
    EntryName=Column(String)

    Title=Column(String)
    YourName=Column(String)
    Comment=Column(String)
    Note=Column(String) 
    DOE=Column(Date)
    Price=Column(Float)

    #0=worst
    #10 or 5 being best
    OutOf10BeingBestAverage=Column(Integer)
    OutOf5BeingBestAverage=Column(Integer)

    #json list containing things like
    #[property_id_1,property_id_2,]
    #where the value is Stored in Properties.Value with the data type being in Properties.Type_ of Properties.PID
    ReviewProperties=Column(String)

EntryRating.metadata.create_all(ENGINE)


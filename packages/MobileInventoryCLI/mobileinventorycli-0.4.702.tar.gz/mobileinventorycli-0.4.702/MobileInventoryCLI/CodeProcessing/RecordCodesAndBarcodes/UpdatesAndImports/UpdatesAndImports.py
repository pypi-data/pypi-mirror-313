import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DatePicker import *
import requests

from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Collector2.Collector2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.LocationSequencer.LocationSequencer import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.PunchCard.PunchCard import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Conversion.Conversion import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.POS.POS import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified

class GetRemoteSource:
	source=''
	destination=''
	tmp=''

	def __init__(self,source,destination='./codesAndBarcodes.tgz',tmp='./tmp_extract',engine=None):
		self.source=source
		self.destination=destination
		self.engine=engine
		self.tmp=tmp

		dp=Path(destination)
		msg=f"Removing old detination file!!!"
		print(msg)
		if dp.exists():
			dp.unlink()

		response=requests.get(self.source)
		if response.status_code == 200:
			pass



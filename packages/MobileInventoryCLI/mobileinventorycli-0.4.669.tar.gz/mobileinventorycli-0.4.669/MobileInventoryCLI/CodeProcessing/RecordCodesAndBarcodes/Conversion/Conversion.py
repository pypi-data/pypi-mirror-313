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
import pint
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExportList.ExportListCurrent import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *


import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc


class Conversion:
	def __init2__(self,engine,parent):
		self.__init__(engine,parent)
		return self.converted
	def __init__(self,engine,parent):
		self.parent=parent
		self.engine=engine

		self.helpText=f"""
"""
		def mkFloat(text,self):
			try:
				return float(text)
			except Exception as e:
				print(e)
				return

		def mkText(text,self):
			return text
		while True:
			try:
				while True:
					try:
						value=Prompt.__init2__(None,func=mkFloat,ptext="Amount:",helpText="How Much to convert.")
						if value == None:
							return
						break
					except Exception as e:
						print(e)
				while True:
					try:
						fromUnit=Prompt.__init2__(None,func=mkText,ptext="From:",helpText="Unit to Convert FROM")
						if fromUnit == None:
							return
						break
					except Exception as e:
						print(e)
				
				while True:
					try:
						toUnit=Prompt.__init2__(None,func=mkText,ptext="TO:",helpText="Unit to Convert TO")
						if toUnit == None:
							return
						break
					except Exception as e:
						print(e)
				
				registry=pint.registry.UnitRegistry()
				self.converted=registry.convert(value,fromUnit,toUnit)
				print(f"{Fore.light_green}{value} {Fore.magenta}{fromUnit}{Style.reset}->{self.converted} {Fore.medium_violet_red}{toUnit}{Style.reset}")
				
			except Exception as e:
				print(e)

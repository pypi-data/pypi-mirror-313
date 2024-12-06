from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.RandomStringUtil import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.ReFormula import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.SetEntryNEU import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.RNE.RNE import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup2.Lookup2 import Lookup as Lookup2
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.masterLookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.blankDataFile import *

from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup2.Lookup2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.glossary_db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DisplayItemDb import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.ExerciseTracker import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Collector2.Collector2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.LocationSequencer.LocationSequencer import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.PunchCard.PunchCard import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Conversion.Conversion import *

from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.POS.POS import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.BNC.BnC import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.EntryRating.ER import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.SystemSettings.SystemSettings import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Comm.RxTx import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Roster.Roster import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.HealthLog.HealthLog import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes import VERSION

from collections import namedtuple,OrderedDict
import nanoid,qrcode,io
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar


filename_blank="codesAndBarcodes-blank.db"
DEVMOD=False
if DEVMOD:
	if Path(filename).exists():
		Path(filename).unlink()
dbfile_blank="sqlite:///"+str(filename_blank)
img_dir=Path("Images")
if not img_dir.exists():
	img_dir.mkdir()
print(dbfile_blank)
#import sqlite3
#z=sqlite3.connect(filename)
#print(z)
ENGINE_BLANK=create_engine(dbfile_blank)



class blankDataFileClass:
	def __init__(self):
		Entry.metadata.create_all(ENGINE_BLANK)
		DayLog.metadata.create_all(ENGINE_BLANK)
		Entry.metadata.create_all(ENGINE_BLANK)
		PairCollection.metadata.create_all(ENGINE_BLANK)
		DayLog.metadata.create_all(ENGINE_BLANK)
		TouchStamp.metadata.create_all(ENGINE_BLANK)
		Shift.metadata.create_all(ENGINE_BLANK)
		MailBox.metadata.create_all(ENGINE_BLANK)
		MailBoxContacts.metadata.create_all(ENGINE_BLANK)
		HealthLog.metadata.create_all(ENGINE_BLANK)
		RoutineDuration.metadata.create_all(ENGINE_BLANK)
		Exercise.metadata.create_all(ENGINE_BLANK)
		Routine.metadata.create_all(ENGINE_BLANK)
		SystemPreference.metadata.create_all(ENGINE_BLANK)
		Billing.metadata.create_all(ENGINE_BLANK)
		RecieptEntry.metadata.create_all(ENGINE_BLANK)
		AdditionalExpenseOrFee.metadata.create_all(ENGINE_BLANK)
		DisplayItem.metadata.create_all(ENGINE_BLANK)
		Reciept.metadata.create_all(ENGINE_BLANK)
		RepackList.metadata.create_all(ENGINE_BLANK)
		RepackItem.metadata.create_all(ENGINE_BLANK)
		ClipBoord.metadata.create_all(ENGINE_BLANK)
		DateMetrics.metadata.create_all(ENGINE_BLANK)
		PH.metadata.create_all(ENGINE_BLANK)
		Roster.metadata.create_all(ENGINE_BLANK)
		RosterShift.metadata.create_all(ENGINE_BLANK)
		Department.metadata.create_all(ENGINE_BLANK)
		FindCmd.metadata.create_all(ENGINE_BLANK)
		HealthLog.metadata.create_all(ENGINE_BLANK)
		RandomString.metadata.create_all(ENGINE_BLANK)
		RandomStringPreferences.metadata.create_all(ENGINE_BLANK)
		RandomString.metadata.create_all(ENGINE_BLANK)
		Glossary.metadata.create_all(ENGINE_BLANK)
		Properties.metadata.create_all(ENGINE_BLANK)
		EntryRating.metadata.create_all(ENGINE_BLANK)
		CashPool.metadata.create_all(ENGINE_BLANK)
		Bill.metadata.create_all(ENGINE_BLANK)
		CashPool.metadata.create_all(ENGINE_BLANK)
		Bill.metadata.create_all(ENGINE_BLANK)
		print("Beginning")

		backup="blank-codesAndBarcodes.tgz"

		with Session(ENGINE) as init,Session(ENGINE_BLANK) as FINAL:
			foremost=init.query(Entry).all()
			foremost_ct=len(foremost)
			start=datetime.now()
			for num,e in enumerate(foremost):
				FINAL.merge(e)
				if num % 300 == 0:
					msg=f"{num}/{num+1} of {foremost_ct}|{start.ctime()}-{datetime.now().ctime()}:Delta={datetime.now()-start} - {e.Name}|{e.Barcode}|{e.Code}"
					print(msg)
					FINAL.commit()
			x=FINAL.query(Entry).update({"Code":'',"Price":0})
			FINAL.commit()
			FINAL.flush()

		with open("version.txt","w+") as version_txt:
			version_txt.write(VERSION)

		with tarfile.open(backup,"w:gz") as gzf:
			with open("Run.py","wb") as runner:
				oldlines=b'''
#!/usr/bin/env python3
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.RecordMyCodes as rmc
rmc.quikRn()
'''
				lines=b'''
#!/usr/bin/env python3
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes import RecordMyCodes as rmc
rmc.quikRn()
'''
				runner.write(lines)
			print("Added 'Run.py'")
			gzf.add("Run.py")
			api_key_file=Path("./api_key")
			if api_key_file.exists():
				gzf.add(api_key_file)
				print(f"Added '{api_key_file}'")

			if Path("version.txt").exists():
				gzf.add("version.txt")
				print("Added ./version.txt")
				Path("version.txt").unlink()


			dbf=Path(filename_blank)
			if dbf.exists():
				print(f"adding {dbf}")
				gzf.add(dbf,arcname=filename)

			imd=Path("Images")
			if imd.exists():
				print(f"adding {imd}")
				gzf.add(imd)
			lclimg=Path("LCL_IMG")
			if lclimg.exists():
				print(f"adding {lclimg}")
				gzf.add(lclimg)
						


def blankDataFile():
	print("btrf")
	blankDataFileClass()
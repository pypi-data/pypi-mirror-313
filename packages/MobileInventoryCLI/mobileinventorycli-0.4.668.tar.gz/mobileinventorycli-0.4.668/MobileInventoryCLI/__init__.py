#!/usr/bin/env python3
'''
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


BASE=automap_base()
cfg=None
p='dbpath.config'
P=Path(__file__).parent/Path(p)
script_dir=P

with open(P,'r') as config:
	cfg=json.load(config)
	
if cfg.get('dbfile') == '':
	with open(P,'w') as config:
		while cfg['dbfile'] in ['']:
			cfg['dbfile']=input('dbfile Path to save: ')
		json.dump(cfg,config)
#filename=Path("/storage/emulated/0/Download/Database/MobileInventoryDB_13-12-2023_01-26-13.db3")
filename=Path(cfg.get('dbfile'))
if not filename.exists():
	raise Exception(str(filename.exists())+":"+str(filename))
dbfile="sqlite:///"+str(filename)
print(dbfile)
import sqlite3
#z=sqlite3.connect(filename)
#print(z)
ENGINE=create_engine(dbfile)
BASE.prepare(autoload_with=ENGINE)
TABLE=BASE.classes


from MobileInventoryCLI.mainloop import mainloop
from MobileInventoryCLI.error.error import writeError

if __name__ == "__main__":
    mainloop.MainLoop(engine=ENGINE,config=P,error_log=Path(__file__).parent/Path("error.log"),tbl=TABLE)
#begin making modules and importing them here
'''
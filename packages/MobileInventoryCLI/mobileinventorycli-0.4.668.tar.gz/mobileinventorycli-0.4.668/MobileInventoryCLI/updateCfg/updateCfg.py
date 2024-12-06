import json
from MobileInventoryCLI.error.error import writeError,obj2dict



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

class Quit:
	def __str__(self):
		return 'Quit'
		
	def __init__(self,config,engine,error_log,tbl):
		self.config=config
		self.error_log=error_log
		self.engine=engine
		self.tbl=tbl
		exit()
		
class StorageConfig:
	def __str__(self):
		return 'StorageConfig'
		
	def __init__(self,config,engine,error_log,tbl):
		self.engine=engine
		self.error_log=error_log
		self.config=config
		self.tbl=tbl
		while True:
			try:
					msg=[
					'-'*10,
					'quit',
					'back',
					'list',
					'set',
					'+'*10,
					]
					cmd=input('\n'.join(msg)+"\n"+"what do you want to do? ")
					if cmd in msg[1:-1]:
						if cmd.lower() =="back":
							break
						elif cmd.lower() =="quit":
							exit("user quit!")
						elif cmd.lower() == 'list':
							with Session(engine) as session:
								results = session.query(tbl.Storage).all()
								for num,item in enumerate(results):
									print(num,obj2dict(item))
						elif cmd.lower() == 'set':
							storageIdStr=''
							while storageIdStr == '':
								storageIdStr=input("StorageId: ")
								try:
									storageId=int(storageIdStr)
									UpdateConfig.updateByKey(self,'storageId',storageId,config,engine,error_log,tbl)
								except Exception as e:
									writeError(e,self.error_log)
						else:
							print(cmd)
					else:
						raise Exception('invalid cmd!')
			except Exception as e:
					writeError(e,self.error_log)
class ListConfig:
	def __str__(self):
		return 'ListConfig'
		
	def __init__(self,config,engine,error_log, tbl):
			cf={}
			self.error_log=error_log
			self.config=config
			self.tbl=tbl
			self.engine=engine
			print(config,config.exists())
			with open(config,'r') as cfg:
				cf=json.load(cfg)
				for k in cf.keys():
					print(k,cf[k])
			
class UpdateConfig:
	def __str__(self):
		return 'UpdateConfig'
		
	def __init__(self,config,error_log, tbl):
			cf={}
			self.error_log=error_log
			self.config=config
			self.tbl=tbl
			
			with open(config,'r') as cfg:
				cf=json.load(cfg)
				for k in cf.keys():
					msg='{}:{}:update[#next/value]? '.format(k,cf[k])
					a=input(msg)
					if a == '#next':
						pass
					else:
						cf[k]=a
			while True:
				t=input('write [y/n]: ').lower()
				if t == 'y':
					with open(config,'w') as cfg:
						json.dump(cf,cfg)
						break
				elif t == 'n':
					break
	
	def updateByKey(self,key,value,config,engine,error_log,tbl):
				try:
					cf={}
					with open(config,'r') as cfg:
						cf=json.load(cfg)
						cf[key]=value
					with open(config,'w') as cfg:
						json.dump(cf,cfg)
				except Exception as e:
					writeError(e,error_log)
					#with error_log.open("a") as log:
						
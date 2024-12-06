from MobileInventoryCLI.error.error import writeError,obj2dict

	
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64

class Search:
	def __str__(self):
		return "LookupCode"
	def seeCustomFields(self,result,config,engine,error_log,tbl):
		if not result:
			raise Exception('result is "{}":{}'.format(result,type(result)))
			with Session(engine) as session:
				query=session.query(tbl.ItemCustomField)
				result=query.filter(tbl.ItemCustomField.ItemCustomFieldId==result.ItemId).all()
				for num,r in enumerate(result):
					print('++++{}++++'.format(num))
					name,typeNo,typeStr='',0,'Text'
					q=session.query(tbl.CustomField)
					q=q.filter(tbl.CustomField.CustomFieldId==r.CustomFieldId)
					qr=q.first()
					name,typeNo=qr.Name,qr.Type
					if typeNo == 0:
						typeStr='Text'
					elif typeNo == 1:
						typeStr='Numbers'
					elif typeNo == 2:
						typeStr='Date'
					for column in r.__table__.columns:
						print(column.name,getattr(column.name))
					print('Name:',name)
					print('Type: ',typeStr)
					print('++++{}++++'.format(num))
		#lookup item result custom fields
	def __init__(self,config,engine,error_log,tbl):
		self.tbl=tbl
		self.engine=engine
		self.error_log=error_log
		self.config=config
		with config.open('r') as d:
			self.cfg=json.load(d)
		self.cmds={
			'1':'lookup by itemCode',
			'2':'lookup by Barcode',
			'3':'lookup by ItemId',
			'4':'lookup by barcode|itemcode|itemid',
			'5':'edit item by itemCode',
			'6':'edit item by Barcode',
			'7':'edit item byItemId',
			'8':'quit',
			'quit':'quit',
			'q':'quit',
			'back':'go back a menu',
		}
		msg='\n'.join(['{}->{}'.format(i,self.cmds[i]) for i in self.cmds.keys()])
		while True:
			cmd=input('{}\n----------\nwhat do you want to do? '.format(msg))
			if cmd.lower() in ('q','quit','8'):
				exit('user quit!')
			elif cmd.lower() == "back":
				break
			else:
				if cmd  == '1':
					while True:
						itemcode=input('itemcode[or #back]: ')
						if itemcode == '#back':
							break
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								result=result.filter(tbl.Item.Code==itemcode)
								results=result.all()
								self.processResults(results)
	def processResults(self,results):
		for num,r in enumerate(results):
			print('---Item ({})---'.format(num))
			o=obj2dict(r)
			for k in o.keys():
				print(k,':',o[k])
			self.seeCustomFields(r,config,engine,error_log,tbl)
			print('===Item ({})==='.format(num))

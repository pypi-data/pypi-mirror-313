from . import *

class ExportTable:
	def lsTables(self,only_return=False):
		with Session(ENGINE) as session:
			metadata=BASE.metadata
			metadata.reflect(ENGINE)
			tables=metadata.tables.keys()
			ct=len(tables)
			msgF=[]
			for num,i in enumerate(tables):
				msg=f"{self.colorized(num,ct)} - {Fore.orange_red_1}{i}{Style.reset}"
				msgF.append(msg)
			if not only_return:
				print('\n'.join(msgF))
			return '\n'.join(msgF)

	def exportSearched(self):
		folder=Path(detectGetOrSet("ExportTablesFolder",value="ExportedTables",literal=True))
		if not folder.exists():
			folder.mkdir()
		with Session(ENGINE) as session:
			search=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What are you looking for with a text search to be exported?: ",helpText="searches all text columns of Entry Table",data="string")
			if search in [None,]:
				return
			keepers=["string","varchar","text"]
			text_fields=[str(i.name) for i in Entry.__table__.columns if str(i.type).lower() in keepers]			
			entries=session.query(Entry)
			fs=[getattr(Entry,i).icontains(search) for i in text_fields]
			
			try:
				entries=entries.filter(or_(*fs))
				df = pd.read_sql(entries.statement, entries.session.bind,dtype=str)
				opathname=folder/Path("EntrySearchedExport"+f"{datetime.now().strftime('_%m-%d-%Y')}.xlsx")
				df.to_excel(opathname,index=None)
				print(f"{Fore.light_red}Finished Writing '{Fore.light_green}{opathname}{Fore.light_red}': {Fore.orange_red_1}{opathname.exists()} | Exported '{Fore.light_steel_blue}{len(df)}{Fore.orange_red_1}' Results{Style.reset}")
			except Exception as e:
				print(e)

	def exportSelectedDaylogEntry(self):
		folder=Path(detectGetOrSet("ExportTablesFolder",value="ExportedTables",literal=True))
		if not folder.exists():
			folder.mkdir()
		with Session(ENGINE) as session:
			search=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What are you looking to Export?: ",helpText="Searches fields in DayLog: Barcode,Code,Comments,Notes,Description,Name",data="string")
			if search in [None,]:
				return
			results=session.query(DayLog).filter(
				or_(
					DayLog.Barcode.icontains(search),
					DayLog.Code.icontains(search),
					DayLog.Name.icontains(search),
					DayLog.Description.icontains(search),
					DayLog.Note.icontains(search),
					)
				).group_by(DayLog.EntryId).order_by(DayLog.DayLogDate).all()
			ct=len(results)
			msgList=[]
			for num,i in enumerate(results):
				msgList.append(f'''{self.colorized(num,ct)} - {i.Name}|{i.Barcode}|{i.Code}|{i.Description}|{i.Note}''')
			msgText='\n'.join(msgList)
			print(msgText)
			which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Which index?: ",helpText=msgText,data='integer')
			if which in [None,'d']:
				print("User Cancelled!")
				return
			finalResult=results[which]
			entries=session.query(DayLog).filter(DayLog.EntryId==finalResult.EntryId)
			df = pd.read_sql(entries.statement, entries.session.bind)
			opathname=folder/Path("SelectedDayLogSetExport"+f"{datetime.now().strftime('_%m-%d-%Y')}.xlsx")
			df.to_excel(opathname,index=None)
			print(f"{Fore.light_red}Finished Writing '{Fore.light_green}{opathname}{Fore.light_red}': {Fore.orange_red_1}{opathname.exists()} | Exported '{Fore.light_steel_blue}{len(df)}{Fore.orange_red_1}' Results{Style.reset}")



	def exportTaggedEntry(self):
		folder=Path(detectGetOrSet("ExportTablesFolder",value="ExportedTables",literal=True))
		if not folder.exists():
			folder.mkdir()
		with Session(ENGINE) as session:
			tags=session.query(Entry).group_by(Entry.Tags).all()
			tags_list=[]
			ct_tags=len(tags)
			for num,i in enumerate(tags):
				msg=f"{self.colorized(num,ct_tags)} -{i.Tags}"
				try:
					t=json.loads(i.Tags)
					for tag in t:
						if tag not in tags_list and tag != None:
							tags_list.append(tag)
				except Exception as e:
					print(e)
			tags_list=sorted(tags_list)
			tag_ct=len(tags_list)
			tagText=[]
			for num,i in enumerate(tags_list):
				msg=f'{self.colorized(num,tag_ct)} - {i}'
				tagText.append(msg)
			tagText='\n'.join(tagText)
			print(tagText)
			entries=session.query(Entry)

			shards=[]
			t=tagText
			print(t)
			which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Export Selected Tags from Entry Table | which index(es): ",helpText=t,data="list")
			if which in [None,]:
				print("User Cancelled!")
				return
			try:
				for i in which:
					try:
						INDEX=int(i)
						shards.append(Entry.Tags.icontains(tags_list[INDEX]))
					except Exception as ee:
						print(ee)
			except Exception as e:
				print(e)
			try:
				entries=entries.filter(or_(*shards))
				df = pd.read_sql(entries.statement, entries.session.bind,dtype=str)
				opathname=folder/Path("EntryTaggedExport"+f"{datetime.now().strftime('_%m-%d-%Y')}.xlsx")
				df.to_excel(opathname,index=None)
				print(f"{Fore.light_red}Finished Writing '{Fore.light_green}{opathname}{Fore.light_red}': {Fore.orange_red_1}{opathname.exists()} | Exported '{Fore.light_steel_blue}{len(df)}{Fore.orange_red_1}' Results{Style.reset}")
			except Exception as e:
				print(e)




	def exportSelected(self):
		folder=Path(detectGetOrSet("ExportTablesFolder",value="ExportedTables",literal=True))
		if not folder.exists():
			folder.mkdir()
		with Session(ENGINE) as session:
			metadata=BASE.metadata
			metadata.reflect(ENGINE)
			tables=metadata.tables.keys()
			tables2=[]
			ct=len(tables)
			msgF=[]
			for num,i in enumerate(tables):
				tables2.append(i)
				msg=f"{self.colorized(num,ct)} - {Fore.orange_red_1}{i}{Style.reset}"
				msgF.append(msg)
			t='\n'.join(msgF)
			print(t)
			which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Export Selected Tables | which index(es): ",helpText=t,data="list")
			if which in [None,]:
				print("User Cancelled!")
				return
			try:
				for i in which:
					try:
						INDEX=int(i)
						query=session.query(metadata.tables[tables2[INDEX]])
						print(tables2[INDEX])
						df = pd.read_sql(query.statement, query.session.bind,dtype=str)
						opathname=folder/Path(tables2[INDEX]+f"{datetime.now().strftime('_%m-%d-%Y')}.xlsx")
						df.to_excel(opathname,index=None)
						print(f"{Fore.light_red}Finished Writing '{Fore.light_green}{opathname}{Fore.light_red}': {Fore.orange_red_1}{opathname.exists()} | Exported '{Fore.light_steel_blue}{len(df)}{Fore.orange_red_1}' Results{Style.reset}")
					except Exception as ee:
						print(ee)
			except Exception as e:
				print(e)

	def colorized(self,num,ct):
		return f'{Fore.light_red}{num}{Fore.orange_red_1}/{Fore.light_green}{num+1} of {Fore.cyan}{ct} {Fore.magenta}'

	def __init__(self):
		self.cmds={
			'list tables':{
				'cmds':['ls tables','list tables','ls tbls'],
				'exec':self.lsTables,
				'desc':'list tables in db',
			},
			'export selected':{
				'cmds':['export selected table','est','xpt slct tbl'],
				'exec':self.exportSelected,
				'desc':'export specific tables'
			},
			'Export Tagged Entry':{
			'cmds':['export tagged entry','ete','xpt tgd ntry'],
			'exec':self.exportTaggedEntry,
			'desc':'export Entry\' Tagged Entries from Entry Table using selected tags'
			},
			'Export Searched Entry':{
			'cmds':['export searched entry','ese','xpt schd ntry'],
			'exec':self.exportSearched,
			'desc':'export Entry\' searched from Entry Table using selected text fields'
			},
			'Export Selected Daylog Entry Set':{
			'cmds':['esdes','exported selected daylog entry set'],
			'exec':self.exportSelectedDaylogEntry,
			'desc':'Export a specific DayLog Entry Set by search'
			}
		}
		helpText=''
		for cmd in self.cmds:
			msg=f'{Fore.light_cyan}{self.cmds[cmd]["cmds"]} {Fore.light_yellow}{self.cmds[cmd]["desc"]}{Style.reset}\n'
			helpText+=msg
		print(helpText)
		while True:
			action=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Export Table Menu | Do what?",helpText=helpText,data="string")
			if action in [None,]:
				return
			elif action in ['d',]:
				print(helpText)
				continue
			for cmd in self.cmds:
				if action.lower() in self.cmds[cmd]['cmds']:
					if self.cmds[cmd]['exec'] != None and callable(self.cmds[cmd]['exec']):
						self.cmds[cmd]['exec']()
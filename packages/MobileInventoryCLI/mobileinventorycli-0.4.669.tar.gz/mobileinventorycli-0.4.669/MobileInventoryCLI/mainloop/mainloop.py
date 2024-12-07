#import made modules

from MobileInventoryCLI.lookup import lookup
from MobileInventoryCLI.error.error import writeError
from MobileInventoryCLI.updateCfg import updateCfg
class MainLoop:
	#interactive modules go here
	#use def __str__ to define command name
	Modules=[
	updateCfg.UpdateConfig,
	updateCfg.Quit,
	updateCfg.StorageConfig,
	updateCfg.ListConfig,
	lookup.Search,
	]
	def __init__(self,engine,config,error_log,tbl):
		self.engine=engine
		self.config=config
		self.error_log=error_log
		self.tbl=tbl
		if error_log.exists():
			with error_log.open('w+') as log:
				log.write('')
		while True:
			msg='\n'.join([i. __str__(None) for i in self.Modules if not isinstance(i,str)])
			cmd=input('-'*10+'\n{}\n__________\nwhat do you want to do: '.format(msg))
			if isinstance(cmd,str) and cmd.lower() == "quit":
				updateCfg.Quit(config=config,engine=engine,error_log=error_log,tbl=tbl)
			else:
				try:
					if cmd.lower() == 'updateconfig':
						updateCfg.UpdateConfig(config,error_log,tbl)
					elif cmd.lower()=="storageconfig":
						updateCfg.StorageConfig(tbl=tbl,config=config,error_log=error_log,engine=engine)
					elif cmd.lower()=="listconfig":
						updateCfg.ListConfig(tbl=tbl,config=config,error_log=error_log,engine=engine)	
					elif cmd.lower()=="lookupcode":
						lookup.Search(tbl=tbl,config=config,error_log=error_log,engine=engine)
				except Exception as e:
					writeError(e,self.error_log)
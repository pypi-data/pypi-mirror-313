from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *

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

class Glossary(BASE,Template):
    __tablename__="Glossary"
    GID=Column(Integer,primary_key=True)
    Term=Column(String)
    Definition=Column(String)
    Note=Column(String)

    def __init__(self,**kwargs):
        kwargs['__tablename__']=self.__tablename__
        self.init(**kwargs,)


Glossary.metadata.create_all(ENGINE)

class GlossaryUI:
    helpText=f'''
{Fore.light_green}{'|'.join(['a2g',"add2glossary","add to glossary"])}{Style.reset} - {Fore.light_steel_blue}add/edit a glossary term{Style.reset}
{Fore.light_green}{'|'.join(['search','define','lookup'])}{Style.reset} - {Fore.light_steel_blue}search for a glossary [Looks in Term,Note,Definition]{Style.reset}
{Fore.light_green}{'|'.join(['delete','remove','rm','dl'])}{Style.reset} - {Fore.light_steel_blue}delete/remove a glossary term{Style.reset}
{Fore.light_green}{'|'.join(['delete_id','remove_id','rmid','dlid'])}{Style.reset} - {Fore.light_steel_blue}delete/remove a glossary term by GID{Style.reset}
{Fore.light_green}{'|'.join(['reset','reset_glossary','clear_all'])}{Style.reset} - {Fore.light_steel_blue}clear/reset entire glossary{Style.reset}
{Fore.light_green}{'|'.join(['va','view_all','view all'])}{Style.reset} - {Fore.light_steel_blue}view entire glossary{Style.reset}
{Fore.light_green}{'|'.join(['ihsv','import_hsv',])}{Style.reset} - {Fore.light_steel_blue}Import HSV data (hashtag separated columns, essentially a csv, with the Headers being the line '{Fore.cyan}Term#Definition{Fore.light_steel_blue}'){Style.reset}
{Fore.light_green}{'|'.join(['ixcel','import_excel',])}{Style.reset} - {Fore.light_steel_blue}Import Excel Data with the Headers being '{Fore.cyan}Term,Definition,Note{Fore.light_steel_blue}'){Style.reset}
    '''
    def mkText(self,text,data):
        return text

    def import_excel(self):
        try:
            filename=Prompt.__init2__(None,func=self.mkText,ptext="File to import data from?",helpText="file to import data from hashtag separated!",data=self)
            filename=Path(filename)
            if filename.exists() and filename.is_file():
                df=pd.read_excel(filename,dtype=str)
                with Session(ENGINE) as session:
                    for num,row in enumerate(df.itertuples()):
                        print(f"{Fore.light_yellow}Extracted Row From File {Fore.light_steel_blue}{num}:{Fore.light_red} {row._asdict()}{Style.reset}")
                        check=session.query(Glossary).filter(Glossary.Term==row.Term).first()
                        if check:
                            print(f"{Fore.light_red}{num+1} not added{Style.reset} -> {check}")
                            continue
                        gt=Glossary(**row._asdict())
                        session.add(gt)
                        session.commit()
                        session.flush()
                        session.refresh(gt)
                        print(f"{Fore.light_green}{num+1} added{Style.reset} -> {gt}")
        except Exception as e:
            print(e)
            print(f"{Fore.orange_red_1}Nothing was imported{Style.reset}")

    def import_hsv(self):
        flush_size=1000
        try:
            import_start=datetime.now()
            filename=Prompt.__init2__(None,func=self.mkText,ptext="File to import data from?",helpText="file to import data from hashtag separated!",data=self)
            filename=Path(filename)
            if filename.exists() and filename.is_file():
                df=pd.read_csv(filename,sep='#',dtype=str)
                with Session(ENGINE) as session:
                    size=len([i for i in df.itertuples()])
                    for num,row in enumerate(df.itertuples()):
                        now=datetime.now()
                        check=session.query(Glossary).filter(Glossary.Term==row.Term,Glossary.Definition==row.Definition).all()
                        if len(check) > 0:
                            if num % flush_size == 0:
                                msg=f"{Fore.light_red}{num+1}/{Fore.light_steel_blue}{size}{Fore.light_red} {round(((num+1)/size)*100,2)}% [{Fore.light_magenta}ET:{now-import_start}{Fore.light_red}] not added{Style.reset} -> [{check[0].Term}..{check[-1].Term}] - [{check[0].Definition}..{check[-1].Definition}]{Style.reset}"
                                modCount=len(Style.reset+Fore.light_red+Fore.light_steel_blue+Fore.light_red+Fore.light_magenta+Fore.light_red+Style.reset)
                                if len(msg) < os.get_terminal_size().columns:
                                    print(msg)
                                else:
                                    print(msg[:os.get_terminal_size().columns+modCount]+Style.reset)
                            continue
                        gt=Glossary(Term=row.Term,Definition=row.Definition)
                        session.add(gt)
                        if num % flush_size == 0:
                            session.commit()
                            session.flush()
                            session.refresh(gt)
                            msg=f"{Fore.light_green}{num+1}/{Fore.light_steel_blue}{size}{Fore.light_green} {round(((num+1)/size)*100,2)}% [{Fore.cyan}ET:{now-import_start}{Fore.light_green}] added{Style.reset} -> {gt.Term}:{gt.Definition}"
                            modCount=len(Style.reset+Fore.light_green+Fore.light_steel_blue+Fore.light_green+Fore.cyan+Fore.light_green+Style.reset)
                            if len(msg) < os.get_terminal_size().columns:
                                print(msg)
                            else:
                                print(msg[:os.get_terminal_size().columns+modCount]+Style.reset)

                    session.commit()
        except Exception as e:
            print(e)
            print(f"{Fore.orange_red_1}Nothing was imported{Style.reset}")

    def mkNew(self,term,definition='',note='',data=None):
        if data == None:
            data={
            'Definition':definition,
            'Note':note,
            }
        self.skipTo=None
        while True:  
            #print(self.skipTo,"#loop top")
            for num,f in enumerate(data):
                #print(self.skipTo,'#2',"1 loop for")
                if self.skipTo != None and num < self.skipTo:
                    continue
                else:
                    self.skipTo=None
                keys=['e','p','d']
                while True:
                    try:
                        def lclt(text,data):
                            return text
                        dtmp=Prompt.__init2__(None,func=lclt,ptext=f"Glossary [default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                        if dtmp in [None,]:
                            print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                            return
                        elif isinstance(dtmp,str):
                            if str(dtmp).lower() in ['e',]:
                                return
                            elif str(dtmp).lower() in ['p',]:
                                #print(num,num-1,"#3 loop while")
                                self.skipTo=num-1
                                break
                            elif str(dtmp).lower() in ['d',]:
                                print(f'{Fore.light_green}{data[f]}{Style.reset}',f'{Fore.orange_red_1}using default{Style.reset}')
                                pass
                            else:
                                fields={i.name:str(i.type) for i in Glossary.__table__.columns}
                                if f in fields.keys():
                                    if fields[f].lower() in ["string",]:
                                        data[f]=dtmp
                                    elif fields[f].lower() in ["float",]:
                                        data[f]=float(eval(dtmp))
                                    elif fields[f].lower() in ["integer",]:
                                        data[f]=int(eval(dtmp))
                                    elif fields[f].lower() in ["boolean",]:
                                        if dtmp.lower() in ['y','yes','t','true','1']:
                                            data[f]=True
                                        else:
                                            data[f]=False
                                    else:
                                        data[f]=dtmp
                                else:
                                    raise Exception(f"{Fore.red}{Style.bold}Unsupported Field {Fore.light_red}'{f}'{Style.reset}")
                                #data[f]=dtmp
                        else:
                            data[f]=dtmp
                        self.skipTo=None
                        break
                    except Exception as e:
                        print(e)
                        break
                if self.skipTo != None:
                    break
            if self.skipTo == None:
                break
        return data

    def add2glossary(self):
        while True:
            with Session(ENGINE) as session:
                term=Prompt.__init2__(None,self.mkText,ptext="Term to Add2Glossary",helpText="term to add/edit to/in glossary",data=self)
                if term in [None,]:
                    return
                check=session.query(Glossary).filter(Glossary.Term==term).all()
                ct=len(check)
                if ct == 0:
                    gl=self.mkNew(term=term)
                    if gl in [None,]:
                        return
                    gl['Term']=term
                    g=Glossary(**gl)
                    session.add(g)
                    session.commit()
                    session.flush()
                    session.refresh(g)
                    print(g)
                else:
                    print(check)
                    result=check
                    fields=['Term','Definition','Note']
                
                    for num,r in enumerate(result):
                        print(f"{Fore.green}{num}/{Fore.light_red}{ct-1}{Style.reset} -> {r}")
                    selected=None
                    
                    def selectInt(text,self):
                        try:
                            if text in ['',]:
                                return False
                            else:
                                return int(eval(text))
                        except Exception as e:
                            print(e)
                            return False
                    while True:
                        select=Prompt.__init2__(self,func=selectInt,ptext="which definition?",helpText=f"the {Fore.green}green{Fore.light_yellow} number before the slash")
                        if isinstance(select,int):
                            if ct == 1:
                                selected=0
                                break
                            elif select in list(range(0,ct-1)):
                                selected=select
                                break
                            else:
                                print("You need to specify one of the green numbers before the slash")
                        elif select in [False,]:
                            continue
                        elif select in [None,]:
                            return
                    if selected != None:
                        upd8=self.mkNew(term=None,data={field:getattr(check[selected],field) for field in fields})
                        if upd8 == None:
                            print(f"{Fore.orange_red_1}User Cancelled and Nothing was changed!{Style.reset}")
                        ud=session.query(Glossary).filter(Glossary.GID==check[selected].GID).first()
                        if ud:
                            for k in upd8:
                                setattr(check[selected],k,upd8[k])
                            session.commit()
                            session.flush()
                            session.refresh(check[selected])
                            print(check[selected])

                    #update term
                    pass

    def delete_term(self):
        gl=self.auto_search(selection=True)
        with Session(ENGINE) as session:
            dl=session.query(Glossary).filter(Glossary.GID==gl.get("GID")).first()
            print(f"{Fore.light_red}{Style.bold}Deleting {Style.reset}->{dl}")
            f=session.delete(dl)
            session.commit()
            session.flush()

    def reset_glossary(self):
        reset=Prompt.__init2__(None,func=mkb,ptext="Reset Entire Glossary?",helpText="reset entire glossary table?",data=self)
        if reset in [None,]:
            return
        elif reset == True:
            with Session(ENGINE) as session:
                deleted=session.query(Glossary).delete()
                session.commit()
                print(deleted)
        else:
            return

    def del_id(self):
        with Session(ENGINE) as session:
            def selectInt(text,self):
                try:
                    if text in ['',]:
                        return False
                    else:
                        return int(eval(text))
                except Exception as e:
                    print(e)
                    return False
            while True:
                select=Prompt.__init2__(self,func=selectInt,ptext="GID to Delete?",helpText=f"the {Fore.green}green{Fore.light_yellow} number before the slash")
                if select in [None,False]:
                    return
                r=session.query(Glossary).filter(Glossary.GID==select).delete()
                print(f"status: {r}")
                session.commit()
                            

    def view_all(self):
        with Session(ENGINE) as session:
                query=session.query(Glossary)
                #query=query.filter(or_(Glossary.Term.icontains(term),Glossary.Definition.icontains(term),Glossary.Note.icontains(term)))
                result=query.all()
                ct=len(result)
                if ct == 0:
                    print(f"{Fore.light_red}No Results!")
                else:
                    for num,r in enumerate(result):
                        print(f"{Fore.green}{num}/{Fore.light_red}{ct-1}{Style.reset} -> {r}")

    def auto_search(self,selection=False,repeat=True):
        try:
            while True:
                term=Prompt.__init2__(None,func=self.mkText,ptext="What are you looking for?",helpText="term, or part of term, or part of note, or part of definition",data=self)
                if term in [None,]:
                    return
                with Session(ENGINE) as session:
                    query=session.query(Glossary)
                    query=query.filter(or_(Glossary.Term.icontains(term),Glossary.Definition.icontains(term),Glossary.Note.icontains(term)))
                    result=query.all()
                    ct=len(result)
                    if ct == 0:
                        print(f"{Fore.light_red}No Results!")
                    else:
                        for num,r in enumerate(result):
                            m=f"{Fore.green}{num}/{Fore.light_red}{ct}{Style.reset} -> {r}"
                            mm=m.lower().replace(term.lower(),f"{Fore.orange_red_1}{term.lower()}{Style.reset}{Fore.light_yellow}")
                            mmm=mm.replace("term","Term").replace("definition","Definition").replace("note","Note").replace("gid","GID").replace("glossary","Glossary")
                            print(mmm)
                        if selection:
                            def selectInt(text,self):
                                try:
                                    if text in ['',]:
                                        return False
                                    else:
                                        return int(eval(text))
                                except Exception as e:
                                    print(e)
                                    return False
                            while True:
                                select=Prompt.__init2__(self,func=selectInt,ptext="which definition?",helpText=f"the {Fore.green}green{Fore.light_yellow} number before the slash")
                                if isinstance(select,int):
                                    if ct == 1:
                                        return {i.name:getattr(result[select],i.name) for i in result[select].__table__.columns}
                                    elif select in list(range(0,ct-1)):
                                        return {i.name:getattr(result[select],i.name) for i in result[select].__table__.columns}
                                        #break
                                    else:
                                        print("You need to specify one of the green numbers before the slash")
                                elif select in [False,]:
                                    continue
                                elif select in [None,]:
                                    return
                        #selection is next
                    if not repeat:
                        break
        except Exception as e:
            print(e)
            return


    def __init__(self,parent,engine):
        while True:
            try:
                fieldname='Menu'
                mode='Glossary'
                h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
                doWhat=Prompt.__init2__(None,func=self.mkText,ptext=f"{h}Do What?",helpText=self.helpText,data=self)
                if doWhat in [None,]:
                    return
                elif doWhat.lower() in ['a2g',"add2glossary","add to glossary"]:
                    self.add2glossary()
                elif doWhat.lower() in ['search','define','lookup']:
                    self.auto_search() 
                elif doWhat.lower() in ['delete','remove','rm','dl']:
                    self.delete_term()
                elif doWhat.lower() in ['reset','reset_glossary','clear_all']:
                    self.reset_glossary()
                elif doWhat.lower() in ['va','view_all','view all']:
                    self.view_all()
                elif doWhat.lower() in ['ihsv','import_hsv']:
                    self.import_hsv()
                elif doWhat.lower() in ['delete_id','remove_id','rmid','dlid']:
                    self.del_id()
                elif doWhat.lower() in ['ixcel','import_excel',]:
                    self.import_excel()
            except Exception as e:
                print(e)
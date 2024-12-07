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
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExportList.ExportListCurrent import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *


import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc

class TouchStampC:
    def search(self):
        def mkT(text,self):
            try:
                if len(text.split(".")) == 2:
                    prefix,code=text.split(".")
                elif len(text.split(".")) == 1:
                    code=text.split(".")[0]
                    prefix=''
                else:
                    raise Exception("Correct # of args is 2 or 1 by split off of '.'")
                return prefix,code
            except Exception as e:
                print(e)
                return

        value=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode: ",helpText=self.helpTxt,data=self)
        if not value:
            return
        else:
            prefix,code=value
            with Session(self.engine) as session:
                query=session.query(Entry)
                if prefix.lower() == '':
                    query=query.filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.Barcode.icontains(code),Entry.Code.icontains(code)))
                elif prefix.lower() == 'c':
                    query=query.filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                elif prefix.lower() == 'b':
                    query=query.filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                elif prefix.lower() == 'e':
                    query=query.filter(Entry.EntryId==int(code))
                results=query.all()
                if len(results) < 1:
                    query=session.query(TouchStamp).filter(TouchStamp.EntryId==code)
                    results=query.all()
                    ct=len(results)
                    if len(results) > 0:
                        for num,r in enumerate(results):
                            print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} -> {r}")
                    else:
                        print("No Results!")
                else:
                    ct=len(results)
                    if len(results) > 0:
                        msg=f"{Fore.light_green}Num{Style.reset}/{Fore.light_red}Total{Style.reset} -> {Fore.dark_goldenrod}Name - Barcode - Code - r.Size - Location - Price - r.EntryId{Style.reset}"
                        print(msg)
                        for num,r in enumerate(results):
                            extra=f'{r.Name} - {r.Barcode} - {r.Code} - {r.Size} - {r.Location} - {r.Price} - {r.EntryId}'
                            if num % 2 == 0:
                                extra=f'{Fore.grey_70}{extra}{Style.reset}'
                            
                            print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} -> {extra}")
                        
                        def mInt(text,self):
                            if text != '':
                                return int(text)
                            return 0
                        print(msg)
                        whichResult=Prompt.__init2__(None,func=mInt,ptext=f"Which result to use(0-{len(results)-1})[0]?",helpText=self.helpTxt,data=self)
                        print(whichResult)
                        if isinstance(whichResult,int):
                            e=results[whichResult]
                            eid=e.EntryId

                            rs=session.query(TouchStamp).filter(TouchStamp.EntryId==eid).all()
                            rs_ct=len(rs)
                            for num,r in enumerate(rs):
                                print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{rs_ct}{Style.reset} -> {r}")
                            print(f"{Fore.light_yellow}There are {Style.reset}{Fore.red}{rs_ct}{Style.reset} TouchStamp Results!")
                        else:
                            print("Please Enter a valid number!")
                    else:
                        print("No Results!")
            


    def __init__(self,engine,parent):
        try:
            self.engine=engine
            self.parent=parent
            #print("TouchStamp Locator for Fast Note Logging!")
            self.helpTxt=f"""TouchStamp Locator for Fast Note Logging!
{Fore.cyan}+ | +,Note,Barcode|Code {Style.reset}-{Fore.grey_70} create a new touchstamp entry, '+' on its own will{Style.reset}
                        {Fore.cyan}{Style.reset} {Fore.grey_70} prompt for details; otherwise use details as describe{Style.reset}
{Fore.cyan}s | s,Note,Barcode|Code {Style.reset}-{Fore.grey_70} synthesize barcode for a new touchstamp entry, 's' on its own will{Style.reset}
                        {Fore.cyan}{Style.reset} {Fore.grey_70} prompt for details; otherwise use details as describe
{Fore.cyan}e | e,Note,TouchStampId {Style.reset}-{Fore.grey_70} edit a touchstamp entry, 'e' on its own will{Style.reset}
                        {Fore.cyan}{Style.reset} {Fore.grey_70} prompt for details; otherwise use details as describe
{Fore.cyan}- | -,TouchStampId      {Style.reset}-{Fore.grey_70} remove an entry by prompt ('-' on its own), or by TouchStampId{Style.reset}
{Fore.cyan}l                       {Style.reset}-{Fore.grey_70} list all{Style.reset}
{Fore.cyan}l,$TouchStampId         {Style.reset}-{Fore.grey_70} list touch stamp id{Style.reset}
{Fore.cyan}l,Note|TouchStampId,$searchable {Style.reset}-{Fore.grey_70} search for in fields{Style.reset}
{Fore.cyan}q|quit {Style.reset}-{Fore.grey_70} quit program{Style.reset}
{Fore.cyan}b|back {Style.reset}-{Fore.grey_70} go back a menu{Style.reset}
{Fore.light_magenta}#code is:
W/ PREFIX:
    b.$code - #code is Entry.Barcode
    c.$code - #code is Entry.Code
    e.$code - #code is Entry.EntryId
W/O PREFIX:
    $code - #code is either Entry.Barcode or Entry.Code
{Style.reset}
{Fore.light_yellow}sc|search_code{Style.reset}-{Fore.grey_70}Search using #code{Style.reset}
            """
            while True:
                def mkT(text,self):
                    return text
                mode='TouchStamp/Notes'
                fieldname='TaskMode'
                h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
                cmd=Prompt.__init2__(None,func=mkT,ptext=f"{h}Do What?",helpText=self.helpTxt,data=self)
                if not cmd:
                    return
                if cmd.lower() in ['sc','search_code']:
                    self.search()
                elif cmd.split(",")[0].lower() in ['+','a']:
                    cmdline=cmd.split(",")
                    ct=len(cmdline)

                    if ct > 1 and ct == 3:
                        barcode=None
                        with Session(self.engine) as session:
                            bcd=session.query(Entry).filter(or_(Entry.Barcode==cmdline[2],Entry.Code==cmdline[2])).first()
                            print(bcd)
                            if bcd:
                                ts=TouchStamp(Note=cmdline[1],EntryId=bcd.EntryId)
                            else:
                                ts=TouchStamp(Note=cmdline[1],EntryId=None)
                            session.add(ts)
                            session.commit()
                            session.refresh(ts)
                            print(ts)
                    else:
                        while True:
                            try:
                                def mkT(text,self):
                                    return text
                                
                                code=Prompt.__init2__(self,func=mkT,ptext='Barcode|Code',helpText="Please enter the code you will be using!",data=self)
                                print(code)
                                if code in [None,]:
                                    break

                                note=Prompt.__init2__(self,func=mkT,ptext='Note',helpText="Please enter the note you will be writing!",data=self)

                                if note in [None,]:
                                    break
                                
                                with Session(self.engine) as session:
                                    bcd=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                                    print(bcd)

                                    if bcd:
                                        ts=TouchStamp(Note=note,EntryId=bcd.EntryId)
                                    else:
                                        ts=TouchStamp(Note=note,EntryId=None)
                                    session.add(ts)
                                    session.commit()
                                    session.refresh(ts)
                                    print(ts)
                                    break
                            except Exception as e:
                                print(e)
                elif cmd.split(",")[0].lower() in ['s']:
                    cmdline=cmd.split(",")
                    ct=len(cmdline)

                    if ct > 1 and ct == 2:
                        barcode=None
                        with Session(self.engine) as session:
                            ts=TouchStamp(Note=cmdline[1],EntryId=Entry.synthetic_field_str(None))
                            session.add(ts)
                            session.commit()
                            session.refresh(ts)
                            print(ts)
                    else:
                        while True:
                            try:
                                def mkT(text,self):
                                    return text
                                note=Prompt.__init2__(self,func=mkT,ptext="Note",helpText="The note you need to record!")
                                if note in [None,]:
                                    break
                                with Session(self.engine) as session:
                                    ts=TouchStamp(Note=note,EntryId=Entry.synthetic_field_str(None))
                                    session.add(ts)
                                    session.commit()
                                    session.refresh(ts)
                                    print(ts)
                                break
                            except Exception as e:
                                print(e)
                elif cmd.split(",")[0].lower() in ['-']:
                    cmdline=cmd.split(",")
                    ct=len(cmdline)

                    if ct > 1 and ct == 2:
                        barcode=None
                        with Session(self.engine) as session:
                            r=session.query(TouchStamp).filter(TouchStamp.TouchStampId==int(cmdline[1])).delete()
                            session.commit()
                            print(f"deleted {r}")
                    else:
                        while True:
                            try:
                                def mkT(text,self):
                                    return text
                                
                                code=Prompt.__init2__(self,func=mkT,ptext='TouchStampId',helpText="Please enter the TouchStampId you wish to delete!",data=self)
                                print(code)
                                if code in [None,]:
                                    break
                                else:
                                    with Session(self.engine) as session:
                                        bcd=session.query(TouchStamp).filter(TouchStamp.TouchStampId==int(code)).delete()
                                        session.commit()
                                        print(bcd) 
                                break
                            except Exception as e:
                                print(e)         
                elif cmd.split(",")[0].lower() in ['e']:
                    cmdline=cmd.split(",")
                    ct=len(cmdline)

                    if ct > 1 and ct == 3:
                        with Session(self.engine) as session:
                            tsid=int(cmdline[2])
                            ts=session.query(TouchStamp).filter(TouchStamp.TouchStampId==tsid).first()
                            if ts:
                                note=input("Note: ")
                                if note.startswith("+"):
                                    ts.Note+=note
                                elif note.endswith("+"):
                                    ts.Note=note+ts.Note
                                elif note.startswith("-"):
                                    ts.Note.replace(note,' '*len(note))
                                else:
                                    ts.Note=note
                                print(ts)
                            else:
                                print(f"No Such TouchStampId!")
                            session.commit()
                    else:
                        while True:
                            try:
                                with Session(self.engine) as session:
                                    def mkT(text,self):
                                        try:
                                            return int(text)
                                        except Exception as e:
                                            return None
                                    tsid=Prompt.__init2__(None,func=mkT,ptext="TouchStampId",helpText="The TouchStampId for the Entry you wish to edit!",data=self)
                                    if tsid in [None,]:
                                        break
                                    ts=session.query(TouchStamp).filter(TouchStamp.TouchStampId==tsid).first()
                                    if ts:
                                        note=input("Note: ")
                                        if note.startswith("+"):
                                            ts.Note+=note[1:]
                                        elif note.endswith("+"):
                                            ts.Note=note[:-1]+ts.Note
                                        elif note.startswith("-"):
                                            ts.Note=ts.Note.replace(note[1:],'')
                                        else:
                                            ts.Note=note
                                        print(ts)
                                    else:
                                        print(f"No Such TouchStampId!")
                                    session.commit()
                                    break
                            except Exception as e:
                                print(e)
                elif cmd.split(",")[0].lower() in ['l']:
                    cmdline=cmd.split(",")
                    ct=len(cmdline)
                    if ct == 1:
                        with Session(self.engine) as session:
                            results=session.query(TouchStamp).all()
                            ct=len(results)
                            for num,i in enumerate(results):
                                print(f"{num}/{ct} -> {i}")
                    elif ct > 1 and ct == 2:
                       with Session(self.engine) as session:
                            results=session.query(TouchStamp).filter(TouchStamp.TouchStampId==int(cmdline[1])).all()
                            ct=len(results)
                            for num,i in enumerate(results):
                                print(f"{num}/{ct} -> {i}")
                    elif ct > 1 and ct == 3:
                        field=cmdline[1]
                        if field not in ['Timestamp',]:
                            if field == 'Note':
                                with Session(self.engine) as session:
                                    results=session.query(TouchStamp).filter(TouchStamp.Note.icontains(cmdline[2].lower())).all()
                                    ct=len(results)
                                    for num,i in enumerate(results):
                                        print(f"{num}/{ct} -> {i}")
                                    print(f"Total Results {ct}")
                            elif field == "TouchStampId":
                                with Session(self.engine) as session:
                                    results=session.query(TouchStamp).filter(TouchStamp.TouchStampId==int(cmdline[2])).all()
                                    ct=len(results)
                                    for num,i in enumerate(results):
                                        print(f"{num}/{ct} -> {i}")
                                    print(f"Total Results {ct}") 
                            else:
                                print("Unsupported Field to Search!")
                        #list items by searching field
                    else:
                        print(self.helpTxt)
                        #prompt for field to search
                        #print relevant touchstamps
                
        except Exception as e:
            print(e)
        except Exception as e:
            print(e)

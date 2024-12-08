#Prompt.py
from colored import Fore,Style,Back
import random
import re,os,sys
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DatePicker import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes import VERSION
import inspect,string
import json
from pathlib import Path
from datetime import date,time,datetime
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *


def FormBuilder(data,extra_tooling=False):
    index=None
    item={}
    for num,k in enumerate(data.keys()):
        item[k]=data[k]['default']
    review=False
    finalize=False
    while True:
        if finalize:
            break
        while True:
            if finalize:
                break
            for num,k in enumerate(data.keys()):
                if isinstance(index,int):
                    if num < index:
                        continue
                    else:
                        index=None
                ht=''
                if data[k]['type'].lower() in ['date','datetime','time']:
                    ht="type 'y' or 'n' to start"
                elif data[k]['type'].lower() in ['list']:
                    ht="type your $DELIMITED list, the you will be asked for $DELIMITED character to use!"
                elif data[k]['type'].lower() in ['bool','boolean']:
                    ht="type y|yes|t|true|1 for yes/True, and n|no|0|false|f for no/False"
                cmd=None
                if data[k]['type']=='str+':
                    while True:
                        lines=[]
                        while True:
                            line=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"You(m):{item.get(k)}|Default(d):{data[k]['default']} Field:{str(k)}",helpText=f'{ht}\nuse {Fore.light_red}{Style.bold}{Back.grey_50}#done#{Style.reset} to stop.',data=data[k]['type'][:-1])
                            if line.lower() in ['#done#',]:
                                break
                            if line.lower() == 'd':
                                line='\n'
                            else:
                                if len(line) in [i for i in range(7,14)]:
                                    with Session(ENGINE) as session:
                                        possible=session.query(Entry).filter(or_(Entry.Barcode==line,Entry.Barcode.icontains(line),Entry.Code==line,Entry.Code.icontains(line))).all()
                                        if len(possible) > 0:
                                            line+="\nBarcode/Code Matches found Below\n"+f"{'-'*len('Barcode/Code Matches found Below')}\n"
                                            for num,i in enumerate(possible):
                                                line+=i.seeShortRaw()+"\n"

                            lines.append(line)
                        cmd='\n'.join(lines)
                        use=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{cmd}\nUse? [y/n]",helpText="type something that can be represented as a boolean, this includes boolean formulas used in if/if-then statements(True=y/1/t/true/yes/1==1,False=n/no/0/f/false/1==0)",data="boolean")
                        if use in [None,]:
                            return
                        elif use:
                            break
                        else:
                            continue
                else:
                    cmd=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"You(m):{item.get(k)}|Default(d):{data[k]['default']} Field:{str(k)}",helpText=f'{ht}',data=data[k]['type'])
                if cmd in [None,]:
                    return
                elif isinstance(cmd,str):
                    if cmd.lower() in ['p',]:
                        if num == 0:
                            index=len(data.keys())-1
                        else:
                            index=num-1
                        break
                    elif cmd.lower() in ['d',]:
                        item[k]=data[k]['default']
                    elif cmd.lower() in ['f','finalize']:
                        finalize=True
                        break
                    elif cmd.lower() in ['m',]:
                        print(f"Not changing User set value '{k}':'{item.get(k)}'")
                        pass
                    else:
                        item[k]=cmd
                else:
                    item[k]=cmd
        review=Prompt.__init2__(None,func=FormBuilderMkText,ptext="review?",helpText="",data="bool")
        #print(review)
        if review in [None,]:
            return 
        elif review in [True,'d']:
            finalize=False
            continue
        else:
            break
    if extra_tooling == True:
        tmp_item={str(num):item[i] for num,i in enumerate(item)}
        #ask if extra data is needed
        count=len(tmp_item)
        while True:
            nkv=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"New Key:Value Pair",helpText="yes or no",data="boolean")
            if nkv in ['d',True]:
                key=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"default[{count}] Key",helpText="yes or no",data="string")
                if key in [None,]:
                    continue
                elif key in ['d',]:
                    key=str(count)
                value=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Value",helpText="data text",data="string")
                if value in [None,]:
                    continue
                tmp_item[key]=value
                count+=1
            else:
                break
        #loop through lines for removal
        final_result={}
        for k in tmp_item:
            keep=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"['{tmp_item[k]}'] keep?",helpText="yes or no",data="boolean")
            if keep in ['d',True]:    
                final_result[k]=tmp_item[k]
        return final_result
    return item            

'''
form=FormBuilder(data=fm_data)
print(form)
'''
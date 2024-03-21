# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 19:03:46 2023

@author: OzSea
"""

import pandas as pd
import os
import time
from datetime import datetime ,timedelta
import numpy as np
# Specify the path to your CSV file
dirname = os.path.dirname(__file__)
#path_svg = os.path.join(dirname, 'pages\SVG\OpenScreenLogo.svg')

global Lexicon
rootPath=r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\הערות פיתוח פנימי\data'
#DataPath=r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\python_codes\Data\data.xlsx'
DataPath=os.path.join(dirname, 'Data/data.xlsx')
checkWork='checkWork -30.12.23.xlsx'
checkWorkPath=os.path.join(dirname, 'Data',checkWork)
Table_actions=pd.read_excel(os.path.join(dirname,'Data',checkWork),sheet_name='actions')
Table_tech=pd.read_excel(os.path.join(dirname,'Data',checkWork),sheet_name='techniques')
Table_Level=pd.read_excel(os.path.join(dirname,'Data',checkWork),sheet_name='levels')


#CSVFiles=os.listdir(rootPath)



#Table_actions=pd.read_excel(r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\הערות פיתוח פנימי\checkWork - 25.06.23.xlsx',sheet_name='actions')
#Table_tech=pd.read_excel(r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\הערות פיתוח פנימי\checkWork - 25.06.23.xlsx',sheet_name='techniques')
#Table_Level=pd.read_excel(r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\הערות פיתוח פנימי\checkWork - 25.06.23.xlsx',sheet_name='levels')

Lexicon=pd.DataFrame({'technic number':list(Table_tech['מספר טכניקה']),
               'technic name':list(Table_tech['שם טכניקה']),
               'total times from start':np.zeros(len(Table_tech['שם טכניקה'])),
               'total times in one week':np.zeros(len(Table_tech['שם טכניקה'])),
               'total times in 4 weeks':np.zeros(len(Table_tech['שם טכניקה']))})


def Lexicon1():
    L=pd.DataFrame({'technic number':list(Table_tech['מספר טכניקה']),
                   'technic name':list(Table_tech['שם טכניקה'])})
    
    for i in range(len(Table_tech)):
        L={}
        pass
    
def ReadCSV(roothPathPath,filename): 
    csv_file_path =os.path.join(rootPath,filename)
    # Read the CSV file into a pandas DataFrame
    return pd.read_csv(csv_file_path)

def ReadData(sheet_name):
    
    pass

    
# Display the DataFrame

def complience(V,userid,date):
    #Comp is complience list of [all time,7days,30days]
    Comp=list()
    Comp.append(len(V['Session'].query('endSession <= @date[0]  and userId == @userid'))/(2*100)*100)
    Comp.append(len(V['Session'].query('endSession <= @date[0] and endSession >= @date[1] and userId == @userid'))/(2*7)*100)
    Comp.append(len(V['Session'].query('endSession <= @date[0] and endSession >= @date[2] and userId == @userid'))/(2*28)*100)
    return Comp
def complience1(V,userid,date):
    #Comp1 is the number of days for atlist one practice a day ,list of [all time,7days,30days]
    Comp1=list()
    for i in range(len(date)):
        c=list(str())
        if i==0:
            a=V['Session'].query('endSession < @date[0] and userId == @userid')
        else:
            a=V['Session'].query('endSession < @date[0] and endSession > @date[@i] and userId == @userid')
        for n in list(a.endSession):
            if n:
                c.append(n[0:10])    
        Comp1.append(len(set(c)))
    return Comp1
    
def AvaragePractiseTime(V,userid,date):
    APT=list() # Average practis time in second for[all,7days,30days]
    for i in range(len(date)):
        if i==0:
            a=V['Exercise'].query('dateStart < @date[0]  and dateEnd and userId == @userid')
        else:
            a=V['Exercise'].query('dateStart < @date[0] and dateStart > @date[@i] and dateEnd and userId == @userid')
        apt=0
        #N=datetime.strptime(a.iloc[0].start_session,"%Y-%m-%d %H:%M:%S")-datetime.strptime(a.iloc[-1].start_session,"%Y-%m-%d %H:%M:%S")
        if len(a)>0:
            #N=datetime.strptime(date[0],"%Y-%m-%d")-datetime.strptime(a.iloc[0].dateStart,"%Y-%m-%d %H:%M:%S")
            D=[]
            for d in a.dateEnd:D.append(str(datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date()))
            N=len(list(set(D)))
           
            for j in range(len(a)):
                t1=datetime.strptime(a.iloc[j].dateStart,"%Y-%m-%d %H:%M:%S")
                t2=datetime.strptime(a.iloc[j].dateEnd,"%Y-%m-%d %H:%M:%S")
                apt+=(t2-t1).seconds/60/N
            APT.append((apt))
        else:
            APT.append(0)
    return(APT)

    
def technics(V,userName,date):
    userid=int(V['App_user'].id[V['App_user'].username==int(userName)].values)
    #tech=list()
    tech=Lexicon
    for i in range(0,len(date)):
        
        if i==0:
            a=V['Exercise'].query('dateStart <= @date[0]  and dateEnd and userId == @userid')
        else:
            a=V['Exercise'].query('dateStart <= @date[0] and dateStart >= @date[@i] and dateEnd and userId == @userid')
        temp=a.actionId.value_counts()
        '''
        if i==0:
            a=V['ActionFinish'].query('dateFinish <= @date[0]   and userId == @userid')
        else:
            a=V['ActionFinish'].query('dateFinish <= @date[0] and dateFinish >= @date[@i] and userId == @userid')
        '''
        #temp=a.action_id.value_counts() 
        # for k in range(len(tech)):
        #     b=Table_actions[Table_actions.keys()[2]]==k+1
        #     A1=(Table_actions[Table_actions.keys()[0]][b]).values
        #     tech[tech.keys()[i+2]][k]=sum(a['actionId'].isin(A1))
            
        for k in tech[tech.keys()[0]]:
            b=Table_actions[Table_actions.keys()[2]]==k
            A1=(Table_actions[Table_actions.keys()[0]][b]).values
            tech[tech.keys()[i+2]][tech[tech[tech.keys()[0]]==k].index]=sum(a['actionId'].isin(A1))
    return(tech)

def Level_Lag_in_days(V,userid,date):
    t=V['Session'].query('userId == @userid')
    if len(t)>0:
        N=(datetime.strptime(date[0],"%Y-%m-%d")-datetime.strptime(t.iloc[0].startSession,"%Y-%m-%d %H:%M:%S")).days
        a=V['PositionLevel'].query('userId==@userid')
        Level=int(a.iloc[0].levelId)
        if Level>1:
            temp=(datetime.strptime(date[0],"%Y-%m-%d")-datetime.strptime(a.iloc[0].startLevel,"%Y-%m-%d %H:%M:%S"))
        else:
            temp=(datetime.strptime(date[0],"%Y-%m-%d")-datetime.strptime(t.iloc[0].startSession,"%Y-%m-%d %H:%M:%S"))
        Lags_in_days=max(temp.days-Table_Level.iloc[int(a.iloc[0].levelId-1)][Table_Level.keys()[2]],0)
        Level=int(a.iloc[0].levelId)
        Total_Lags=max(N-sum(Table_Level.iloc[0:int(a.iloc[0].levelId)][Table_Level.keys()[2]]),0)
        weeks=(N/7)
    else:
         Level=np.nan
         Lags_in_days=np.nan
         Total_Lags=np.nan
         weeks=np.nan
    
    return(Level,weeks,Lags_in_days,Total_Lags)
    
def Power(n1,n2):
    D=n1-n2
    if D<=0:
        P=D*n2
    else:
        P=D*(10-n2)
    return P
           

def Index(V,userid,date,TypeSession,Patient):
    #INDX0=list()
    #for i in range(len(date)):
    sud1=list();sud2=list();sudPower=list()
    vas1=list();vas2=list();vasPower=list()
    fat1=list();fat2=list();fatPower=list()
    well1=list();well2=list();wellPower=list()
    Dateslist=list()
    #Temp={}
    
    if Patient=='.....' :
        N=8
    else:
        try:
            t=V['Session'].query('userId == @userid')
            N=(datetime.strptime(date[0],"%Y-%m-%d")-datetime.strptime(t.iloc[0].startSession,"%Y-%m-%d %H:%M:%S")).days+3
            if N<=1:
                N=2
        except:
            N=2
    #D=datetime.strptime(date[0], "%Y-%m-%d")
    #D=str(D.date())        
    #Dateslist.append(D)        
    for j in range(1,N):
        #D=datetime.strptime(date[0], "%Y-%m-%d")-timedelta(days=j)
        #D=str(D.date())
        D1=datetime.strptime(date[0], "%Y-%m-%d")-timedelta(days=j-1)
        D=D1-timedelta(days=1)
        D=str(D.date())
        D1=str(D1.date())
        Dateslist.append(D)
        a=V['Session'].query('endSession >@D and endSession <= @D1 and userId == @userid and typeSession==@TypeSession')
        #print(a)
        if len(a)>0:
            #sud1.append(a.iloc[0].sudsQ1) ;sud2.append(a.iloc[0].sudsQ2);sudPower.append(a.iloc[0].sudsQ2*(a.iloc[0].sudsQ1-a.iloc[0].sudsQ2))
            #vas1.append(a.iloc[0].vasQ1) ;vas2.append(a.iloc[0].vasQ2);vasPower.append(a.iloc[0].vasQ2*(a.iloc[0].vasQ1-a.iloc[0].vasQ2))
            #fat1.append(a.iloc[0].fatigueQ1) ;fat2.append(a.iloc[0].fatigueQ2);fatPower.append(a.iloc[0].fatigueQ2*(a.iloc[0].fatigueQ1-a.iloc[0].fatigueQ2))
            #well1.append(a.iloc[0].well_beingQ1) ;well2.append(a.iloc[0].well_beingQ2);wellPower.append(-a.iloc[0].well_beingQ2*(a.iloc[0].well_beingQ1-a.iloc[0].well_beingQ2))
            
            sud1.append(a.iloc[0].sudsQ1) ;sud2.append(a.iloc[-1].sudsQ2);sudPower.append(Power(a.iloc[0].sudsQ1,a.iloc[-1].sudsQ2))
            vas1.append(a.iloc[0].vasQ1) ;vas2.append(a.iloc[-1].vasQ2);vasPower.append(Power(a.iloc[0].vasQ1,a.iloc[-1].vasQ2))
            fat1.append(a.iloc[0].fatigueQ1) ;fat2.append(a.iloc[-1].fatigueQ2);fatPower.append(Power(a.iloc[0].fatigueQ1,a.iloc[-1].fatigueQ2))
            well1.append(a.iloc[0].well_beingQ1) ;well2.append(a.iloc[-1].well_beingQ2);wellPower.append(Power(10-a.iloc[0].well_beingQ1,10-a.iloc[-1].well_beingQ2))
            
            #Temp.update({str("%s%d" % ('befor_',j)):[a.iloc[0].sudsQ1],
            #      str("%s%d" % ('after_',j)):[a.iloc[0].sudsQ2],str("%s%d"%('poewr_',j)):[a.iloc[0].sudsQ1*(a.iloc[0].sudsQ1-a.iloc[0].sudsQ2)]})
        else:
            sud1.append(np.nan);sud2.append(np.nan);sudPower.append(np.nan)
            vas1.append(np.nan);vas2.append(np.nan);vasPower.append(np.nan)
            fat1.append(np.nan);fat2.append(np.nan);fatPower.append(np.nan)
            well1.append(np.nan);well2.append(np.nan);wellPower.append(np.nan)
            #Temp.update({str("%s%d" % ('befor_',j)):[np.nan],
            #      str("%s%d" % ('after_',j)):[np.nan],str("%s%d"%('poewr_',j)):[np.nan]})
    table1=pd.DataFrame({'sud1':sud1,'sud2': sud2,'sud power': sudPower,
                         'vas1':vas1,'vas2': vas2,'vas power': vasPower,
                         'fat1':fat1,'fat2': fat2,'fat power': fatPower,
                         'well1':well1,'well2': well2,'well power': wellPower},index=Dateslist)
    return(table1)

def Extract_Exercise_information(T,V,Session_Id):
    Total_time=0
    Actions_list=str()
    #Session_Id=1328
    Exercise_list=list(V['list_exercises_ids'].query('sessionId==@Session_Id')['list_exercises_ids'])
    for i in Exercise_list:
        if V['Exercise'].query('exerciseId==@i')['dateEnd'].iloc[0] ==V['Exercise'].query('exerciseId==@i')['dateEnd'].iloc[0]:
            # List of Action
            Action_id=(int((V['Exercise'].query('exerciseId==@i')['actionId']).iloc[0]))
            Action_Name=T['actions'].query('Action_Number == @Action_id')['Action_Name'].iloc[0]
            #Actions_list.append(str(Action_id)+'-'+Action_Name)
            Actions_list+=str(Action_id)+'-'+Action_Name+'\n'
            
            #total time calculation
            Endtime=datetime.strptime((V['Exercise'].query('exerciseId==@i')['dateEnd']).iloc[0],"%Y-%m-%d %H:%M:%S")
            Starttime=datetime.strptime((V['Exercise'].query('exerciseId==@i')['dateStart']).iloc[0],"%Y-%m-%d %H:%M:%S")
            Total_time+=(Endtime-Starttime).seconds//60
    return(Actions_list,Total_time)    
    

def Patient_Records(T,V,Patient):
    userid=float(V['App_user'].id[V['App_user'].username==int(Patient)].values)
    # sud1=list();sud2=list();sudPower=list()
    # vas1=list();vas2=list();vasPower=list()
    # fat1=list();fat2=list();fatPower=list()
    # well1=list();well2=list();wellPower=list()
    # Dateslist=list()
    table=dict()
    #Temp={}
    GroupType=''
    Level=''
    if Patient=='.....' :
        N=8
    else:
        #try:
            t=V['Session'].query('userId == @userid')
            Level=V['PositionLevel'].query('userId == @userid')['levelId'].iloc[0]
            if V['App_user'].query('id == @userid')['groupType'].iloc[0]=='C':
                GroupType='Control'
            elif V['App_user'].query('id == @userid')['groupType'].iloc[0]=='E':
                GroupType='Experimental'
        #     N=(datetime.strptime(date[0],"%Y-%m-%d")-datetime.strptime(t.iloc[0].startSession,"%Y-%m-%d %H:%M:%S")).days+3
        #     if N<=1:
        #         N=2
        # #except:
        #     N=2
    table=dict()        
    tableE=dict()
    tableM=dict()        
    Today=datetime.now().date
    Ne_practic=0
    Nm_practic=0
    Actions_list={'Evening':str(),'Morning':str()}   # Evening , Morning
    Total_time={'Evening':0,'Morning':0}
    SudE=list() ; SudM=list();vasE=list() ; vasM=list();fatE=list() ; fatM=list();wellE=list() ; wellM=list();
    j=-1;        
    while j <len(t)-1:
        j+=1
        N=(Today()-(datetime.strptime(t.iloc[j].startSession,"%Y-%m-%d %H:%M:%S")).date()).days
        
        if N==0:
            # appdate suds list
            if t['typeSession'].iloc[j]=='Evening':
                Ne_practic+=1
                SudE.append([t['sudsQ1'].iloc[j],t['sudsQ2'].iloc[j]])
                vasE.append([t['vasQ1'].iloc[j],t['vasQ2'].iloc[j]])
                fatE.append([t['fatigueQ1'].iloc[j],t['fatigueQ2'].iloc[j]])
                wellE.append([t['well_beingQ1'].iloc[j],t['well_beingQ2'].iloc[j]])
                Session_Id=int(t['sessionId'].iloc[j])
                AL,Tt=Extract_Exercise_information(T,V,Session_Id)
                #if Tt!=0:
                Actions_list['Evening']+=AL
                Total_time['Evening']+=Tt
            else:
                Nm_practic+=1
                SudM.append([t['sudsQ1'].iloc[j],t['sudsQ2'].iloc[j]])
                vasM.append([t['vasQ1'].iloc[j],t['vasQ2'].iloc[j]])
                fatM.append([t['fatigueQ1'].iloc[j],t['fatigueQ2'].iloc[j]])
                wellM.append([t['well_beingQ1'].iloc[j],t['well_beingQ2'].iloc[j]])
                Session_Id=int(t['sessionId'].iloc[j])
                AL,Tt=Extract_Exercise_information(T,V,Session_Id)
                #if Tt!=0:
                Actions_list['Morning']+=AL
                Total_time['Morning']+=Tt
            #print((datetime.strptime(t.iloc[j].startSession,"%Y-%m-%d %H:%M:%S")).date())
            #print(j)
        else:
            if Ne_practic:
                table[str(Today())+' E']={'Action list':Actions_list['Evening'],
                                          'Total time':Total_time['Evening'],'Number Of Sessions':Ne_practic,
                                          'SUDS':SudE,'Pain':vasE,'Fatigue':fatE,'Well-being':wellE
                                      }
                tableE[str(Today())]={'SUDS':SudE,'Pain':vasE,'Fatigue':fatE,'Well-being':wellE,
                                      'Action list':Actions_list['Evening'],'Total time':Total_time['Evening'],
                                      'Number Of Sessions':Ne_practic}
            if Nm_practic:
                table[str(Today())+' M']={'Action list':Actions_list['Morning'],
                                          'Total time':Total_time['Morning'],'Number Of Sessions':Nm_practic,
                                          'SUDS':SudM,'Pain':vasM,'Fatigue':fatM,'Well-being':wellM
                                          }
                                      
                tableM[str(Today())]={'SUDS':SudM,'Pain':vasM,'Fatigue':fatM,'Well-being':wellM,
                                      'Action list':Actions_list['Morning'],'Total time':Total_time['Morning'],
                                      'Number Of Sessions':Nm_practic}
            Today=(datetime.strptime(t.iloc[j].startSession,"%Y-%m-%d %H:%M:%S")).date
            j-=1
            Ne_practic=0
            Nm_practic=0
            SudE=list() ; SudM=list();vasE=list() ; vasM=list();fatE=list() ; fatM=list();wellE=list() ; wellM=list();
            Actions_list={'Evening':str(),'Morning':str()}   # Evening , Morning
            Total_time={'Evening':0,'Morning':0}       
            
    if Ne_practic:
        table[str(Today())+' E']={'Action list':Actions_list['Evening'],
                                  'Total time':Total_time['Evening'],'Number Of Sessions':Ne_practic,
                                  'SUDS':SudE,'Pain':vasE,'Fatigue':fatE,'Well-being':wellE
                              }
        tableE[str(Today())]={'SUDS':SudE,'Pain':vasE,'Fatigue':fatE,'Well-being':wellE,
                              'Action list':Actions_list['Evening'],'Total time':Total_time['Evening'],
                              'Number Of Sessions':Ne_practic}
    if Nm_practic:
        table[str(Today())+' M']={'Action list':Actions_list['Morning'],
                                  'Total time':Total_time['Morning'],'Number Of Sessions':Nm_practic,
                                  'SUDS':SudM,'Pain':vasM,'Fatigue':fatM,'Well-being':wellM
                                  }
                              
        tableM[str(Today())]={'SUDS':SudM,'Pain':vasM,'Fatigue':fatM,'Well-being':wellM,
                              'Action list':Actions_list['Morning'],'Total time':Total_time['Morning'],
                              'Number Of Sessions':Nm_practic}      
    # #D=datetime.strptime(date[0], "%Y-%m-%d")
    # #D=str(D.date())        
    # #Dateslist.append(D)        
    # for j in range(1,N):
    #     #D=datetime.strptime(date[0], "%Y-%m-%d")-timedelta(days=j)
    #     #D=str(D.date())
    #     D1=datetime.strptime(date[0], "%Y-%m-%d")-timedelta(days=j-1)
    #     D=D1-timedelta(days=1)
    #     D=str(D.date())
    #     D1=str(D1.date())
    #     Dateslist.append(D)
    #     a=V['Session'].query('endSession >@D and endSession <= @D1 and userId == @userid and typeSession==@TypeSession')
    #     #print(a)
    #     if len(a)>0:
    #         #sud1.append(a.iloc[0].sudsQ1) ;sud2.append(a.iloc[0].sudsQ2);sudPower.append(a.iloc[0].sudsQ2*(a.iloc[0].sudsQ1-a.iloc[0].sudsQ2))
    #         #vas1.append(a.iloc[0].vasQ1) ;vas2.append(a.iloc[0].vasQ2);vasPower.append(a.iloc[0].vasQ2*(a.iloc[0].vasQ1-a.iloc[0].vasQ2))
    #         #fat1.append(a.iloc[0].fatigueQ1) ;fat2.append(a.iloc[0].fatigueQ2);fatPower.append(a.iloc[0].fatigueQ2*(a.iloc[0].fatigueQ1-a.iloc[0].fatigueQ2))
    #         #well1.append(a.iloc[0].well_beingQ1) ;well2.append(a.iloc[0].well_beingQ2);wellPower.append(-a.iloc[0].well_beingQ2*(a.iloc[0].well_beingQ1-a.iloc[0].well_beingQ2))
            
    #         sud1.append(a.iloc[0].sudsQ1) ;sud2.append(a.iloc[-1].sudsQ2);sudPower.append(Power(a.iloc[0].sudsQ1,a.iloc[-1].sudsQ2))
    #         vas1.append(a.iloc[0].vasQ1) ;vas2.append(a.iloc[-1].vasQ2);vasPower.append(Power(a.iloc[0].vasQ1,a.iloc[-1].vasQ2))
    #         fat1.append(a.iloc[0].fatigueQ1) ;fat2.append(a.iloc[-1].fatigueQ2);fatPower.append(Power(a.iloc[0].fatigueQ1,a.iloc[-1].fatigueQ2))
    #         well1.append(a.iloc[0].well_beingQ1) ;well2.append(a.iloc[-1].well_beingQ2);wellPower.append(Power(10-a.iloc[0].well_beingQ1,10-a.iloc[-1].well_beingQ2))
            
    #         #Temp.update({str("%s%d" % ('befor_',j)):[a.iloc[0].sudsQ1],
    #         #      str("%s%d" % ('after_',j)):[a.iloc[0].sudsQ2],str("%s%d"%('poewr_',j)):[a.iloc[0].sudsQ1*(a.iloc[0].sudsQ1-a.iloc[0].sudsQ2)]})
    #     else:
    #         sud1.append(np.nan);sud2.append(np.nan);sudPower.append(np.nan)
    #         vas1.append(np.nan);vas2.append(np.nan);vasPower.append(np.nan)
    #         fat1.append(np.nan);fat2.append(np.nan);fatPower.append(np.nan)
    #         well1.append(np.nan);well2.append(np.nan);wellPower.append(np.nan)
    #         #Temp.update({str("%s%d" % ('befor_',j)):[np.nan],
    #         #      str("%s%d" % ('after_',j)):[np.nan],str("%s%d"%('poewr_',j)):[np.nan]})
    
    return (pd.DataFrame.from_dict(table,orient='index'),Level,GroupType)

        
def ActiveUsers(V):
    
    pass
def Table1(V,date,ActiveUsers_id,TypeSession,Patient):
    Table={}
    for user in ActiveUsers_id:
        
        userName=str(V['App_user'].username[V['App_user'].id==user].values)[1:-1]
        Table[userName]=[userName]
        Temp=complience(V,user,date)
        for Z in Temp :Table[userName].append(Z)
        Temp=complience1(V,user,date)
        for Z in Temp :Table[userName].append(Z)
        Temp=Level_Lag_in_days(V,user,date)
        for Z in Temp :Table[userName].append(Z)
        Temp=AvaragePractiseTime(V,user,date)
        for Z in Temp :Table[userName].append(Z)
        Temp=Index(V,user,date,TypeSession,Patient)
        for Z in Temp['sud power'] :Table[userName].append(Z)
        for Z in Temp['vas power'] :Table[userName].append(Z)
        for Z in Temp['fat power'] :Table[userName].append(Z)
        for Z in Temp['well power'] :Table[userName].append(Z)
        
    titles=['AppID','Compliance All[%]','Compliance 7 days [%]','Compliance 4 weeks [%]',
            '<1 practice a day [all]','<1 practice a day [7 days]','<1 practice a day [4 weeks]',
            'Level','weeks from start','Lag days in current Level','Total Lag days',
            'average practice time in minutes[all]','average practice time in minutes[7 days]','average practice time in minutes[4 weeks]',
            'sud 1','sud 2','sud 3','sud 4','sud 5','sud 6','sud 7',
            'vas 1','vas 2','vas 3','vas 4','vas 5','vas 6','vas 7',
            'fat 1','fat 2','fat 3','fat 4','fat 5','fat 6','fat 7',
            'well 1','well 2','well 3','well 4','well 5','well 6','well 7']
    
    Tableall=pd.DataFrame(Table,index=titles)
    return(Tableall)    

def Convert_acount2id(V,userName):
    userID=int(V['App_user'].id[V['App_user'].username==int(userName)].values)
    return userID

def userData(V,date,userName,TypeSession):
    userID=float(V['App_user'].id[V['App_user'].username==int(userName)].values)
    temp=Index(V,userID,date,TypeSession,userName)

    return(temp)

def UnImprove(table1,N):
    for n in range(N,1,-1):
        #print(n)
        if sum((table1.well2[0:n]-table1.well1[0:n])<=0)+(table1.well2[0:n]-table1.well1[0:n]).isna().sum()>=n:
            if sum((table1.sud1[0:n]-table1.sud2[0:n])<0)+(table1.sud1[0:n]-table1.sud2[0:n]).isna().sum()>=n:
                return(True,n)
            elif sum((table1.fat1[0:n]-table1.fat2[0:n])<0)+(table1.fat1[0:n]-table1.fat2[0:n]).isna().sum()>=n:
                return(True,n)
            elif sum((table1.vas1[0:n]-table1.vas2[0:n])<0)+(table1.vas1[0:n]-table1.vas2[0:n]).isna().sum()>=n:
                return(True,n)
            #else:
            #    return(False,i)
        #else:
    return(False,n)

def InLevelAdviseList(Level,tec):
    #this function get level and table of practiced technics and returen the less practice action numbers
    # at the current level in the last week 
    n1=str(Level)
    n2=str(Level+1)
    a=Table_actions.query('`מספר סידורי` >= @n1 and `מספר סידורי` < @n2')
    tecNumberMin=min(a.iloc[:,2])
    tecNumberMax=max(a.iloc[:,2])
    b=tec.query('`technic number`>=@tecNumberMin and `technic number`<=@tecNumberMax')
    AdvicedTechNumber=b.iloc[b.iloc[:,3].idxmin(),0] # the less technic that was practice in the last week
    # for last week is 3 , last 4 weeks is 4 and all time us 2
    return(list(a.iloc[a.set_index(a.iloc[:,2]).index.get_loc(AdvicedTechNumber),0]))
    
def OutLevelAdviseList(Level,tec):
    n1=str(Level)
    n2=str(Level+1)
    a=Table_actions.query('`מספר סידורי` <= @n1')
    tecNumberMin=min(a.iloc[:,2])
    tecNumberMax=max(a.iloc[:,2])
    b=tec.query('`technic number`<=@tecNumberMax')
    AdvicedTechNumber=b.iloc[b.iloc[:,3].idxmin(),0] # the less technic that was practice in the last week
    return(list(a.iloc[a.set_index(a.iloc[:,2]).index.get_loc(AdvicedTechNumber),0]))
    


def advisor(userName,V,date,TypeSession):
    userID=float(V['App_user'].id[V['App_user'].username==int(userName)].values)
    a=V['PositionLevel'].query('userId==@userID')
    Level=int(a.iloc[0].levelId)
    TypeSession='Morning'
    table1=userData(V,date,userName,TypeSession)
    tec=technics(V,userName,date)
    Yes,n=UnImprove(table1,13)
    print(n)
    if Yes and n==13:
        return(OutLevelAdviseList(Level,tec))
        
        #tec=DB.technics(V,'222',date)
    elif  Yes and n<13 and n>=7:
        return(InLevelAdviseList(Level,tec))
    elif  Yes and n<7 and n>3:
        return(OutLevelAdviseList(Level,tec))
    elif  n<=3:
        return(InLevelAdviseList(Level,tec))
    
    
        pass
        
    
    

    
def start():
    
    # V = {}
    # for filename in CSVFiles:    
    #    V[filename[:-4]]=ReadCSV(rootPath,filename)
    V={}
    #xls = pd.ExcelFile(DataPath)
    xls = pd.ExcelFile('http://ec2-3-69-87-195.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel')
    for sheet_name in xls.sheet_names:
        V[sheet_name]= xls.parse(sheet_name)
    ActiveUsers_id=list(set(V['ActionFinish'].userId))
    date=[str(datetime.now().date()),str(datetime.now().date()-timedelta(days=7)),
          str(datetime.now().date()-timedelta(days=28))]

    xls.close()   
    
    T={}
    xls = pd.ExcelFile(checkWorkPath)
    for sheet_name in xls.sheet_names:
        T[sheet_name]= xls.parse(sheet_name)
    xls.close()
    T['actions'].rename(columns = {T["actions"].keys()[0]:'Action_Number'}, inplace = True)
    T['actions'].rename(columns = {T["actions"].keys()[1]:'Action_Name'}, inplace = True)  
    #date=[str(datetime.now().date()),"2023-07-08","2023-07-15"]
    userid=175
    
    #complience(V,userid,date)
    #complience1(V,userid,date)
    #V['session'].query('end_session > @date[0] and end_session < @date[1] and user_id == @userid')
    
    #tech=technics(V,userid,date)
    return(T,V,date,userid,ActiveUsers_id)
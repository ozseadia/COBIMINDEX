# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 08:31:49 2023

@author: OzSea
"""

import os
import time
from datetime import timedelta ,datetime 
import openpyxl
import streamlit as st
import DataBase as DB
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px 
import DeshbordAPP as De

st.set_page_config(page_title="Patient details settings", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
#path_svg=(r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\python_codes\pages\SVG\OpenScreenLogo.svg')
De.render_svg(De.read_svg())
S_options=['...',
           'Naama Peled-Ironi',
           'Milca Hanukoglu',
           'Helen Israel',
           'Adi Vilensky',
           'Noa Schultz',
           'Oneg Kabizon',
           'Shachar Michael',
           'Zohar Peled-Zinger',
           'Noa Shultz','Hila Askayo','Ganit Goren']

SW=st.sidebar.selectbox('Assigned Coordinator/Therapist',S_options)
rootPath=r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\python_codes'
filename=os.path.join(rootPath,'Data/acount and passwords.xlsx')
Table_acounts=pd.read_excel(filename)

def highlight_max(x, color):
    return np.where(x <=-10, "background-color: {color}", None)

def highlight_cols(s):
    color = 'red' if s < 0 else ''
    return 'background-color: % s' % color

def highlight_cols1(s):
    color = 'red' if s > 2 else ''
    return 'background-color: % s' % color

def Chart_data(Table2):
    Temp=pd.DataFrame(columns=['Value'])
    Temp['Value']=pd.concat([Table2['sud power'],Table2['vas power'],Table2['fat power'],Table2['well power']])
    df1=pd.DataFrame(columns=['Ind','Date'])
    df1['Ind']=pd.DataFrame(['sud']*len(Table2)+['vas']*len(Table2)+['fat']*len(Table2)+['well']*len(Table2),
                     index=Temp['Value'].index)
    df1['Date']=list(Temp.index)
    C_data=pd.concat([Temp['Value'],df1['Ind'],df1['Date']],axis="columns")
    C=alt.Chart(C_data).mark_bar().encode(
    x='Ind:O',
    y='Value:Q',
    color='Ind:N',
    column='Date:N')
    return(C)

def Ploty(Table2,Ind):
    plot=px.bar(x=Table2.index,y=Table2[Ind])
    #plot['layout']['xaxis']['autorange'] = "reversed"
    return plot

def PlotyMulty(Table2,Ind):
    plot=px.line(x=Table2.index,y=Table2[Ind])
    return(plot)
    pass

    
def ComplinesTable(TABLE):
    ind=list(range(0,13))
    return(TABLE.iloc[ind])

def IndexTable(TABLE):
    ind=list(range(13,len(TABLE)))
    return(TABLE.iloc[ind])
def Extract_Patien_List():
    a=Table_acounts.query('Therapist==@SW or Coordinator==@SW')
    return a['acount']
    
st.title('Dash Board')
V,date,userid,ActiveUsers_id=DB.start()
if not(SW=='...'):
    PatientList=Extract_Patien_List()
    ids_List=[]
    for temp in PatientList:
        ids_List.append(DB.Convert_acount2id(V,temp))
    TABLE=DB.Table1(V,date,ids_List,'Morning','.....')
#TABLE.style.apply(highlight_max, color='red')
    placeholder1 = st.empty()
    with placeholder1.container():
        st.subheader(" :woman-running: :runner: Patients' Complince table")
        Tc=ComplinesTable(TABLE)
        st.dataframe(Tc.style.applymap(highlight_cols1,
                                       subset = pd.IndexSlice[['Lag days in current Level','Total Lag days'],:]).set_precision(0))
        st.subheader("Patients' Index table")
        col1,col2 = st.columns([1,3])
        with col1:
            TypeSession=st.selectbox('Select Morning or Evenining :sun_with_face:/:first_quarter_moon_with_face:',['Morning','Evening'])
        TABLE=DB.Table1(V,date,ids_List,TypeSession,'.....')
        Ti=IndexTable(TABLE)
        st.dataframe(Ti.style.applymap(highlight_cols,
                                       ).set_precision(0))
    

    options=list(TABLE.keys())
    options.insert(0,'.....')
    NAME=st.sidebar.selectbox('Select Patient', options)
    if not (NAME==options[0]):
        placeholder1.empty()
        with placeholder1.container():
            col1,col2 = st.columns([1,3])
            with col1:
                TypeSession=st.selectbox('Please Select Morning or Evenining :sun_with_face:/:first_quarter_moon_with_face:',['Morning','Evening'])
            Table2=DB.userData(V,date,NAME,TypeSession)
            #C=Chart_data(Table2)
            st.title(':chart_with_downwards_trend: :chart_with_upwards_trend: Patient '+ NAME + ' ' + TypeSession+ ' indexes results')
            st.dataframe(Table2.style.applymap(highlight_cols).set_precision(0))
            #st.altair_chart(C)
            st.subheader('SUDS Power')
            plot=Ploty(Table2,'sud power')
            plot=De.PlotyMulty(Table2)
            st.plotly_chart(plot)
            #st.bar_chart(Table2['sud power'])
            st.subheader('VAS Power')
            plot=Ploty(Table2,'vas power')
            st.plotly_chart(plot)
            #st.bar_chart(Table2['vas power'])
            st.subheader('Fatigue Power')
            plot=Ploty(Table2,'fat power')
            st.plotly_chart(plot)
            #st.bar_chart(Table2['fat power'])
            st.subheader('Well being Power')
            plot=Ploty(Table2,'well power')
            st.plotly_chart(plot)
            #st.bar_chart(Table2['well power'])
    
            #st.bar_chart(pd.DataFrame(chart_data))
            #userID=str(V['App_user'].id[V['App_user'].username==int(NAME)].values)[1:-1]
            st.title(':clipboard: Patient '+NAME +' exercises table ')
            Table3=DB.technics(V,NAME,date)
            #df1=Table3.iloc[:, 2:4]
            st.dataframe(Table3.iloc[:,0:5].set_index('technic number').style.hide_index().set_precision(0))
            #st.text(userID)
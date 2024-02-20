# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 22:40:13 2023

@author: OzSea
"""

import streamlit as st
import DataBase as DB
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px 
import plotly.graph_objects as go
from PIL import Image
import re
import base64
import os

global path_svg
dirname = os.path.dirname(__file__)
path_svg = os.path.join(dirname, 'pages/SVG/OpenScreenLogo.svg')


#path_svg=(r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\python_codes\pages\SVG\OpenScreenLogo.svg')
#image = Image.open(SVG_path)
st.set_page_config(page_title="Patient details settings", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

def read_svg(path_svg=os.path.join(dirname, 'pages/SVG/OpenScreenLogo.svg')):
    """Get a SVG file as HTML

    Args:
        path_svg(str): Path of a SVG file
    Returns:
        svg_logo(str): HTML <svg> element
    """

    try:
        with open(path_svg, "r") as file:
            svg_logo = file.read().splitlines()
            _maped_list = map(str, svg_logo)
            svg_logo = "".join(_maped_list)
            temp_svg_logo = re.findall("<svg.*</svg>", svg_logo, flags=re.IGNORECASE)
            svg_logo = temp_svg_logo[0]
    except:  # None
        svg_logo = '<svg xmlns="http://www.w3.org/2000/svg" width="150px" height="1px" viewBox="0 0 150 1"></svg>'

    return svg_logo


def render_svg(svg):
    """Rendering SVG on Streamlit

    Args:
        svg(str): HTML <svg> element
    Returns: None
    """
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = (
        r"""
        <div align="left up">
        <img src="data:image/svg+xml;base64,%s" alt="SVG Image" style="width: 10em;"/>
        </div>
        """
        % b64
    )
    st.markdown(html, unsafe_allow_html=True)




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
def PlotyCandlestick(Table2,Ind):
    #plot=px.bar(x=Table2.index,y=Table2[Ind])
    Topen=Ind+"1"
    Tclose=Ind+"2"
    if Ind=='well':
        plot = go.Figure(data=[go.Candlestick(x=Table2.index,
                    open=Table2[Topen],
                    high=Table2[[Topen,Tclose]].max(axis=1),
                    low=Table2[[Topen,Tclose]].min(axis=1),
                    close=Table2[Tclose],
                    increasing_line_color= 'green', decreasing_line_color= 'red')])
    else:
        plot = go.Figure(data=[go.Candlestick(x=Table2.index,
                    open=Table2[Topen],
                    high=Table2[[Topen,Tclose]].max(axis=1),
                    low=Table2[[Topen,Tclose]].min(axis=1),
                    close=Table2[Tclose],
                    increasing_line_color= 'red', decreasing_line_color= 'green')])
        
    plot.update_layout(xaxis_rangeslider_visible=False)
    f2 = go.FigureWidget(plot)
    #plot['layout']['xaxis']['autorange'] = "reversed"
    return f2
def Ploty(Table2,Ind):
    plot=px.bar(x=Table2.index,y=Table2[Ind])
    #plot['layout']['xaxis']['autorange'] = "reversed"
    return plot
def PlotyMulty(Table2):
    plot=px.line(Table2,x=Table2.index,y=['sud power','vas power','fat power','well power'],markers=True)
    #plot.
    return(plot)
    
def ComplinesTable(TABLE):
    ind=list(range(0,14))
    return(TABLE.iloc[ind])

def IndexTable(TABLE):
    ind=list(range(14,len(TABLE)))
    return(TABLE.iloc[ind])

@st.cache_data
def Start():
    st.session_state['Start']=1
    return (st.session_state['Start'])
@st.cache_data(ttl=3600)
def load_data(temp):
    T,V,date,userid,ActiveUsers_id=DB.start()
    return (T,V,date,userid,ActiveUsers_id)
    
def DataDownload():
    import os
    import shutil
    import webbrowser
    import time

    #url = 'http://ec2-3-123-19-109.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel'

    url='http://ec2-3-69-87-195.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel'
    #webbrowser.open_new(url)
    #time.sleep(10)
    
    button_code = f'''
            <p>
                <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                Download Data 
                </a>
            </p>'''
    
    return st.sidebar.markdown(button_code, unsafe_allow_html=True)
    #shutil.move(r'C:\Users\OzSea.LAPTOP-LLBIIFTU\Downloads\data.xlsx', r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\python_codes\COBIMINDEX\Data\data.xlsx')

    
#st.image(image,width=100) 
#st.markdown("<br>", unsafe_allow_html=True)
#render_svg(read_svg(r"src/undraw_Decide_re_ixfw.svg"))
render_svg(read_svg())
st.title('Dash Board')
T,V,date,userid,ActiveUsers_id=load_data(temp=Start())
#V,date,userid,ActiveUsers_id=DB.start()
TABLE=DB.Table1(V,date,ActiveUsers_id,'Morning','.....')
#TABLE.style.apply(highlight_max, color='red')
placeholder1 = st.empty()
with placeholder1.container():
    st.subheader('Complince table')
    Tc=ComplinesTable(TABLE)
    #Tc.set_precision(0)
    st.dataframe(Tc.style.applymap(highlight_cols1,
                                   subset = pd.IndexSlice[['Lag days in current Level','Total Lag days'],:]).format(precision=0))
    st.subheader('Index table')
    col1,col2 = st.columns([1,3])
    with col1:
        TypeSession=st.selectbox('Select Morning or Evenining :sun_with_face:/:first_quarter_moon_with_face:',['Morning','Evening'])
    TABLE=DB.Table1(V,date,ActiveUsers_id,TypeSession,'.....')
    Ti=IndexTable(TABLE)
    #Ti.set_precision(0)
    st.dataframe(Ti.style.applymap(highlight_cols,
                                   ).format(precision=0))
    

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
        st.dataframe(Table2.style.applymap(highlight_cols).format(precision=0))
        #st.altair_chart(C)
        st.subheader('SUD')
        plot=PlotyCandlestick(Table2,'sud')
        #plot=De.PlotyMulty(Table2)
        st.plotly_chart(plot)
        #st.bar_chart(Table2['sud power'])
        st.subheader('VAS')
        plot=PlotyCandlestick(Table2,'vas')
        st.plotly_chart(plot)
        #st.bar_chart(Table2['vas power'])
        st.subheader('Fatigue')
        plot=PlotyCandlestick(Table2,'fat')
        st.plotly_chart(plot)
        #st.bar_chart(Table2['fat power'])
        st.subheader('Well being')
        plot=PlotyCandlestick(Table2,'well')
        st.plotly_chart(plot)
        #st.bar_chart(Table2['well power'])

        #st.bar_chart(pd.DataFrame(chart_data))
        #userID=str(V['App_user'].id[V['App_user'].username==int(NAME)].values)[1:-1]
        st.title(':clipboard: Patient '+NAME +' exercises table ')
        Table3=DB.technics(V,NAME,date)
        #df1=Table3.iloc[:, 2:4]
        st.dataframe(Table3.iloc[:,0:5].set_index('technic number').style.format(precision=0))
        #st.text(userID)
        
#if st.sidebar.button('Download Data'):
DataDownload()
    
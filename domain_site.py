
import streamlit as st
import sqlite3 as sq
import requests
import pandas as pd
# import aiohttp
# import asyncio
from streamlit_app import showInfo
import random



def createDataFrame(table_name):
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()
    query = f"select * from {table_name}"
    data = list(cur.execute(query))
    data = list(set(data))
    st.write(len(data))
    return data

def setTable(): 
    st.session_state['current_view'] = ['table',None] 

def filtered(start,data):
    st.session_state['filt_data'] = data[10*start:10*(start+1)]
    st.rerun()

def setPage(x):
    st.session_state['pg_num'] +=x
    
def setSearch():
    query = st.session_state['search']
    if(query==""):
        st.session_state['pg_num'] = 0
        st.session_state['cur_data'] = st.session_state['datax']
        st.session_state['filt_data'] = st.session_state['datax'][:10]
    else:
        final_arr = [i for i in st.session_state['datax'] if(i[1].find(query)!=-1)]
        st.session_state['pg_num'] = 0
        st.session_state['cur_data'] = final_arr
        st.session_state['filt_data'] = final_arr[:10]


if 'current_view' not in st.session_state:
    st.session_state['current_view'] = ['table',None]

if 'datax' not in st.session_state:
    st.session_state['datax'] = createDataFrame("DOMAIN_LINKS")

if "pg_num" not in st.session_state:
    st.session_state['pg_num'] = 0

if 'filt_data' not in st.session_state:
    st.session_state['filt_data'] = st.session_state['datax'][:10]

if 'cur_data' not in st.session_state:
    st.session_state['cur_data'] = createDataFrame("DOMAIN_LINKS")



st.markdown("""
        <style>
        .stButton > button {
            min-height : 1rem;
            min-width : unset;
            height: 2rem;  /* Adjust height here */
        }
        </style>
    """, unsafe_allow_html=True)



st.title(".IN Sites")

def mainPage():
    x1, x2,x3,x4, x5 = st.columns([1,3,1,1,1])
    x1.subheader("Date")
    x2.subheader("Domain Link")
    x3.subheader("TLD")
    x4.subheader("Status")
    x5.subheader("Info")

    for i in st.session_state['filt_data']:
        col1, col2, col3, col4, col5 = st.container().columns([1,3,1,1,1])
        col1.write(f"<div class='row-height'>{i[0]}</div>", unsafe_allow_html=True)
        col2.markdown(f'https://{i[1]}')
        col3.write(f"<div class='row-height'>{i[2]}</div>", unsafe_allow_html=True)
        col4.write(f"<div class='row-height'>{i[3]}</div>", unsafe_allow_html=True)


        if col5.button("Get Info", key= i[1]+i[0]):
            st.session_state['current_view'] = ['info',i[1]]
            st.rerun()
        
def showInfoPage():
    if(st.session_state['current_view'][0]=='info'):
        st.button('Back', on_click = setTable)
        if st.session_state['current_view'][1]:
            print("Show Entered")
            showInfo(st.session_state['current_view'][1])
            
            

if st.session_state['current_view'][0]=='table':
    search = st.text_input("Search for domain",key = "search", on_change = setSearch)
    # st.rerun()
    mainPage()
    col1,col2,col3,col4 = st.columns([4,1,1,4])
    if col3.button("Next"):
        setPage(1)
        filtered(st.session_state['pg_num'],st.session_state['cur_data'])
    if col2.button("Prev"):
        if(st.session_state['pg_num']>0):
            setPage(-1)
            filtered(st.session_state['pg_num'],st.session_state['cur_data'])
    # st.write(st.session_state['search'])

elif st.session_state['current_view'][0]=='info':
    showInfoPage()
    
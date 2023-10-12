# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 11:38:05 2023

@author: VictorTorres
"""

#CORE
import streamlit as st
from PIL import Image

#EDA
import pandas as pd

#PAGE SETUP
APP_TITLE = "CNT - Perforadores"
img=Image.open('DATA/IMG/CNT.png')

img_tab=Image.open('DATA/IMG/CNT_2.png')
st.set_page_config(
    page_title = APP_TITLE,
    page_icon = img_tab,
    layout = "wide")

img_sidebar= st.sidebar.columns(3)
img_sidebar[1].image(img,width=100)

#Layout Title
title_cols = st.columns(3)

title_cols[1].image("DATA/IMG/PEMEX_1.png", width=420)
title_font_size = "25px"  # Puedes ajustar el tamaño aquí
title_text = f"""
<h1 style="color: #e2b8a0; font-family: Calibri; text-align: center; font-size: {title_font_size};">ROTACION DE PERFORADORES</h1>
"""
# title_cols[1].markdown(title_text, unsafe_allow_html=True)
st.markdown(title_text, unsafe_allow_html=True)
#################### Data ####################

def data():
    drillers = pd.read_excel('DATA/EXCEL/perforador.xlsx', 'DRILLER')
    drillers['FECHA'] = pd.to_datetime(drillers['FECHA']).dt.date
    drillers['PERFORADOR'] = drillers['PERFORADOR'].fillna("")
    drillers.index = range(2, len(drillers) + 2)
    return drillers
drillers = data()

with st.sidebar.expander('SEGMENTACION DE DATOS'):
      wells = drillers['POZO'].unique()
      #shift = drillers['TURNO'].unique()
      week = drillers['SEMANA'].unique()
      filt_well = st.selectbox('POZOS', wells)
      #filt_shift = st.selectbox('TURNO', shift)
      filt_week = st.selectbox('SEMANA', week)
     
      driller_well = drillers[drillers['POZO'] == filt_well]
      #driller_shift = driller_well[driller_well['TURNO'] == filt_shift]
      driller_week = driller_well[driller_well['SEMANA'] == filt_week]


driller_week2 = driller_week.groupby(['SEMANA', 'TURNO']).agg({'POZO': 'first', 'EQUIPO': 'first', 'FECHA': 'first', 'PERFORADOR': 'first'}).reset_index()

column_order = ["POZO", "EQUIPO", "FECHA", "SEMANA", "TURNO", "PERFORADOR"]

driller_week2 = driller_week2[column_order]

st.caption('PLANTILLA DE PERFORADORES POR POZO, EQUIPO Y SEMANA')
drillers_edited = st.data_editor(driller_week2, disabled=['SEMANA', 'TURNO', 'POZO', 'EQUIPO', 'FECHA'], hide_index=True, use_container_width=True)


drillers = drillers.merge(drillers_edited[['SEMANA', 'PERFORADOR']], on='SEMANA', how='left')

drillers['PERFORADOR'] = drillers['PERFORADOR_y']
drillers['PERFORADOR_x'].fillna(drillers['PERFORADOR_y'], inplace=True)

drillers.drop(columns='PERFORADOR_y', inplace=True)
drillers.drop(columns='PERFORADOR_x', inplace=True)
drillers.drop_duplicates(inplace=True)

drillers.to_excel('DATA/EXCEL/perforador2.xlsx', 'DRILLER', index=False)

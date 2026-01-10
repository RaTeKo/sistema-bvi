import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="BVI - Histórico", page_icon="📋", layout="wide")

# Ligação à Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📋 Histórico Permanente (Google Sheets)")

try:
    df = conn.read()
    
    # Filtros
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: pesquisa = st.text_input("🔍 Pesquisa livre:")
    with c2: 
        anos = ["Todos"] + sorted(pd.to_datetime(df['DATA REGISTO'], dayfirst=True).dt.year.unique().astype(str).tolist(), reverse=True)
        filtro_ano = st.selectbox("Ano:", anos)
    with c3:
        lista_motivos = ["Todos"] + sorted(df['MOTIVO'].unique().tolist())
        filtro_motivo = st.selectbox("Motivo:", lista_motivos)

    # Lógica de Filtro
    df_f = df.copy()
    if pesquisa:
        df_f = df_f[df_f.apply(lambda r: r.astype(str).str.contains(pesquisa, case=False).any(), axis=1)]
    if filtro_ano != "Todos":
        df_f = df_f[pd.to_datetime(df_f['DATA REGISTO'], dayfirst=True).dt.year.astype(str) == filtro_ano]
    if filtro_motivo != "Todos":
        df_f = df_f[df_f['MOTIVO'] == filtro_motivo]

    st.dataframe(df_f.iloc[::-1], use_container_width=True, hide_index=True)
    
except Exception as e:
    st.info("A carregar base de dados ou vazia...")

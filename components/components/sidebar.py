import streamlit as st
import pandas as pd
import numpy as np

def render_sidebar(data):
    """Render the sidebar with filtering options"""
    
    st.sidebar.header("🔍 Filtros de Análise")
    
    filters = {}
    
    # Neighborhood filter
    st.sidebar.subheader("📍 Localização")
    bairros = sorted(data['Bairro'].dropna().unique())
    filters['bairro'] = st.sidebar.selectbox(
        "Selecione o bairro:",
        options=['Todos'] + list(bairros),
        help="Filtrar escolas por bairro específico"
    )
    
    # Air conditioning percentage filter
    st.sidebar.subheader("❄️ Climatização")
    
    # Calculate AC percentage for filtering
    data_temp = data.copy()
    data_temp['Percentual_AC'] = (data_temp['Salas com Ar'] / data_temp['Total de Salas'] * 100).fillna(0)
    
    min_ac = float(data_temp['Percentual_AC'].min())
    max_ac = float(data_temp['Percentual_AC'].max())
    
    filters['ac_range'] = st.sidebar.slider(
        "Percentual de salas com ar-condicionado:",
        min_value=min_ac,
        max_value=max_ac,
        value=(min_ac, max_ac),
        step=1.0,
        format="%.0f%%",
        help="Filtrar escolas pelo percentual de climatização"
    )
    
    # School size filter
    st.sidebar.subheader("🏫 Tamanho da Escola")
    min_salas = int(data['Total de Salas'].min())
    max_salas = int(data['Total de Salas'].max())
    
    filters['salas_range'] = st.sidebar.slider(
        "Número total de salas:",
        min_value=min_salas,
        max_value=max_salas,
        value=(min_salas, max_salas),
        help="Filtrar escolas pelo número total de salas"
    )
    
    # IDEB filters
    st.sidebar.subheader("📚 Performance IDEB")
    
    # IDEB Iniciais filter
    ideb_iniciais_valid = data['IDEB Iniciais'].dropna()
    if not ideb_iniciais_valid.empty:
        min_ideb_i = float(ideb_iniciais_valid.min())
        max_ideb_i = float(ideb_iniciais_valid.max())
        filters['ideb_iniciais_range'] = st.sidebar.slider(
            "IDEB Anos Iniciais:",
            min_value=min_ideb_i,
            max_value=max_ideb_i,
            value=(min_ideb_i, max_ideb_i),
            step=0.1,
            format="%.1f",
            help="Filtrar por performance nos anos iniciais"
        )
    else:
        filters['ideb_iniciais_range'] = None
    
    # IDEB Finais filter
    ideb_finais_valid = data['IDEB Finais'].dropna()
    if not ideb_finais_valid.empty:
        min_ideb_f = float(ideb_finais_valid.min())
        max_ideb_f = float(ideb_finais_valid.max())
        filters['ideb_finais_range'] = st.sidebar.slider(
            "IDEB Anos Finais:",
            min_value=min_ideb_f,
            max_value=max_ideb_f,
            value=(min_ideb_f, max_ideb_f),
            step=0.1,
            format="%.1f",
            help="Filtrar por performance nos anos finais"
        )
    else:
        filters['ideb_finais_range'] = None
    
    # Data export section
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Exportar Dados")
    
    return filters

import streamlit as st
import pandas as pd
import numpy as np
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.data_upload import render_data_upload
from components.preloaded_data import render_preloaded_data_option
from components.header import render_header
from utils.data_processor import DataProcessor
from utils.statistical_analysis import StatisticalAnalysis
from utils.visualizations import Visualizations

# Page configuration
st.set_page_config(
    page_title="Análise de Climatização e IDEB - Escolas Públicas do Rio",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

def main():
    # University header with logo and student info
    render_header()
    
    # Main title
    st.title("🏫 Análise de Climatização e Qualidade das Escolas Públicas do Rio")
    st.markdown("---")
    
    # Data upload section
    if not st.session_state.analysis_complete:
        st.header("📊 Upload dos Dados")
        
        # Check for preloaded data option first
        preloaded_success = render_preloaded_data_option()
        
        if not preloaded_success:
            st.markdown("---")
            st.subheader("📁 Ou faça upload dos seus próprios arquivos:")
            uploaded_files = render_data_upload()
            
            if uploaded_files and all(uploaded_files.values()):
                try:
                    with st.spinner("Processando dados..."):
                        # Initialize data processor
                        st.session_state.data_processor = DataProcessor()
                        
                        # Process the uploaded files
                        st.session_state.processed_data = st.session_state.data_processor.process_files(
                            uploaded_files['escolas'],
                            uploaded_files['ideb_iniciais'],
                            uploaded_files['ideb_finais']
                        )
                        
                        st.session_state.analysis_complete = True
                        st.success("✅ Dados processados com sucesso!")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar os dados: {str(e)}")
                    st.session_state.analysis_complete = False
    
    # Main analysis section
    if st.session_state.analysis_complete and st.session_state.processed_data is not None:
        # Sidebar for filters
        filters = render_sidebar(st.session_state.processed_data)
        
        # Apply filters to data
        filtered_data = st.session_state.data_processor.apply_filters(
            st.session_state.processed_data, 
            filters
        )
        
        if filtered_data.empty:
            st.warning("⚠️ Nenhuma escola encontrada com os filtros selecionados.")
        else:
            # Main dashboard
            render_dashboard(filtered_data, st.session_state.processed_data)
    
    # Footer
    st.markdown("---")
    st.markdown("*Desenvolvido para análise de infraestrutura educacional*")

if __name__ == "__main__":
    main()

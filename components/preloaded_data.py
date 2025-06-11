import streamlit as st
import pandas as pd
import os
from utils.data_processor import DataProcessor

def render_preloaded_data_option():
    """Render option to use preloaded data files"""
    
    # Check if sample files exist
    sample_files = {
        'escolas': 'escolas_rio.xlsx',
        'ideb_iniciais': 'ideb_iniciais.xlsx', 
        'ideb_finais': 'ideb_finais.xlsx'
    }
    
    files_exist = all(os.path.exists(f) for f in sample_files.values())
    
    if files_exist:
        st.info("📁 Arquivos de dados detectados no sistema")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            Os seguintes arquivos estão disponíveis:
            - **Escolas do Rio**: Dados de infraestrutura das escolas públicas
            - **IDEB Anos Iniciais**: Dados de performance educacional
            - **IDEB Anos Finais**: Dados de performance educacional
            """)
        
        with col2:
            if st.button("🚀 Usar Dados Disponíveis", type="primary"):
                return load_preloaded_data(sample_files)
    
    return None

def load_preloaded_data(file_paths):
    """Load and process the preloaded data files"""
    
    try:
        with st.spinner("Carregando dados..."):
            processor = DataProcessor()
            
            # Create file-like objects for the processor
            class FileWrapper:
                def __init__(self, filepath):
                    self.filepath = filepath
                    self.name = os.path.basename(filepath)
            
            file_objects = {
                'escolas': FileWrapper(file_paths['escolas']),
                'ideb_iniciais': FileWrapper(file_paths['ideb_iniciais']),
                'ideb_finais': FileWrapper(file_paths['ideb_finais'])
            }
            
            # Process using file paths directly
            processed_data = processor.process_files_from_paths(
                file_paths['escolas'],
                file_paths['ideb_iniciais'],
                file_paths['ideb_finais']
            )
            
            st.session_state.data_processor = processor
            st.session_state.processed_data = processed_data
            st.session_state.analysis_complete = True
            
            st.success(f"✅ Dados carregados com sucesso! {len(processed_data)} escolas processadas.")
            return True
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar os dados: {str(e)}")
        return False
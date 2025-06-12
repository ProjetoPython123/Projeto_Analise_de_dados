import streamlit as st

def render_data_upload():
    """Render the data upload interface"""
    
    st.markdown("""
    ### Instruções de Upload
    Por favor, faça o upload dos três arquivos Excel necessários para a análise:
    1. **Planilha de Escolas**: Dados gerais das escolas (infraestrutura, localização)
    2. **IDEB Anos Iniciais**: Dados de desempenho para anos iniciais
    3. **IDEB Anos Finais**: Dados de desempenho para anos finais
    """)
    
    col1, col2, col3 = st.columns(3)
    
    uploaded_files = {}
    
    with col1:
        st.subheader("📋 Dados das Escolas")
        uploaded_files['escolas'] = st.file_uploader(
            "Selecione a planilha de escolas",
            type=["xlsx", "xls"],
            key="escolas",
            help="Arquivo contendo dados de infraestrutura das escolas"
        )
        
    with col2:
        st.subheader("📈 IDEB Anos Iniciais")
        uploaded_files['ideb_iniciais'] = st.file_uploader(
            "Selecione a planilha de IDEB (anos iniciais)",
            type=["xlsx", "xls"],
            key="ideb_iniciais",
            help="Dados de desempenho para ensino fundamental I"
        )
        
    with col3:
        st.subheader("📊 IDEB Anos Finais")
        uploaded_files['ideb_finais'] = st.file_uploader(
            "Selecione a planilha de IDEB (anos finais)",
            type=["xlsx", "xls"],
            key="ideb_finais",
            help="Dados de desempenho para ensino fundamental II"
        )
    
    # Show upload status
    if any(uploaded_files.values()):
        st.markdown("#### Status do Upload:")
        cols = st.columns(3)
        files = ['escolas', 'ideb_iniciais', 'ideb_finais']
        labels = ['Escolas', 'IDEB Iniciais', 'IDEB Finais']
        
        for i, (file_key, label) in enumerate(zip(files, labels)):
            with cols[i]:
                if uploaded_files[file_key] is not None:
                    st.success(f"✅ {label}")
                else:
                    st.info(f"⏳ {label}")
    
    return uploaded_files

import streamlit as st
import pandas as pd
import numpy as np
from utils.statistical_analysis import StatisticalAnalysis
from utils.visualizations import Visualizations
import io

def render_dashboard(filtered_data, full_data):
    """Render the main dashboard with analysis and visualizations"""
    
    # Initialize analysis tools
    stats_analyzer = StatisticalAnalysis()
    viz = Visualizations()
    
    # Summary statistics section
    render_summary_stats(filtered_data, full_data)
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", 
        "🔍 Análise Detalhada", 
        "📈 Correlações", 
        "🗺️ Distribuição", 
        "📋 Dados Brutos"
    ])
    
    with tab1:
        render_overview_tab(filtered_data, viz)
    
    with tab2:
        render_detailed_analysis_tab(filtered_data, stats_analyzer, viz)
    
    with tab3:
        render_correlation_tab(filtered_data, stats_analyzer, viz)
    
    with tab4:
        render_distribution_tab(filtered_data, viz)
    
    with tab5:
        render_raw_data_tab(filtered_data)

def render_summary_stats(filtered_data, full_data):
    """Render summary statistics cards"""
    
    st.header("📊 Resumo Executivo")
    
    # Calculate key metrics
    total_escolas = len(filtered_data)
    total_salas = filtered_data['Total de Salas'].sum()
    salas_com_ar = filtered_data['Salas com Ar'].sum()
    percentual_climatizacao = (salas_com_ar / total_salas * 100) if total_salas > 0 else 0
    
    # IDEB averages
    ideb_iniciais_media = filtered_data['IDEB Iniciais'].mean()
    ideb_finais_media = filtered_data['IDEB Finais'].mean()
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🏫 Total de Escolas",
            value=f"{total_escolas:,}",
            delta=f"{((total_escolas/len(full_data))*100):.1f}% do total" if len(full_data) > 0 else None
        )
    
    with col2:
        st.metric(
            label="🏛️ Total de Salas",
            value=f"{total_salas:,}",
            delta=f"{salas_com_ar:,} com AC"
        )
    
    with col3:
        st.metric(
            label="❄️ Climatização",
            value=f"{percentual_climatizacao:.1f}%",
            delta="das salas"
        )
    
    with col4:
        if not pd.isna(ideb_iniciais_media):
            st.metric(
                label="📚 IDEB Iniciais",
                value=f"{ideb_iniciais_media:.1f}",
                delta="Média"
            )
        else:
            st.metric(label="📚 IDEB Iniciais", value="N/A")
    
    with col5:
        if not pd.isna(ideb_finais_media):
            st.metric(
                label="📊 IDEB Finais",
                value=f"{ideb_finais_media:.1f}",
                delta="Média"
            )
        else:
            st.metric(label="📊 IDEB Finais", value="N/A")

def render_overview_tab(filtered_data, viz):
    """Render overview visualizations"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição de Climatização")
        fig_climate = viz.create_climate_distribution_chart(filtered_data)
        if fig_climate:
            st.plotly_chart(fig_climate, use_container_width=True)
    
    with col2:
        st.subheader("Performance IDEB")
        fig_ideb = viz.create_ideb_comparison_chart(filtered_data)
        if fig_ideb:
            st.plotly_chart(fig_ideb, use_container_width=True)
    
    # Schools comparison chart
    st.subheader("Comparação por Escola")
    fig_comparison = viz.create_school_comparison_chart(filtered_data)
    if fig_comparison:
        st.plotly_chart(fig_comparison, use_container_width=True)

def render_detailed_analysis_tab(filtered_data, stats_analyzer, viz):
    """Render detailed statistical analysis"""
    
    st.subheader("Análise Estatística Detalhada")
    
    # Calculate AC percentage for analysis
    filtered_data_analysis = filtered_data.copy()
    filtered_data_analysis['Percentual_AC'] = (
        filtered_data_analysis['Salas com Ar'] / filtered_data_analysis['Total de Salas'] * 100
    ).fillna(0)
    
    # Statistical summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Estatísticas de Climatização")
        climate_stats = stats_analyzer.calculate_descriptive_stats(
            filtered_data_analysis['Percentual_AC']
        )
        
        for stat, value in climate_stats.items():
            st.metric(stat, f"{value:.2f}%")
    
    with col2:
        st.markdown("#### 📚 Estatísticas de IDEB")
        if not filtered_data_analysis['IDEB Iniciais'].dropna().empty:
            ideb_stats = stats_analyzer.calculate_descriptive_stats(
                filtered_data_analysis['IDEB Iniciais'].dropna()
            )
            
            for stat, value in ideb_stats.items():
                st.metric(f"IDEB Iniciais - {stat}", f"{value:.2f}")

def render_correlation_tab(filtered_data, stats_analyzer, viz):
    """Render correlation analysis"""
    
    st.subheader("Análise de Correlação")
    
    # Calculate correlations
    correlation_results = stats_analyzer.analyze_correlations(filtered_data)
    
    if correlation_results:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 🔗 Correlações Identificadas")
            for correlation in correlation_results:
                st.write(f"**{correlation['variables']}**")
                st.write(f"Correlação: {correlation['correlation']:.3f}")
                st.write(f"P-valor: {correlation['p_value']:.3f}")
                st.write(f"Significância: {correlation['significance']}")
                st.write("---")
        
        with col2:
            # Alternative box plot analysis
            fig_alternative = viz.create_alternative_analysis_chart(filtered_data)
            if fig_alternative:
                st.plotly_chart(fig_alternative, use_container_width=True)
    
    # Additional insights section
    st.markdown("---")
    st.markdown("#### 💡 Insights da Análise")
    
    if correlation_results:
        # Find strongest correlation
        strongest_corr = max(correlation_results, key=lambda x: abs(x['correlation']))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Correlação Mais Forte",
                f"{strongest_corr['correlation']:.3f}",
                delta=strongest_corr['variables']
            )
        
        with col2:
            # Count significant correlations
            significant_count = sum(1 for corr in correlation_results if corr['p_value'] < 0.05)
            st.metric(
                "Correlações Significativas",
                significant_count,
                delta=f"de {len(correlation_results)} total"
            )
        
        with col3:
            # Average correlation strength
            avg_correlation = np.mean([abs(corr['correlation']) for corr in correlation_results])
            st.metric(
                "Força Média das Correlações",
                f"{avg_correlation:.3f}",
                delta="Valor absoluto"
            )

def render_distribution_tab(filtered_data, viz):
    """Render distribution analysis"""
    
    st.subheader("Análise de Distribuição")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📍 Distribuição por Bairro")
        fig_neighborhood = viz.create_neighborhood_distribution(filtered_data)
        if fig_neighborhood:
            st.plotly_chart(fig_neighborhood, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Histograma de Performance")
        fig_histogram = viz.create_performance_histogram(filtered_data)
        if fig_histogram:
            st.plotly_chart(fig_histogram, use_container_width=True)

def render_raw_data_tab(filtered_data):
    """Render raw data table with export functionality"""
    
    st.subheader("Dados Brutos")
    
    # Data summary
    st.write(f"**Total de registros:** {len(filtered_data)}")
    
    # Search functionality
    search_term = st.text_input("🔍 Buscar escola por nome:")
    
    if search_term:
        mask = filtered_data['Nome da Escola'].str.contains(search_term, case=False, na=False)
        display_data = filtered_data[mask]
    else:
        display_data = filtered_data
    
    # Display data
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Export functionality
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Baixar dados filtrados (CSV)"):
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="escolas_analise.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Baixar dados filtrados (Excel)"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                display_data.to_excel(writer, index=False, sheet_name='Análise Escolas')
            
            st.download_button(
                label="Download Excel",
                data=buffer.getvalue(),
                file_name="escolas_analise.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

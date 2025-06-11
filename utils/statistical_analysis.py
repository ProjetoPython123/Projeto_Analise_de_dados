import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import streamlit as st

class StatisticalAnalysis:
    """Class for performing statistical analysis on school data"""
    
    def __init__(self):
        pass
    
    def calculate_descriptive_stats(self, data_series):
        """Calculate descriptive statistics for a data series"""
        
        if data_series.empty or data_series.dropna().empty:
            return {}
        
        clean_data = data_series.dropna()
        
        stats_dict = {
            'Média': clean_data.mean(),
            'Mediana': clean_data.median(),
            'Desvio Padrão': clean_data.std(),
            'Mínimo': clean_data.min(),
            'Máximo': clean_data.max(),
            'Q1 (25%)': clean_data.quantile(0.25),
            'Q3 (75%)': clean_data.quantile(0.75)
        }
        
        return stats_dict
    
    def analyze_correlations(self, data):
        """Analyze correlations between air conditioning and IDEB scores"""
        
        correlations = []
        
        # Calculate AC percentage
        data_analysis = data.copy()
        data_analysis['Percentual_AC'] = (
            data_analysis['Salas com Ar'] / data_analysis['Total de Salas'] * 100
        ).fillna(0)
        
        # Correlation between AC percentage and IDEB Iniciais
        if not data_analysis['IDEB Iniciais'].dropna().empty:
            ac_data = data_analysis['Percentual_AC']
            ideb_iniciais = data_analysis['IDEB Iniciais']
            
            # Remove rows where either value is NaN
            valid_mask = ~(ac_data.isna() | ideb_iniciais.isna())
            if valid_mask.sum() > 2:  # Need at least 3 data points
                correlation, p_value = pearsonr(
                    ac_data[valid_mask], 
                    ideb_iniciais[valid_mask]
                )
                
                significance = self._interpret_significance(p_value)
                
                correlations.append({
                    'variables': 'Climatização vs IDEB Iniciais',
                    'correlation': correlation,
                    'p_value': p_value,
                    'significance': significance,
                    'n_samples': valid_mask.sum()
                })
        
        # Correlation between AC percentage and IDEB Finais
        if not data_analysis['IDEB Finais'].dropna().empty:
            ac_data = data_analysis['Percentual_AC']
            ideb_finais = data_analysis['IDEB Finais']
            
            valid_mask = ~(ac_data.isna() | ideb_finais.isna())
            if valid_mask.sum() > 2:
                correlation, p_value = pearsonr(
                    ac_data[valid_mask], 
                    ideb_finais[valid_mask]
                )
                
                significance = self._interpret_significance(p_value)
                
                correlations.append({
                    'variables': 'Climatização vs IDEB Finais',
                    'correlation': correlation,
                    'p_value': p_value,
                    'significance': significance,
                    'n_samples': valid_mask.sum()
                })
        
        # Correlation between IDEB Iniciais and Finais
        ideb_iniciais = data_analysis['IDEB Iniciais']
        ideb_finais = data_analysis['IDEB Finais']
        
        valid_mask = ~(ideb_iniciais.isna() | ideb_finais.isna())
        if valid_mask.sum() > 2:
            correlation, p_value = pearsonr(
                ideb_iniciais[valid_mask], 
                ideb_finais[valid_mask]
            )
            
            significance = self._interpret_significance(p_value)
            
            correlations.append({
                'variables': 'IDEB Iniciais vs IDEB Finais',
                'correlation': correlation,
                'p_value': p_value,
                'significance': significance,
                'n_samples': valid_mask.sum()
            })
        
        # Correlation between school size and performance
        school_size = data_analysis['Total de Salas']
        
        for ideb_col, label in [('IDEB Iniciais', 'Iniciais'), ('IDEB Finais', 'Finais')]:
            ideb_data = data_analysis[ideb_col]
            valid_mask = ~(school_size.isna() | ideb_data.isna())
            
            if valid_mask.sum() > 2:
                correlation, p_value = pearsonr(
                    school_size[valid_mask], 
                    ideb_data[valid_mask]
                )
                
                significance = self._interpret_significance(p_value)
                
                correlations.append({
                    'variables': f'Tamanho da Escola vs IDEB {label}',
                    'correlation': correlation,
                    'p_value': p_value,
                    'significance': significance,
                    'n_samples': valid_mask.sum()
                })
        
        return correlations
    
    def _interpret_significance(self, p_value):
        """Interpret statistical significance of p-value"""
        
        if p_value < 0.001:
            return "Altamente significativo (p < 0.001)"
        elif p_value < 0.01:
            return "Muito significativo (p < 0.01)"
        elif p_value < 0.05:
            return "Significativo (p < 0.05)"
        elif p_value < 0.1:
            return "Marginalmente significativo (p < 0.1)"
        else:
            return "Não significativo (p ≥ 0.1)"
    
    def calculate_correlation_matrix(self, data):
        """Calculate correlation matrix for numerical variables"""
        
        data_analysis = data.copy()
        data_analysis['Percentual_AC'] = (
            data_analysis['Salas com Ar'] / data_analysis['Total de Salas'] * 100
        ).fillna(0)
        
        # Select numerical columns for correlation
        numerical_cols = [
            'Total de Salas', 'Salas com Ar', 'Percentual_AC',
            'IDEB Iniciais', 'IDEB Finais'
        ]
        
        # Filter columns that exist and have data
        available_cols = []
        for col in numerical_cols:
            if col in data_analysis.columns and not data_analysis[col].dropna().empty:
                available_cols.append(col)
        
        if len(available_cols) < 2:
            return None
        
        correlation_matrix = data_analysis[available_cols].corr()
        return correlation_matrix
    
    def perform_group_analysis(self, data, group_by='AC_Category'):
        """Perform analysis by grouping schools into categories"""
        
        data_analysis = data.copy()
        data_analysis['Percentual_AC'] = (
            data_analysis['Salas com Ar'] / data_analysis['Total de Salas'] * 100
        ).fillna(0)
        
        # Create AC categories
        data_analysis['AC_Category'] = pd.cut(
            data_analysis['Percentual_AC'],
            bins=[0, 25, 50, 75, 100],
            labels=['Baixa (0-25%)', 'Média-Baixa (25-50%)', 'Média-Alta (50-75%)', 'Alta (75-100%)'],
            include_lowest=True
        )
        
        # Group analysis
        group_stats = {}
        
        for category in data_analysis['AC_Category'].dropna().unique():
            category_data = data_analysis[data_analysis['AC_Category'] == category]
            
            stats = {
                'count': len(category_data),
                'avg_ideb_iniciais': category_data['IDEB Iniciais'].mean(),
                'avg_ideb_finais': category_data['IDEB Finais'].mean(),
                'avg_total_salas': category_data['Total de Salas'].mean(),
                'avg_ac_percentage': category_data['Percentual_AC'].mean()
            }
            
            group_stats[category] = stats
        
        return group_stats
    
    def perform_statistical_tests(self, data):
        """Perform various statistical tests"""
        
        results = {}
        
        data_analysis = data.copy()
        data_analysis['Percentual_AC'] = (
            data_analysis['Salas com Ar'] / data_analysis['Total de Salas'] * 100
        ).fillna(0)
        
        # Create high/low AC groups for comparison
        median_ac = data_analysis['Percentual_AC'].median()
        data_analysis['AC_Group'] = data_analysis['Percentual_AC'].apply(
            lambda x: 'High AC' if x >= median_ac else 'Low AC'
        )
        
        # T-test for IDEB differences between high/low AC schools
        high_ac_data = data_analysis[data_analysis['AC_Group'] == 'High AC']
        low_ac_data = data_analysis[data_analysis['AC_Group'] == 'Low AC']
        
        for ideb_col in ['IDEB Iniciais', 'IDEB Finais']:
            high_ac_ideb = high_ac_data[ideb_col].dropna()
            low_ac_ideb = low_ac_data[ideb_col].dropna()
            
            if len(high_ac_ideb) > 1 and len(low_ac_ideb) > 1:
                t_stat, p_value = stats.ttest_ind(high_ac_ideb, low_ac_ideb)
                
                results[f't_test_{ideb_col.replace(" ", "_")}'] = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'high_ac_mean': high_ac_ideb.mean(),
                    'low_ac_mean': low_ac_ideb.mean(),
                    'significance': self._interpret_significance(p_value)
                }
        
        return results

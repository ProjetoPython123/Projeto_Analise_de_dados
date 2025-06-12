import pandas as pd
import numpy as np
import streamlit as st

class DataProcessor:
    """Class for processing and cleaning school data"""
    
    def __init__(self):
        self.processed_data = None
    
    def process_files(self, arquivo_escolas, arquivo_ideb_iniciais, arquivo_ideb_finais):
        """Process the uploaded Excel files and return cleaned data"""
        
        try:
            # Read Excel files - skip rows with NaN in first column for IDEB files
            df_escolas = pd.read_excel(arquivo_escolas)
            
            # For IDEB files, read and skip empty header rows
            df_ideb_iniciais = pd.read_excel(arquivo_ideb_iniciais)
            df_ideb_iniciais = df_ideb_iniciais.dropna(subset=['Sigla da UF']).reset_index(drop=True)
            
            df_ideb_finais = pd.read_excel(arquivo_ideb_finais)
            df_ideb_finais = df_ideb_finais.dropna(subset=['Sigla da UF']).reset_index(drop=True)
            
            return self._process_dataframes(df_escolas, df_ideb_iniciais, df_ideb_finais)
            
        except Exception as e:
            raise Exception(f"Erro no processamento dos dados: {str(e)}")
    
    def process_files_from_paths(self, path_escolas, path_ideb_iniciais, path_ideb_finais):
        """Process Excel files from file paths"""
        
        try:
            # Read Excel files - skip rows with NaN in first column for IDEB files
            df_escolas = pd.read_excel(path_escolas)
            
            # For IDEB files, read and skip empty header rows
            df_ideb_iniciais = pd.read_excel(path_ideb_iniciais)
            df_ideb_iniciais = df_ideb_iniciais.dropna(subset=['Sigla da UF']).reset_index(drop=True)
            
            df_ideb_finais = pd.read_excel(path_ideb_finais)
            df_ideb_finais = df_ideb_finais.dropna(subset=['Sigla da UF']).reset_index(drop=True)
            
            return self._process_dataframes(df_escolas, df_ideb_iniciais, df_ideb_finais)
            
        except Exception as e:
            raise Exception(f"Erro no processamento dos dados: {str(e)}")
    
    def _process_dataframes(self, df_escolas, df_ideb_iniciais, df_ideb_finais):
        """Common processing logic for dataframes"""
        
        # Validate required columns exist
        self._validate_columns(df_escolas, df_ideb_iniciais, df_ideb_finais)
        
        # Process school data
        df_escolas_processed = self._process_school_data(df_escolas)
        
        # Process IDEB data
        df_ideb_iniciais_processed = self._process_ideb_data(df_ideb_iniciais, 'iniciais')
        df_ideb_finais_processed = self._process_ideb_data(df_ideb_finais, 'finais')
        
        # Merge all data
        final_data = self._merge_data(
            df_escolas_processed,
            df_ideb_iniciais_processed,
            df_ideb_finais_processed
        )
        
        # Final cleaning and validation
        final_data = self._final_cleanup(final_data)
        
        self.processed_data = final_data
        return final_data
    
    def _validate_columns(self, df_escolas, df_ideb_iniciais, df_ideb_finais):
        """Validate that required columns exist in the dataframes"""
        
        required_escola_cols = [
            'NO_ENTIDADE', 'CO_ENTIDADE', 'TP_DEPENDENCIA',
            'QT_SALAS_UTILIZADAS', 'QT_SALAS_UTILIZA_CLIMATIZADAS'
        ]
        
        # Check if NO_BAIRRO exists, if not try alternatives
        bairro_cols = ['NO_BAIRRO', 'BAIRRO', 'Bairro']
        bairro_col = None
        for col in bairro_cols:
            if col in df_escolas.columns:
                bairro_col = col
                break
        
        if bairro_col:
            required_escola_cols.append(bairro_col)
        
        missing_cols = [col for col in required_escola_cols if col not in df_escolas.columns]
        if missing_cols:
            available_cols = list(df_escolas.columns)
            raise ValueError(
                f"Colunas obrigatórias não encontradas na planilha de escolas: {missing_cols}. "
                f"Colunas disponíveis: {available_cols}"
            )
        
        # Validate IDEB files have required columns
        ideb_required = ['Código da Escola', 'Taxa de Aprovação - 2023']
        
        # Try alternative column names for IDEB files
        for df, name in [(df_ideb_iniciais, 'IDEB Iniciais'), (df_ideb_finais, 'IDEB Finais')]:
            # Clean up column names - remove newlines and extra whitespace
            df.columns = [str(col).strip().replace('\n', ' ') for col in df.columns]
            
            if 'CO_ENTIDADE' in df.columns and 'Código da Escola' not in df.columns:
                df.rename(columns={'CO_ENTIDADE': 'Código da Escola'}, inplace=True)
            
            # Look for approval rate columns with different names
            rate_cols = [col for col in df.columns if 'Taxa' in str(col) or 'Aprovação' in str(col)]
            if rate_cols and 'Taxa de Aprovação - 2023' not in df.columns:
                df.rename(columns={rate_cols[0]: 'Taxa de Aprovação - 2023'}, inplace=True)
    
    def _process_school_data(self, df_escolas):
        """Process and clean school infrastructure data"""
        
        # Filter only public schools (TP_DEPENDENCIA == 3)
        df_escolas = df_escolas[df_escolas['TP_DEPENDENCIA'] == 3].copy()
        
        # Determine bairro column name
        bairro_col = None
        for col in ['NO_BAIRRO', 'BAIRRO', 'Bairro']:
            if col in df_escolas.columns:
                bairro_col = col
                break
        
        # Select and rename columns
        columns_to_select = [
            'NO_ENTIDADE', 'CO_ENTIDADE',
            'QT_SALAS_UTILIZADAS', 'QT_SALAS_UTILIZA_CLIMATIZADAS'
        ]
        
        if bairro_col:
            columns_to_select.append(bairro_col)
        
        df_escolas = df_escolas[columns_to_select].copy()
        
        # Rename columns
        rename_dict = {
            'CO_ENTIDADE': 'Código da Escola',
            'NO_ENTIDADE': 'Nome da Escola',
            'QT_SALAS_UTILIZADAS': 'Total de Salas',
            'QT_SALAS_UTILIZA_CLIMATIZADAS': 'Salas com Ar'
        }
        
        if bairro_col:
            rename_dict[bairro_col] = 'Bairro'
        
        df_escolas.rename(columns=rename_dict, inplace=True)
        
        # Clean and validate numerical data
        df_escolas['Total de Salas'] = pd.to_numeric(df_escolas['Total de Salas'], errors='coerce')
        df_escolas['Salas com Ar'] = pd.to_numeric(df_escolas['Salas com Ar'], errors='coerce')
        
        # Fill NaN values with 0 for air conditioned rooms
        df_escolas['Salas com Ar'] = df_escolas['Salas com Ar'].fillna(0)
        
        # Remove schools with invalid data
        df_escolas = df_escolas[
            (df_escolas['Total de Salas'] > 0) & 
            (df_escolas['Salas com Ar'] >= 0) &
            (df_escolas['Salas com Ar'] <= df_escolas['Total de Salas'])
        ]
        
        # Clean school and neighborhood names
        df_escolas['Nome da Escola'] = df_escolas['Nome da Escola'].astype(str).str.strip()
        if 'Bairro' in df_escolas.columns:
            df_escolas['Bairro'] = df_escolas['Bairro'].astype(str).str.strip()
            df_escolas['Bairro'] = df_escolas['Bairro'].replace(['nan', 'None'], np.nan)
        
        return df_escolas
    
    def _process_ideb_data(self, df_ideb, level):
        """Process IDEB performance data"""
        
        df_ideb = df_ideb.copy()
        
        # Ensure required columns exist
        if 'Código da Escola' not in df_ideb.columns or 'Taxa de Aprovação - 2023' not in df_ideb.columns:
            raise ValueError(f"IDEB {level}: Colunas obrigatórias não encontradas")
        
        # Select only necessary columns
        df_ideb = df_ideb[['Código da Escola', 'Taxa de Aprovação - 2023']].copy()
        
        # Clean the approval rate data
        df_ideb['Taxa de Aprovação - 2023'] = pd.to_numeric(
            df_ideb['Taxa de Aprovação - 2023'], 
            errors='coerce'
        )
        
        # Remove invalid entries
        df_ideb = df_ideb.dropna(subset=['Código da Escola'])
        
        return df_ideb
    
    def _merge_data(self, df_escolas, df_ideb_iniciais, df_ideb_finais):
        """Merge school data with IDEB performance data"""
        
        # Merge with IDEB iniciais
        merged_data = pd.merge(
            df_escolas,
            df_ideb_iniciais,
            on='Código da Escola',
            how='left'
        )
        merged_data.rename(columns={'Taxa de Aprovação - 2023': 'IDEB Iniciais'}, inplace=True)
        
        # Merge with IDEB finais
        merged_data = pd.merge(
            merged_data,
            df_ideb_finais,
            on='Código da Escola',
            how='left'
        )
        merged_data.rename(columns={'Taxa de Aprovação - 2023': 'IDEB Finais'}, inplace=True)
        
        return merged_data
    
    def _final_cleanup(self, df):
        """Final data cleaning and validation"""
        
        # Remove duplicates based on school code
        df = df.drop_duplicates(subset=['Código da Escola'])
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Add calculated fields
        df['Percentual_AC'] = (df['Salas com Ar'] / df['Total de Salas'] * 100).fillna(0)
        df['Salas sem Ar'] = df['Total de Salas'] - df['Salas com Ar']
        
        # Validate final data
        if len(df) == 0:
            raise ValueError("Nenhuma escola válida encontrada após o processamento")
        
        return df
    
    def apply_filters(self, data, filters):
        """Apply user-selected filters to the data"""
        
        filtered_data = data.copy()
        
        # Neighborhood filter
        if filters.get('bairro') and filters['bairro'] != 'Todos':
            filtered_data = filtered_data[filtered_data['Bairro'] == filters['bairro']]
        
        # Air conditioning percentage filter
        if filters.get('ac_range'):
            min_ac, max_ac = filters['ac_range']
            mask = (filtered_data['Percentual_AC'] >= min_ac) & (filtered_data['Percentual_AC'] <= max_ac)
            filtered_data = filtered_data[mask]
        
        # School size filter
        if filters.get('salas_range'):
            min_salas, max_salas = filters['salas_range']
            mask = (filtered_data['Total de Salas'] >= min_salas) & (filtered_data['Total de Salas'] <= max_salas)
            filtered_data = filtered_data[mask]
        
        # IDEB filters
        if filters.get('ideb_iniciais_range'):
            min_ideb, max_ideb = filters['ideb_iniciais_range']
            mask = (
                (filtered_data['IDEB Iniciais'] >= min_ideb) & 
                (filtered_data['IDEB Iniciais'] <= max_ideb)
            ) | filtered_data['IDEB Iniciais'].isna()
            filtered_data = filtered_data[mask]
        
        if filters.get('ideb_finais_range'):
            min_ideb, max_ideb = filters['ideb_finais_range']
            mask = (
                (filtered_data['IDEB Finais'] >= min_ideb) & 
                (filtered_data['IDEB Finais'] <= max_ideb)
            ) | filtered_data['IDEB Finais'].isna()
            filtered_data = filtered_data[mask]
        
        return filtered_data

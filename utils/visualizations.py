import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class Visualizations:
    """Class for creating interactive visualizations"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd'
        }
    
    def create_climate_distribution_chart(self, data):
        """Create a chart showing air conditioning distribution"""
        
        if data.empty:
            return None
        
        # Calculate AC percentage
        data_viz = data.copy()
        data_viz['Percentual_AC'] = (data_viz['Salas com Ar'] / data_viz['Total de Salas'] * 100).fillna(0)
        
        # Create AC categories
        data_viz['AC_Category'] = pd.cut(
            data_viz['Percentual_AC'],
            bins=[0, 25, 50, 75, 100],
            labels=['0-25%', '25-50%', '50-75%', '75-100%'],
            include_lowest=True
        )
        
        # Count schools in each category
        category_counts = data_viz['AC_Category'].value_counts().sort_index()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Distribuição de Escolas por Nível de Climatização",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        return fig
    
    def create_ideb_comparison_chart(self, data):
        """Create a chart comparing IDEB scores"""
        
        if data.empty:
            return None
        
        # Prepare data for comparison
        ideb_data = []
        
        if not data['IDEB Iniciais'].dropna().empty:
            ideb_data.extend([
                {'Nível': 'Anos Iniciais', 'IDEB': val} 
                for val in data['IDEB Iniciais'].dropna()
            ])
        
        if not data['IDEB Finais'].dropna().empty:
            ideb_data.extend([
                {'Nível': 'Anos Finais', 'IDEB': val} 
                for val in data['IDEB Finais'].dropna()
            ])
        
        if not ideb_data:
            return None
        
        df_ideb = pd.DataFrame(ideb_data)
        
        fig = px.box(
            df_ideb,
            x='Nível',
            y='IDEB',
            title="Distribuição das Taxas de Aprovação (IDEB)",
            color='Nível',
            color_discrete_sequence=[self.color_palette['primary'], self.color_palette['secondary']]
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_school_comparison_chart(self, data):
        """Create a comprehensive comparison chart for schools"""
        
        if data.empty or len(data) > 50:  # Limit to 50 schools for readability
            data_sample = data.head(50) if len(data) > 50 else data
        else:
            data_sample = data
        
        # Prepare truncated names and full names for tooltips
        def truncate_name(name, max_length=20):
            if len(name) > max_length:
                return name[:max_length] + "..."
            return name
        
        truncated_names = [truncate_name(name) for name in data_sample['Nome da Escola']]
        full_names = list(data_sample['Nome da Escola'])
        
        # Create subplots with increased vertical spacing
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=[
                "Salas com e sem Ar-condicionado por Escola",
                "Performance IDEB por Escola"
            ],
            vertical_spacing=0.2  # Increased spacing between titles
        )
        
        # Define hover colors for interactive highlighting
        hover_colors = {
            'success_hover': '#1e7e34',  # Darker green
            'warning_hover': '#bd2130',  # Darker red
            'primary_hover': '#155a85',  # Darker blue
            'secondary_hover': '#cc5500'  # Darker orange
        }
        
        # Classroom distribution chart
        fig.add_trace(
            go.Bar(
                name='Salas com Ar',
                x=truncated_names,
                y=data_sample['Salas com Ar'],
                marker=dict(
                    color=self.color_palette['success'],
                    line=dict(width=2, color='rgba(0,0,0,0)')
                ),
                text=full_names,
                hovertemplate='<b>%{text}</b><br>Salas com Ar: %{y}<extra></extra>',
                hoverlabel=dict(bgcolor=hover_colors['success_hover'], font_color='white')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                name='Salas sem Ar',
                x=truncated_names,
                y=data_sample['Salas sem Ar'],
                marker=dict(
                    color=self.color_palette['warning'],
                    line=dict(width=2, color='rgba(0,0,0,0)')
                ),
                text=full_names,
                hovertemplate='<b>%{text}</b><br>Salas sem Ar: %{y}<extra></extra>',
                hoverlabel=dict(bgcolor=hover_colors['warning_hover'], font_color='white')
            ),
            row=1, col=1
        )
        
        # IDEB performance chart
        if not data_sample['IDEB Iniciais'].dropna().empty:
            fig.add_trace(
                go.Scatter(
                    name='IDEB Iniciais',
                    x=truncated_names,
                    y=data_sample['IDEB Iniciais'],
                    mode='markers+lines',
                    marker=dict(
                        color=self.color_palette['primary'],
                        size=8,
                        line=dict(width=2, color='white')
                    ),
                    line=dict(
                        dash='dot',
                        width=3,
                        color=self.color_palette['primary']
                    ),
                    text=full_names,
                    hovertemplate='<b>%{text}</b><br>IDEB Iniciais: %{y:.1f}<extra></extra>',
                    hoverlabel=dict(bgcolor=hover_colors['primary_hover'], font_color='white')
                ),
                row=2, col=1
            )
        
        if not data_sample['IDEB Finais'].dropna().empty:
            fig.add_trace(
                go.Scatter(
                    name='IDEB Finais',
                    x=truncated_names,
                    y=data_sample['IDEB Finais'],
                    mode='markers+lines',
                    marker=dict(
                        color=self.color_palette['secondary'],
                        size=8,
                        line=dict(width=2, color='white')
                    ),
                    line=dict(
                        dash='dash',
                        width=3,
                        color=self.color_palette['secondary']
                    ),
                    text=full_names,
                    hovertemplate='<b>%{text}</b><br>IDEB Finais: %{y:.1f}<extra></extra>',
                    hoverlabel=dict(bgcolor=hover_colors['secondary_hover'], font_color='white')
                ),
                row=2, col=1
            )
        
        # Update layout with interactive features
        fig.update_xaxes(tickangle=45)
        fig.update_layout(
            height=900,  # Increased height to accommodate better spacing
            barmode='stack',
            title_text="Análise Comparativa por Escola",
            showlegend=True,
            # Add hover interactions
            hovermode='closest',
            # Improved styling
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            margin=dict(l=60, r=60, t=120, b=100)  # Better margins for titles
        )
        
        # Style the subplot titles with better spacing
        fig.update_annotations(
            font_size=14,
            font_color="#2c3e50"
        )
        
        # Add shadow/glow effect on hover using update_traces
        fig.update_traces(
            selector=dict(type='bar'),
            marker_line_width=0,
            hoverlabel=dict(
                bordercolor="white",
                font_size=12
            )
        )
        
        fig.update_traces(
            selector=dict(type='scatter'),
            hoverlabel=dict(
                bordercolor="white",
                font_size=12
            )
        )
        
        # Grid styling for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        return fig
    
    def create_correlation_scatter_plot(self, data):
        """Create scatter plot showing correlation between AC and IDEB"""
        
        if data.empty:
            return None
        
        data_viz = data.copy()
        data_viz['Percentual_AC'] = (data_viz['Salas com Ar'] / data_viz['Total de Salas'] * 100).fillna(0)
        
        # Create subplot for both IDEB levels
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['IDEB Iniciais vs Climatização', 'IDEB Finais vs Climatização']
        )
        
        # IDEB Iniciais scatter
        if not data_viz['IDEB Iniciais'].dropna().empty:
            fig.add_trace(
                go.Scatter(
                    x=data_viz['Percentual_AC'],
                    y=data_viz['IDEB Iniciais'],
                    mode='markers',
                    name='Anos Iniciais',
                    marker=dict(
                        color=self.color_palette['primary'],
                        size=8,
                        opacity=0.7
                    ),
                    text=data_viz['Nome da Escola'],
                    hovertemplate='<b>%{text}</b><br>Climatização: %{x:.1f}%<br>IDEB: %{y:.1f}<extra></extra>'
                ),
                row=1, col=1
            )
        
        # IDEB Finais scatter
        if not data_viz['IDEB Finais'].dropna().empty:
            fig.add_trace(
                go.Scatter(
                    x=data_viz['Percentual_AC'],
                    y=data_viz['IDEB Finais'],
                    mode='markers',
                    name='Anos Finais',
                    marker=dict(
                        color=self.color_palette['secondary'],
                        size=8,
                        opacity=0.7
                    ),
                    text=data_viz['Nome da Escola'],
                    hovertemplate='<b>%{text}</b><br>Climatização: %{x:.1f}%<br>IDEB: %{y:.1f}<extra></extra>'
                ),
                row=1, col=2
            )
        
        fig.update_xaxes(title_text="Percentual de Climatização (%)")
        fig.update_yaxes(title_text="Taxa de Aprovação IDEB")
        fig.update_layout(height=500, title_text="Correlação: Climatização vs Performance IDEB")
        
        return fig
    
    def create_correlation_heatmap(self, data):
        """Create correlation heatmap for numerical variables"""
        
        if data.empty:
            return None
        
        data_viz = data.copy()
        data_viz['Percentual_AC'] = (data_viz['Salas com Ar'] / data_viz['Total de Salas'] * 100).fillna(0)
        
        # Select numerical columns
        numerical_cols = ['Total de Salas', 'Salas com Ar', 'Percentual_AC']
        
        # Add IDEB columns if they have data
        if not data_viz['IDEB Iniciais'].dropna().empty:
            numerical_cols.append('IDEB Iniciais')
        if not data_viz['IDEB Finais'].dropna().empty:
            numerical_cols.append('IDEB Finais')
        
        if len(numerical_cols) < 2:
            return None
        
        # Calculate correlation matrix
        corr_matrix = data_viz[numerical_cols].corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Matriz de Correlação entre Variáveis",
            color_continuous_scale='RdBu',
            zmin=-1,
            zmax=1
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def create_neighborhood_distribution(self, data):
        """Create neighborhood distribution chart"""
        
        if data.empty or 'Bairro' not in data.columns:
            return None
        
        # Count schools by neighborhood
        neighborhood_counts = data['Bairro'].value_counts().head(20)  # Top 20 neighborhoods
        
        fig = px.bar(
            x=neighborhood_counts.index,
            y=neighborhood_counts.values,
            title="Distribuição de Escolas por Bairro (Top 20)",
            labels={'x': 'Bairro', 'y': 'Número de Escolas'},
            color=neighborhood_counts.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500)
        
        return fig
    
    def create_performance_histogram(self, data):
        """Create histogram of IDEB performance"""
        
        if data.empty:
            return None
        
        # Prepare data for histogram
        hist_data = []
        
        if not data['IDEB Iniciais'].dropna().empty:
            hist_data.extend([
                {'Nível': 'Anos Iniciais', 'IDEB': val} 
                for val in data['IDEB Iniciais'].dropna()
            ])
        
        if not data['IDEB Finais'].dropna().empty:
            hist_data.extend([
                {'Nível': 'Anos Finais', 'IDEB': val} 
                for val in data['IDEB Finais'].dropna()
            ])
        
        if not hist_data:
            return None
        
        df_hist = pd.DataFrame(hist_data)
        
        fig = px.histogram(
            df_hist,
            x='IDEB',
            color='Nível',
            title="Distribuição das Taxas de Aprovação IDEB",
            barmode='overlay',
            opacity=0.7,
            nbins=20
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_size_vs_performance_chart(self, data):
        """Create chart showing relationship between school size and performance"""
        
        if data.empty:
            return None
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Tamanho vs IDEB Iniciais', 'Tamanho vs IDEB Finais']
        )
        
        # Size vs IDEB Iniciais
        if not data['IDEB Iniciais'].dropna().empty:
            fig.add_trace(
                go.Scatter(
                    x=data['Total de Salas'],
                    y=data['IDEB Iniciais'],
                    mode='markers',
                    name='Anos Iniciais',
                    marker=dict(
                        color=data['Salas com Ar'],
                        colorscale='Viridis',
                        size=8,
                        opacity=0.7,
                        colorbar=dict(title="Salas com AC")
                    ),
                    text=data['Nome da Escola'],
                    hovertemplate='<b>%{text}</b><br>Total Salas: %{x}<br>IDEB: %{y:.1f}<extra></extra>'
                ),
                row=1, col=1
            )
        
        # Size vs IDEB Finais
        if not data['IDEB Finais'].dropna().empty:
            fig.add_trace(
                go.Scatter(
                    x=data['Total de Salas'],
                    y=data['IDEB Finais'],
                    mode='markers',
                    name='Anos Finais',
                    marker=dict(
                        color=data['Salas com Ar'],
                        colorscale='Plasma',
                        size=8,
                        opacity=0.7
                    ),
                    text=data['Nome da Escola'],
                    hovertemplate='<b>%{text}</b><br>Total Salas: %{x}<br>IDEB: %{y:.1f}<extra></extra>'
                ),
                row=1, col=2
            )
        
        fig.update_xaxes(title_text="Número Total de Salas")
        fig.update_yaxes(title_text="Taxa de Aprovação IDEB")
        fig.update_layout(height=500, title_text="Relação: Tamanho da Escola vs Performance")
        
        return fig

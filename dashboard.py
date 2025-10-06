#!/usr/bin/env python3
"""
Comprehensive Medical Device Incidents Dashboard
Interactive web-based dashboard with advanced analytics and insights
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from collections import Counter
from wordcloud import WordCloud
import base64
import io
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns


class MedicalDeviceDashboard:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.load_data()
        self.setup_layout()
        self.setup_callbacks()
    
    def load_data(self):
        """Load and prepare the medical device incidents data"""
        print("Loading data for dashboard...")
        
        # Load main incident data
        if os.path.exists("medical_device_incidents_enhanced_sept2024_sept2025.csv"):
            self.df = pd.read_csv("medical_device_incidents_enhanced_sept2024_sept2025.csv")
        else:
            self.df = pd.read_csv("medical_device_incidents_sept2024_sept2025.csv")
        
        # Clean and prepare data
        self.df['RECEIPT_DT'] = pd.to_datetime(self.df['RECEIPT_DT'])
        self.df['month_year'] = self.df['RECEIPT_DT'].dt.to_period('M')
        self.df['weekday'] = self.df['RECEIPT_DT'].dt.day_name()
        self.df['quarter'] = self.df['RECEIPT_DT'].dt.quarter
        
        # Load additional datasets
        self.load_device_data()
        self.load_company_data()
        
        print(f"Loaded {len(self.df)} incident records")
    
    def load_device_data(self):
        """Load device-specific data"""
        device_file = "mdi_data/INCIDENT_DEVICE.dsv"
        if os.path.exists(device_file):
            self.device_df = pd.read_csv(device_file, sep='|', encoding='utf-8')
            print(f"Loaded {len(self.device_df)} device records")
        else:
            self.device_df = pd.DataFrame()
    
    def load_company_data(self):
        """Load company-specific data"""
        company_file = "mdi_data/INCIDENT_COMPANY.dsv"
        if os.path.exists(company_file):
            self.company_df = pd.read_csv(company_file, sep='|', encoding='utf-8')
            print(f"Loaded {len(self.company_df)} company records")
        else:
            self.company_df = pd.DataFrame()
    
    def setup_layout(self):
        """Setup the dashboard layout"""
        self.app.layout = html.Div([
            html.H1("🏥 Medical Device Incidents Dashboard", 
                   style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
            
            html.Div([
                html.H3("📊 September 2024 - September 2025 Analysis"),
                html.P(f"Total Incidents: {len(self.df):,}")
            ], style={'textAlign': 'center', 'backgroundColor': '#ecf0f1', 'padding': 20, 'marginBottom': 30}),
            
            # Key Metrics Cards
            html.Div([
                html.Div([
                    html.H4("Total Incidents"),
                    html.H2(f"{len(self.df):,}", style={'color': '#e74c3c'})
                ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%', 
                                                  'padding': 20, 'backgroundColor': '#fff', 'border': '1px solid #ddd', 'borderRadius': 5}),
                
                html.Div([
                    html.H4("Deaths"),
                    html.H2(f"{len(self.df[self.df['HAZARD_SEVERITY_CODE_E'] == 'DEATH']):,}", style={'color': '#c0392b'})
                ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%',
                                                  'padding': 20, 'backgroundColor': '#fff', 'border': '1px solid #ddd', 'borderRadius': 5}),
                
                html.Div([
                    html.H4("Injuries"),
                    html.H2(f"{len(self.df[self.df['HAZARD_SEVERITY_CODE_E'] == 'INJURY']):,}", style={'color': '#f39c12'})
                ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%',
                                                  'padding': 20, 'backgroundColor': '#fff', 'border': '1px solid #ddd', 'borderRadius': 5}),
                
                html.Div([
                    html.H4("Companies Involved"),
                    html.H2(f"{len(self.company_df['COMPANY_NAME'].unique()) if not self.company_df.empty else 'N/A'}", style={'color': '#3498db'})
                ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%',
                                                  'padding': 20, 'backgroundColor': '#fff', 'border': '1px solid #ddd', 'borderRadius': 5})
            ]),
            
            # Tabs for different analyses
            dcc.Tabs(id="tabs", value='temporal', children=[
                dcc.Tab(label='📅 Temporal Analysis', value='temporal'),
                dcc.Tab(label='⚠️ Severity Analysis', value='severity'),
                dcc.Tab(label='🏭 Company Analysis', value='company'),
                dcc.Tab(label='🔧 Device Analysis', value='device'),
                dcc.Tab(label='🎯 Advanced Analytics', value='advanced'),
                dcc.Tab(label='📈 Trends & Patterns', value='trends')
            ]),
            
            html.Div(id='tab-content')
        ])
    
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        @callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
        def render_content(tab):
            if tab == 'temporal':
                return self.render_temporal_analysis()
            elif tab == 'severity':
                return self.render_severity_analysis()
            elif tab == 'company':
                return self.render_company_analysis()
            elif tab == 'device':
                return self.render_device_analysis()
            elif tab == 'advanced':
                return self.render_advanced_analytics()
            elif tab == 'trends':
                return self.render_trends_patterns()
    
    def render_temporal_analysis(self):
        """Render temporal analysis tab"""
        # Monthly trend
        monthly_counts = self.df.groupby('month_year').size().reset_index(name='count')
        monthly_counts['month_year_str'] = monthly_counts['month_year'].astype(str)
        
        fig_monthly = px.line(monthly_counts, x='month_year_str', y='count',
                             title='Monthly Incident Trends',
                             labels={'month_year_str': 'Month', 'count': 'Number of Incidents'})
        fig_monthly.update_layout(height=400)
        
        # Weekly pattern
        weekday_counts = self.df['weekday'].value_counts()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_counts = weekday_counts.reindex(weekday_order)
        
        fig_weekday = px.bar(x=weekday_counts.index, y=weekday_counts.values,
                            title='Incidents by Day of Week',
                            labels={'x': 'Day of Week', 'y': 'Number of Incidents'})
        fig_weekday.update_layout(height=400)
        
        # Heatmap of incidents by month and severity
        severity_month = pd.crosstab(self.df['month_year'].astype(str), 
                                   self.df['HAZARD_SEVERITY_CODE_E'], margins=True)
        
        fig_heatmap = px.imshow(severity_month.iloc[:-1, :-1].T,
                               title='Incidents Heatmap: Month vs Severity',
                               labels={'x': 'Month', 'y': 'Severity Level', 'color': 'Count'})
        fig_heatmap.update_layout(height=400)
        
        return html.Div([
            html.H2("📅 Temporal Analysis"),
            dcc.Graph(figure=fig_monthly),
            html.Div([
                html.Div([dcc.Graph(figure=fig_weekday)], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(figure=fig_heatmap)], style={'width': '48%', 'float': 'right'})
            ])
        ])
    
    def render_severity_analysis(self):
        """Render severity analysis tab"""
        # Severity distribution
        severity_counts = self.df['HAZARD_SEVERITY_CODE_E'].value_counts()
        
        fig_severity_pie = px.pie(values=severity_counts.values, names=severity_counts.index,
                                 title='Distribution of Incident Severity Levels')
        
        # Severity trends over time
        severity_monthly = self.df.groupby(['month_year', 'HAZARD_SEVERITY_CODE_E']).size().reset_index(name='count')
        severity_monthly['month_year_str'] = severity_monthly['month_year'].astype(str)
        
        fig_severity_trend = px.line(severity_monthly, x='month_year_str', y='count',
                                   color='HAZARD_SEVERITY_CODE_E',
                                   title='Severity Trends Over Time')
        fig_severity_trend.update_layout(height=400)
        
        # Death and injury incidents by type
        critical_incidents = self.df[self.df['HAZARD_SEVERITY_CODE_E'].isin(['DEATH', 'INJURY'])]
        critical_by_type = critical_incidents.groupby(['INCIDENT_TYPE_E', 'HAZARD_SEVERITY_CODE_E']).size().reset_index(name='count')
        
        fig_critical = px.bar(critical_by_type, x='INCIDENT_TYPE_E', y='count',
                             color='HAZARD_SEVERITY_CODE_E',
                             title='Death and Injury Incidents by Report Type')
        fig_critical.update_layout(height=400, xaxis_tickangle=-45)
        
        return html.Div([
            html.H2("⚠️ Severity Analysis"),
            html.Div([
                html.Div([dcc.Graph(figure=fig_severity_pie)], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(figure=fig_severity_trend)], style={'width': '48%', 'float': 'right'})
            ]),
            dcc.Graph(figure=fig_critical)
        ])
    
    def render_company_analysis(self):
        """Render company analysis tab"""
        if self.company_df.empty:
            return html.Div([html.H2("🏭 Company Analysis"), html.P("No company data available")])
        
        # Top companies by incident count
        company_incidents = self.company_df['COMPANY_NAME'].value_counts().head(15)
        
        fig_companies = px.bar(x=company_incidents.values, y=company_incidents.index,
                              orientation='h',
                              title='Top 15 Companies by Incident Count',
                              labels={'x': 'Number of Incidents', 'y': 'Company'})
        fig_companies.update_layout(height=600)
        
        # Company types
        if 'COMPANY_TYPE_E' in self.company_df.columns:
            company_types = self.company_df['COMPANY_TYPE_E'].value_counts()
            fig_types = px.pie(values=company_types.values, names=company_types.index,
                              title='Distribution of Company Types')
        else:
            fig_types = go.Figure()
        
        # Company role analysis
        if 'ROLE_E' in self.company_df.columns:
            role_counts = self.company_df['ROLE_E'].value_counts()
            fig_roles = px.bar(x=role_counts.index, y=role_counts.values,
                              title='Company Roles in Incidents')
            fig_roles.update_layout(xaxis_tickangle=-45)
        else:
            fig_roles = go.Figure()
        
        return html.Div([
            html.H2("🏭 Company Analysis"),
            dcc.Graph(figure=fig_companies),
            html.Div([
                html.Div([dcc.Graph(figure=fig_types)], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(figure=fig_roles)], style={'width': '48%', 'float': 'right'})
            ])
        ])
    
    def render_device_analysis(self):
        """Render device analysis tab"""
        if self.device_df.empty:
            return html.Div([html.H2("🔧 Device Analysis"), html.P("No device data available")])
        
        # Device usage categories
        if 'USAGE_CODE_TERM_E' in self.device_df.columns:
            usage_counts = self.device_df['USAGE_CODE_TERM_E'].value_counts().head(15)
            fig_usage = px.bar(x=usage_counts.values, y=usage_counts.index,
                              orientation='h',
                              title='Top Device Usage Categories',
                              labels={'x': 'Number of Incidents', 'y': 'Usage Category'})
            fig_usage.update_layout(height=500)
        else:
            fig_usage = go.Figure()
        
        # Risk classification
        if 'RISK_CLASSIFICATION' in self.device_df.columns:
            risk_counts = self.device_df['RISK_CLASSIFICATION'].value_counts()
            fig_risk = px.pie(values=risk_counts.values, names=risk_counts.index,
                             title='Device Risk Classification Distribution')
        else:
            fig_risk = go.Figure()
        
        # Top trade names
        if 'TRADE_NAME' in self.device_df.columns:
            trade_names = self.device_df['TRADE_NAME'].value_counts().head(10)
            fig_trade = px.bar(x=trade_names.index, y=trade_names.values,
                              title='Top 10 Device Trade Names by Incidents')
            fig_trade.update_layout(xaxis_tickangle=-45)
        else:
            fig_trade = go.Figure()
        
        return html.Div([
            html.H2("🔧 Device Analysis"),
            dcc.Graph(figure=fig_usage),
            html.Div([
                html.Div([dcc.Graph(figure=fig_risk)], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(figure=fig_trade)], style={'width': '48%', 'float': 'right'})
            ])
        ])
    
    def render_advanced_analytics(self):
        """Render advanced analytics tab"""
        # Incident clustering analysis
        clustering_data = self.prepare_clustering_data()
        
        # Correlation analysis
        correlation_fig = self.create_correlation_analysis()
        
        # Risk prediction model insights
        risk_insights = self.analyze_risk_patterns()
        
        # Seasonal decomposition
        seasonal_fig = self.create_seasonal_analysis()
        
        return html.Div([
            html.H2("🎯 Advanced Analytics"),
            html.H3("📊 Incident Clustering Analysis"),
            dcc.Graph(figure=clustering_data),
            html.H3("🔗 Correlation Analysis"),
            dcc.Graph(figure=correlation_fig),
            html.H3("📈 Seasonal Pattern Analysis"),
            dcc.Graph(figure=seasonal_fig),
            html.H3("🎯 Risk Pattern Insights"),
            html.Div(risk_insights)
        ])
    
    def render_trends_patterns(self):
        """Render trends and patterns analysis"""
        # Growth rate analysis
        growth_fig = self.analyze_growth_patterns()
        
        # Anomaly detection
        anomaly_fig = self.detect_anomalies()
        
        # Predictive insights
        prediction_insights = self.generate_predictions()
        
        return html.Div([
            html.H2("📈 Trends & Patterns"),
            html.H3("📊 Growth Rate Analysis"),
            dcc.Graph(figure=growth_fig),
            html.H3("🚨 Anomaly Detection"),
            dcc.Graph(figure=anomaly_fig),
            html.H3("🔮 Predictive Insights"),
            html.Div(prediction_insights)
        ])
    
    def prepare_clustering_data(self):
        """Prepare data for clustering analysis"""
        try:
            # Create features for clustering
            monthly_stats = self.df.groupby('month_year').agg({
                'INCIDENT_ID': 'count',
                'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum(),
                'INCIDENT_TYPE_E': lambda x: (x == 'Mandatory problem report').sum()
            }).reset_index()
            
            monthly_stats.columns = ['month', 'total_incidents', 'deaths', 'mandatory_reports']
            monthly_stats['month_str'] = monthly_stats['month'].astype(str)
            
            # Perform clustering
            features = monthly_stats[['total_incidents', 'deaths', 'mandatory_reports']]
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            kmeans = KMeans(n_clusters=3, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            monthly_stats['cluster'] = clusters
            
            fig = px.scatter_3d(monthly_stats, x='total_incidents', y='deaths', z='mandatory_reports',
                               color='cluster', hover_data=['month_str'],
                               title='Monthly Incident Patterns Clustering')
            return fig
        except Exception as e:
            return go.Figure().add_annotation(text=f"Clustering analysis unavailable: {str(e)}")
    
    def create_correlation_analysis(self):
        """Create correlation analysis visualization"""
        try:
            # Create numeric features for correlation
            monthly_data = self.df.groupby('month_year').agg({
                'INCIDENT_ID': 'count',
                'HAZARD_SEVERITY_CODE_E': [
                    lambda x: (x == 'DEATH').sum(),
                    lambda x: (x == 'INJURY').sum(),
                    lambda x: (x == 'POTENTIAL FOR DEATH/INJURY').sum()
                ],
                'INCIDENT_TYPE_E': lambda x: (x == 'Mandatory problem report').sum()
            }).reset_index()
            
            # Flatten column names
            monthly_data.columns = ['month', 'total_incidents', 'deaths', 'injuries', 'potential_harm', 'mandatory_reports']
            
            # Calculate correlation matrix
            corr_matrix = monthly_data[['total_incidents', 'deaths', 'injuries', 'potential_harm', 'mandatory_reports']].corr()
            
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                           title='Correlation Matrix of Incident Metrics')
            return fig
        except Exception as e:
            return go.Figure().add_annotation(text=f"Correlation analysis unavailable: {str(e)}")
    
    def create_seasonal_analysis(self):
        """Create seasonal decomposition analysis"""
        try:
            monthly_counts = self.df.groupby('month_year').size()
            
            # Simple moving average for trend
            ma_3 = monthly_counts.rolling(window=3).mean()
            ma_6 = monthly_counts.rolling(window=6).mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly_counts.index.astype(str), y=monthly_counts.values,
                                   mode='lines+markers', name='Actual'))
            fig.add_trace(go.Scatter(x=ma_3.index.astype(str), y=ma_3.values,
                                   mode='lines', name='3-Month MA'))
            fig.add_trace(go.Scatter(x=ma_6.index.astype(str), y=ma_6.values,
                                   mode='lines', name='6-Month MA'))
            
            fig.update_layout(title='Seasonal Trends with Moving Averages',
                            xaxis_title='Month', yaxis_title='Number of Incidents')
            return fig
        except Exception as e:
            return go.Figure().add_annotation(text=f"Seasonal analysis unavailable: {str(e)}")
    
    def analyze_risk_patterns(self):
        """Analyze risk patterns and return insights"""
        insights = []
        
        # Death rate analysis
        total_incidents = len(self.df)
        deaths = len(self.df[self.df['HAZARD_SEVERITY_CODE_E'] == 'DEATH'])
        death_rate = (deaths / total_incidents) * 100 if total_incidents > 0 else 0
        
        insights.append(html.P(f"• Death rate: {death_rate:.2f}% ({deaths} deaths out of {total_incidents:,} incidents)"))
        
        # High-risk periods
        monthly_deaths = self.df[self.df['HAZARD_SEVERITY_CODE_E'] == 'DEATH'].groupby('month_year').size()
        if not monthly_deaths.empty:
            worst_month = monthly_deaths.idxmax()
            insights.append(html.P(f"• Highest death incidents in: {worst_month} ({monthly_deaths.max()} deaths)"))
        
        # Risk by incident type
        risk_by_type = self.df.groupby('INCIDENT_TYPE_E')['HAZARD_SEVERITY_CODE_E'].apply(
            lambda x: (x == 'DEATH').sum()
        ).sort_values(ascending=False)
        
        if not risk_by_type.empty:
            riskiest_type = risk_by_type.index[0]
            insights.append(html.P(f"• Riskiest incident type: {riskiest_type} ({risk_by_type.iloc[0]} deaths)"))
        
        return insights
    
    def analyze_growth_patterns(self):
        """Analyze growth patterns"""
        monthly_counts = self.df.groupby('month_year').size().reset_index(name='count')
        monthly_counts['month_str'] = monthly_counts['month_year'].astype(str)
        monthly_counts['growth_rate'] = monthly_counts['count'].pct_change() * 100
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=monthly_counts['month_str'], y=monthly_counts['count'], name="Incidents"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=monthly_counts['month_str'], y=monthly_counts['growth_rate'], 
                      mode='lines+markers', name="Growth Rate %"),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Number of Incidents", secondary_y=False)
        fig.update_yaxes(title_text="Growth Rate (%)", secondary_y=True)
        fig.update_layout(title_text="Incident Growth Patterns")
        
        return fig
    
    def detect_anomalies(self):
        """Detect anomalies in incident patterns"""
        monthly_counts = self.df.groupby('month_year').size()
        
        # Simple anomaly detection using standard deviation
        mean_incidents = monthly_counts.mean()
        std_incidents = monthly_counts.std()
        
        anomalies = monthly_counts[(monthly_counts > mean_incidents + 2*std_incidents) | 
                                 (monthly_counts < mean_incidents - 2*std_incidents)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly_counts.index.astype(str), y=monthly_counts.values,
                               mode='lines+markers', name='Normal'))
        
        if not anomalies.empty:
            fig.add_trace(go.Scatter(x=anomalies.index.astype(str), y=anomalies.values,
                                   mode='markers', marker=dict(size=12, color='red'),
                                   name='Anomalies'))
        
        fig.add_hline(y=mean_incidents, line_dash="dash", annotation_text="Mean")
        fig.add_hline(y=mean_incidents + 2*std_incidents, line_dash="dot", annotation_text="Upper Threshold")
        fig.add_hline(y=mean_incidents - 2*std_incidents, line_dash="dot", annotation_text="Lower Threshold")
        
        fig.update_layout(title='Anomaly Detection in Monthly Incidents')
        return fig
    
    def generate_predictions(self):
        """Generate predictive insights"""
        insights = []
        
        # Simple trend analysis
        monthly_counts = self.df.groupby('month_year').size()
        recent_trend = monthly_counts.tail(3).mean()
        overall_avg = monthly_counts.mean()
        
        if recent_trend > overall_avg:
            insights.append(html.P("📈 Upward trend detected in recent months"))
        else:
            insights.append(html.P("📉 Downward or stable trend in recent months"))
        
        # Seasonality insights
        self.df['month_num'] = self.df['RECEIPT_DT'].dt.month
        seasonal_pattern = self.df.groupby('month_num').size()
        peak_month = seasonal_pattern.idxmax()
        month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                      5: 'May', 6: 'June', 7: 'July', 8: 'August',
                      9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        
        insights.append(html.P(f"📅 Peak incident month historically: {month_names.get(peak_month, peak_month)}"))
        
        # Risk prediction
        death_rate = len(self.df[self.df['HAZARD_SEVERITY_CODE_E'] == 'DEATH']) / len(self.df) * 100
        if death_rate > 2:
            insights.append(html.P("⚠️ High death rate detected - enhanced monitoring recommended"))
        
        return insights
    
    def run(self, debug=True, port=8050):
        """Run the dashboard"""
        print(f"Starting Medical Device Incidents Dashboard...")
        print(f"Dashboard will be available at: http://localhost:{port}")
        self.app.run_server(debug=debug, port=port)


if __name__ == "__main__":
    dashboard = MedicalDeviceDashboard()
    dashboard.run()
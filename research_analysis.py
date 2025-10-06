#!/usr/bin/env python3
"""
Medical Device Incidents Research Insights Generator
Advanced research analytics and insights for the medical device incidents data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class MedicalDeviceResearch:
    """Advanced research analytics for medical device incidents"""
    
    def __init__(self):
        self.load_data()
        self.prepare_features()
    
    def load_data(self):
        """Load all available datasets"""
        # Main incident data
        if os.path.exists("medical_device_incidents_enhanced_sept2024_sept2025.csv"):
            self.incidents = pd.read_csv("medical_device_incidents_enhanced_sept2024_sept2025.csv")
        else:
            self.incidents = pd.read_csv("medical_device_incidents_sept2024_sept2025.csv")
        
        # Device data
        if os.path.exists("mdi_data/INCIDENT_DEVICE.dsv"):
            self.devices = pd.read_csv("mdi_data/INCIDENT_DEVICE.dsv", sep='|', encoding='utf-8')
        else:
            self.devices = pd.DataFrame()
        
        # Company data
        if os.path.exists("mdi_data/INCIDENT_COMPANY.dsv"):
            self.companies = pd.read_csv("mdi_data/INCIDENT_COMPANY.dsv", sep='|', encoding='utf-8')
        else:
            self.companies = pd.DataFrame()
        
        print(f"Loaded data: {len(self.incidents)} incidents, {len(self.devices)} devices, {len(self.companies)} companies")
    
    def prepare_features(self):
        """Prepare features for analysis"""
        self.incidents['RECEIPT_DT'] = pd.to_datetime(self.incidents['RECEIPT_DT'])
        self.incidents['month'] = self.incidents['RECEIPT_DT'].dt.month
        self.incidents['weekday'] = self.incidents['RECEIPT_DT'].dt.weekday
        self.incidents['is_weekend'] = self.incidents['weekday'].isin([5, 6])
        self.incidents['quarter'] = self.incidents['RECEIPT_DT'].dt.quarter
        
        # Create severity score
        severity_mapping = {
            'DEATH': 5,
            'INJURY': 4,
            'POTENTIAL FOR DEATH/INJURY': 3,
            'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES': 2,
            'UNASSIGNED': 1
        }
        self.incidents['severity_score'] = self.incidents['HAZARD_SEVERITY_CODE_E'].map(severity_mapping).fillna(1)
    
    def generate_research_insights(self):
        """Generate comprehensive research insights"""
        insights = {
            'temporal_patterns': self.analyze_temporal_patterns(),
            'risk_factors': self.identify_risk_factors(),
            'device_analysis': self.analyze_device_patterns(),
            'company_analysis': self.analyze_company_patterns(),
            'predictive_modeling': self.build_predictive_models(),
            'clustering_analysis': self.perform_clustering_analysis(),
            'statistical_tests': self.perform_statistical_tests()
        }
        
        return insights
    
    def analyze_temporal_patterns(self):
        """Analyze temporal patterns in incidents"""
        results = {}
        
        # Monthly seasonality
        monthly_stats = self.incidents.groupby('month').agg({
            'INCIDENT_ID': 'count',
            'severity_score': 'mean',
            'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
        }).round(2)
        
        results['monthly_patterns'] = {
            'peak_month': monthly_stats['INCIDENT_ID'].idxmax(),
            'peak_incidents': monthly_stats['INCIDENT_ID'].max(),
            'lowest_month': monthly_stats['INCIDENT_ID'].idxmin(),
            'lowest_incidents': monthly_stats['INCIDENT_ID'].min(),
            'most_severe_month': monthly_stats['severity_score'].idxmax(),
            'highest_death_month': monthly_stats['HAZARD_SEVERITY_CODE_E'].idxmax()
        }
        
        # Weekend vs weekday analysis
        weekend_stats = self.incidents.groupby('is_weekend').agg({
            'INCIDENT_ID': 'count',
            'severity_score': 'mean'
        }).round(2)
        
        results['weekend_analysis'] = {
            'weekend_incidents': weekend_stats.loc[True, 'INCIDENT_ID'] if True in weekend_stats.index else 0,
            'weekday_incidents': weekend_stats.loc[False, 'INCIDENT_ID'] if False in weekend_stats.index else 0,
            'weekend_severity': weekend_stats.loc[True, 'severity_score'] if True in weekend_stats.index else 0,
            'weekday_severity': weekend_stats.loc[False, 'severity_score'] if False in weekend_stats.index else 0
        }
        
        # Growth trend analysis
        monthly_trend = self.incidents.groupby(self.incidents['RECEIPT_DT'].dt.to_period('M')).size()
        growth_rates = monthly_trend.pct_change().dropna()
        
        results['growth_analysis'] = {
            'avg_monthly_growth': growth_rates.mean() * 100,
            'volatility': growth_rates.std() * 100,
            'months_with_growth': (growth_rates > 0).sum(),
            'months_with_decline': (growth_rates < 0).sum()
        }
        
        return results
    
    def identify_risk_factors(self):
        """Identify key risk factors for severe incidents"""
        results = {}
        
        # Create binary target for severe incidents (death or injury)
        severe_incidents = self.incidents['HAZARD_SEVERITY_CODE_E'].isin(['DEATH', 'INJURY'])
        
        # Risk by incident type
        risk_by_type = self.incidents.groupby('INCIDENT_TYPE_E').agg({
            'INCIDENT_ID': 'count',
            'HAZARD_SEVERITY_CODE_E': lambda x: (x.isin(['DEATH', 'INJURY'])).sum()
        })
        risk_by_type['risk_rate'] = (risk_by_type['HAZARD_SEVERITY_CODE_E'] / risk_by_type['INCIDENT_ID'] * 100).round(2)
        
        results['incident_type_risk'] = risk_by_type.sort_values('risk_rate', ascending=False).to_dict()
        
        # Risk by source
        if 'SOURCE_OF_RECALL_E' in self.incidents.columns:
            risk_by_source = self.incidents.groupby('SOURCE_OF_RECALL_E').agg({
                'INCIDENT_ID': 'count',
                'HAZARD_SEVERITY_CODE_E': lambda x: (x.isin(['DEATH', 'INJURY'])).sum()
            })
            risk_by_source['risk_rate'] = (risk_by_source['HAZARD_SEVERITY_CODE_E'] / risk_by_source['INCIDENT_ID'] * 100).round(2)
            results['source_risk'] = risk_by_source.sort_values('risk_rate', ascending=False).to_dict()
        
        # Temporal risk factors
        temporal_risk = self.incidents.groupby(['month', 'is_weekend']).agg({
            'INCIDENT_ID': 'count',
            'severity_score': 'mean'
        }).round(2)
        
        results['temporal_risk'] = temporal_risk.to_dict()
        
        return results
    
    def analyze_device_patterns(self):
        """Analyze device-related patterns"""
        if self.devices.empty:
            return {"message": "No device data available"}
        
        results = {}
        
        # Merge device data with incidents
        device_incidents = self.devices.merge(self.incidents[['INCIDENT_ID', 'HAZARD_SEVERITY_CODE_E', 'severity_score']], 
                                            on='INCIDENT_ID', how='inner')
        
        # Risk by device usage category
        if 'USAGE_CODE_TERM_E' in device_incidents.columns:
            usage_risk = device_incidents.groupby('USAGE_CODE_TERM_E').agg({
                'INCIDENT_ID': 'count',
                'severity_score': 'mean',
                'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
            }).round(2)
            
            usage_risk['death_rate'] = (usage_risk['HAZARD_SEVERITY_CODE_E'] / usage_risk['INCIDENT_ID'] * 100).round(2)
            results['usage_category_risk'] = usage_risk.sort_values('death_rate', ascending=False).head(10).to_dict()
        
        # Risk by device classification
        if 'RISK_CLASSIFICATION' in device_incidents.columns:
            class_risk = device_incidents.groupby('RISK_CLASSIFICATION').agg({
                'INCIDENT_ID': 'count',
                'severity_score': 'mean',
                'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
            }).round(2)
            
            results['risk_classification_analysis'] = class_risk.to_dict()
        
        # Most problematic devices
        if 'TRADE_NAME' in device_incidents.columns:
            device_problems = device_incidents.groupby('TRADE_NAME').agg({
                'INCIDENT_ID': 'count',
                'severity_score': 'mean',
                'HAZARD_SEVERITY_CODE_E': lambda x: (x.isin(['DEATH', 'INJURY'])).sum()
            }).round(2)
            
            # Filter devices with at least 5 incidents
            device_problems = device_problems[device_problems['INCIDENT_ID'] >= 5]
            device_problems['severe_rate'] = (device_problems['HAZARD_SEVERITY_CODE_E'] / device_problems['INCIDENT_ID'] * 100).round(2)
            
            results['problematic_devices'] = device_problems.sort_values('severe_rate', ascending=False).head(10).to_dict()
        
        return results
    
    def analyze_company_patterns(self):
        """Analyze company-related patterns"""
        if self.companies.empty:
            return {"message": "No company data available"}
        
        results = {}
        
        # Merge company data with incidents
        company_incidents = self.companies.merge(self.incidents[['INCIDENT_ID', 'HAZARD_SEVERITY_CODE_E', 'severity_score']], 
                                               on='INCIDENT_ID', how='inner')
        
        # Company performance analysis
        company_stats = company_incidents.groupby('COMPANY_NAME').agg({
            'INCIDENT_ID': 'count',
            'severity_score': 'mean',
            'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
        }).round(2)
        
        # Filter companies with at least 10 incidents
        company_stats = company_stats[company_stats['INCIDENT_ID'] >= 10]
        company_stats['death_rate'] = (company_stats['HAZARD_SEVERITY_CODE_E'] / company_stats['INCIDENT_ID'] * 100).round(2)
        
        results['company_performance'] = {
            'highest_incident_companies': company_stats.sort_values('INCIDENT_ID', ascending=False).head(10).to_dict(),
            'highest_death_rate_companies': company_stats.sort_values('death_rate', ascending=False).head(10).to_dict(),
            'highest_severity_companies': company_stats.sort_values('severity_score', ascending=False).head(10).to_dict()
        }
        
        # Role analysis
        if 'ROLE_E' in company_incidents.columns:
            role_stats = company_incidents.groupby('ROLE_E').agg({
                'INCIDENT_ID': 'count',
                'severity_score': 'mean'
            }).round(2)
            
            results['role_analysis'] = role_stats.to_dict()
        
        return results
    
    def build_predictive_models(self):
        """Build predictive models for incident severity"""
        try:
            # Prepare features for modeling
            model_data = self.incidents.copy()
            
            # Create target variable (binary: severe vs not severe)
            model_data['is_severe'] = model_data['HAZARD_SEVERITY_CODE_E'].isin(['DEATH', 'INJURY'])
            
            # Select features
            features = ['month', 'weekday', 'is_weekend', 'quarter']
            
            # Encode categorical variables
            le_incident_type = LabelEncoder()
            model_data['incident_type_encoded'] = le_incident_type.fit_transform(model_data['INCIDENT_TYPE_E'])
            features.append('incident_type_encoded')
            
            if 'SOURCE_OF_RECALL_E' in model_data.columns:
                le_source = LabelEncoder()
                model_data['source_encoded'] = le_source.fit_transform(model_data['SOURCE_OF_RECALL_E'].fillna('Unknown'))
                features.append('source_encoded')
            
            X = model_data[features]
            y = model_data['is_severe']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            # Train Random Forest model
            rf = RandomForestClassifier(n_estimators=100, random_state=42)
            rf.fit(X_train, y_train)
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': features,
                'importance': rf.feature_importances_
            }).sort_values('importance', ascending=False)
            
            # Predictions
            y_pred = rf.predict(X_test)
            
            # Classification report
            report = classification_report(y_test, y_pred, output_dict=True)
            
            return {
                'model_performance': {
                    'accuracy': report['accuracy'],
                    'precision': report['True']['precision'],
                    'recall': report['True']['recall'],
                    'f1_score': report['True']['f1-score']
                },
                'feature_importance': feature_importance.to_dict('records'),
                'prediction_insights': {
                    'most_important_factor': feature_importance.iloc[0]['feature'],
                    'top_3_factors': feature_importance.head(3)['feature'].tolist()
                }
            }
        
        except Exception as e:
            return {"error": f"Predictive modeling failed: {str(e)}"}
    
    def perform_clustering_analysis(self):
        """Perform clustering analysis on incidents"""
        try:
            # Prepare features for clustering
            cluster_features = self.incidents.groupby(self.incidents['RECEIPT_DT'].dt.to_period('M')).agg({
                'INCIDENT_ID': 'count',
                'severity_score': 'mean',
                'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
            }).reset_index()
            
            cluster_features.columns = ['month', 'incident_count', 'avg_severity', 'death_count']
            
            # Standardize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(cluster_features[['incident_count', 'avg_severity', 'death_count']])
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=3, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            cluster_features['cluster'] = clusters
            
            # Analyze clusters
            cluster_analysis = cluster_features.groupby('cluster').agg({
                'incident_count': ['mean', 'std'],
                'avg_severity': ['mean', 'std'],
                'death_count': ['mean', 'std']
            }).round(2)
            
            return {
                'cluster_centers': kmeans.cluster_centers_.tolist(),
                'cluster_analysis': cluster_analysis.to_dict(),
                'cluster_assignments': cluster_features[['month', 'cluster']].to_dict('records')
            }
        
        except Exception as e:
            return {"error": f"Clustering analysis failed: {str(e)}"}
    
    def perform_statistical_tests(self):
        """Perform statistical tests on the data"""
        from scipy import stats
        
        results = {}
        
        try:
            # Test if weekend incidents are more severe
            weekend_severity = self.incidents[self.incidents['is_weekend'] == True]['severity_score']
            weekday_severity = self.incidents[self.incidents['is_weekend'] == False]['severity_score']
            
            t_stat, p_value = stats.ttest_ind(weekend_severity, weekday_severity)
            results['weekend_severity_test'] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'interpretation': 'Weekend incidents are significantly different in severity' if p_value < 0.05 else 'No significant difference in weekend vs weekday severity'
            }
            
            # Chi-square test for incident type vs severity
            contingency_table = pd.crosstab(self.incidents['INCIDENT_TYPE_E'], 
                                          self.incidents['HAZARD_SEVERITY_CODE_E'])
            chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
            
            results['incident_type_severity_test'] = {
                'chi2_statistic': chi2,
                'p_value': p_val,
                'degrees_of_freedom': dof,
                'significant': p_val < 0.05,
                'interpretation': 'Incident type is significantly associated with severity' if p_val < 0.05 else 'No significant association between incident type and severity'
            }
            
            # Correlation analysis
            numeric_cols = ['month', 'weekday', 'quarter', 'severity_score']
            correlation_matrix = self.incidents[numeric_cols].corr()
            
            results['correlations'] = correlation_matrix.to_dict()
            
        except Exception as e:
            results['error'] = f"Statistical tests failed: {str(e)}"
        
        return results
    
    def create_research_report(self):
        """Create a comprehensive research report"""
        print("Generating comprehensive research insights...")
        insights = self.generate_research_insights()
        
        report_file = "medical_device_incidents_research_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("MEDICAL DEVICE INCIDENTS RESEARCH REPORT\n")
            f.write("="*50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data Period: September 2024 - September 2025\n")
            f.write(f"Total Incidents Analyzed: {len(self.incidents):,}\n\n")
            
            # Temporal Patterns
            f.write("1. TEMPORAL PATTERNS ANALYSIS\n")
            f.write("-" * 30 + "\n")
            temp_patterns = insights['temporal_patterns']
            
            f.write(f"Peak Month: Month {temp_patterns['monthly_patterns']['peak_month']} ")
            f.write(f"({temp_patterns['monthly_patterns']['peak_incidents']} incidents)\n")
            f.write(f"Lowest Month: Month {temp_patterns['monthly_patterns']['lowest_month']} ")
            f.write(f"({temp_patterns['monthly_patterns']['lowest_incidents']} incidents)\n")
            f.write(f"Most Severe Month: Month {temp_patterns['monthly_patterns']['most_severe_month']}\n")
            f.write(f"Highest Death Month: Month {temp_patterns['monthly_patterns']['highest_death_month']}\n\n")
            
            f.write("Weekend vs Weekday Analysis:\n")
            weekend_data = temp_patterns['weekend_analysis']
            f.write(f"- Weekend incidents: {weekend_data['weekend_incidents']}\n")
            f.write(f"- Weekday incidents: {weekend_data['weekday_incidents']}\n")
            f.write(f"- Weekend severity: {weekend_data['weekend_severity']}\n")
            f.write(f"- Weekday severity: {weekend_data['weekday_severity']}\n\n")
            
            # Risk Factors
            f.write("2. RISK FACTORS ANALYSIS\n")
            f.write("-" * 30 + "\n")
            risk_factors = insights['risk_factors']
            
            if 'incident_type_risk' in risk_factors:
                f.write("Risk by Incident Type (Top 5):\n")
                risk_data = risk_factors['incident_type_risk']['risk_rate']
                for incident_type, risk_rate in list(risk_data.items())[:5]:
                    f.write(f"- {incident_type}: {risk_rate}% severe\n")
                f.write("\n")
            
            # Predictive Modeling
            f.write("3. PREDICTIVE MODELING RESULTS\n")
            f.write("-" * 30 + "\n")
            pred_results = insights['predictive_modeling']
            
            if 'model_performance' in pred_results:
                perf = pred_results['model_performance']
                f.write(f"Model Accuracy: {perf['accuracy']:.3f}\n")
                f.write(f"Precision: {perf['precision']:.3f}\n")
                f.write(f"Recall: {perf['recall']:.3f}\n")
                f.write(f"F1-Score: {perf['f1_score']:.3f}\n\n")
                
                f.write("Most Important Predictive Factors:\n")
                for factor in pred_results['feature_importance'][:5]:
                    f.write(f"- {factor['feature']}: {factor['importance']:.3f}\n")
                f.write("\n")
            
            # Statistical Tests
            f.write("4. STATISTICAL TESTS\n")
            f.write("-" * 30 + "\n")
            stats_results = insights['statistical_tests']
            
            if 'weekend_severity_test' in stats_results:
                weekend_test = stats_results['weekend_severity_test']
                f.write(f"Weekend vs Weekday Severity Test:\n")
                f.write(f"- P-value: {weekend_test['p_value']:.6f}\n")
                f.write(f"- Significant: {weekend_test['significant']}\n")
                f.write(f"- Interpretation: {weekend_test['interpretation']}\n\n")
            
            # Device Analysis
            f.write("5. DEVICE ANALYSIS\n")
            f.write("-" * 30 + "\n")
            device_analysis = insights['device_analysis']
            
            if 'usage_category_risk' in device_analysis:
                f.write("Highest Risk Device Categories:\n")
                risk_data = device_analysis['usage_category_risk']['death_rate']
                for category, death_rate in list(risk_data.items())[:5]:
                    f.write(f"- {category}: {death_rate}% death rate\n")
                f.write("\n")
            
            # Company Analysis
            f.write("6. COMPANY ANALYSIS\n")
            f.write("-" * 30 + "\n")
            company_analysis = insights['company_analysis']
            
            if 'company_performance' in company_analysis:
                f.write("Companies with Highest Incident Counts:\n")
                high_incident = company_analysis['company_performance']['highest_incident_companies']['INCIDENT_ID']
                for company, count in list(high_incident.items())[:5]:
                    f.write(f"- {company}: {count} incidents\n")
                f.write("\n")
        
        print(f"Research report saved to: {report_file}")
        return insights
    
    def create_visualizations(self):
        """Create advanced visualization plots"""
        print("Creating advanced visualizations...")
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Monthly trend with severity overlay
        monthly_data = self.incidents.groupby(self.incidents['RECEIPT_DT'].dt.to_period('M')).agg({
            'INCIDENT_ID': 'count',
            'severity_score': 'mean'
        })
        
        ax1 = axes[0, 0]
        ax1_twin = ax1.twinx()
        
        line1 = ax1.plot(range(len(monthly_data)), monthly_data['INCIDENT_ID'], 'b-', marker='o', label='Incident Count')
        line2 = ax1_twin.plot(range(len(monthly_data)), monthly_data['severity_score'], 'r-', marker='s', label='Avg Severity')
        
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Incident Count', color='b')
        ax1_twin.set_ylabel('Average Severity Score', color='r')
        ax1.set_title('Monthly Incidents vs Severity Trends')
        ax1.tick_params(axis='x', rotation=45)
        
        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_twin.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # 2. Severity distribution by incident type
        severity_type = pd.crosstab(self.incidents['INCIDENT_TYPE_E'], 
                                  self.incidents['HAZARD_SEVERITY_CODE_E'])
        
        ax2 = axes[0, 1]
        severity_type.plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title('Incident Types vs Severity Distribution')
        ax2.set_xlabel('Incident Type')
        ax2.set_ylabel('Count')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 3. Correlation heatmap
        numeric_cols = ['month', 'weekday', 'quarter', 'severity_score']
        correlation_matrix = self.incidents[numeric_cols].corr()
        
        ax3 = axes[1, 0]
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax3)
        ax3.set_title('Correlation Matrix of Key Variables')
        
        # 4. Risk timeline
        monthly_risk = self.incidents.groupby(self.incidents['RECEIPT_DT'].dt.to_period('M')).agg({
            'INCIDENT_ID': 'count',
            'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
        })
        monthly_risk['death_rate'] = (monthly_risk['HAZARD_SEVERITY_CODE_E'] / monthly_risk['INCIDENT_ID'] * 100)
        
        ax4 = axes[1, 1]
        ax4.bar(range(len(monthly_risk)), monthly_risk['death_rate'], alpha=0.7)
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Death Rate (%)')
        ax4.set_title('Monthly Death Rate Trends')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('medical_device_incidents_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Visualizations saved to: medical_device_incidents_analysis.png")


def main():
    """Main function to run research analysis"""
    print("🔬 Medical Device Incidents Research Analysis")
    print("=" * 50)
    
    research = MedicalDeviceResearch()
    
    # Generate comprehensive insights
    insights = research.create_research_report()
    
    # Create visualizations
    research.create_visualizations()
    
    print("\n✅ Research analysis completed!")
    print("📁 Files generated:")
    print("  • medical_device_incidents_research_report.txt")
    print("  • medical_device_incidents_analysis.png")
    
    return insights


if __name__ == "__main__":
    main()
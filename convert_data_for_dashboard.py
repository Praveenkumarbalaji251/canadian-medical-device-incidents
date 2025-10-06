#!/usr/bin/env python3
"""
Convert extracted Medical Device Incidents data to JSON format for the React dashboard
"""

import pandas as pd
import json
from datetime import datetime
import os


def convert_data_for_dashboard():
    """
    Convert the extracted CSV data to JSON format optimized for the React dashboard
    """
    print("🔄 Converting data for dashboard...")
    
    # Check if the enhanced CSV file exists
    csv_file = "medical_device_incidents_enhanced_sept2024_sept2025.csv"
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        print("Please run the data extraction first.")
        return
    
    # Load the data
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} records")
    
    # Create dashboard data structure
    dashboard_data = {
        "metadata": {
            "lastUpdated": datetime.now().isoformat(),
            "totalRecords": len(df),
            "dateRange": {
                "start": df['RECEIPT_DT'].min(),
                "end": df['RECEIPT_DT'].max()
            }
        },
        "summary": create_summary_stats(df),
        "incidents": convert_incidents(df),
        "devices": create_device_summary(df),
        "companies": create_company_summary(df),
        "trends": create_trend_data(df),
        "severity": create_severity_data(df)
    }
    
    # Save to JSON files
    output_dir = "dashboard/public/data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Main data file
    with open(f"{output_dir}/dashboard_data.json", 'w') as f:
        json.dump(dashboard_data, f, indent=2, default=str)
    
    # Separate files for different sections
    with open(f"{output_dir}/incidents.json", 'w') as f:
        json.dump(dashboard_data["incidents"], f, indent=2, default=str)
    
    with open(f"{output_dir}/devices.json", 'w') as f:
        json.dump(dashboard_data["devices"], f, indent=2, default=str)
    
    with open(f"{output_dir}/companies.json", 'w') as f:
        json.dump(dashboard_data["companies"], f, indent=2, default=str)
    
    print("✅ Data conversion completed!")
    print(f"📁 Files saved to: {output_dir}/")
    print("📊 Dashboard data is ready for use")


def create_summary_stats(df):
    """Create summary statistics for the dashboard"""
    return {
        "totalIncidents": len(df),
        "dateRange": {
            "start": df['RECEIPT_DT'].min(),
            "end": df['RECEIPT_DT'].max()
        },
        "severityBreakdown": df['HAZARD_SEVERITY_CODE_E'].value_counts().to_dict(),
        "incidentTypes": df['INCIDENT_TYPE_E'].value_counts().to_dict(),
        "monthlyStats": create_monthly_stats(df)
    }


def create_monthly_stats(df):
    """Create monthly statistics"""
    df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'])
    monthly = df.groupby(df['RECEIPT_DT'].dt.to_period('M')).agg({
        'INCIDENT_ID': 'count',
        'HAZARD_SEVERITY_CODE_E': lambda x: (x == 'DEATH').sum()
    }).reset_index()
    
    monthly['RECEIPT_DT'] = monthly['RECEIPT_DT'].astype(str)
    monthly.columns = ['month', 'incidents', 'deaths']
    
    return monthly.to_dict('records')


def convert_incidents(df):
    """Convert incident data for the dashboard"""
    # Sample a subset for performance (dashboard will have pagination)
    sample_df = df.head(1000) if len(df) > 1000 else df
    
    incidents = []
    for _, row in sample_df.iterrows():
        incident = {
            "id": str(row['INCIDENT_ID']),
            "date": row['RECEIPT_DT'],
            "type": row['INCIDENT_TYPE_E'],
            "severity": row['HAZARD_SEVERITY_CODE_E'],
            "source": row.get('SOURCE_OF_RECALL_E', ''),
            "deviceName": row.get('TRADE_NAME', ''),
            "companyName": row.get('COMPANY_NAME', ''),
            "category": row.get('USAGE_CODE_TERM_E', ''),
            "riskClassification": row.get('RISK_CLASSIFICATION', '')
        }
        incidents.append(incident)
    
    return incidents


def create_device_summary(df):
    """Create device summary for analysis"""
    if 'TRADE_NAME' not in df.columns:
        return []
    
    device_summary = df.groupby('TRADE_NAME').agg({
        'INCIDENT_ID': 'count',
        'HAZARD_SEVERITY_CODE_E': lambda x: calculate_risk_score(x),
        'COMPANY_NAME': 'first',
        'USAGE_CODE_TERM_E': 'first',
        'RISK_CLASSIFICATION': 'first'
    }).reset_index()
    
    device_summary.columns = ['name', 'incidents', 'riskScore', 'manufacturer', 'category', 'riskClass']
    device_summary = device_summary.sort_values('incidents', ascending=False)
    
    # Add risk level based on incidents and severity
    device_summary['riskLevel'] = device_summary.apply(lambda row: 
        'High' if row['incidents'] > 150 or row['riskScore'] > 3.5 else
        'Medium' if row['incidents'] > 50 or row['riskScore'] > 2.5 else
        'Low', axis=1
    )
    
    return device_summary.head(50).to_dict('records')


def create_company_summary(df):
    """Create company summary for analysis"""
    if 'COMPANY_NAME' not in df.columns:
        return []
    
    company_summary = df.groupby('COMPANY_NAME').agg({
        'INCIDENT_ID': 'count',
        'HAZARD_SEVERITY_CODE_E': lambda x: calculate_risk_score(x),
        'ROLE_E': 'first'
    }).reset_index()
    
    company_summary.columns = ['name', 'incidents', 'riskScore', 'role']
    company_summary = company_summary.sort_values('incidents', ascending=False)
    
    # Add risk level
    company_summary['riskLevel'] = company_summary.apply(lambda row: 
        'High' if row['incidents'] > 300 or row['riskScore'] > 3.5 else
        'Medium' if row['incidents'] > 100 or row['riskScore'] > 2.5 else
        'Low', axis=1
    )
    
    return company_summary.head(50).to_dict('records')


def create_trend_data(df):
    """Create trend data for analysis"""
    df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'])
    
    # Monthly trends
    monthly_trends = df.groupby(df['RECEIPT_DT'].dt.to_period('M')).agg({
        'INCIDENT_ID': 'count',
        'HAZARD_SEVERITY_CODE_E': [
            lambda x: (x == 'DEATH').sum(),
            lambda x: (x == 'INJURY').sum(),
            lambda x: (x == 'POTENTIAL FOR DEATH/INJURY').sum()
        ]
    }).reset_index()
    
    # Flatten the multi-level columns
    monthly_trends.columns = ['month', 'incidents', 'deaths', 'injuries', 'potential']
    monthly_trends['month'] = monthly_trends['month'].astype(str)
    
    return {
        "monthly": monthly_trends.to_dict('records'),
        "growth_rate": calculate_growth_rate(monthly_trends['incidents'].tolist()),
        "seasonality": analyze_seasonality(df)
    }


def create_severity_data(df):
    """Create severity analysis data"""
    severity_counts = df['HAZARD_SEVERITY_CODE_E'].value_counts()
    
    return {
        "distribution": severity_counts.to_dict(),
        "percentages": (severity_counts / len(df) * 100).round(1).to_dict(),
        "trends": analyze_severity_trends(df)
    }


def calculate_risk_score(severity_series):
    """Calculate a risk score based on severity distribution"""
    severity_weights = {
        'DEATH': 5.0,
        'INJURY': 4.0,
        'POTENTIAL FOR DEATH/INJURY': 3.0,
        'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES': 1.0,
        'UNASSIGNED': 2.0
    }
    
    total_weight = 0
    total_count = len(severity_series)
    
    for severity in severity_series:
        total_weight += severity_weights.get(severity, 2.0)
    
    return round(total_weight / total_count if total_count > 0 else 0, 2)


def calculate_growth_rate(values):
    """Calculate growth rate between first and last values"""
    if len(values) < 2:
        return 0
    
    start_val = values[0]
    end_val = values[-1]
    
    if start_val == 0:
        return 0
    
    return round(((end_val - start_val) / start_val) * 100, 2)


def analyze_seasonality(df):
    """Analyze seasonal patterns in the data"""
    df['month'] = pd.to_datetime(df['RECEIPT_DT']).dt.month
    monthly_avg = df.groupby('month')['INCIDENT_ID'].count().mean()
    
    return {
        "peak_month": int(df.groupby('month')['INCIDENT_ID'].count().idxmax()),
        "low_month": int(df.groupby('month')['INCIDENT_ID'].count().idxmin()),
        "monthly_average": round(monthly_avg, 2)
    }


def analyze_severity_trends(df):
    """Analyze trends in severity over time"""
    df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'])
    df['month'] = df['RECEIPT_DT'].dt.to_period('M').astype(str)
    
    severity_trends = df.groupby(['month', 'HAZARD_SEVERITY_CODE_E']).size().unstack(fill_value=0)
    
    # Calculate percentage of deaths over time
    if 'DEATH' in severity_trends.columns:
        death_trend = (severity_trends['DEATH'] / severity_trends.sum(axis=1) * 100).round(2)
        death_trend_dict = {str(k): v for k, v in death_trend.to_dict().items()}
        return {
            "death_rate_trend": death_trend_dict,
            "improving": death_trend.iloc[-1] < death_trend.iloc[0] if len(death_trend) > 1 else False
        }
    
    return {"death_rate_trend": {}, "improving": False}


if __name__ == "__main__":
    convert_data_for_dashboard()
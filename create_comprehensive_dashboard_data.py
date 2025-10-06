#!/usr/bin/env python3
"""
Create comprehensive dashboard data with detailed analysis and sorting capabilities
"""

import pandas as pd
import json
from datetime import datetime
import numpy as np

def create_comprehensive_dashboard_data():
    """Create comprehensive data for the enhanced dashboard"""
    
    # Load the enhanced data
    df = pd.read_csv('/Users/Dell/Desktop/CanadianMedicalDevices/medical_device_incidents_enhanced_sept2024_sept2025.csv')
    
    # Convert date columns
    df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'], errors='coerce')
    df['INCIDENT_DT'] = pd.to_datetime(df['INCIDENT_DT'], errors='coerce')
    df['INC_AWARE_DT'] = pd.to_datetime(df['INC_AWARE_DT'], errors='coerce')
    
    # Add derived fields
    df['YEAR_MONTH'] = df['RECEIPT_DT'].dt.to_period('M').astype(str)
    df['IS_DEATH'] = (df['HAZARD_SEVERITY_CODE_E'] == 'DEATH').astype(int)
    df['IS_INJURY'] = (df['HAZARD_SEVERITY_CODE_E'] == 'INJURY').astype(int)
    df['IS_POTENTIAL_HARM'] = (df['HAZARD_SEVERITY_CODE_E'] == 'POTENTIAL FOR DEATH/INJURY').astype(int)
    
    # Clean company names (remove long role descriptions)
    df['COMPANY_CLEAN'] = df['COMPANY_NAME'].str.split(';').str[0].str.strip()
    
    print("Creating comprehensive dashboard data...")
    
    # 1. MAIN INCIDENTS DATA
    incidents_data = []
    for _, row in df.iterrows():
        incident = {
            'id': str(row['INCIDENT_ID']),
            'receiptDate': row['RECEIPT_DT'].strftime('%Y-%m-%d') if pd.notna(row['RECEIPT_DT']) else None,
            'incidentDate': row['INCIDENT_DT'].strftime('%Y-%m-%d') if pd.notna(row['INCIDENT_DT']) else None,
            'deviceName': str(row['TRADE_NAME']) if pd.notna(row['TRADE_NAME']) else 'Unknown',
            'deviceCode': str(row['PREF_NAME_CODE']) if pd.notna(row['PREF_NAME_CODE']) else 'Unknown',
            'company': str(row['COMPANY_CLEAN']) if pd.notna(row['COMPANY_CLEAN']) else 'Unknown',
            'severityCode': str(row['HAZARD_SEVERITY_CODE_E']) if pd.notna(row['HAZARD_SEVERITY_CODE_E']) else 'Unknown',
            'riskClass': str(row['RISK_CLASSIFICATION']) if pd.notna(row['RISK_CLASSIFICATION']) else 'Unknown',
            'isDeath': bool(row['IS_DEATH']),
            'isInjury': bool(row['IS_INJURY']),
            'isPotentialHarm': bool(row['IS_POTENTIAL_HARM']),
            'yearMonth': str(row['YEAR_MONTH']) if pd.notna(row['YEAR_MONTH']) else None
        }
        incidents_data.append(incident)
    
    # 2. DEVICE ANALYSIS
    device_analysis = df.groupby(['TRADE_NAME', 'PREF_NAME_CODE']).agg({
        'INCIDENT_ID': 'count',
        'IS_DEATH': 'sum',
        'IS_INJURY': 'sum',
        'IS_POTENTIAL_HARM': 'sum',
        'COMPANY_CLEAN': 'first'
    }).reset_index()
    
    device_analysis = device_analysis.sort_values('INCIDENT_ID', ascending=False)
    
    devices_data = []
    for _, row in device_analysis.iterrows():
        device = {
            'name': str(row['TRADE_NAME']),
            'code': str(row['PREF_NAME_CODE']),
            'totalIncidents': int(row['INCIDENT_ID']),
            'deaths': int(row['IS_DEATH']),
            'injuries': int(row['IS_INJURY']),
            'potentialHarms': int(row['IS_POTENTIAL_HARM']),
            'primaryCompany': str(row['COMPANY_CLEAN']),
            'riskScore': float(row['IS_DEATH'] * 10 + row['IS_INJURY'] * 5 + row['IS_POTENTIAL_HARM'] * 1)
        }
        devices_data.append(device)
    
    # 3. COMPANY ANALYSIS
    company_analysis = df.groupby('COMPANY_CLEAN').agg({
        'INCIDENT_ID': 'count',
        'IS_DEATH': 'sum',
        'IS_INJURY': 'sum',
        'IS_POTENTIAL_HARM': 'sum',
        'TRADE_NAME': 'nunique'
    }).reset_index()
    
    company_analysis = company_analysis.sort_values('INCIDENT_ID', ascending=False)
    
    companies_data = []
    for _, row in company_analysis.iterrows():
        company = {
            'name': str(row['COMPANY_CLEAN']),
            'totalIncidents': int(row['INCIDENT_ID']),
            'deaths': int(row['IS_DEATH']),
            'injuries': int(row['IS_INJURY']),
            'potentialHarms': int(row['IS_POTENTIAL_HARM']),
            'uniqueDevices': int(row['TRADE_NAME']),
            'riskScore': float(row['IS_DEATH'] * 10 + row['IS_INJURY'] * 5 + row['IS_POTENTIAL_HARM'] * 1)
        }
        companies_data.append(company)
    
    # 4. MONTHLY TRENDS
    monthly_data = df.groupby('YEAR_MONTH').agg({
        'INCIDENT_ID': 'count',
        'IS_DEATH': 'sum',
        'IS_INJURY': 'sum',
        'IS_POTENTIAL_HARM': 'sum'
    }).reset_index()
    
    trends_data = []
    for _, row in monthly_data.iterrows():
        trend = {
            'month': str(row['YEAR_MONTH']),
            'totalIncidents': int(row['INCIDENT_ID']),
            'deaths': int(row['IS_DEATH']),
            'injuries': int(row['IS_INJURY']),
            'potentialHarms': int(row['IS_POTENTIAL_HARM'])
        }
        trends_data.append(trend)
    
    # 5. SEVERITY ANALYSIS
    severity_data = df['HAZARD_SEVERITY_CODE_E'].value_counts().to_dict()
    severity_analysis = [{'severity': k, 'count': int(v)} for k, v in severity_data.items()]
    
    # 6. RISK CLASSIFICATION
    risk_data = df['RISK_CLASSIFICATION'].value_counts().to_dict()
    risk_analysis = [{'riskClass': k, 'count': int(v)} for k, v in risk_data.items()]
    
    # 7. SUMMARY STATISTICS
    summary_stats = {
        'totalIncidents': int(len(df)),
        'totalDeaths': int(df['IS_DEATH'].sum()),
        'totalInjuries': int(df['IS_INJURY'].sum()),
        'totalPotentialHarms': int(df['IS_POTENTIAL_HARM'].sum()),
        'uniqueDevices': int(df['TRADE_NAME'].nunique()),
        'uniqueCompanies': int(df['COMPANY_CLEAN'].nunique()),
        'dateRange': {
            'start': df['RECEIPT_DT'].min().strftime('%Y-%m-%d'),
            'end': df['RECEIPT_DT'].max().strftime('%Y-%m-%d')
        },
        'monthsOfData': int(df['YEAR_MONTH'].nunique())
    }
    
    # Create comprehensive dashboard data
    dashboard_data = {
        'incidents': incidents_data,
        'devices': devices_data,
        'companies': companies_data,
        'monthlyTrends': trends_data,
        'severityAnalysis': severity_analysis,
        'riskAnalysis': risk_analysis,
        'summary': summary_stats,
        'lastUpdated': datetime.now().isoformat()
    }
    
    # Save to JSON file
    output_file = '/Users/Dell/Desktop/CanadianMedicalDevices/dashboard/public/comprehensive_dashboard_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Comprehensive dashboard data saved to: {output_file}")
    print(f"📊 Data summary:")
    print(f"   • {len(incidents_data):,} individual incidents")
    print(f"   • {len(devices_data):,} unique devices")
    print(f"   • {len(companies_data):,} companies")
    print(f"   • {len(trends_data):,} months of data")
    print(f"   • {summary_stats['totalDeaths']} deaths, {summary_stats['totalInjuries']} injuries")
    
    return dashboard_data

if __name__ == "__main__":
    create_comprehensive_dashboard_data()
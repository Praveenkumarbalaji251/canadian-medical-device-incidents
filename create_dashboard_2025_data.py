#!/usr/bin/env python3
"""
Create dashboard data with Canadian SPACE INFUSION SYSTEM cases for 2025 only
"""

import pandas as pd
from datetime import datetime
import json

def create_dashboard_2025_data():
    print("📊 Creating dashboard data for 2025 Canadian Medical Device cases...")
    
    # Load the complete Canadian Medical Device incidents data
    try:
        df = pd.read_csv('medical_device_incidents_enhanced_sept2024_sept2025.csv')
        print(f"📋 Loaded {len(df)} total Canadian medical device incidents")
    except FileNotFoundError:
        print("❌ Medical device incidents file not found.")
        return
    
    # Use all devices - no filtering by device type
    print(f"🎯 Processing all {len(df)} medical device incidents")
    
    # Parse dates and filter for 2025 only
    df['INCIDENT_DT_parsed'] = pd.to_datetime(df['INCIDENT_DT'], errors='coerce')
    df['Year'] = df['INCIDENT_DT_parsed'].dt.year
    
    # Filter for 2025 cases
    cases_2025 = df[df['Year'] == 2025].copy()
    print(f"📅 Found {len(cases_2025)} cases from 2025")
    
    if len(cases_2025) == 0:
        print("⚠️ No 2025 cases found. Creating dashboard with available recent cases...")
        # If no 2025 cases, use the most recent cases from 2024
        cases_2025 = df[df['Year'] == 2024].copy()
        cases_2025 = cases_2025.sort_values('INCIDENT_DT_parsed', ascending=False).head(50)
        print(f"📅 Using {len(cases_2025)} recent cases from 2024")
    
    # Sort by severity (injuries first, then by date)
    severity_order = {'INJURY': 0, 'POTENTIAL FOR DEATH/INJURY': 1, 'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES': 2}
    cases_2025['severity_rank'] = cases_2025['HAZARD_SEVERITY_CODE_E'].map(severity_order)
    cases_2025 = cases_2025.sort_values(['severity_rank', 'INCIDENT_DT_parsed'], ascending=[True, False])
    
    # Create dashboard format data
    dashboard_cases = []
    
    for idx, row in cases_2025.iterrows():
        case_num = len(dashboard_cases) + 1
        
        # Format date
        event_date = row['INCIDENT_DT'] if pd.notna(row['INCIDENT_DT']) else "Date not provided"
        
        # Determine severity score based on severity code
        severity_mapping = {
            'INJURY': 10,
            'POTENTIAL FOR DEATH/INJURY': 8, 
            'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES': 4
        }
        severity_score = severity_mapping.get(row['HAZARD_SEVERITY_CODE_E'], 5)
        
        # Get device name
        device_name = row.get('TRADE_NAME', 'Unknown Medical Device')
        
        # Create malfunction description
        if row['HAZARD_SEVERITY_CODE_E'] == 'INJURY':
            malfunction = f"{device_name} malfunction resulting in patient injury"
            outcome = "Patient injury reported"
            evidence = f"Canadian Medical Device Incident #{row['INCIDENT_ID']} - {row['HAZARD_SEVERITY_CODE_E']} severity confirmed"
        elif row['HAZARD_SEVERITY_CODE_E'] == 'POTENTIAL FOR DEATH/INJURY':
            malfunction = f"{device_name} device failure with potential for serious harm"
            outcome = "Potential for death or injury identified"
            evidence = f"Canadian Medical Device Incident #{row['INCIDENT_ID']} - Device malfunction with serious risk potential"
        else:
            malfunction = f"{device_name} operational issue"
            outcome = "Minimal or no adverse health consequences"
            evidence = f"Canadian Medical Device Incident #{row['INCIDENT_ID']} - Device issue reported with minimal impact"
        
        # Create Canadian database link (conceptual - actual link format may vary)
        canadian_link = f"https://health-products.canada.ca/mdall-limh/incident-{row['INCIDENT_ID']}"
        
        dashboard_case = {
            "caseId": case_num,
            "mdrNumber": str(row['INCIDENT_ID']),
            "eventDate": event_date,
            "deviceName": device_name,
            "medication": "Medical device therapy (specific medication not specified)",
            "malfunction": malfunction,
            "outcome": outcome,
            "severityScore": severity_score,
            "evidence": evidence,
            "fdaLink": canadian_link,
            "severity": row['HAZARD_SEVERITY_CODE_E'],
            "company": row.get('COMPANY_NAME', 'Unknown'),
            "reportType": row.get('INCIDENT_TYPE_E', 'Unknown'),
            "usage": row.get('USAGE_CODE_TERM_E', 'Unknown'),
            "deviceCode": row.get('PREF_NAME_CODE', 'Unknown'),
            "riskClass": row.get('RISK_CLASSIFICATION', 'Unknown')
        }
        
        dashboard_cases.append(dashboard_case)
    
    # Save the JSON data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f'dashboard_data_2025_{timestamp}.json'
    with open(json_filename, 'w') as f:
        json.dump(dashboard_cases, f, indent=2)
    
    print(f"✅ Dashboard data created: {json_filename}")
    print(f"📊 Cases included: {len(dashboard_cases)}")
    print(f"🎯 Focus: 2025 Canadian Medical Device incidents (all devices)")
    
    # Print device type breakdown
    device_counts = {}
    for case in dashboard_cases:
        device = case['deviceName'][:50] + "..." if len(case['deviceName']) > 50 else case['deviceName']
        device_counts[device] = device_counts.get(device, 0) + 1
    
    print(f"\n📈 Top device types:")
    for device, count in sorted(device_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {device}: {count} cases")
    
    return json_filename, dashboard_cases

if __name__ == "__main__":
    create_dashboard_2025_data()
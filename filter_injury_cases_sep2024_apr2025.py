#!/usr/bin/env python3
"""
Filter SPACE INFUSION SYSTEM injury cases from September 2024 to April 2025
"""

import pandas as pd
from datetime import datetime, timedelta
import os

def filter_injury_cases_sep2024_apr2025():
    print("🩹 Filtering SPACE INFUSION SYSTEM injury cases from September 2024 to April 2025...")
    
    # Load the complete INFUSOMAT complaints data
    try:
        df = pd.read_csv('INFUSOMAT_CANADIAN_COMPLAINTS_20251007_130602.csv')
        print(f"📊 Loaded {len(df)} total INFUSOMAT complaints")
    except FileNotFoundError:
        print("❌ INFUSOMAT complaints file not found.")
        return
    
    # Filter for SPACE INFUSION SYSTEM incidents
    space_infusion_mask = df['TRADE_NAME'] == 'SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP'
    space_df = df[space_infusion_mask].copy()
    
    print(f"🎯 Found {len(space_df)} total SPACE INFUSION SYSTEM incidents")
    
    # Filter for injury cases only
    injury_mask = space_df['HAZARD_SEVERITY_CODE_E'] == 'INJURY'
    injury_df = space_df[injury_mask].copy()
    
    print(f"🩹 Found {len(injury_df)} total INJURY cases")
    
    # Parse dates for filtering
    date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
    for col in date_columns:
        if col in injury_df.columns:
            injury_df[f'{col}_parsed'] = pd.to_datetime(injury_df[col], errors='coerce')
    
    # Set specific date range: September 1, 2024 to April 30, 2025
    start_date = datetime(2024, 9, 1)
    end_date = datetime(2025, 4, 30)
    print(f"📅 Filtering for incidents from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Filter for September 2024 - April 2025 based on incident date
    date_mask = (injury_df['INCIDENT_DT_parsed'] >= start_date) & (injury_df['INCIDENT_DT_parsed'] <= end_date)
    period_injury_df = injury_df[date_mask].copy()
    
    print(f"🎯 Found {len(period_injury_df)} INJURY cases from September 2024 to April 2025")
    
    if len(period_injury_df) == 0:
        print("⚠️ No injury cases found in September 2024 - April 2025")
        
        # Show all injury cases with dates to understand the timeline
        print("\\n📅 All injury cases timeline:")
        injury_with_dates = injury_df.dropna(subset=['INCIDENT_DT_parsed'])
        for idx, row in injury_with_dates.iterrows():
            print(f"   • ID: {row['INCIDENT_ID']} - Date: {row['INCIDENT_DT']} - {row['INCIDENT_DT_parsed'].strftime('%Y-%m-%d')}")
        
        return
    
    # Add analysis columns
    if 'INCIDENT_DT_parsed' in period_injury_df.columns:
        period_injury_df['Year'] = period_injury_df['INCIDENT_DT_parsed'].dt.year
        period_injury_df['Month'] = period_injury_df['INCIDENT_DT_parsed'].dt.month
        period_injury_df['Month_Year'] = period_injury_df['INCIDENT_DT_parsed'].dt.strftime('%B %Y')
    
    # Sort by incident date (most recent first)
    if 'INCIDENT_DT_parsed' in period_injury_df.columns:
        period_injury_df = period_injury_df.sort_values('INCIDENT_DT_parsed', ascending=False)
    
    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the period injury cases
    csv_filename = f'SPACE_INFUSION_INJURY_CASES_SEP2024_APR2025_{timestamp}.csv'
    excel_filename = f'SPACE_INFUSION_INJURY_CASES_SEP2024_APR2025_{timestamp}.xlsx'
    
    period_injury_df.to_csv(csv_filename, index=False)
    period_injury_df.to_excel(excel_filename, index=False)
    
    print(f"💾 Saved period injury cases to:")
    print(f"   📄 {csv_filename}")
    print(f"   📊 {excel_filename}")
    
    # Analyze the period injury cases
    print(f"\\n🔍 SEPTEMBER 2024 - APRIL 2025 INJURY CASES ANALYSIS:")
    print(f"   • Period Injury Cases: {len(period_injury_df)}")
    print(f"   • Total Injury Cases: {len(injury_df)}")
    print(f"   • Period vs Total: {(len(period_injury_df)/len(injury_df)*100):.1f}% of all injuries occurred in this period")
    
    # Date range analysis
    if 'INCIDENT_DT_parsed' in period_injury_df.columns:
        valid_dates = period_injury_df['INCIDENT_DT_parsed'].dropna()
        if len(valid_dates) > 0:
            print(f"   • Actual Date Range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
    
    # Monthly breakdown
    if 'Month_Year' in period_injury_df.columns:
        monthly_counts = period_injury_df['Month_Year'].value_counts().sort_index()
        print(f"\\n📅 Injury Cases by Month:")
        for month, count in monthly_counts.items():
            print(f"   • {month}: {count} injury cases")
    
    # Display individual cases
    print(f"\\n📋 INDIVIDUAL INJURY CASES (September 2024 - April 2025):")
    for idx, row in period_injury_df.iterrows():
        case_num = len(period_injury_df) - list(period_injury_df.index).index(idx)
        print(f"\\n📋 INJURY CASE #{case_num:2d}")
        print('-' * 40)
        print(f"🆔 Incident ID: {row['INCIDENT_ID']}")
        print(f"📅 Incident Date: {row['INCIDENT_DT']}")
        print(f"📥 Receipt Date: {row['RECEIPT_DT']}")
        print(f"🔔 Aware Date: {row['INC_AWARE_DT']}")
        print(f"📝 Report Type: {row['INCIDENT_TYPE_E']}")
        print(f"🚨 Severity: {row['HAZARD_SEVERITY_CODE_E']} / {row['HAZARD_SEVERITY_CODE_F']}")
        print(f"🏥 Usage: {row['USAGE_CODE_TERM_E']}")
        print(f"🏢 Company: {row['COMPANY_NAME']}")
        print(f"👥 Role: {row['ROLE_E']}")
        print(f"🔧 Device Code: {row['PREF_NAME_CODE']}")
        print(f"⚠️ Risk Class: {row['RISK_CLASSIFICATION']}")
        print(f"📊 Mandatory Report: {row['MANDATORY_RPT']}")
    
    # Generate summary report
    summary_filename = f'SPACE_INFUSION_INJURY_CASES_SEP2024_APR2025_SUMMARY_{timestamp}.md'
    
    with open(summary_filename, 'w') as f:
        f.write(f"# SPACE INFUSION SYSTEM - INJURY CASES (September 2024 - April 2025)\\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\\n\\n")
        
        f.write(f"## 📊 Overview\\n")
        f.write(f"- **Device**: SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP\\n")
        f.write(f"- **Period Injury Cases**: {len(period_injury_df)} (Sep 2024 - Apr 2025)\\n")
        f.write(f"- **Total Injury Cases**: {len(injury_df)} (All time)\\n")
        f.write(f"- **Period vs Total**: {(len(period_injury_df)/len(injury_df)*100):.1f}% of all injuries occurred in this period\\n")
        f.write(f"- **Date Range**: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\\n\\n")
        
        if len(period_injury_df) > 0:
            if 'INCIDENT_DT_parsed' in period_injury_df.columns:
                valid_dates = period_injury_df['INCIDENT_DT_parsed'].dropna()
                if len(valid_dates) > 0:
                    f.write(f"- **Actual Date Range**: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}\\n\\n")
            
            f.write(f"## 📅 Monthly Breakdown\\n")
            if 'Month_Year' in period_injury_df.columns:
                monthly_counts = period_injury_df['Month_Year'].value_counts().sort_index()
                for month, count in monthly_counts.items():
                    f.write(f"- **{month}**: {count} injury cases\\n")
            f.write(f"\\n")
            
            f.write(f"## 📋 Individual Injury Cases\\n")
            for idx, row in period_injury_df.iterrows():
                case_num = len(period_injury_df) - list(period_injury_df.index).index(idx)
                f.write(f"### Case {case_num}\\n")
                f.write(f"- **Incident ID**: {row['INCIDENT_ID']}\\n")
                f.write(f"- **Date**: {row.get('INCIDENT_DT', 'Unknown')}\\n")
                f.write(f"- **Report Type**: {row.get('INCIDENT_TYPE_E', 'Unknown')}\\n")
                f.write(f"- **Company**: {row.get('COMPANY_NAME', 'Unknown')}\\n")
                f.write(f"- **Receipt Date**: {row.get('RECEIPT_DT', 'Unknown')}\\n")
                f.write(f"- **Severity**: {row.get('HAZARD_SEVERITY_CODE_E', 'Unknown')} / {row.get('HAZARD_SEVERITY_CODE_F', 'Unknown')}\\n")
                f.write(f"\\n")
    
    print(f"📋 Summary report saved to: {summary_filename}")
    print(f"\\n✅ September 2024 - April 2025 injury cases filtering complete!")
    print(f"📊 Found {len(period_injury_df)} injury cases in the 8-month period")

if __name__ == "__main__":
    filter_injury_cases_sep2024_apr2025()
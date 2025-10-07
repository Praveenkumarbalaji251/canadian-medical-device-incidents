#!/usr/bin/env python3
"""
Filter SPACE INFUSION SYSTEM injury cases for the last 8 months only
"""

import pandas as pd
from datetime import datetime, timedelta
import os

def filter_injury_cases_8months():
    print("🩹 Filtering SPACE INFUSION SYSTEM injury cases for last 8 months...")
    
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
    
    if len(injury_df) == 0:
        print("⚠️ No injury cases found")
        return
    
    # Parse dates for filtering
    date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
    for col in date_columns:
        if col in injury_df.columns:
            injury_df[f'{col}_parsed'] = pd.to_datetime(injury_df[col], errors='coerce')
    
    # Calculate 8 months ago from today
    today = datetime.now()
    eight_months_ago = today - timedelta(days=8*30)  # Approximate 8 months
    print(f"📅 Filtering for incidents from {eight_months_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
    
    # Filter for past 8 months based on incident date
    recent_mask = injury_df['INCIDENT_DT_parsed'] >= eight_months_ago
    recent_injury_df = injury_df[recent_mask].copy()
    
    print(f"🎯 Found {len(recent_injury_df)} INJURY cases in the past 8 months")
    
    if len(recent_injury_df) == 0:
        print("⚠️ No injury cases found in the past 8 months")
        print("ℹ️ This matches our previous finding that all injuries occurred in 2023-2024")
        return
    
    # Add analysis columns
    if 'INCIDENT_DT_parsed' in recent_injury_df.columns:
        recent_injury_df['Year'] = recent_injury_df['INCIDENT_DT_parsed'].dt.year
        recent_injury_df['Month'] = recent_injury_df['INCIDENT_DT_parsed'].dt.month
        recent_injury_df['Month_Year'] = recent_injury_df['INCIDENT_DT_parsed'].dt.strftime('%B %Y')
    
    # Sort by incident date (most recent first)
    if 'INCIDENT_DT_parsed' in recent_injury_df.columns:
        recent_injury_df = recent_injury_df.sort_values('INCIDENT_DT_parsed', ascending=False)
    
    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the recent injury cases
    csv_filename = f'SPACE_INFUSION_INJURY_CASES_LAST_8_MONTHS_{timestamp}.csv'
    excel_filename = f'SPACE_INFUSION_INJURY_CASES_LAST_8_MONTHS_{timestamp}.xlsx'
    
    recent_injury_df.to_csv(csv_filename, index=False)
    recent_injury_df.to_excel(excel_filename, index=False)
    
    print(f"💾 Saved recent injury cases to:")
    print(f"   📄 {csv_filename}")
    print(f"   📊 {excel_filename}")
    
    # Analyze the recent injury cases
    print(f"\n🔍 RECENT INJURY CASES ANALYSIS:")
    print(f"   • Recent Injury Cases: {len(recent_injury_df)}")
    print(f"   • Total Injury Cases: {len(injury_df)}")
    print(f"   • Recent vs Total: {(len(recent_injury_df)/len(injury_df)*100):.1f}% of all injuries are recent")
    
    # Date range analysis
    if 'INCIDENT_DT_parsed' in recent_injury_df.columns:
        valid_dates = recent_injury_df['INCIDENT_DT_parsed'].dropna()
        if len(valid_dates) > 0:
            print(f"   • Date Range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
    
    # Monthly breakdown
    if 'Month_Year' in recent_injury_df.columns:
        monthly_counts = recent_injury_df['Month_Year'].value_counts()
        print(f"\n📅 Recent Injury Cases by Month:")
        for month, count in monthly_counts.items():
            print(f"   • {month}: {count} injury cases")
    
    # Display individual recent cases
    print(f"\n📋 INDIVIDUAL RECENT INJURY CASES:")
    for idx, row in recent_injury_df.iterrows():
        case_num = len(recent_injury_df) - list(recent_injury_df.index).index(idx)
        incident_id = row['INCIDENT_ID']
        incident_date = row.get('INCIDENT_DT', 'Unknown')
        report_type = row.get('INCIDENT_TYPE_E', 'Unknown')
        
        print(f"   {case_num:2d}. ID: {incident_id} | Date: {incident_date} | Type: {report_type}")
    
    # Generate summary report
    summary_filename = f'SPACE_INFUSION_INJURY_CASES_LAST_8_MONTHS_SUMMARY_{timestamp}.md'
    
    with open(summary_filename, 'w') as f:
        f.write(f"# SPACE INFUSION SYSTEM - INJURY CASES (Last 8 Months)\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
        
        f.write(f"## 📊 Overview\n")
        f.write(f"- **Device**: SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP\n")
        f.write(f"- **Recent Injury Cases**: {len(recent_injury_df)} (Last 8 months)\n")
        f.write(f"- **Total Injury Cases**: {len(injury_df)} (All time)\n")
        f.write(f"- **Recent vs Total**: {(len(recent_injury_df)/len(injury_df)*100):.1f}% of all injuries are recent\n")
        f.write(f"- **Date Range**: {eight_months_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}\n\n")
        
        if len(recent_injury_df) > 0:
            if 'INCIDENT_DT_parsed' in recent_injury_df.columns:
                valid_dates = recent_injury_df['INCIDENT_DT_parsed'].dropna()
                if len(valid_dates) > 0:
                    f.write(f"- **Actual Date Range**: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}\n\n")
            
            f.write(f"## 📅 Monthly Breakdown\n")
            if 'Month_Year' in recent_injury_df.columns:
                monthly_counts = recent_injury_df['Month_Year'].value_counts()
                for month, count in monthly_counts.items():
                    f.write(f"- **{month}**: {count} injury cases\n")
            f.write(f"\n")
            
            f.write(f"## 📋 Individual Recent Injury Cases\n")
            for idx, row in recent_injury_df.iterrows():
                case_num = len(recent_injury_df) - list(recent_injury_df.index).index(idx)
                f.write(f"### Case {case_num}\n")
                f.write(f"- **Incident ID**: {row['INCIDENT_ID']}\n")
                f.write(f"- **Date**: {row.get('INCIDENT_DT', 'Unknown')}\n")
                f.write(f"- **Report Type**: {row.get('INCIDENT_TYPE_E', 'Unknown')}\n")
                f.write(f"- **Company**: {row.get('COMPANY_NAME', 'Unknown')}\n")
                f.write(f"- **Receipt Date**: {row.get('RECEIPT_DT', 'Unknown')}\n")
                f.write(f"\n")
        else:
            f.write(f"## ✅ No Recent Injury Cases\n")
            f.write(f"No injury cases found in the past 8 months. This indicates:\n")
            f.write(f"- All 12 injury cases occurred before {eight_months_ago.strftime('%Y-%m-%d')}\n")
            f.write(f"- Recent incidents (2025) have been classified as 'POTENTIAL FOR DEATH/INJURY' or 'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES'\n")
            f.write(f"- This could indicate improved safety measures or reporting classification changes\n\n")
    
    print(f"📋 Summary report saved to: {summary_filename}")
    print(f"\n✅ Recent injury cases filtering complete!")
    
    if len(recent_injury_df) == 0:
        print("🎯 KEY FINDING: No injury cases in the past 8 months!")
        print("   This means all 12 injury cases occurred before February 2025")
        print("   Recent 2025 incidents are 'POTENTIAL' but not confirmed injuries")

if __name__ == "__main__":
    filter_injury_cases_8months()
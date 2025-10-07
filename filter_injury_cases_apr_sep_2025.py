#!/usr/bin/env python3
"""
Filter SPACE INFUSION SYSTEM injury cases from April 2025 to September 2025
"""

import pandas as pd
from datetime import datetime, timedelta
import os

def filter_injury_cases_apr_sep_2025():
    print("🩹 Filtering SPACE INFUSION SYSTEM injury cases from April 2025 to September 2025...")
    
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
    
    # Set specific date range: April 1, 2025 to September 30, 2025
    start_date = datetime(2025, 4, 1)
    end_date = datetime(2025, 9, 30)
    print(f"📅 Filtering for incidents from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Filter for April-September 2025 based on incident date
    date_mask = (injury_df['INCIDENT_DT_parsed'] >= start_date) & (injury_df['INCIDENT_DT_parsed'] <= end_date)
    period_injury_df = injury_df[date_mask].copy()
    
    print(f"🎯 Found {len(period_injury_df)} INJURY cases from April-September 2025")
    
    if len(period_injury_df) == 0:
        print("⚠️ No injury cases found in April-September 2025")
        print("ℹ️ Checking what we DO have in this period...")
        
        # Check all incidents (not just injuries) in this period
        all_space_mask = (space_df['INCIDENT_DT'].notna())
        space_df['INCIDENT_DT_parsed'] = pd.to_datetime(space_df['INCIDENT_DT'], errors='coerce')
        period_all_mask = (space_df['INCIDENT_DT_parsed'] >= start_date) & (space_df['INCIDENT_DT_parsed'] <= end_date)
        period_all_df = space_df[period_all_mask].copy()
        
        print(f"📊 Total incidents in April-September 2025: {len(period_all_df)}")
        
        if len(period_all_df) > 0:
            severity_counts = period_all_df['HAZARD_SEVERITY_CODE_E'].value_counts()
            print(f"🚨 Severity breakdown for April-September 2025:")
            for severity, count in severity_counts.items():
                print(f"   • {severity}: {count} cases")
        
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
    csv_filename = f'SPACE_INFUSION_INJURY_CASES_APR_SEP_2025_{timestamp}.csv'
    excel_filename = f'SPACE_INFUSION_INJURY_CASES_APR_SEP_2025_{timestamp}.xlsx'
    
    period_injury_df.to_csv(csv_filename, index=False)
    period_injury_df.to_excel(excel_filename, index=False)
    
    print(f"💾 Saved period injury cases to:")
    print(f"   📄 {csv_filename}")
    print(f"   📊 {excel_filename}")
    
    # Analyze the period injury cases
    print(f"\n🔍 APRIL-SEPTEMBER 2025 INJURY CASES ANALYSIS:")
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
        monthly_counts = period_injury_df['Month_Year'].value_counts()
        print(f"\n📅 Injury Cases by Month (April-September 2025):")
        for month, count in monthly_counts.items():
            print(f"   • {month}: {count} injury cases")
    
    # Display individual cases
    print(f"\n📋 INDIVIDUAL INJURY CASES (April-September 2025):")
    for idx, row in period_injury_df.iterrows():
        case_num = len(period_injury_df) - list(period_injury_df.index).index(idx)
        incident_id = row['INCIDENT_ID']
        incident_date = row.get('INCIDENT_DT', 'Unknown')
        report_type = row.get('INCIDENT_TYPE_E', 'Unknown')
        
        print(f"   {case_num:2d}. ID: {incident_id} | Date: {incident_date} | Type: {report_type}")
    
    print(f"\n✅ April-September 2025 injury cases filtering complete!")

if __name__ == "__main__":
    filter_injury_cases_apr_sep_2025()
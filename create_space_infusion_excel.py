#!/usr/bin/env python3
"""
Extract all SPACE INFUSION SYSTEM incidents to Excel with all columns
"""

import pandas as pd
from datetime import datetime
import os

def create_space_infusion_excel():
    print("🔍 Extracting all SPACE INFUSION SYSTEM incidents...")
    
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
    
    print(f"🎯 Found {len(space_df)} SPACE INFUSION SYSTEM incidents")
    
    if len(space_df) == 0:
        print("⚠️ No SPACE INFUSION SYSTEM incidents found")
        return
    
    # Parse dates for better analysis
    date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
    for col in date_columns:
        if col in space_df.columns:
            space_df[f'{col}_parsed'] = pd.to_datetime(space_df[col], errors='coerce')
    
    # Add analysis columns
    if 'INCIDENT_DT_parsed' in space_df.columns:
        space_df['Year'] = space_df['INCIDENT_DT_parsed'].dt.year
        space_df['Month'] = space_df['INCIDENT_DT_parsed'].dt.month
        space_df['Month_Year'] = space_df['INCIDENT_DT_parsed'].dt.strftime('%B %Y')
    
    # Sort by incident date (most recent first)
    if 'INCIDENT_DT_parsed' in space_df.columns:
        space_df = space_df.sort_values('INCIDENT_DT_parsed', ascending=False)
    
    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create comprehensive Excel file
    excel_filename = f'SPACE_INFUSION_SYSTEM_ALL_INCIDENTS_{timestamp}.xlsx'
    
    # Create Excel writer with multiple sheets
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        # Main data sheet
        space_df.to_excel(writer, sheet_name='All_Incidents', index=False)
        
        # Summary statistics sheet
        summary_data = []
        
        # Basic stats
        summary_data.append(['Total Incidents', len(space_df)])
        
        # Date range
        if 'INCIDENT_DT_parsed' in space_df.columns:
            valid_dates = space_df['INCIDENT_DT_parsed'].dropna()
            if len(valid_dates) > 0:
                summary_data.append(['Earliest Incident', valid_dates.min().strftime('%Y-%m-%d')])
                summary_data.append(['Latest Incident', valid_dates.max().strftime('%Y-%m-%d')])
        
        # Severity breakdown
        severity_counts = space_df['HAZARD_SEVERITY_CODE_E'].value_counts()
        summary_data.append(['', ''])  # Empty row
        summary_data.append(['SEVERITY BREAKDOWN', ''])
        for severity, count in severity_counts.items():
            percentage = (count / len(space_df)) * 100
            summary_data.append([severity, f"{count} ({percentage:.1f}%)"])
        
        # Yearly breakdown
        if 'Year' in space_df.columns:
            yearly_counts = space_df['Year'].value_counts().sort_index()
            summary_data.append(['', ''])  # Empty row
            summary_data.append(['YEARLY BREAKDOWN', ''])
            for year, count in yearly_counts.items():
                if pd.notna(year):
                    summary_data.append([int(year), count])
        
        # Monthly breakdown for 2025
        if 'Month_Year' in space_df.columns:
            space_2025 = space_df[space_df['Year'] == 2025]
            if len(space_2025) > 0:
                monthly_2025 = space_2025['Month_Year'].value_counts()
                summary_data.append(['', ''])  # Empty row
                summary_data.append(['2025 MONTHLY BREAKDOWN', ''])
                for month, count in monthly_2025.items():
                    summary_data.append([month, count])
        
        # Create summary DataFrame
        summary_df = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # High severity cases sheet
        high_severity_mask = space_df['HAZARD_SEVERITY_CODE_E'].isin([
            'POTENTIAL FOR DEATH/INJURY', 'DEATH', 'INJURY'
        ])
        high_severity_df = space_df[high_severity_mask]
        
        if len(high_severity_df) > 0:
            high_severity_df.to_excel(writer, sheet_name='High_Severity', index=False)
            print(f"⚠️ Found {len(high_severity_df)} high-severity cases")
        
        # Recent incidents (2025) sheet
        if 'Year' in space_df.columns:
            recent_2025 = space_df[space_df['Year'] == 2025]
            if len(recent_2025) > 0:
                recent_2025.to_excel(writer, sheet_name='Recent_2025', index=False)
                print(f"📅 Found {len(recent_2025)} incidents in 2025")
    
    print(f"💾 Saved comprehensive Excel file: {excel_filename}")
    
    # Print summary statistics
    print(f"\n📊 SPACE INFUSION SYSTEM Summary:")
    print(f"   • Total Incidents: {len(space_df)}")
    
    if 'INCIDENT_DT_parsed' in space_df.columns:
        valid_dates = space_df['INCIDENT_DT_parsed'].dropna()
        if len(valid_dates) > 0:
            print(f"   • Date Range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
    
    print(f"\n🚨 Severity Breakdown:")
    severity_counts = space_df['HAZARD_SEVERITY_CODE_E'].value_counts()
    for severity, count in severity_counts.items():
        percentage = (count / len(space_df)) * 100
        print(f"   • {severity}: {count} ({percentage:.1f}%)")
    
    if 'Year' in space_df.columns:
        yearly_counts = space_df['Year'].value_counts().sort_index()
        print(f"\n📅 Yearly Distribution:")
        for year, count in yearly_counts.items():
            if pd.notna(year):
                print(f"   • {int(year)}: {count} incidents")
    
    print(f"\n✅ Excel file created with all {len(space_df)} SPACE INFUSION SYSTEM incidents!")
    print(f"📁 File: {excel_filename}")
    print(f"📋 Sheets: All_Incidents, Summary, High_Severity, Recent_2025")

if __name__ == "__main__":
    create_space_infusion_excel()
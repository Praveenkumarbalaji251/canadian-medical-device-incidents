#!/usr/bin/env python3
"""
Filter the 12 SPACE INFUSION SYSTEM injury cases from Canadian database
"""

import pandas as pd
from datetime import datetime
import os

def filter_space_infusion_injuries():
    print("🔍 Filtering SPACE INFUSION SYSTEM injury cases...")
    
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
    
    print(f"🩹 Found {len(injury_df)} INJURY cases for SPACE INFUSION SYSTEM")
    
    if len(injury_df) == 0:
        print("⚠️ No injury cases found")
        return
    
    # Parse dates for better analysis
    date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
    for col in date_columns:
        if col in injury_df.columns:
            injury_df[f'{col}_parsed'] = pd.to_datetime(injury_df[col], errors='coerce')
    
    # Add analysis columns
    if 'INCIDENT_DT_parsed' in injury_df.columns:
        injury_df['Year'] = injury_df['INCIDENT_DT_parsed'].dt.year
        injury_df['Month'] = injury_df['INCIDENT_DT_parsed'].dt.month
        injury_df['Month_Year'] = injury_df['INCIDENT_DT_parsed'].dt.strftime('%B %Y')
    
    # Sort by incident date (most recent first)
    if 'INCIDENT_DT_parsed' in injury_df.columns:
        injury_df = injury_df.sort_values('INCIDENT_DT_parsed', ascending=False)
    
    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the injury cases
    csv_filename = f'SPACE_INFUSION_SYSTEM_12_INJURY_CASES_{timestamp}.csv'
    excel_filename = f'SPACE_INFUSION_SYSTEM_12_INJURY_CASES_{timestamp}.xlsx'
    
    injury_df.to_csv(csv_filename, index=False)
    injury_df.to_excel(excel_filename, index=False)
    
    print(f"💾 Saved injury cases to:")
    print(f"   📄 {csv_filename}")
    print(f"   📊 {excel_filename}")
    
    # Analyze the injury cases
    print(f"\n🔍 INJURY CASES ANALYSIS:")
    print(f"   • Total Injury Cases: {len(injury_df)}")
    
    # Date range analysis
    if 'INCIDENT_DT_parsed' in injury_df.columns:
        valid_dates = injury_df['INCIDENT_DT_parsed'].dropna()
        if len(valid_dates) > 0:
            print(f"   • Date Range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
    
    # Yearly breakdown
    if 'Year' in injury_df.columns:
        yearly_counts = injury_df['Year'].value_counts().sort_index()
        print(f"\n📅 Injury Cases by Year:")
        for year, count in yearly_counts.items():
            if pd.notna(year):
                print(f"   • {int(year)}: {count} injury cases")
    
    # Report type analysis
    if 'INCIDENT_TYPE_E' in injury_df.columns:
        report_types = injury_df['INCIDENT_TYPE_E'].value_counts()
        print(f"\n📝 Report Types for Injury Cases:")
        for report_type, count in report_types.items():
            print(f"   • {report_type}: {count} cases")
    
    # Company analysis
    if 'COMPANY_NAME' in injury_df.columns:
        companies = injury_df['COMPANY_NAME'].value_counts().head(3)
        print(f"\n🏢 Companies Involved in Injury Cases:")
        for company, count in companies.items():
            print(f"   • {company}: {count} cases")
    
    # Display individual cases summary
    print(f"\n📋 INDIVIDUAL INJURY CASES:")
    for idx, row in injury_df.iterrows():
        incident_id = row['INCIDENT_ID']
        incident_date = row.get('INCIDENT_DT', 'Unknown')
        report_type = row.get('INCIDENT_TYPE_E', 'Unknown')
        company = row.get('COMPANY_NAME', 'Unknown')[:50] + "..." if len(str(row.get('COMPANY_NAME', ''))) > 50 else row.get('COMPANY_NAME', 'Unknown')
        
        print(f"   {len(injury_df) - list(injury_df.index).index(idx)}. ID: {incident_id} | Date: {incident_date} | Type: {report_type}")
        print(f"      Company: {company}")
        print()
    
    # Generate summary report
    summary_filename = f'SPACE_INFUSION_SYSTEM_12_INJURY_CASES_SUMMARY_{timestamp}.md'
    
    with open(summary_filename, 'w') as f:
        f.write(f"# SPACE INFUSION SYSTEM - 12 INJURY CASES ANALYSIS\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
        
        f.write(f"## 📊 Overview\n")
        f.write(f"- **Device**: SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP\n")
        f.write(f"- **Total Injury Cases**: {len(injury_df)}\n")
        f.write(f"- **Total Device Incidents**: 264\n")
        f.write(f"- **Injury Rate**: {(len(injury_df)/264*100):.1f}% of all incidents resulted in actual injury\n\n")
        
        if 'INCIDENT_DT_parsed' in injury_df.columns:
            valid_dates = injury_df['INCIDENT_DT_parsed'].dropna()
            if len(valid_dates) > 0:
                f.write(f"- **Date Range**: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}\n\n")
        
        f.write(f"## 📅 Injury Cases by Year\n")
        if 'Year' in injury_df.columns:
            yearly_counts = injury_df['Year'].value_counts().sort_index()
            for year, count in yearly_counts.items():
                if pd.notna(year):
                    f.write(f"- **{int(year)}**: {count} injury cases\n")
        f.write(f"\n")
        
        f.write(f"## 📝 Report Types\n")
        if 'INCIDENT_TYPE_E' in injury_df.columns:
            report_types = injury_df['INCIDENT_TYPE_E'].value_counts()
            for report_type, count in report_types.items():
                f.write(f"- **{report_type}**: {count} cases\n")
        f.write(f"\n")
        
        f.write(f"## 🏢 Companies Involved\n")
        if 'COMPANY_NAME' in injury_df.columns:
            companies = injury_df['COMPANY_NAME'].value_counts().head(5)
            for company, count in companies.items():
                f.write(f"- **{company}**: {count} cases\n")
        f.write(f"\n")
        
        f.write(f"## 📋 Individual Injury Cases\n")
        for idx, row in injury_df.iterrows():
            case_num = len(injury_df) - list(injury_df.index).index(idx)
            f.write(f"### Case {case_num}\n")
            f.write(f"- **Incident ID**: {row['INCIDENT_ID']}\n")
            f.write(f"- **Date**: {row.get('INCIDENT_DT', 'Unknown')}\n")
            f.write(f"- **Report Type**: {row.get('INCIDENT_TYPE_E', 'Unknown')}\n")
            f.write(f"- **Company**: {row.get('COMPANY_NAME', 'Unknown')}\n")
            f.write(f"- **Receipt Date**: {row.get('RECEIPT_DT', 'Unknown')}\n")
            f.write(f"- **Aware Date**: {row.get('INC_AWARE_DT', 'Unknown')}\n")
            f.write(f"\n")
    
    print(f"📋 Summary report saved to: {summary_filename}")
    print(f"\n✅ Injury cases filtering complete!")
    print(f"📊 Found {len(injury_df)} injury cases out of 264 total SPACE INFUSION SYSTEM incidents ({(len(injury_df)/264*100):.1f}% injury rate)")

if __name__ == "__main__":
    filter_space_infusion_injuries()
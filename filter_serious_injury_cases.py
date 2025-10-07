#!/usr/bin/env python3
"""
Filter SPACE INFUSION SYSTEM serious injury cases (POTENTIAL FOR DEATH/INJURY) separately
"""

import pandas as pd
from datetime import datetime
import os

def filter_serious_injury_cases():
    print("🚨 Filtering SPACE INFUSION SYSTEM serious injury cases...")
    print("   (POTENTIAL FOR DEATH/INJURY severity)")
    
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
    
    # Filter for POTENTIAL FOR DEATH/INJURY cases only
    serious_mask = space_df['HAZARD_SEVERITY_CODE_E'] == 'POTENTIAL FOR DEATH/INJURY'
    serious_df = space_df[serious_mask].copy()
    
    print(f"⚠️ Found {len(serious_df)} POTENTIAL FOR DEATH/INJURY cases")
    
    if len(serious_df) == 0:
        print("⚠️ No serious injury cases found")
        return
    
    # Parse dates for better analysis
    date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
    for col in date_columns:
        if col in serious_df.columns:
            serious_df[f'{col}_parsed'] = pd.to_datetime(serious_df[col], errors='coerce')
    
    # Add analysis columns
    if 'INCIDENT_DT_parsed' in serious_df.columns:
        serious_df['Year'] = serious_df['INCIDENT_DT_parsed'].dt.year
        serious_df['Month'] = serious_df['INCIDENT_DT_parsed'].dt.month
        serious_df['Month_Year'] = serious_df['INCIDENT_DT_parsed'].dt.strftime('%B %Y')
    
    # Sort by incident date (most recent first)
    if 'INCIDENT_DT_parsed' in serious_df.columns:
        serious_df = serious_df.sort_values('INCIDENT_DT_parsed', ascending=False)
    
    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the serious injury cases
    csv_filename = f'SPACE_INFUSION_SERIOUS_INJURY_CASES_{timestamp}.csv'
    excel_filename = f'SPACE_INFUSION_SERIOUS_INJURY_CASES_{timestamp}.xlsx'
    
    serious_df.to_csv(csv_filename, index=False)
    serious_df.to_excel(excel_filename, index=False)
    
    print(f"💾 Saved serious injury cases to:")
    print(f"   📄 {csv_filename}")
    print(f"   📊 {excel_filename}")
    
    # Analyze the serious injury cases
    print(f"\n🔍 SERIOUS INJURY CASES ANALYSIS:")
    print(f"   • Total Cases: {len(serious_df)}")
    print(f"   • Percentage of all SPACE INFUSION incidents: {(len(serious_df)/len(space_df)*100):.1f}%")
    
    # Date range analysis
    if 'INCIDENT_DT_parsed' in serious_df.columns:
        valid_dates = serious_df['INCIDENT_DT_parsed'].dropna()
        if len(valid_dates) > 0:
            print(f"   • Date Range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
    
    # Yearly breakdown
    if 'Year' in serious_df.columns:
        yearly_counts = serious_df['Year'].value_counts().sort_index()
        print(f"\n📅 Serious Cases by Year:")
        for year, count in yearly_counts.items():
            if pd.notna(year):
                print(f"   • {int(year)}: {count} cases")
    
    # Monthly breakdown for recent years
    if 'Month_Year' in serious_df.columns:
        recent_years = [2024, 2025]
        for year in recent_years:
            year_data = serious_df[serious_df['Year'] == year]
            if len(year_data) > 0:
                monthly_counts = year_data['Month_Year'].value_counts()
                print(f"\n📊 {year} Monthly Breakdown:")
                for month, count in monthly_counts.items():
                    print(f"   • {month}: {count} cases")
    
    # Report type analysis
    if 'INCIDENT_TYPE_E' in serious_df.columns:
        report_types = serious_df['INCIDENT_TYPE_E'].value_counts()
        print(f"\n📝 Report Types for Serious Cases:")
        for report_type, count in report_types.items():
            print(f"   • {report_type}: {count} cases")
    
    # Company analysis
    if 'COMPANY_NAME' in serious_df.columns:
        companies = serious_df['COMPANY_NAME'].value_counts().head(3)
        print(f"\n🏢 Top Companies in Serious Cases:")
        for company, count in companies.items():
            print(f"   • {company[:60]}...: {count} cases")
    
    # Show recent serious cases (last 10)
    print(f"\n🚨 MOST RECENT SERIOUS CASES (Last 10):")
    recent_cases = serious_df.head(10)
    for idx, row in recent_cases.iterrows():
        case_num = list(serious_df.index).index(idx) + 1
        incident_date = row.get('INCIDENT_DT', 'Unknown')
        incident_id = row['INCIDENT_ID']
        report_type = row.get('INCIDENT_TYPE_E', 'Unknown')
        
        print(f"   {case_num:2d}. ID: {incident_id} | Date: {incident_date} | {report_type}")
    
    # Generate summary report
    summary_filename = f'SPACE_INFUSION_SERIOUS_INJURY_CASES_SUMMARY_{timestamp}.md'
    
    with open(summary_filename, 'w') as f:
        f.write(f"# SPACE INFUSION SYSTEM - SERIOUS INJURY CASES ANALYSIS\n")
        f.write(f"## (POTENTIAL FOR DEATH/INJURY Severity)\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
        
        f.write(f"## 📊 Overview\n")
        f.write(f"- **Device**: SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP\n")
        f.write(f"- **Serious Cases**: {len(serious_df)} (POTENTIAL FOR DEATH/INJURY)\n")
        f.write(f"- **Total Device Incidents**: {len(space_df)}\n")
        f.write(f"- **Serious Case Rate**: {(len(serious_df)/len(space_df)*100):.1f}% of all incidents\n\n")
        
        if 'INCIDENT_DT_parsed' in serious_df.columns:
            valid_dates = serious_df['INCIDENT_DT_parsed'].dropna()
            if len(valid_dates) > 0:
                f.write(f"- **Date Range**: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}\n\n")
        
        f.write(f"## 📅 Serious Cases by Year\n")
        if 'Year' in serious_df.columns:
            yearly_counts = serious_df['Year'].value_counts().sort_index()
            for year, count in yearly_counts.items():
                if pd.notna(year):
                    f.write(f"- **{int(year)}**: {count} serious cases\n")
        f.write(f"\n")
        
        # Recent years monthly breakdown
        if 'Month_Year' in serious_df.columns:
            recent_years = [2024, 2025]
            for year in recent_years:
                year_data = serious_df[serious_df['Year'] == year]
                if len(year_data) > 0:
                    f.write(f"## 📊 {year} Monthly Breakdown\n")
                    monthly_counts = year_data['Month_Year'].value_counts()
                    for month, count in monthly_counts.items():
                        f.write(f"- **{month}**: {count} cases\n")
                    f.write(f"\n")
        
        f.write(f"## 📝 Report Types\n")
        if 'INCIDENT_TYPE_E' in serious_df.columns:
            report_types = serious_df['INCIDENT_TYPE_E'].value_counts()
            for report_type, count in report_types.items():
                f.write(f"- **{report_type}**: {count} cases\n")
        f.write(f"\n")
        
        f.write(f"## 🚨 Most Recent Serious Cases (Last 20)\n")
        recent_cases = serious_df.head(20)
        for idx, row in recent_cases.iterrows():
            case_num = list(serious_df.index).index(idx) + 1
            f.write(f"### Case {case_num}\n")
            f.write(f"- **Incident ID**: {row['INCIDENT_ID']}\n")
            f.write(f"- **Date**: {row.get('INCIDENT_DT', 'Unknown')}\n")
            f.write(f"- **Report Type**: {row.get('INCIDENT_TYPE_E', 'Unknown')}\n")
            f.write(f"- **Company**: {row.get('COMPANY_NAME', 'Unknown')}\n")
            f.write(f"- **Receipt Date**: {row.get('RECEIPT_DT', 'Unknown')}\n")
            f.write(f"\n")
    
    print(f"📋 Summary report saved to: {summary_filename}")
    print(f"\n✅ Serious injury cases filtering complete!")
    print(f"⚠️ {len(serious_df)} cases with POTENTIAL FOR DEATH/INJURY out of {len(space_df)} total incidents")
    print(f"📊 Serious case rate: {(len(serious_df)/len(space_df)*100):.1f}%")

if __name__ == "__main__":
    filter_serious_injury_cases()
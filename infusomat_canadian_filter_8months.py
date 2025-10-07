#!/usr/bin/env python3
"""
Filter Canadian INFUSOMAT complaints for the past 8 months
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import os

def filter_infusomat_8months():
    print("🔍 Filtering Canadian INFUSOMAT complaints for past 8 months...")
    
    # Load the INFUSOMAT complaints data
    try:
        df = pd.read_csv('INFUSOMAT_CANADIAN_COMPLAINTS_20251007_130602.csv')
        print(f"📊 Loaded {len(df)} total INFUSOMAT complaints")
    except FileNotFoundError:
        print("❌ INFUSOMAT complaints file not found. Please run infusomat_canadian_filter.py first.")
        return
    
    # Convert date columns to datetime
    date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
    for col in date_columns:
        if col in df.columns:
            # Create parsed versions
            df[f'{col}_parsed'] = pd.to_datetime(df[col], errors='coerce')
    
    # Calculate 8 months ago from today
    today = datetime.now()
    eight_months_ago = today - timedelta(days=8*30)  # Approximate 8 months
    print(f"📅 Filtering for incidents from {eight_months_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
    
    # Filter for past 8 months based on incident date
    recent_mask = df['INCIDENT_DT_parsed'] >= eight_months_ago
    recent_df = df[recent_mask].copy()
    
    print(f"🎯 Found {len(recent_df)} INFUSOMAT complaints in the past 8 months")
    
    if len(recent_df) == 0:
        print("⚠️ No complaints found in the past 8 months")
        return
    
    # Sort by incident date (most recent first)
    recent_df = recent_df.sort_values('INCIDENT_DT_parsed', ascending=False)
    
    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the filtered data
    csv_filename = f'INFUSOMAT_CANADIAN_LAST_8_MONTHS_{timestamp}.csv'
    excel_filename = f'INFUSOMAT_CANADIAN_LAST_8_MONTHS_{timestamp}.xlsx'
    
    recent_df.to_csv(csv_filename, index=False)
    recent_df.to_excel(excel_filename, index=False)
    
    print(f"💾 Saved recent complaints to:")
    print(f"   📄 {csv_filename}")
    print(f"   📊 {excel_filename}")
    
    # Analyze severity distribution
    severity_counts = recent_df['HAZARD_SEVERITY_CODE_E'].value_counts()
    print(f"\n🚨 Severity Analysis (Last 8 Months):")
    for severity, count in severity_counts.items():
        percentage = (count / len(recent_df)) * 100
        print(f"   • {severity}: {count} cases ({percentage:.1f}%)")
    
    # Monthly breakdown
    recent_df['Month_Year'] = recent_df['INCIDENT_DT_parsed'].dt.strftime('%B %Y')
    monthly_counts = recent_df['Month_Year'].value_counts().sort_index()
    print(f"\n📅 Monthly Breakdown:")
    for month, count in monthly_counts.items():
        print(f"   • {month}: {count} complaints")
    
    # Device model analysis
    device_counts = recent_df['TRADE_NAME'].value_counts().head(5)
    print(f"\n🔧 Top Device Models (Last 8 Months):")
    for device, count in device_counts.items():
        print(f"   • {device}: {count} complaints")
    
    # Filter high-severity cases
    high_severity_mask = recent_df['HAZARD_SEVERITY_CODE_E'] == 'POTENTIAL FOR DEATH/INJURY'
    high_severity_df = recent_df[high_severity_mask]
    
    if len(high_severity_df) > 0:
        high_severity_filename = f'INFUSOMAT_CANADIAN_LAST_8_MONTHS_{timestamp}_HIGH_SEVERITY.csv'
        high_severity_df.to_csv(high_severity_filename, index=False)
        print(f"⚠️ High-severity cases saved to: {high_severity_filename}")
        print(f"   📊 {len(high_severity_df)} high-severity cases out of {len(recent_df)} total")
    
    # Generate summary report
    summary_filename = f'INFUSOMAT_CANADIAN_LAST_8_MONTHS_{timestamp}_SUMMARY.md'
    
    with open(summary_filename, 'w') as f:
        f.write(f"# INFUSOMAT Canadian Complaints - Last 8 Months\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
        
        f.write(f"## 📊 Overview\n")
        f.write(f"- **Recent INFUSOMAT Complaints**: {len(recent_df)} (Last 8 months)\n")
        f.write(f"- **Total INFUSOMAT Complaints**: {len(df)} (All time)\n")
        f.write(f"- **Data Source**: Canadian Medical Device Incidents Database\n")
        f.write(f"- **Date Range**: {eight_months_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}\n")
        f.write(f"- **Recent vs All-time**: {(len(recent_df)/len(df)*100):.1f}% of complaints are from last 8 months\n\n")
        
        f.write(f"## 🚨 Recent Severity Analysis\n")
        for severity, count in severity_counts.items():
            percentage = (count / len(recent_df)) * 100
            f.write(f"- **{severity}**: {count} cases ({percentage:.1f}%)\n")
        f.write(f"\n")
        
        f.write(f"## 📅 Monthly Breakdown\n")
        for month, count in monthly_counts.items():
            f.write(f"- **{month}**: {count} complaints\n")
        f.write(f"\n")
        
        f.write(f"## 🔧 Recent Top Device Models\n")
        for device, count in device_counts.items():
            f.write(f"- **{device}**: {count} complaints\n")
        f.write(f"\n")
        
        # Data completeness analysis
        f.write(f"## 📋 Recent Data Columns Available\n")
        for col in recent_df.columns:
            non_null_count = recent_df[col].notna().sum()
            f.write(f"- `{col}`: {non_null_count}/{len(recent_df)} values\n")
        f.write(f"\n")
    
    print(f"📋 Summary report saved to: {summary_filename}")
    
    print(f"\n✅ 8-month filtering complete!")
    print(f"📊 Summary: {len(recent_df)} complaints from {len(df)} total INFUSOMAT cases")
    if len(high_severity_df) > 0:
        print(f"⚠️ High-severity rate: {len(high_severity_df)}/{len(recent_df)} ({(len(high_severity_df)/len(recent_df)*100):.1f}%)")

if __name__ == "__main__":
    filter_infusomat_8months()
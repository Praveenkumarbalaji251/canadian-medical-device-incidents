#!/usr/bin/env python3
"""
Detailed analysis of Medical Device Incidents data from September 2024 to September 2025
"""

import pandas as pd
import os


def analyze_incident_data():
    """
    Perform detailed analysis of the extracted incident data
    """
    # Load the extracted data
    data_file = "medical_device_incidents_sept2024_sept2025.csv"
    
    if not os.path.exists(data_file):
        print("❌ Data file not found. Please run the extraction first.")
        return
    
    print("📊 Detailed Analysis of Medical Device Incidents")
    print("📅 September 2024 - September 2025")
    print("=" * 60)
    
    # Load the data
    df = pd.read_csv(data_file)
    print(f"✅ Loaded {len(df)} incident records")
    
    # Basic statistics
    print(f"\n📈 Basic Statistics:")
    print(f"   Total incidents: {len(df):,}")
    
    # Date range analysis
    df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'])
    print(f"   Date range: {df['RECEIPT_DT'].min().strftime('%Y-%m-%d')} to {df['RECEIPT_DT'].max().strftime('%Y-%m-%d')}")
    
    # Monthly breakdown
    print(f"\n📅 Monthly Breakdown:")
    monthly_counts = df.groupby(df['RECEIPT_DT'].dt.to_period('M')).size()
    for month, count in monthly_counts.items():
        print(f"   {month}: {count:,} incidents")
    
    # Incident types
    print(f"\n🔍 Incident Types (English):")
    incident_types = df['INCIDENT_TYPE_E'].value_counts()
    for incident_type, count in incident_types.head(10).items():
        percentage = (count / len(df)) * 100
        print(f"   {incident_type}: {count:,} ({percentage:.1f}%)")
    
    # Severity analysis
    if 'HAZARD_SEVERITY_CODE_E' in df.columns:
        print(f"\n⚠️  Hazard Severity Levels:")
        severity_counts = df['HAZARD_SEVERITY_CODE_E'].value_counts()
        for severity, count in severity_counts.items():
            if pd.notna(severity):
                percentage = (count / len(df)) * 100
                print(f"   {severity}: {count:,} ({percentage:.1f}%)")
    
    # Source analysis
    if 'SOURCE_OF_RECALL_E' in df.columns:
        print(f"\n📢 Source of Reports:")
        source_counts = df['SOURCE_OF_RECALL_E'].value_counts()
        for source, count in source_counts.head(5).items():
            if pd.notna(source):
                percentage = (count / len(df)) * 100
                print(f"   {source}: {count:,} ({percentage:.1f}%)")
    
    # Load related device data if available
    device_file = "mdi_data/INCIDENT_DEVICE.dsv"
    if os.path.exists(device_file):
        print(f"\n🏥 Loading device information...")
        device_df = pd.read_csv(device_file, sep='|', encoding='utf-8')
        
        # Merge with incident data
        incident_ids = df['INCIDENT_ID'].tolist()
        related_devices = device_df[device_df['INCIDENT_ID'].isin(incident_ids)]
        
        print(f"   Found {len(related_devices)} device records related to these incidents")
        
        if len(related_devices) > 0:
            print(f"\n🔧 Top Device Types (if available):")
            if 'TRADE_NAME' in related_devices.columns:
                device_names = related_devices['TRADE_NAME'].value_counts()
                for device_name, count in device_names.head(10).items():
                    if pd.notna(device_name) and device_name.strip():
                        print(f"   {device_name}: {count:,} incidents")
            
            if 'USAGE_CODE_TERM_E' in related_devices.columns:
                print(f"\n🔧 Top Device Usage Categories:")
                usage_terms = related_devices['USAGE_CODE_TERM_E'].value_counts()
                for usage, count in usage_terms.head(10).items():
                    if pd.notna(usage) and usage.strip():
                        print(f"   {usage}: {count:,} incidents")
    
    # Load company data if available
    company_file = "mdi_data/INCIDENT_COMPANY.dsv"
    if os.path.exists(company_file):
        print(f"\n🏢 Loading company information...")
        company_df = pd.read_csv(company_file, sep='|', encoding='utf-8')
        
        # Merge with incident data
        related_companies = company_df[company_df['INCIDENT_ID'].isin(incident_ids)]
        
        print(f"   Found {len(related_companies)} company records related to these incidents")
        
        if len(related_companies) > 0:
            print(f"\n🏭 Top Companies Involved:")
            if 'COMPANY_NAME' in related_companies.columns:
                company_names = related_companies['COMPANY_NAME'].value_counts()
                for company_name, count in company_names.head(10).items():
                    if pd.notna(company_name) and company_name.strip():
                        print(f"   {company_name}: {count:,} incidents")
    
    # Create enhanced export with additional data
    create_enhanced_export(df, device_file, company_file)
    
    print(f"\n📁 Analysis complete! Check the enhanced export files for detailed data.")


def create_enhanced_export(incident_df, device_file, company_file):
    """
    Create enhanced export files with merged data from multiple tables
    """
    print(f"\n🔄 Creating enhanced export with merged data...")
    
    enhanced_df = incident_df.copy()
    
    # Add device information
    if os.path.exists(device_file):
        device_df = pd.read_csv(device_file, sep='|', encoding='utf-8')
        
        # Group devices by incident ID to avoid duplication
        device_summary = device_df.groupby('INCIDENT_ID').agg({
            'TRADE_NAME': lambda x: '; '.join(x.dropna().astype(str).unique()) if len(x.dropna()) > 0 else '',
            'PREF_NAME_CODE': lambda x: '; '.join(x.dropna().astype(str).unique()) if len(x.dropna()) > 0 else '',
            'RISK_CLASSIFICATION': lambda x: '; '.join(x.dropna().astype(str).unique()) if len(x.dropna()) > 0 else '',
            'USAGE_CODE_TERM_E': lambda x: '; '.join(x.dropna().astype(str).unique()) if len(x.dropna()) > 0 else ''
        }).reset_index()
        
        enhanced_df = enhanced_df.merge(device_summary, on='INCIDENT_ID', how='left')
    
    # Add company information
    if os.path.exists(company_file):
        company_df = pd.read_csv(company_file, sep='|', encoding='utf-8')
        
        # Group companies by incident ID
        company_summary = company_df.groupby('INCIDENT_ID').agg({
            'COMPANY_NAME': lambda x: '; '.join(x.dropna().astype(str).unique()) if len(x.dropna()) > 0 else '',
            'ROLE_E': lambda x: '; '.join(x.dropna().astype(str).unique()) if len(x.dropna()) > 0 else ''
        }).reset_index()
        
        enhanced_df = enhanced_df.merge(company_summary, on='INCIDENT_ID', how='left')
    
    # Export enhanced data
    enhanced_csv = "medical_device_incidents_enhanced_sept2024_sept2025.csv"
    enhanced_xlsx = "medical_device_incidents_enhanced_sept2024_sept2025.xlsx"
    
    enhanced_df.to_csv(enhanced_csv, index=False)
    enhanced_df.to_excel(enhanced_xlsx, index=False)
    
    print(f"   ✅ Enhanced CSV: {enhanced_csv}")
    print(f"   ✅ Enhanced Excel: {enhanced_xlsx}")
    
    # Create a summary report
    create_summary_report(enhanced_df)


def create_summary_report(df):
    """
    Create a comprehensive summary report
    """
    report_file = "medical_device_incidents_analysis_report.txt"
    
    with open(report_file, 'w') as f:
        f.write("MEDICAL DEVICE INCIDENTS ANALYSIS REPORT\n")
        f.write("=========================================\n")
        f.write("Data Period: September 2024 - September 2025\n")
        f.write(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"SUMMARY STATISTICS\n")
        f.write(f"------------------\n")
        f.write(f"Total Incidents: {len(df):,}\n")
        
        if 'RECEIPT_DT' in df.columns:
            df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'])
            f.write(f"Date Range: {df['RECEIPT_DT'].min().strftime('%Y-%m-%d')} to {df['RECEIPT_DT'].max().strftime('%Y-%m-%d')}\n")
        
        f.write(f"\nINCIDENT TYPES\n")
        f.write(f"--------------\n")
        incident_types = df['INCIDENT_TYPE_E'].value_counts()
        for incident_type, count in incident_types.items():
            percentage = (count / len(df)) * 100
            f.write(f"{incident_type}: {count:,} ({percentage:.1f}%)\n")
        
        if 'HAZARD_SEVERITY_CODE_E' in df.columns:
            f.write(f"\nSEVERITY LEVELS\n")
            f.write(f"---------------\n")
            severity_counts = df['HAZARD_SEVERITY_CODE_E'].value_counts()
            for severity, count in severity_counts.items():
                if pd.notna(severity):
                    percentage = (count / len(df)) * 100
                    f.write(f"{severity}: {count:,} ({percentage:.1f}%)\n")
        
        if 'TRADE_NAME' in df.columns:
            f.write(f"\nTOP DEVICES\n")
            f.write(f"-----------\n")
            # Split device names and count
            all_devices = []
            for devices in df['TRADE_NAME'].dropna():
                all_devices.extend([d.strip() for d in str(devices).split(';') if d.strip()])
            
            device_counts = pd.Series(all_devices).value_counts()
            for device, count in device_counts.head(20).items():
                f.write(f"{device}: {count:,}\n")
        
        if 'COMPANY_NAME' in df.columns:
            f.write(f"\nTOP COMPANIES\n")
            f.write(f"-------------\n")
            # Split company names and count
            all_companies = []
            for companies in df['COMPANY_NAME'].dropna():
                all_companies.extend([c.strip() for c in str(companies).split(';') if c.strip()])
            
            company_counts = pd.Series(all_companies).value_counts()
            for company, count in company_counts.head(20).items():
                f.write(f"{company}: {count:,}\n")
    
    print(f"   ✅ Summary Report: {report_file}")


if __name__ == "__main__":
    analyze_incident_data()
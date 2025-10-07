#!/usr/bin/env python3
"""
INFUSOMAT Canadian Complaints Filter
Filters Canadian Medical Device Incidents database for INFUSOMAT-related complaints only
"""

import pandas as pd
import re
from datetime import datetime
import json

class InfusomatCanadianFilter:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.infusomat_complaints = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_canadian_data(self):
        """Load the Canadian medical device incidents CSV file"""
        try:
            print("📊 Loading Canadian Medical Device Incidents data...")
            self.df = pd.read_csv(self.csv_file_path)
            print(f"✅ Loaded {len(self.df)} total incidents from Canadian database")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def filter_infusomat_complaints(self):
        """Filter for INFUSOMAT-related incidents only"""
        print("\n🔍 Filtering for INFUSOMAT complaints...")
        
        # Define INFUSOMAT search patterns
        infusomat_patterns = [
            r'INFUSOMAT',
            r'INFUSO MAT',
            r'B\.?\s*BRAUN.*INFUS',
            r'BRAUN.*PUMP',
            r'INFUSION.*PUMP.*BRAUN',
            r'B\.?\s*BRAUN.*SPACE',
            r'INFUSOMAT.*SPACE'
        ]
        
        # Combine all patterns
        pattern = '|'.join(infusomat_patterns)
        
        # Search in relevant columns
        search_columns = ['TRADE_NAME', 'COMPANY_NAME']
        if 'INCIDENT_DESCRIPTION' in self.df.columns:
            search_columns.append('INCIDENT_DESCRIPTION')
        if 'EVENT_DESCRIPTION' in self.df.columns:
            search_columns.append('EVENT_DESCRIPTION')
        if 'PROBLEM_DESCRIPTION' in self.df.columns:
            search_columns.append('PROBLEM_DESCRIPTION')
            
        # Filter for INFUSOMAT incidents
        infusomat_mask = pd.Series([False] * len(self.df))
        
        for column in search_columns:
            if column in self.df.columns:
                column_mask = self.df[column].fillna('').str.contains(pattern, case=False, regex=True)
                infusomat_mask = infusomat_mask | column_mask
                print(f"  🔍 Found {column_mask.sum()} matches in {column}")
        
        self.infusomat_df = self.df[infusomat_mask].copy()
        print(f"\n✅ Total INFUSOMAT complaints found: {len(self.infusomat_df)}")
        
        return len(self.infusomat_df) > 0
    
    def analyze_infusomat_data(self):
        """Analyze the filtered INFUSOMAT complaints"""
        if len(self.infusomat_df) == 0:
            print("❌ No INFUSOMAT complaints to analyze")
            return
            
        print("\n📊 INFUSOMAT Complaints Analysis:")
        print("=" * 50)
        
        # Basic statistics
        print(f"📈 Total INFUSOMAT Complaints: {len(self.infusomat_df)}")
        
        # Date range analysis
        if 'INCIDENT_DT' in self.infusomat_df.columns:
            self.infusomat_df['INCIDENT_DT'] = pd.to_datetime(self.infusomat_df['INCIDENT_DT'], errors='coerce')
            date_range = self.infusomat_df['INCIDENT_DT'].dropna()
            if len(date_range) > 0:
                print(f"📅 Date Range: {date_range.min().strftime('%Y-%m-%d')} to {date_range.max().strftime('%Y-%m-%d')}")
        
        # Severity analysis
        if 'HAZARD_SEVERITY_CODE_E' in self.infusomat_df.columns:
            severity_counts = self.infusomat_df['HAZARD_SEVERITY_CODE_E'].value_counts()
            print(f"\n🚨 Severity Breakdown:")
            for severity, count in severity_counts.items():
                print(f"  • {severity}: {count} cases")
        
        # Company analysis
        if 'COMPANY_NAME' in self.infusomat_df.columns:
            company_counts = self.infusomat_df['COMPANY_NAME'].value_counts()
            print(f"\n🏥 Top Companies:")
            for company, count in company_counts.head(5).items():
                print(f"  • {company}: {count} complaints")
        
        # Trade name analysis
        if 'TRADE_NAME' in self.infusomat_df.columns:
            trade_counts = self.infusomat_df['TRADE_NAME'].value_counts()
            print(f"\n🔧 Device Models:")
            for trade_name, count in trade_counts.head(10).items():
                if pd.notna(trade_name):
                    print(f"  • {trade_name}: {count} complaints")
    
    def export_filtered_data(self):
        """Export filtered INFUSOMAT complaints to multiple formats"""
        base_filename = f"INFUSOMAT_CANADIAN_COMPLAINTS_{self.timestamp}"
        
        try:
            # Export to CSV
            csv_file = f"{base_filename}.csv"
            self.infusomat_df.to_csv(csv_file, index=False)
            print(f"\n💾 Exported to CSV: {csv_file}")
            
            # Export to Excel
            excel_file = f"{base_filename}.xlsx"
            self.infusomat_df.to_excel(excel_file, index=False)
            print(f"💾 Exported to Excel: {excel_file}")
            
            # Create summary report
            summary_file = f"{base_filename}_SUMMARY.md"
            self.create_summary_report(summary_file)
            print(f"📋 Created summary report: {summary_file}")
            
            # Export high-severity cases
            if 'HAZARD_SEVERITY_CODE_E' in self.infusomat_df.columns:
                high_severity = self.infusomat_df[
                    self.infusomat_df['HAZARD_SEVERITY_CODE_E'].str.contains(
                        'DEATH|SERIOUS|CRITICAL', case=False, na=False
                    )
                ]
                if len(high_severity) > 0:
                    high_severity_file = f"{base_filename}_HIGH_SEVERITY.csv"
                    high_severity.to_csv(high_severity_file, index=False)
                    print(f"⚠️ High severity cases: {high_severity_file} ({len(high_severity)} cases)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False
    
    def create_summary_report(self, filename):
        """Create a markdown summary report"""
        with open(filename, 'w') as f:
            f.write(f"# INFUSOMAT Canadian Complaints Summary\n")
            f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
            
            f.write(f"## 📊 Overview\n")
            f.write(f"- **Total INFUSOMAT Complaints**: {len(self.infusomat_df)}\n")
            f.write(f"- **Data Source**: Canadian Medical Device Incidents Database\n")
            f.write(f"- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            if 'HAZARD_SEVERITY_CODE_E' in self.infusomat_df.columns:
                f.write(f"## 🚨 Severity Analysis\n")
                severity_counts = self.infusomat_df['HAZARD_SEVERITY_CODE_E'].value_counts()
                for severity, count in severity_counts.items():
                    percentage = (count / len(self.infusomat_df)) * 100
                    f.write(f"- **{severity}**: {count} cases ({percentage:.1f}%)\n")
                f.write("\n")
            
            if 'TRADE_NAME' in self.infusomat_df.columns:
                f.write(f"## 🔧 Top Device Models\n")
                trade_counts = self.infusomat_df['TRADE_NAME'].value_counts().head(10)
                for trade_name, count in trade_counts.items():
                    if pd.notna(trade_name) and 'INFUSOMAT' in str(trade_name).upper():
                        f.write(f"- **{trade_name}**: {count} complaints\n")
                f.write("\n")
            
            f.write(f"## 📋 Data Columns Available\n")
            for col in self.infusomat_df.columns:
                non_null = self.infusomat_df[col].count()
                f.write(f"- `{col}`: {non_null}/{len(self.infusomat_df)} values\n")
    
    def run_complete_analysis(self):
        """Run the complete INFUSOMAT filtering and analysis"""
        print("🚀 Starting INFUSOMAT Canadian Complaints Analysis")
        print("=" * 60)
        
        # Load data
        if not self.load_canadian_data():
            return False
        
        # Filter for INFUSOMAT
        if not self.filter_infusomat_complaints():
            print("❌ No INFUSOMAT complaints found in database")
            return False
        
        # Analyze data
        self.analyze_infusomat_data()
        
        # Export results
        if self.export_filtered_data():
            print("\n✅ INFUSOMAT filtering and analysis completed successfully!")
            print("\n📁 Generated Files:")
            print(f"  • CSV: INFUSOMAT_CANADIAN_COMPLAINTS_{self.timestamp}.csv")
            print(f"  • Excel: INFUSOMAT_CANADIAN_COMPLAINTS_{self.timestamp}.xlsx")
            print(f"  • Summary: INFUSOMAT_CANADIAN_COMPLAINTS_{self.timestamp}_SUMMARY.md")
            return True
        else:
            return False

def main():
    # Path to Canadian medical device incidents CSV
    csv_file_path = "medical_device_incidents_enhanced_sept2024_sept2025.csv"
    
    # Create and run the INFUSOMAT filter
    infusomat_filter = InfusomatCanadianFilter(csv_file_path)
    success = infusomat_filter.run_complete_analysis()
    
    if success:
        print("\n🎯 INFUSOMAT Canadian complaints successfully extracted and analyzed!")
    else:
        print("\n❌ Analysis failed. Please check the input file and try again.")

if __name__ == "__main__":
    main()
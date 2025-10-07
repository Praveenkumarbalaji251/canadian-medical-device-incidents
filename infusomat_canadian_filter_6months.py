#!/usr/bin/env python3
"""
INFUSOMAT Canadian Complaints Filter - Last 6 Months
Filters Canadian Medical Device Incidents database for INFUSOMAT-related complaints from the past 6 months only
"""

import pandas as pd
import re
from datetime import datetime, timedelta
import json

class InfusomatCanadianFilter6Months:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.infusomat_complaints = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Calculate 6 months ago from today
        self.six_months_ago = datetime.now() - timedelta(days=180)
        self.today = datetime.now()
        
        print(f"📅 Filtering for incidents from {self.six_months_ago.strftime('%Y-%m-%d')} to {self.today.strftime('%Y-%m-%d')}")
        
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
    
    def filter_last_6_months(self):
        """Filter for incidents from the last 6 months"""
        print(f"\n📅 Filtering for incidents from the last 6 months...")
        
        # Convert date columns to datetime
        date_columns = ['INCIDENT_DT', 'RECEIPT_DT', 'INC_AWARE_DT']
        
        # Try different date columns to find the most relevant one
        for date_col in date_columns:
            if date_col in self.infusomat_df.columns:
                print(f"  📅 Processing {date_col}...")
                
                # Convert to datetime
                self.infusomat_df[f'{date_col}_parsed'] = pd.to_datetime(
                    self.infusomat_df[date_col], 
                    errors='coerce'
                )
                
                # Count valid dates
                valid_dates = self.infusomat_df[f'{date_col}_parsed'].notna().sum()
                print(f"    ✅ {valid_dates} valid dates in {date_col}")
        
        # Use INCIDENT_DT as primary filter, fall back to RECEIPT_DT
        primary_date_col = None
        if 'INCIDENT_DT_parsed' in self.infusomat_df.columns:
            primary_date_col = 'INCIDENT_DT_parsed'
            print(f"  🎯 Using INCIDENT_DT as primary date filter")
        elif 'RECEIPT_DT_parsed' in self.infusomat_df.columns:
            primary_date_col = 'RECEIPT_DT_parsed'
            print(f"  🎯 Using RECEIPT_DT as primary date filter")
        elif 'INC_AWARE_DT_parsed' in self.infusomat_df.columns:
            primary_date_col = 'INC_AWARE_DT_parsed'
            print(f"  🎯 Using INC_AWARE_DT as primary date filter")
        
        if primary_date_col:
            # Filter for last 6 months
            recent_mask = (
                (self.infusomat_df[primary_date_col] >= self.six_months_ago) &
                (self.infusomat_df[primary_date_col] <= self.today)
            )
            
            self.recent_infusomat_df = self.infusomat_df[recent_mask].copy()
            
            print(f"\n✅ INFUSOMAT complaints from last 6 months: {len(self.recent_infusomat_df)}")
            
            if len(self.recent_infusomat_df) > 0:
                date_range = self.recent_infusomat_df[primary_date_col].dropna()
                if len(date_range) > 0:
                    print(f"📅 Filtered date range: {date_range.min().strftime('%Y-%m-%d')} to {date_range.max().strftime('%Y-%m-%d')}")
            
            return len(self.recent_infusomat_df) > 0
        else:
            print("❌ No valid date columns found for filtering")
            self.recent_infusomat_df = self.infusomat_df.copy()
            return True
    
    def analyze_recent_infusomat_data(self):
        """Analyze the filtered recent INFUSOMAT complaints"""
        if len(self.recent_infusomat_df) == 0:
            print("❌ No recent INFUSOMAT complaints to analyze")
            return
            
        print("\n📊 Recent INFUSOMAT Complaints Analysis (Last 6 Months):")
        print("=" * 60)
        
        # Basic statistics
        print(f"📈 Total Recent INFUSOMAT Complaints: {len(self.recent_infusomat_df)}")
        
        # Monthly breakdown
        if 'INCIDENT_DT_parsed' in self.recent_infusomat_df.columns:
            monthly_counts = self.recent_infusomat_df.set_index('INCIDENT_DT_parsed').resample('M').size()
            print(f"\n📊 Monthly Breakdown:")
            for month, count in monthly_counts.items():
                if count > 0:
                    print(f"  • {month.strftime('%B %Y')}: {count} complaints")
        
        # Severity analysis
        if 'HAZARD_SEVERITY_CODE_E' in self.recent_infusomat_df.columns:
            severity_counts = self.recent_infusomat_df['HAZARD_SEVERITY_CODE_E'].value_counts()
            print(f"\n🚨 Recent Severity Breakdown:")
            for severity, count in severity_counts.items():
                percentage = (count / len(self.recent_infusomat_df)) * 100
                print(f"  • {severity}: {count} cases ({percentage:.1f}%)")
        
        # Company analysis
        if 'COMPANY_NAME' in self.recent_infusomat_df.columns:
            company_counts = self.recent_infusomat_df['COMPANY_NAME'].value_counts()
            print(f"\n🏥 Top Companies (Recent):")
            for company, count in company_counts.head(5).items():
                print(f"  • {company}: {count} complaints")
        
        # Trade name analysis
        if 'TRADE_NAME' in self.recent_infusomat_df.columns:
            trade_counts = self.recent_infusomat_df['TRADE_NAME'].value_counts()
            print(f"\n🔧 Recent Device Models:")
            for trade_name, count in trade_counts.head(10).items():
                if pd.notna(trade_name):
                    print(f"  • {trade_name}: {count} complaints")
        
        # Compare with all-time data
        print(f"\n📈 Comparison:")
        print(f"  • Recent (6 months): {len(self.recent_infusomat_df)} complaints")
        print(f"  • All-time total: {len(self.infusomat_df)} complaints")
        if len(self.infusomat_df) > 0:
            recent_percentage = (len(self.recent_infusomat_df) / len(self.infusomat_df)) * 100
            print(f"  • Recent represents {recent_percentage:.1f}% of all complaints")
    
    def export_recent_data(self):
        """Export filtered recent INFUSOMAT complaints to multiple formats"""
        base_filename = f"INFUSOMAT_CANADIAN_LAST_6_MONTHS_{self.timestamp}"
        
        try:
            # Export to CSV
            csv_file = f"{base_filename}.csv"
            self.recent_infusomat_df.to_csv(csv_file, index=False)
            print(f"\n💾 Exported recent data to CSV: {csv_file}")
            
            # Export to Excel
            excel_file = f"{base_filename}.xlsx"
            self.recent_infusomat_df.to_excel(excel_file, index=False)
            print(f"💾 Exported recent data to Excel: {excel_file}")
            
            # Create summary report
            summary_file = f"{base_filename}_SUMMARY.md"
            self.create_recent_summary_report(summary_file)
            print(f"📋 Created recent summary report: {summary_file}")
            
            # Export high-severity recent cases
            if 'HAZARD_SEVERITY_CODE_E' in self.recent_infusomat_df.columns:
                high_severity = self.recent_infusomat_df[
                    self.recent_infusomat_df['HAZARD_SEVERITY_CODE_E'].str.contains(
                        'DEATH|INJURY|POTENTIAL FOR DEATH', case=False, na=False
                    )
                ]
                if len(high_severity) > 0:
                    high_severity_file = f"{base_filename}_HIGH_SEVERITY.csv"
                    high_severity.to_csv(high_severity_file, index=False)
                    print(f"⚠️ Recent high severity cases: {high_severity_file} ({len(high_severity)} cases)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting recent data: {e}")
            return False
    
    def create_recent_summary_report(self, filename):
        """Create a markdown summary report for recent data"""
        with open(filename, 'w') as f:
            f.write(f"# INFUSOMAT Canadian Complaints - Last 6 Months\n")
            f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
            
            f.write(f"## 📊 Overview\n")
            f.write(f"- **Recent INFUSOMAT Complaints**: {len(self.recent_infusomat_df)} (Last 6 months)\n")
            f.write(f"- **Total INFUSOMAT Complaints**: {len(self.infusomat_df)} (All time)\n")
            f.write(f"- **Data Source**: Canadian Medical Device Incidents Database\n")
            f.write(f"- **Date Range**: {self.six_months_ago.strftime('%Y-%m-%d')} to {self.today.strftime('%Y-%m-%d')}\n")
            if len(self.infusomat_df) > 0:
                recent_percentage = (len(self.recent_infusomat_df) / len(self.infusomat_df)) * 100
                f.write(f"- **Recent vs All-time**: {recent_percentage:.1f}% of complaints are from last 6 months\n")
            f.write("\n")
            
            if 'HAZARD_SEVERITY_CODE_E' in self.recent_infusomat_df.columns:
                f.write(f"## 🚨 Recent Severity Analysis\n")
                severity_counts = self.recent_infusomat_df['HAZARD_SEVERITY_CODE_E'].value_counts()
                for severity, count in severity_counts.items():
                    percentage = (count / len(self.recent_infusomat_df)) * 100
                    f.write(f"- **{severity}**: {count} cases ({percentage:.1f}%)\n")
                f.write("\n")
            
            # Monthly breakdown
            if 'INCIDENT_DT_parsed' in self.recent_infusomat_df.columns:
                f.write(f"## 📅 Monthly Breakdown\n")
                monthly_counts = self.recent_infusomat_df.set_index('INCIDENT_DT_parsed').resample('M').size()
                for month, count in monthly_counts.items():
                    if count > 0:
                        f.write(f"- **{month.strftime('%B %Y')}**: {count} complaints\n")
                f.write("\n")
            
            if 'TRADE_NAME' in self.recent_infusomat_df.columns:
                f.write(f"## 🔧 Recent Top Device Models\n")
                trade_counts = self.recent_infusomat_df['TRADE_NAME'].value_counts().head(10)
                for trade_name, count in trade_counts.items():
                    if pd.notna(trade_name) and 'INFUSOMAT' in str(trade_name).upper():
                        f.write(f"- **{trade_name}**: {count} complaints\n")
                f.write("\n")
            
            f.write(f"## 📋 Recent Data Columns Available\n")
            for col in self.recent_infusomat_df.columns:
                non_null = self.recent_infusomat_df[col].count()
                f.write(f"- `{col}`: {non_null}/{len(self.recent_infusomat_df)} values\n")
    
    def run_complete_analysis(self):
        """Run the complete recent INFUSOMAT filtering and analysis"""
        print("🚀 Starting Recent INFUSOMAT Canadian Complaints Analysis (Last 6 Months)")
        print("=" * 70)
        
        # Load data
        if not self.load_canadian_data():
            return False
        
        # Filter for INFUSOMAT
        if not self.filter_infusomat_complaints():
            print("❌ No INFUSOMAT complaints found in database")
            return False
        
        # Filter for last 6 months
        if not self.filter_last_6_months():
            print("❌ No recent INFUSOMAT complaints found")
            return False
        
        # Analyze recent data
        self.analyze_recent_infusomat_data()
        
        # Export results
        if self.export_recent_data():
            print("\n✅ Recent INFUSOMAT filtering and analysis completed successfully!")
            print("\n📁 Generated Files:")
            print(f"  • CSV: INFUSOMAT_CANADIAN_LAST_6_MONTHS_{self.timestamp}.csv")
            print(f"  • Excel: INFUSOMAT_CANADIAN_LAST_6_MONTHS_{self.timestamp}.xlsx")
            print(f"  • Summary: INFUSOMAT_CANADIAN_LAST_6_MONTHS_{self.timestamp}_SUMMARY.md")
            return True
        else:
            return False

def main():
    # Path to Canadian medical device incidents CSV
    csv_file_path = "medical_device_incidents_enhanced_sept2024_sept2025.csv"
    
    # Create and run the recent INFUSOMAT filter
    recent_filter = InfusomatCanadianFilter6Months(csv_file_path)
    success = recent_filter.run_complete_analysis()
    
    if success:
        print("\n🎯 Recent INFUSOMAT Canadian complaints (last 6 months) successfully extracted and analyzed!")
    else:
        print("\n❌ Analysis failed. Please check the input file and try again.")

if __name__ == "__main__":
    main()
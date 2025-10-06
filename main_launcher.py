#!/usr/bin/env python3
"""
Dashboard Launcher and Quick Insights Summary
"""

import os
import pandas as pd


def display_quick_insights():
    """Display quick insights from the analysis"""
    print("🏥 MEDICAL DEVICE INCIDENTS DASHBOARD")
    print("=" * 60)
    print("📅 Data Period: September 2024 - September 2025")
    print("🌐 Source: Health Canada Medical Device Incidents Database")
    print()
    
    # Load the main data for quick stats
    if os.path.exists("medical_device_incidents_enhanced_sept2024_sept2025.csv"):
        df = pd.read_csv("medical_device_incidents_enhanced_sept2024_sept2025.csv")
    else:
        df = pd.read_csv("medical_device_incidents_sept2024_sept2025.csv")
    
    print("📊 KEY METRICS:")
    print(f"   • Total Incidents: {len(df):,}")
    
    # Severity breakdown
    severity_counts = df['HAZARD_SEVERITY_CODE_E'].value_counts()
    print(f"   • Deaths: {severity_counts.get('DEATH', 0):,}")
    print(f"   • Injuries: {severity_counts.get('INJURY', 0):,}")
    print(f"   • Potential for Death/Injury: {severity_counts.get('POTENTIAL FOR DEATH/INJURY', 0):,}")
    print()
    
    # Date range
    df['RECEIPT_DT'] = pd.to_datetime(df['RECEIPT_DT'])
    print(f"📅 TEMPORAL ANALYSIS:")
    print(f"   • Date Range: {df['RECEIPT_DT'].min().strftime('%Y-%m-%d')} to {df['RECEIPT_DT'].max().strftime('%Y-%m-%d')}")
    
    # Monthly breakdown
    monthly_counts = df.groupby(df['RECEIPT_DT'].dt.to_period('M')).size()
    peak_month = monthly_counts.idxmax()
    print(f"   • Peak Month: {peak_month} ({monthly_counts.max()} incidents)")
    print()
    
    # Top incident types
    print("🔍 TOP INCIDENT TYPES:")
    incident_types = df['INCIDENT_TYPE_E'].value_counts().head(3)
    for i, (incident_type, count) in enumerate(incident_types.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"   {i}. {incident_type}: {count:,} ({percentage:.1f}%)")
    print()
    
    print("📁 AVAILABLE FILES:")
    files = [
        ("medical_device_incidents_sept2024_sept2025.csv", "Main incident data (CSV)"),
        ("medical_device_incidents_sept2024_sept2025.xlsx", "Main incident data (Excel)"),
        ("medical_device_incidents_enhanced_sept2024_sept2025.csv", "Enhanced data with device/company info"),
        ("medical_device_incidents_enhanced_sept2024_sept2025.xlsx", "Enhanced data (Excel)"),
        ("medical_device_incidents_research_report.txt", "Comprehensive research report"),
        ("medical_device_incidents_analysis.png", "Statistical visualizations")
    ]
    
    for filename, description in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024 / 1024  # Size in MB
            print(f"   ✅ {filename} - {description} ({size:.1f} MB)")
        else:
            print(f"   ❌ {filename} - {description} (not found)")
    print()
    
    print("🚀 ANALYSIS TOOLS:")
    print("   1. Interactive Dashboard: python dashboard.py")
    print("   2. Detailed Analysis: python analyze_data.py")
    print("   3. Research Insights: python research_analysis.py")
    print("   4. Data Extraction: python run_extraction.py")
    print()
    
    print("💡 RESEARCH INSIGHTS SUMMARY:")
    
    # Read insights from research report if available
    if os.path.exists("medical_device_incidents_research_report.txt"):
        print("   📖 Comprehensive research report generated")
        print("   📊 Statistical analysis completed")
        print("   🎯 Predictive modeling performed")
        print("   📈 Trend analysis available")
    
    print()
    print("🔗 DASHBOARD FEATURES:")
    print("   • Temporal Analysis - Monthly trends and patterns")
    print("   • Severity Analysis - Risk distribution and trends")
    print("   • Company Analysis - Top companies and risk factors")
    print("   • Device Analysis - Device categories and risks")
    print("   • Advanced Analytics - Clustering and predictions")
    print("   • Trends & Patterns - Growth and anomaly detection")
    print()
    
    print("🎯 KEY RESEARCH FINDINGS:")
    
    # Death rate
    death_rate = (severity_counts.get('DEATH', 0) / len(df)) * 100
    print(f"   • Overall death rate: {death_rate:.2f}%")
    
    # Injury rate
    injury_rate = (severity_counts.get('INJURY', 0) / len(df)) * 100
    print(f"   • Injury rate: {injury_rate:.1f}%")
    
    # High-risk percentage
    high_risk = severity_counts.get('DEATH', 0) + severity_counts.get('INJURY', 0)
    high_risk_rate = (high_risk / len(df)) * 100
    print(f"   • High-risk incidents (death/injury): {high_risk_rate:.1f}%")
    
    print()
    print("📈 DASHBOARD INSIGHTS TO EXPLORE:")
    print("   1. Seasonal patterns in medical device incidents")
    print("   2. Company performance and risk assessment")
    print("   3. Device category risk analysis")
    print("   4. Predictive factors for severe incidents")
    print("   5. Geographic and temporal clustering")
    print("   6. Anomaly detection in incident reporting")
    print()


def launch_dashboard():
    """Launch the interactive dashboard"""
    print("🚀 Launching Interactive Dashboard...")
    print("📱 The dashboard will open in your web browser")
    print("🔗 URL: http://localhost:8050")
    print()
    print("Dashboard Features:")
    print("• Real-time filtering and interaction")
    print("• Multiple analysis tabs")
    print("• Export capabilities")
    print("• Advanced visualizations")
    print()
    
    try:
        from dashboard import MedicalDeviceDashboard
        dashboard = MedicalDeviceDashboard()
        dashboard.run(debug=False, port=8050)
    except ImportError as e:
        print(f"❌ Error importing dashboard: {e}")
        print("Make sure all required packages are installed:")
        print("pip install plotly dash")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")


def main():
    """Main function"""
    display_quick_insights()
    
    while True:
        print("🎮 CHOOSE AN ACTION:")
        print("1. Launch Interactive Dashboard")
        print("2. View Quick Summary (refresh)")
        print("3. Run Detailed Analysis")
        print("4. Generate Research Report")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            launch_dashboard()
            break
        elif choice == "2":
            print("\n" + "="*60)
            display_quick_insights()
        elif choice == "3":
            print("🔍 Running detailed analysis...")
            os.system("python analyze_data.py")
        elif choice == "4":
            print("📊 Generating research report...")
            os.system("python research_analysis.py")
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
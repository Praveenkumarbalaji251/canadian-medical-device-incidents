#!/usr/bin/env python3
"""
Quick runner script to extract Medical Device Incidents data from September 2024 to September 2025
"""

from mdi_extractor import MedicalDeviceIncidentsExtractor


def main():
    """
    Run the extraction for Medical Device Incidents from September 2024 to September 2025
    """
    print("🏥 Medical Device Incidents Data Extractor")
    print("📅 Extracting data from September 2024 to September 2025")
    print("🌐 Source: Health Canada Medical Device Incidents Database")
    print("=" * 60)
    
    # Create extractor instance
    extractor = MedicalDeviceIncidentsExtractor()
    
    try:
        # Extract the data
        incident_data = extractor.extract_september_2024_to_2025()
        
        if incident_data is not None and not incident_data.empty:
            print("\n✅ SUCCESS: Data extraction completed!")
            print(f"📊 Total incidents found: {len(incident_data)}")
            print("\n📁 Output files created:")
            print("  • medical_device_incidents_sept2024_sept2025.csv")
            print("  • medical_device_incidents_sept2024_sept2025.xlsx") 
            print("  • medical_device_incidents_sept2024_sept2025_summary.txt")
            print("\n💡 You can now:")
            print("  1. Open the Excel file for easy viewing")
            print("  2. Use the CSV file for further analysis")
            print("  3. Check the summary file for data overview")
            
        else:
            print("\n⚠️  No data found for the specified date range")
            print("This could mean:")
            print("  • No incidents reported in September 2024 - September 2025")
            print("  • Date format issues in the source data")
            print("  • Changes in the database structure")
            
    except Exception as e:
        print(f"\n❌ ERROR: Data extraction failed")
        print(f"Error details: {e}")
        print("\nTroubleshooting tips:")
        print("  • Check your internet connection")
        print("  • Verify the database URL is accessible")
        print("  • Try running the script again (sometimes network issues are temporary)")


if __name__ == "__main__":
    main()
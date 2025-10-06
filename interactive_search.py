#!/usr/bin/env python3
"""
Interactive script to search and extract Canadian Medical Devices data
"""

from medical_devices_extractor import CanadianMedicalDevicesExtractor
import json


def interactive_search():
    """
    Interactive command-line interface for searching medical devices
    """
    extractor = CanadianMedicalDevicesExtractor()
    
    print("🏥 Canadian Medical Devices Database Extractor")
    print("=" * 50)
    print("This tool helps you extract data from Health Canada's Medical Devices Active Licence Listing (MDALL)")
    print()
    
    while True:
        print("\nSearch Options:")
        print("1. Search by Device Name")
        print("2. Search by Company Name")
        print("3. Search by License Number")
        print("4. Search by Device Identifier")
        print("5. Custom Search (multiple criteria)")
        print("6. Export all results")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "7":
            print("Goodbye!")
            break
            
        try:
            devices = []
            
            if choice == "1":
                device_name = input("Enter device name (e.g., 'pacemaker', 'stent'): ").strip()
                if device_name:
                    print(f"Searching for devices containing '{device_name}'...")
                    devices = extractor.search_active_licenses(device_name=device_name)
                    
            elif choice == "2":
                company_name = input("Enter company name (e.g., 'Abbott', 'Medtronic'): ").strip()
                if company_name:
                    print(f"Searching for devices from '{company_name}'...")
                    devices = extractor.search_active_licenses(company_name=company_name)
                    
            elif choice == "3":
                license_number = input("Enter license number: ").strip()
                if license_number:
                    print(f"Searching for license number '{license_number}'...")
                    devices = extractor.search_active_licenses(license_number=license_number)
                    
            elif choice == "4":
                device_identifier = input("Enter device identifier: ").strip()
                if device_identifier:
                    print(f"Searching for device identifier '{device_identifier}'...")
                    devices = extractor.search_active_licenses(device_identifier=device_identifier)
                    
            elif choice == "5":
                print("Enter search criteria (leave blank to skip):")
                device_name = input("Device name: ").strip() or None
                company_name = input("Company name: ").strip() or None
                license_number = input("License number: ").strip() or None
                device_identifier = input("Device identifier: ").strip() or None
                
                max_results = input("Maximum results (default 100): ").strip()
                max_results = int(max_results) if max_results.isdigit() else 100
                
                print("Searching...")
                devices = extractor.search_active_licenses(
                    device_name=device_name,
                    company_name=company_name,
                    license_number=license_number,
                    device_identifier=device_identifier,
                    max_results=max_results
                )
                
            elif choice == "6":
                print("This feature will be implemented to export all previously searched results")
                continue
                
            else:
                print("Invalid choice. Please try again.")
                continue
            
            # Display results
            if devices:
                print(f"\n✅ Found {len(devices)} devices:")
                print("-" * 80)
                
                for i, device in enumerate(devices[:10], 1):  # Show first 10
                    print(f"{i:2d}. {device['device_name'][:50]}")
                    print(f"    Company: {device['company_name']}")
                    print(f"    License: {device['license_number']}")
                    print(f"    Date: {device['license_date']}")
                    if device['device_class']:
                        print(f"    Class: {device['device_class']}")
                    print()
                
                if len(devices) > 10:
                    print(f"... and {len(devices) - 10} more devices")
                
                # Ask if user wants to export
                export = input("\nWould you like to export these results? (y/n): ").strip().lower()
                if export == 'y':
                    format_choice = input("Export format - CSV (c) or Excel (e): ").strip().lower()
                    filename = input("Enter filename (without extension): ").strip()
                    
                    if not filename:
                        filename = "medical_devices_search"
                    
                    if format_choice == 'e':
                        extractor.export_to_excel(devices, f"{filename}.xlsx")
                    else:
                        extractor.export_to_csv(devices, f"{filename}.csv")
                        
            else:
                print("\n❌ No devices found with the specified criteria.")
                
        except Exception as e:
            print(f"\n❌ Error during search: {e}")
            print("Please try again with different search criteria.")


if __name__ == "__main__":
    interactive_search()
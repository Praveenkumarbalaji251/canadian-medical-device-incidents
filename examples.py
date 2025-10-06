"""
Sample scripts demonstrating different ways to extract Canadian medical device data
"""

from medical_devices_extractor import CanadianMedicalDevicesExtractor
import time


def example_1_device_categories():
    """Extract data for different device categories"""
    extractor = CanadianMedicalDevicesExtractor()
    
    device_categories = [
        "pacemaker",
        "stent",
        "insulin pump",
        "catheter",
        "artificial heart valve",
        "defibrillator",
        "surgical robot",
        "MRI scanner",
        "ultrasound",
        "X-ray"
    ]
    
    all_results = []
    
    for category in device_categories:
        print(f"Searching for: {category}")
        try:
            devices = extractor.search_active_licenses(
                device_name=category,
                max_results=25
            )
            
            # Add category tag to each device
            for device in devices:
                device['search_category'] = category
            
            all_results.extend(devices)
            print(f"  Found {len(devices)} devices")
            
            # Be respectful with requests
            time.sleep(1)
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Export combined results
    if all_results:
        extractor.export_to_excel(all_results, "device_categories_analysis.xlsx")
        print(f"\nTotal devices extracted: {len(all_results)}")


def example_2_major_manufacturers():
    """Extract data for major medical device manufacturers"""
    extractor = CanadianMedicalDevicesExtractor()
    
    manufacturers = [
        "Abbott",
        "Medtronic",
        "Johnson & Johnson",
        "Siemens",
        "GE Healthcare",
        "Philips",
        "Boston Scientific",
        "Stryker",
        "Baxter",
        "BD"
    ]
    
    manufacturer_data = {}
    
    for manufacturer in manufacturers:
        print(f"Searching for devices from: {manufacturer}")
        try:
            devices = extractor.search_active_licenses(
                company_name=manufacturer,
                max_results=50
            )
            
            manufacturer_data[manufacturer] = devices
            print(f"  Found {len(devices)} devices")
            
            # Be respectful with requests
            time.sleep(1)
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Export individual manufacturer files
    for manufacturer, devices in manufacturer_data.items():
        if devices:
            filename = f"{manufacturer.replace(' ', '_').replace('&', 'and').lower()}_devices.csv"
            extractor.export_to_csv(devices, filename)
    
    # Export combined data
    all_devices = []
    for devices in manufacturer_data.values():
        all_devices.extend(devices)
    
    if all_devices:
        extractor.export_to_excel(all_devices, "major_manufacturers_analysis.xlsx")
        print(f"\nTotal devices from major manufacturers: {len(all_devices)}")


def example_3_device_classes():
    """Search for devices and analyze by class"""
    extractor = CanadianMedicalDevicesExtractor()
    
    # Search broadly and then analyze by class
    search_terms = [
        "cardiac",
        "orthopedic",
        "surgical",
        "diagnostic",
        "monitoring",
        "therapeutic"
    ]
    
    all_devices = []
    
    for term in search_terms:
        print(f"Searching for: {term}")
        try:
            devices = extractor.search_active_licenses(
                device_name=term,
                max_results=30
            )
            
            all_devices.extend(devices)
            print(f"  Found {len(devices)} devices")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Analyze device classes
    class_counts = {}
    for device in all_devices:
        device_class = device.get('device_class', 'Unknown')
        class_counts[device_class] = class_counts.get(device_class, 0) + 1
    
    print("\nDevice Class Distribution:")
    for device_class, count in sorted(class_counts.items()):
        print(f"  {device_class}: {count} devices")
    
    # Export results
    if all_devices:
        extractor.export_to_excel(all_devices, "device_classes_analysis.xlsx")


def example_4_recent_licenses():
    """Search for recently licensed devices (broad search)"""
    extractor = CanadianMedicalDevicesExtractor()
    
    # Perform broad searches to find recent licenses
    broad_terms = ["device", "system", "monitor", "pump", "scanner"]
    
    all_devices = []
    
    for term in broad_terms:
        print(f"Broad search for: {term}")
        try:
            devices = extractor.search_active_licenses(
                device_name=term,
                max_results=100
            )
            
            all_devices.extend(devices)
            print(f"  Found {len(devices)} devices")
            
            time.sleep(2)  # Longer delay for broad searches
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Sort by license date (if available and parseable)
    try:
        # Filter for devices with license dates in 2023-2024
        recent_devices = []
        for device in all_devices:
            license_date = device.get('license_date', '')
            if any(year in license_date for year in ['2023', '2024', '2025']):
                recent_devices.append(device)
        
        print(f"\nFound {len(recent_devices)} recent devices (2023-2025)")
        
        if recent_devices:
            extractor.export_to_excel(recent_devices, "recent_licenses_2023_2025.xlsx")
            
    except Exception as e:
        print(f"Error processing dates: {e}")
        if all_devices:
            extractor.export_to_excel(all_devices, "broad_search_results.xlsx")


if __name__ == "__main__":
    print("Canadian Medical Devices - Sample Data Extraction")
    print("=" * 50)
    
    examples = [
        ("Device Categories Analysis", example_1_device_categories),
        ("Major Manufacturers Analysis", example_2_major_manufacturers), 
        ("Device Classes Analysis", example_3_device_classes),
        ("Recent Licenses Search", example_4_recent_licenses)
    ]
    
    print("\nAvailable examples:")
    for i, (name, func) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("0. Run all examples")
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    if choice == "0":
        for name, func in examples:
            print(f"\n{'='*20} {name} {'='*20}")
            func()
            print("\nWaiting 5 seconds before next example...")
            time.sleep(5)
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        print(f"\n{'='*20} {name} {'='*20}")
        func()
    else:
        print("Invalid choice.")
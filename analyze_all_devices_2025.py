#!/usr/bin/env python3
"""
Analyze all medical devices from 2025 Canadian incidents in descending order by count
"""

import pandas as pd
from datetime import datetime
import json

def analyze_all_devices_2025():
    print("📊 Analyzing ALL medical devices from 2025 Canadian incidents...")
    
    # Load the 2025 dashboard data
    try:
        with open('dashboard_data_2025_20251007_163751.json', 'r') as f:
            data = json.load(f)
        print(f"📋 Loaded {len(data)} total 2025 cases")
    except FileNotFoundError:
        print("❌ 2025 dashboard data file not found.")
        return
    
    # Count devices
    device_counts = {}
    
    for case in data:
        device_name = case['deviceName']
        device_counts[device_name] = device_counts.get(device_name, 0) + 1
    
    # Sort by count (descending)
    sorted_devices = sorted(device_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\\n🎯 COMPLETE MEDICAL DEVICE ANALYSIS - 2025")
    print(f"📅 Total Devices: {len(sorted_devices)}")
    print(f"📊 Total Incidents: {sum(device_counts.values())}")
    print(f"{'='*80}")
    
    # Display all devices
    for rank, (device_name, count) in enumerate(sorted_devices, 1):
        percentage = (count / len(data)) * 100
        print(f"#{rank:3d} | {count:4d} cases ({percentage:5.1f}%) | {device_name}")
    
    # Create detailed CSV report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'ALL_MEDICAL_DEVICES_2025_ANALYSIS_{timestamp}.csv'
    
    device_df = pd.DataFrame([
        {
            'Rank': rank,
            'Device_Name': device_name,
            'Incident_Count': count,
            'Percentage': round((count / len(data)) * 100, 2)
        }
        for rank, (device_name, count) in enumerate(sorted_devices, 1)
    ])
    
    device_df.to_csv(csv_filename, index=False)
    print(f"\\n💾 Detailed report saved: {csv_filename}")
    
    # Top 20 summary
    print(f"\\n🔥 TOP 20 MEDICAL DEVICES (2025):")
    print(f"{'Rank':<4} {'Cases':<6} {'%':<6} {'Device Name'}")
    print('-' * 80)
    
    for rank, (device_name, count) in enumerate(sorted_devices[:20], 1):
        percentage = (count / len(data)) * 100
        # Truncate long device names for display
        display_name = device_name[:60] + "..." if len(device_name) > 60 else device_name
        print(f"{rank:<4} {count:<6} {percentage:<6.1f} {display_name}")
    
    # Category analysis
    print(f"\\n📈 DEVICE CATEGORY INSIGHTS:")
    
    # Group by device type keywords
    categories = {
        'INFUSION/PUMP': ['INFUSION', 'PUMP', 'INFUSOMAT'],
        'INSULIN': ['INSULIN', 'T:SLIM'],
        'DIALYSIS': ['DIALYSIS', 'BVM'],
        'SURGICAL': ['SURGICAL', 'CLIP', 'IOL'],
        'IMPLANT': ['IMPLANT', 'BREAST'],
        'CARDIAC': ['CARDIAC', 'HEART', 'PACEMAKER'],
        'MONITORING': ['MONITOR', 'SENSOR'],
        'RESPIRATORY': ['VENTILATOR', 'CPAP', 'OXYGEN']
    }
    
    category_counts = {cat: 0 for cat in categories}
    
    for device_name, count in sorted_devices:
        device_upper = device_name.upper()
        for category, keywords in categories.items():
            if any(keyword in device_upper for keyword in keywords):
                category_counts[category] += count
                break
    
    # Sort categories by count
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    
    for category, count in sorted_categories:
        if count > 0:
            percentage = (count / len(data)) * 100
            print(f"   • {category:<15}: {count:4d} cases ({percentage:5.1f}%)")
    
    # Statistical summary
    print(f"\\n📊 STATISTICAL SUMMARY:")
    counts_only = [count for _, count in sorted_devices]
    print(f"   • Mean incidents per device: {sum(counts_only)/len(counts_only):.1f}")
    print(f"   • Median incidents per device: {sorted(counts_only)[len(counts_only)//2]}")
    print(f"   • Max incidents (single device): {max(counts_only)}")
    print(f"   • Min incidents (single device): {min(counts_only)}")
    print(f"   • Devices with >10 incidents: {len([c for c in counts_only if c > 10])}")
    print(f"   • Devices with >50 incidents: {len([c for c in counts_only if c > 50])}")
    print(f"   • Devices with >100 incidents: {len([c for c in counts_only if c > 100])}")
    
    # Create Excel report with categories
    excel_filename = f'ALL_MEDICAL_DEVICES_2025_COMPREHENSIVE_{timestamp}.xlsx'
    
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        # All devices sheet
        device_df.to_excel(writer, sheet_name='All Devices', index=False)
        
        # Top 50 devices sheet
        top_50_df = device_df.head(50)
        top_50_df.to_excel(writer, sheet_name='Top 50 Devices', index=False)
        
        # Category analysis sheet
        category_df = pd.DataFrame([
            {'Category': cat, 'Incident_Count': count, 'Percentage': round((count/len(data))*100, 2)}
            for cat, count in sorted_categories if count > 0
        ])
        category_df.to_excel(writer, sheet_name='Device Categories', index=False)
    
    print(f"📊 Comprehensive Excel report saved: {excel_filename}")
    
    return sorted_devices

if __name__ == "__main__":
    analyze_all_devices_2025()
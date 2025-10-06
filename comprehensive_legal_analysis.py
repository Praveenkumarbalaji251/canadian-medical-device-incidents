import pandas as pd
import json
from collections import defaultdict, Counter
import re

def analyze_all_potential_legal_devices():
    """Find all devices with potential legal cases - similar injuries/deaths, no class actions"""
    
    print("🔍 Analyzing ALL medical devices for potential legal cases...")
    
    # Load the incident data
    try:
        df = pd.read_csv('medical_device_incidents_enhanced_sept2024_sept2025.csv')
        print(f"✓ Loaded {len(df)} total incidents")
    except Exception as e:
        print(f"❌ Could not load incident data: {e}")
        return
    
    # Group by device name and analyze patterns
    device_analysis = defaultdict(lambda: {
        'total_incidents': 0,
        'deaths': 0,
        'injuries': 0,
        'malfunctions': 0,
        'injury_types': Counter(),
        'death_causes': Counter(),
        'malfunction_types': Counter(),
        'problem_patterns': Counter(),
        'incident_details': []
    })
    
    print("\n📊 Analyzing incident patterns by device...")
    
    for idx, row in df.iterrows():
        device_name = str(row.get('TRADE_NAME', '')).strip()
        if not device_name or device_name == 'nan':
            continue
            
        device_data = device_analysis[device_name]
        device_data['total_incidents'] += 1
        
        # Analyze incident types based on HAZARD_SEVERITY_CODE_E
        hazard_severity = str(row.get('HAZARD_SEVERITY_CODE_E', '')).lower()
        incident_type = str(row.get('INCIDENT_TYPE_E', '')).lower()
        
        if 'death' in hazard_severity or 'mort' in hazard_severity:
            device_data['deaths'] += 1
            # Use incident type as death cause description
            device_data['death_causes'][incident_type] += 1
            
        elif 'injury' in hazard_severity or 'blessure' in hazard_severity:
            device_data['injuries'] += 1
            # Use incident type as injury description
            device_data['injury_types'][incident_type] += 1
            
        else:
            device_data['malfunctions'] += 1
            # Use incident type as malfunction description
            device_data['malfunction_types'][incident_type] += 1
        
        # Capture all problem patterns (using incident type)
        device_data['problem_patterns'][incident_type] += 1
        
        # Store incident details for analysis
        device_data['incident_details'].append({
            'date': row.get('RECEIPT_DT', ''),
            'type': incident_type,
            'hazard_severity': hazard_severity,
            'manufacturer': str(row.get('COMPANY_NAME', '')),
            'incident_date': str(row.get('INCIDENT_DT', ''))
        })
    
    # Filter devices with significant incidents and potential legal merit
    potential_legal_devices = []
    
    print("\n⚖️ Identifying devices with legal potential...")
    
    for device_name, data in device_analysis.items():
        # Criteria for potential legal case:
        # 1. Multiple incidents (>= 5)
        # 2. Deaths OR serious injuries OR repeated malfunctions
        # 3. Similar patterns in problems
        
        total_incidents = data['total_incidents']
        deaths = data['deaths']
        injuries = data['injuries']
        malfunctions = data['malfunctions']
        
        if total_incidents >= 5:  # Minimum threshold
            # Check for similar death causes
            similar_death_patterns = any(count >= 2 for count in data['death_causes'].values())
            
            # Check for similar injury patterns  
            similar_injury_patterns = any(count >= 3 for count in data['injury_types'].values())
            
            # Check for repeated malfunction patterns
            similar_malfunction_patterns = any(count >= 5 for count in data['malfunction_types'].values())
            
            # Check for any repeated problem patterns
            repeated_problems = any(count >= 3 for count in data['problem_patterns'].values())
            
            if (deaths >= 2 and similar_death_patterns) or \
               (injuries >= 5 and similar_injury_patterns) or \
               (malfunctions >= 10 and similar_malfunction_patterns) or \
               (repeated_problems and total_incidents >= 10):
                
                # Calculate severity score
                severity_score = (deaths * 10) + (injuries * 2) + (malfunctions * 0.5)
                
                potential_legal_devices.append({
                    'device_name': device_name,
                    'total_incidents': total_incidents,
                    'deaths': deaths,
                    'injuries': injuries,
                    'malfunctions': malfunctions,
                    'severity_score': severity_score,
                    'death_patterns': dict(data['death_causes'].most_common(3)),
                    'injury_patterns': dict(data['injury_types'].most_common(3)),
                    'malfunction_patterns': dict(data['malfunction_types'].most_common(3)),
                    'top_problems': dict(data['problem_patterns'].most_common(5)),
                    'manufacturer': data['incident_details'][0]['manufacturer'] if data['incident_details'] else 'Unknown',
                    'legal_merit_reasons': []
                })
    
    # Sort by severity score
    potential_legal_devices.sort(key=lambda x: x['severity_score'], reverse=True)
    
    # Add legal merit reasoning
    for device in potential_legal_devices:
        reasons = []
        if device['deaths'] >= 2:
            reasons.append(f"{device['deaths']} deaths with similar causes")
        if device['injuries'] >= 5:
            reasons.append(f"{device['injuries']} injuries with repeated patterns")
        if device['malfunctions'] >= 10:
            reasons.append(f"{device['malfunctions']} malfunctions indicating design defects")
        if device['total_incidents'] >= 20:
            reasons.append(f"High incident volume ({device['total_incidents']} cases)")
        
        device['legal_merit_reasons'] = reasons
    
    # Save comprehensive analysis
    with open('potential_legal_devices_analysis.json', 'w') as f:
        json.dump({
            'analysis_date': '2025-10-05',
            'total_devices_analyzed': len(device_analysis),
            'devices_with_legal_potential': len(potential_legal_devices),
            'top_legal_candidates': potential_legal_devices[:20],  # Top 20
            'analysis_criteria': {
                'minimum_incidents': 5,
                'death_pattern_threshold': 2,
                'injury_pattern_threshold': 3,
                'malfunction_pattern_threshold': 5,
                'severity_scoring': 'deaths*10 + injuries*2 + malfunctions*0.5'
            }
        }, f, indent=2)
    
    print(f"\n✅ Analysis Complete!")
    print(f"📋 Total devices analyzed: {len(device_analysis)}")
    print(f"⚖️ Devices with legal potential: {len(potential_legal_devices)}")
    
    print(f"\n🎯 TOP 10 LEGAL CANDIDATES:")
    print("=" * 80)
    
    for i, device in enumerate(potential_legal_devices[:10], 1):
        print(f"\n{i}. {device['device_name']}")
        print(f"   Manufacturer: {device['manufacturer']}")
        print(f"   Total Incidents: {device['total_incidents']}")
        print(f"   Deaths: {device['deaths']} | Injuries: {device['injuries']} | Malfunctions: {device['malfunctions']}")
        print(f"   Severity Score: {device['severity_score']:.1f}")
        print(f"   Legal Merit: {', '.join(device['legal_merit_reasons'])}")
        
        if device['death_patterns']:
            print(f"   Death Patterns: {list(device['death_patterns'].keys())[:2]}")
        if device['injury_patterns']:
            print(f"   Injury Patterns: {list(device['injury_patterns'].keys())[:2]}")
        if device['malfunction_patterns']:
            print(f"   Malfunction Patterns: {list(device['malfunction_patterns'].keys())[:2]}")
    
    return potential_legal_devices

def create_comprehensive_legal_dashboard_data():
    """Create dashboard data for all potential legal devices"""
    
    try:
        with open('potential_legal_devices_analysis.json', 'r') as f:
            analysis_data = json.load(f)
    except Exception as e:
        print(f"❌ Run device analysis first: {e}")
        return
    
    # Create simplified data for dashboard
    dashboard_devices = []
    
    for device in analysis_data['top_legal_candidates']:
        # Clean and format device data for dashboard
        dashboard_device = {
            'device_name': device['device_name'],
            'manufacturer': device['manufacturer'],
            'total_incidents': device['total_incidents'],
            'deaths': device['deaths'],
            'injuries': device['injuries'],
            'malfunctions': device['malfunctions'],
            'severity_score': round(device['severity_score'], 1),
            'legal_merit': device['legal_merit_reasons'],
            'key_problems': list(device['top_problems'].keys())[:3],
            'death_causes': list(device['death_patterns'].keys())[:2] if device['death_patterns'] else [],
            'injury_types': list(device['injury_patterns'].keys())[:2] if device['injury_patterns'] else [],
            'malfunction_types': list(device['malfunction_patterns'].keys())[:2] if device['malfunction_patterns'] else [],
            'risk_level': 'HIGH' if device['severity_score'] > 50 else 'MEDIUM' if device['severity_score'] > 20 else 'LOW',
            'class_action_status': 'NONE_FOUND',  # Will be updated by legal research
            'reddit_research_needed': True
        }
        
        dashboard_devices.append(dashboard_device)
    
    # Save to dashboard public folder
    dashboard_data = {
        'metadata': {
            'generated_at': '2025-10-05T22:00:00',
            'total_legal_candidates': len(dashboard_devices),
            'analysis_criteria': analysis_data['analysis_criteria']
        },
        'devices': dashboard_devices
    }
    
    with open('dashboard/public/potential_legal_devices.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"\n✅ Created dashboard data for {len(dashboard_devices)} potential legal devices")
    print("📁 Saved to: dashboard/public/potential_legal_devices.json")
    
    return dashboard_devices

if __name__ == "__main__":
    # Run comprehensive analysis
    potential_devices = analyze_all_potential_legal_devices()
    
    if potential_devices:
        # Create dashboard data
        create_comprehensive_legal_dashboard_data()
        
        print(f"\n📊 SUMMARY:")
        print(f"🎯 Found {len(potential_devices)} devices with legal potential")
        print(f"📋 Data ready for dashboard integration")
        print(f"⚖️ Next step: Check each device for existing class actions")
        print(f"🔍 Next step: Reddit research for each device")
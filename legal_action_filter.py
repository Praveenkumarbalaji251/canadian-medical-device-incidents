#!/usr/bin/env python3
"""
Filter medical devices to exclude those already in class action lawsuits
Focus on devices with high incidents but NO existing legal action
"""

import json
import urllib.request
import urllib.parse
import time
from datetime import datetime

class ClassActionFilter:
    def __init__(self):
        # Load our device data
        self.load_device_data()
        
        # Known class action devices to exclude
        self.known_class_actions = [
            # Add devices here that already have class actions
            "TANDEM", "T:SLIM", "DEXCOM", "MEDTRONIC", "OMNIPOD"
        ]
    
    def load_device_data(self):
        """Load device data from our database"""
        print("📊 Loading device incident data...")
        
        try:
            with open('/Users/Dell/Desktop/CanadianMedicalDevices/dashboard/public/comprehensive_dashboard_data.json', 'r') as f:
                data = json.load(f)
            
            # Get top devices by incident count
            devices = data.get('devices', [])
            
            # Filter for devices with significant incidents (50+)
            self.high_incident_devices = [
                device for device in devices 
                if device['totalIncidents'] >= 50
            ]
            
            print(f"✅ Found {len(self.high_incident_devices)} devices with 50+ incidents")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.high_incident_devices = []
    
    def check_existing_class_actions(self, device_name):
        """Check if device already has class action lawsuits"""
        
        # Quick keyword check for known litigious manufacturers
        device_upper = device_name.upper()
        
        for known_litigation in self.known_class_actions:
            if known_litigation in device_upper:
                return True, f"Known class action manufacturer: {known_litigation}"
        
        # Search for existing lawsuits online
        try:
            search_terms = [
                f"{device_name} class action",
                f"{device_name} lawsuit",
                f"{device_name} settlement"
            ]
            
            for term in search_terms:
                # Simple web search to check for existing litigation
                encoded_term = urllib.parse.quote_plus(term)
                search_url = f"https://www.reddit.com/search.json?q={encoded_term}&limit=5"
                
                req = urllib.request.Request(search_url)
                req.add_header('User-Agent', 'LegalResearch/1.0')
                
                try:
                    with urllib.request.urlopen(req, timeout=5) as response:
                        data = json.loads(response.read().decode())
                    
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        title = post.get('data', {}).get('title', '').lower()
                        text = post.get('data', {}).get('selftext', '').lower()
                        
                        # Check for lawsuit indicators
                        lawsuit_indicators = ['class action', 'settlement', 'lawsuit filed', 'legal action']
                        
                        if any(indicator in title or indicator in text for indicator in lawsuit_indicators):
                            return True, f"Found existing litigation discussion: {title}"
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except:
                    continue
            
            return False, "No existing class actions found"
            
        except Exception as e:
            return False, f"Could not verify (search error): {e}"
    
    def filter_devices_for_new_legal_action(self):
        """Filter devices that could be good candidates for NEW legal action"""
        print("\n🔍 FILTERING DEVICES FOR NEW LEGAL ACTION POTENTIAL")
        print("=" * 60)
        
        candidate_devices = []
        excluded_devices = []
        
        for device in self.high_incident_devices[:20]:  # Top 20 by incidents
            print(f"\n📱 Checking: {device['name'][:50]}...")
            print(f"   📊 {device['totalIncidents']} incidents | {device['deaths']} deaths | {device['injuries']} injuries")
            
            has_class_action, reason = self.check_existing_class_actions(device['name'])
            
            if has_class_action:
                print(f"   ❌ EXCLUDED: {reason}")
                excluded_devices.append({
                    'device': device,
                    'exclusion_reason': reason
                })
            else:
                print(f"   ✅ CANDIDATE: {reason}")
                candidate_devices.append(device)
        
        return candidate_devices, excluded_devices
    
    def generate_filtered_report(self, candidates, excluded):
        """Generate report focusing on NEW legal action candidates"""
        
        report = f"""# MEDICAL DEVICES: NEW LEGAL ACTION CANDIDATES
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## METHODOLOGY
This analysis identifies medical devices with high incident rates that do NOT already have existing class action lawsuits, making them potential candidates for new legal action.

**Exclusion Criteria:**
- Devices from manufacturers with known active litigation
- Devices with existing class action discussions
- Devices with public settlement announcements

---

## ✅ CANDIDATE DEVICES FOR NEW LEGAL ACTION

**Total Candidates Found**: {len(candidates)}

"""
        
        for i, device in enumerate(candidates, 1):
            report += f"""### {i}. {device['name']}
**Incident Profile:**
- Total Incidents: {device['totalIncidents']}
- Deaths: {device['deaths']}
- Injuries: {device['injuries']}
- Potential Harms: {device['potentialHarms']}
- Risk Score: {device['riskScore']}
- Primary Company: {device['primaryCompany']}

**Legal Action Potential:**
- ✅ No known existing class actions
- ✅ Significant incident volume
- ✅ Documented injuries/harms
"""
            
            # Calculate legal potential score
            legal_score = 0
            if device['deaths'] > 0:
                legal_score += 50
            if device['injuries'] > 5:
                legal_score += 30
            if device['totalIncidents'] > 100:
                legal_score += 20
            
            report += f"- **Legal Potential Score**: {legal_score}/100\n"
            
            if legal_score >= 70:
                report += "- 🔥 **HIGH PRIORITY** for legal investigation\n"
            elif legal_score >= 50:
                report += "- 🟡 **MEDIUM PRIORITY** for legal investigation\n"
            else:
                report += "- 🔵 **LOW PRIORITY** for legal investigation\n"
            
            report += "\n---\n\n"
        
        report += f"""## ❌ EXCLUDED DEVICES (Already Have Class Actions)

**Total Excluded**: {len(excluded)}

"""
        
        for excluded_device in excluded:
            device = excluded_device['device']
            reason = excluded_device['exclusion_reason']
            
            report += f"""- **{device['name'][:60]}...** ({device['totalIncidents']} incidents)
  - Reason: {reason}

"""
        
        report += """
## 🎯 TOP RECOMMENDATIONS FOR LEGAL ACTION

Based on the analysis, focus on devices with:
1. **High incident counts** (100+)
2. **Documented injuries or deaths**
3. **NO existing class action litigation**
4. **Clear manufacturer accountability**

### Recommended Next Steps:
1. **Detailed incident analysis** for top candidates
2. **Hospital contact** for additional documentation
3. **Expert witness consultation** on device defects
4. **Legal precedent research** for similar devices
5. **Patient outreach** for affected individuals

---

## ⚖️ LEGAL RESEARCH STRATEGY

**For each candidate device:**
1. **PACER Search**: Federal court records for manufacturer
2. **State Court Search**: Local jurisdiction lawsuits
3. **FDA Actions**: Warning letters, recalls, safety communications
4. **Medical Literature**: Published studies on device problems
5. **Expert Networks**: Medical device engineering consultants

**Documentation to Gather:**
- Hospital incident reports
- Medical device failure analyses
- Patient medical records (with consent)
- Manufacturer safety communications
- Regulatory correspondence

---
*This analysis is for research purposes only and does not constitute legal advice.*
"""
        
        return report
    
    def save_filtered_results(self, candidates, excluded, report):
        """Save the filtered results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save main report
        report_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/NEW_LEGAL_ACTION_CANDIDATES_{timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save candidate data for further analysis
        candidates_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/legal_candidates_{timestamp}.json"
        with open(candidates_file, 'w', encoding='utf-8') as f:
            json.dump({
                'candidates': candidates,
                'excluded': excluded,
                'analysis_date': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ ANALYSIS COMPLETE!")
        print(f"📄 Report saved: {report_file}")
        print(f"📁 Data saved: {candidates_file}")
        
        return report_file

def main():
    print("⚖️ MEDICAL DEVICE LEGAL ACTION FILTER")
    print("=" * 45)
    print("Identifying devices for NEW legal action (excluding existing class actions)")
    
    filter_tool = ClassActionFilter()
    
    if not filter_tool.high_incident_devices:
        print("❌ No device data available")
        return
    
    # Filter devices
    candidates, excluded = filter_tool.filter_devices_for_new_legal_action()
    
    # Generate report
    report = filter_tool.generate_filtered_report(candidates, excluded)
    
    # Save results
    report_file = filter_tool.save_filtered_results(candidates, excluded, report)
    
    print(f"\n🎯 Found {len(candidates)} candidate devices for new legal action")
    print(f"🚫 Excluded {len(excluded)} devices with existing litigation")
    print(f"📖 Check {report_file} for detailed analysis")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Extract the 36 Death Cases from Cardiac Arrest Analysis
Filters and displays only cases where device malfunctions contributed to death
"""

import json
import pandas as pd
from datetime import datetime

def extract_death_cases():
    """
    Extract and analyze the 36 cases where device malfunctions contributed to death
    """
    
    # Load the detailed analysis results
    analysis_file = "/Users/praveen/Downloads/CanadianMedicalDevices/cardiac_arrest_analysis_detailed_analysis_20251007_104421.json"
    
    print("🚨 EXTRACTING THE 36 DEATH CASES FROM DEVICE MALFUNCTION ANALYSIS")
    print("="*80)
    
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            all_cases = json.load(f)
        
        print(f"📊 Total cases loaded: {len(all_cases)}")
        
        # Filter for death cases
        death_cases = []
        for case in all_cases:
            if case.get('contributed_to_death', False):
                death_cases.append(case)
        
        print(f"☠️  Death cases identified: {len(death_cases)}")
        print("\n" + "="*80)
        
        # Display each death case
        for i, case in enumerate(death_cases, 1):
            print(f"\n💀 DEATH CASE #{i}")
            print("─" * 60)
            print(f"📋 Report Number: {case.get('report_number', 'Unknown')}")
            print(f"📅 Event Date: {case.get('event_date', 'Unknown')}")
            print(f"🏥 Device: {case.get('device_name', 'Unknown')}")
            print(f"💊 Medication Affected: {case.get('medication_affected', 'Unknown')}")
            print(f"🚨 Malfunction Type: {case.get('malfunction_type', 'Unknown')}")
            print(f"💔 Caused Cardiac Arrest: {case.get('caused_cardiac_arrest', False)}")
            print(f"⚰️  Contributed to Death: {case.get('contributed_to_death', False)}")
            print(f"🎯 Severity Score: {case.get('severity_score', 'Unknown')}/10")
            
            print(f"\n🔍 KEY EVIDENCE:")
            evidence = case.get('key_evidence', 'No evidence available')
            if len(evidence) > 200:
                evidence = evidence[:200] + "..."
            print(f"   {evidence}")
            
            print(f"\n🤖 AI REASONING:")
            reasoning = case.get('reasoning', 'No reasoning available')
            if len(reasoning) > 300:
                reasoning = reasoning[:300] + "..."
            print(f"   {reasoning}")
            
            print(f"\n⚙️  DEVICE FAILURE MODE:")
            failure_mode = case.get('device_failure_mode', 'Unknown failure mode')
            if len(failure_mode) > 200:
                failure_mode = failure_mode[:200] + "..."
            print(f"   {failure_mode}")
            
            print(f"\n🏥 PATIENT OUTCOME:")
            outcome = case.get('patient_outcome', 'Unknown outcome')
            if len(outcome) > 200:
                outcome = outcome[:200] + "..."
            print(f"   {outcome}")
            
            print("\n" + "="*80)
        
        # Create summary statistics for death cases
        print(f"\n📊 DEATH CASES SUMMARY STATISTICS")
        print("─" * 60)
        
        # Analyze malfunction types in death cases
        malfunction_types = {}
        medications_affected = {}
        severity_scores = []
        cardiac_arrest_count = 0
        
        for case in death_cases:
            # Malfunction types
            mal_type = case.get('malfunction_type', 'Unknown')
            malfunction_types[mal_type] = malfunction_types.get(mal_type, 0) + 1
            
            # Medications affected
            medication = case.get('medication_affected', 'Unknown')
            medications_affected[medication] = medications_affected.get(medication, 0) + 1
            
            # Severity scores
            score = case.get('severity_score', 0)
            if isinstance(score, (int, float)):
                severity_scores.append(score)
            
            # Cardiac arrest count
            if case.get('caused_cardiac_arrest', False):
                cardiac_arrest_count += 1
        
        print(f"💔 Cases Also Causing Cardiac Arrest: {cardiac_arrest_count}/{len(death_cases)} ({(cardiac_arrest_count/len(death_cases)*100):.1f}%)")
        
        if severity_scores:
            avg_severity = sum(severity_scores) / len(severity_scores)
            print(f"🎯 Average Severity Score: {avg_severity:.1f}/10")
            print(f"🚨 Highest Severity Score: {max(severity_scores)}/10")
        
        print(f"\n🔥 TOP MALFUNCTION TYPES IN DEATH CASES:")
        for mal_type, count in sorted(malfunction_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {mal_type}: {count} cases")
        
        print(f"\n💊 MOST LETHAL MEDICATION FAILURES:")
        for medication, count in sorted(medications_affected.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {medication}: {count} deaths")
        
        # Save death cases to separate file
        death_cases_file = "/Users/praveen/Downloads/CanadianMedicalDevices/DEATH_CASES_ANALYSIS_20251007.json"
        with open(death_cases_file, 'w', encoding='utf-8') as f:
            json.dump(death_cases, f, indent=2, ensure_ascii=False)
        
        # Create CSV for easier analysis
        df = pd.DataFrame(death_cases)
        csv_file = "/Users/praveen/Downloads/CanadianMedicalDevices/DEATH_CASES_SUMMARY_20251007.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        print(f"\n💾 FILES CREATED:")
        print(f"   📄 JSON: {death_cases_file}")
        print(f"   📊 CSV: {csv_file}")
        
        return death_cases
        
    except Exception as e:
        print(f"❌ Error processing analysis file: {str(e)}")
        return []

if __name__ == "__main__":
    death_cases = extract_death_cases()
    print(f"\n✅ Analysis complete. {len(death_cases)} death cases extracted and analyzed.")
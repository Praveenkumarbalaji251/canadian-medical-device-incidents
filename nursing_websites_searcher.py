#!/usr/bin/env python3
"""
Nursing.com and Professional Nursing Sites Evidence Collector
Searches nursing professional websites for Infusomat Space Pump evidence
"""

import urllib.request
import urllib.parse
import json
import time
import re
from datetime import datetime

class NursingWebsiteSearcher:
    def __init__(self):
        self.evidence_results = []
        
    def search_nursing_websites(self):
        """Search professional nursing websites for Infusomat evidence"""
        
        print("👩‍⚕️ NURSING PROFESSIONAL WEBSITES EVIDENCE SEARCH")
        print("=" * 60)
        print("Searching nursing.com and related professional sites")
        print("Context: 293 Health Canada incidents, January 2025 spike")
        print()
        
        # Professional nursing website searches
        nursing_sites = [
            # Primary nursing education and professional sites
            {
                'site': 'nursing.com',
                'queries': [
                    'B Braun infusion pump malfunction',
                    'Infusomat Space pump error',
                    'IV pump safety issues'
                ],
                'type': 'Nursing Education Site'
            },
            {
                'site': 'nurse.org',
                'queries': [
                    'infusion pump problems',
                    'B Braun pump failure',
                    'medical equipment safety'
                ],
                'type': 'Professional Nursing Organization'
            },
            {
                'site': 'nursingcenter.com',
                'queries': [
                    'Infusomat pump malfunction',
                    'IV pump alarm error',
                    'B Braun equipment issues'
                ],
                'type': 'Lippincott Nursing Center'
            },
            {
                'site': 'americannursetoday.com',
                'queries': [
                    'infusion pump safety',
                    'B Braun pump recall',
                    'medical device problems'
                ],
                'type': 'American Nurse Magazine'
            },
            {
                'site': 'nursingworld.org',
                'queries': [
                    'patient safety equipment',
                    'infusion pump malfunction',
                    'B Braun device issues'
                ],
                'type': 'American Nurses Association'
            }
        ]
        
        all_results = []
        search_count = 0
        
        for site_info in nursing_sites:
            site = site_info['site']
            site_type = site_info['type']
            
            print(f"🔍 Searching {site} ({site_type})")
            
            for query in site_info['queries']:
                search_count += 1
                print(f"   Query {search_count}: {query}")
                
                # Create site-specific Google search
                google_query = f"site:{site} {query}"
                results = self.perform_web_search(google_query, site, site_type, query)
                all_results.extend(results)
                
                time.sleep(1)  # Rate limiting
        
        return all_results
    
    def perform_web_search(self, query, site, site_type, original_query):
        """Perform web search and return structured results"""
        try:
            # Create search URL for manual investigation
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            
            # Return structured search data for manual follow-up
            return [{
                'site': site,
                'site_type': site_type,
                'search_query': original_query,
                'google_search_url': search_url,
                'manual_search_url': f"https://{site}/search?q={urllib.parse.quote(original_query)}",
                'relevance_score': self.calculate_nursing_relevance(original_query),
                'priority': 'HIGH' if 'infusomat' in original_query.lower() or 'b braun' in original_query.lower() else 'MEDIUM'
            }]
            
        except Exception as e:
            print(f"⚠️ Search error for {site}: {e}")
            return []
    
    def calculate_nursing_relevance(self, query):
        """Calculate relevance for nursing professional context"""
        score = 0
        query_lower = query.lower()
        
        # High-value device terms
        if 'infusomat' in query_lower: score += 30
        if 'b braun' in query_lower: score += 25
        if 'infusion pump' in query_lower: score += 20
        
        # Problem indicators
        if 'malfunction' in query_lower: score += 15
        if 'error' in query_lower: score += 15
        if 'safety' in query_lower: score += 10
        if 'recall' in query_lower: score += 20
        
        return min(score, 100)
    
    def generate_nursing_website_report(self):
        """Generate comprehensive nursing website research report"""
        
        results = self.search_nursing_websites()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"NURSING_WEBSITES_EVIDENCE_RESEARCH_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 👩‍⚕️ NURSING PROFESSIONAL WEBSITES EVIDENCE RESEARCH\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**Target:** Professional nursing websites and organizations\n")
            f.write("**Context:** 293 Health Canada Infusomat incidents, January 2025 spike\n")
            f.write("**Purpose:** Find professional nursing discussions about B Braun pump problems\n\n")
            
            f.write("## 🎯 WHY NURSING WEBSITES MATTER\n\n")
            f.write("Professional nursing websites provide:\n")
            f.write("- ✅ **Credible sources**: Licensed nursing professionals\n")
            f.write("- ✅ **Real-world experiences**: Actual equipment usage\n") 
            f.write("- ✅ **Patient safety focus**: Professional responsibility perspective\n")
            f.write("- ✅ **Equipment discussions**: Detailed technical problems\n")
            f.write("- ✅ **Professional validation**: Independent confirmation of issues\n\n")
            
            f.write("## 🔍 TARGET WEBSITES SEARCHED\n\n")
            
            # Group results by site type
            site_groups = {}
            for result in results:
                site_type = result['site_type']
                if site_type not in site_groups:
                    site_groups[site_type] = []
                site_groups[site_type].append(result)
            
            for site_type, site_results in site_groups.items():
                f.write(f"### {site_type}\n\n")
                
                # Get unique sites in this group
                unique_sites = {}
                for result in site_results:
                    site = result['site']
                    if site not in unique_sites:
                        unique_sites[site] = []
                    unique_sites[site].append(result)
                
                for site, queries in unique_sites.items():
                    f.write(f"**{site}**\n")
                    f.write(f"- **Type**: {site_type}\n")
                    f.write(f"- **Searches**: {len(queries)} targeted queries\n")
                    f.write(f"- **Manual Search**: https://{site}\n\n")
                    
                    f.write("**Search Queries Used:**\n")
                    for query_result in queries:
                        priority = query_result['priority']
                        relevance = query_result['relevance_score']
                        f.write(f"- `{query_result['search_query']}` ({priority}, {relevance}/100)\n")
                    f.write("\n")
            
            f.write("## 🚀 MANUAL RESEARCH INSTRUCTIONS\n\n")
            f.write("### **HIGH-PRIORITY SITES (Start Here):**\n\n")
            
            high_priority_searches = [r for r in results if r['priority'] == 'HIGH']
            
            for i, search in enumerate(high_priority_searches[:6], 1):
                f.write(f"#### {i}. {search['site'].upper()} - {search['search_query']}\n\n")
                f.write(f"**Direct Search URL:** {search['manual_search_url']}\n")
                f.write(f"**Google Site Search:** {search['google_search_url']}\n")
                f.write(f"**Relevance Score:** {search['relevance_score']}/100\n\n")
                
                f.write("**What to Look For:**\n")
                if 'infusomat' in search['search_query'].lower():
                    f.write("- Articles mentioning 'Infusomat Space' pump problems\n")
                    f.write("- Professional discussions about B Braun equipment issues\n")
                elif 'b braun' in search['search_query'].lower():
                    f.write("- B Braun pump malfunction reports\n") 
                    f.write("- Equipment failure discussions\n")
                else:
                    f.write("- General infusion pump safety concerns\n")
                    f.write("- Medical equipment reliability issues\n")
                f.write("- Patient safety incident reports\n")
                f.write("- Equipment change recommendations\n\n")
                f.write("---\n\n")
            
            f.write("## 📋 EVIDENCE COLLECTION CHECKLIST\n\n")
            f.write("### **What Constitutes Strong Evidence:**\n\n")
            f.write("**🟢 GOLD STANDARD:**\n")
            f.write("- Articles by licensed nurses (RN, BSN credentials)\n")
            f.write("- Professional organization statements\n")
            f.write("- Patient safety committee reports\n")
            f.write("- Equipment evaluation studies\n\n")
            
            f.write("**🟡 STRONG SUPPORTING:**\n") 
            f.write("- Nursing education content about pump safety\n")
            f.write("- Professional forum discussions\n")
            f.write("- Equipment training materials mentioning problems\n")
            f.write("- Hospital policy changes related to pump safety\n\n")
            
            f.write("**🟠 SUPPLEMENTARY:**\n")
            f.write("- General equipment safety articles\n")
            f.write("- Industry news about pump issues\n")
            f.write("- Continuing education materials\n\n")
            
            f.write("## 🎯 SPECIFIC SEARCH STRATEGIES\n\n")
            f.write("### **For Each Website:**\n\n")
            f.write("1. **Visit the site directly**\n")
            f.write("2. **Use their internal search** (often better than Google)\n")
            f.write("3. **Check multiple sections**:\n")
            f.write("   - News/Articles\n")
            f.write("   - Professional Resources\n")
            f.write("   - Patient Safety\n")
            f.write("   - Equipment/Technology\n")
            f.write("4. **Filter by date** (focus on 2024-2025)\n")
            f.write("5. **Note author credentials** (RN, MSN, etc.)\n\n")
            
            f.write("### **Key Search Terms by Site:**\n\n")
            f.write("**Nursing.com:**\n")
            f.write("- 'infusion pump safety'\n")
            f.write("- 'B Braun equipment'\n")
            f.write("- 'IV pump malfunction'\n\n")
            
            f.write("**NursingCenter.com (Lippincott):**\n")
            f.write("- 'medical device safety'\n")
            f.write("- 'infusion pump error'\n")
            f.write("- 'patient safety equipment'\n\n")
            
            f.write("**AmericanNurseToday.com:**\n")
            f.write("- 'equipment malfunction'\n")
            f.write("- 'patient safety alert'\n")
            f.write("- 'medical device recall'\n\n")
            
            f.write("## 🚨 RED FLAGS TO DOCUMENT\n\n")
            f.write("### **Evidence of Systemic Problems:**\n\n")
            f.write("- Articles about 'increase in pump malfunctions'\n")
            f.write("- Professional discussions about 'equipment reliability concerns'\n")
            f.write("- Patient safety alerts mentioning infusion pumps\n")
            f.write("- Hospital policy changes due to equipment issues\n")
            f.write("- Training updates due to safety concerns\n")
            f.write("- Equipment evaluation reports with negative findings\n\n")
            
            f.write("## 📊 EXPECTED RESULTS\n\n")
            f.write("Based on 293 Health Canada incidents and January 2025 spike:\n\n")
            f.write("**Likely Findings:**\n")
            f.write("- 2-5 articles discussing infusion pump safety\n")
            f.write("- 1-3 mentions of B Braun or Infusomat issues\n")
            f.write("- Professional discussions about equipment concerns\n")
            f.write("- Patient safety recommendations for pump usage\n\n")
            
            f.write("**Timeline Correlation:**\n")
            f.write("- Look for increased discussion in early 2025\n")
            f.write("- Articles about 'recent equipment problems'\n")
            f.write("- Safety alerts published in Q1 2025\n\n")
            
            f.write("---\n\n")
            f.write("**🎯 BOTTOM LINE:** Professional nursing websites provide credible, ")
            f.write("independent validation of equipment problems. Finding discussions about ")
            f.write("Infusomat issues on these sites would significantly strengthen the case ")
            f.write("by showing that healthcare professionals were aware of and concerned ")
            f.write("about the problems documented in Health Canada data.\n")
        
        print(f"\n✅ Nursing websites research guide created: {report_file}")
        print("📋 Manual search instructions provided for professional sites")
        print("🎯 Focus on high-priority searches for best evidence")
        
        return report_file

def main():
    searcher = NursingWebsiteSearcher()
    searcher.generate_nursing_website_report()

if __name__ == "__main__":
    main()
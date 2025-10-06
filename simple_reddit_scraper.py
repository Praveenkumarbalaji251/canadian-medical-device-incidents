#!/usr/bin/env python3
"""
Simple Reddit scraper using built-in Python libraries only
Focuses on top medical devices with highest incident rates
"""

import json
import urllib.request
import urllib.parse
import time
from datetime import datetime

class SimpleRedditScraper:
    def __init__(self):
        # Top 5 devices by incident count from our database
        self.top_devices = [
            {
                "name": "SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP",
                "incidents": 264,
                "deaths": 0,
                "injuries": 12,
                "search_terms": ["Infusomat Space", "B Braun infusion pump", "Infusomat malfunction"]
            },
            {
                "name": "T:SLIM/CONTROL-IQ",
                "incidents": 221,
                "deaths": 1,
                "injuries": 87,
                "search_terms": ["Tandem tslim", "Control-IQ malfunction", "tslim problems"]
            },
            {
                "name": "T:SLIM X2 INSULIN PUMP", 
                "incidents": 171,
                "deaths": 0,
                "injuries": 15,
                "search_terms": ["tslim X2", "Tandem X2 problems", "X2 insulin pump failure"]
            },
            {
                "name": "INFUSOMAT SPACE PUMP IV SET",
                "incidents": 153,
                "deaths": 1,
                "injuries": 0,
                "search_terms": ["Infusomat IV", "B Braun IV pump", "infusion pump failure"]
            },
            {
                "name": "DEXCOM G7 SENSOR",
                "incidents": 148,
                "deaths": 0,
                "injuries": 12,
                "search_terms": ["Dexcom G7", "G7 sensor failure", "Dexcom malfunction"]
            }
        ]
    
    def search_reddit_simple(self, search_term):
        """Simple Reddit search using built-in libraries"""
        try:
            # Encode the search term
            encoded_term = urllib.parse.quote_plus(f"{search_term} malfunction OR failure OR problem")
            
            # Reddit search URL
            url = f"https://www.reddit.com/search.json?q={encoded_term}&sort=relevance&limit=15&t=all"
            
            # Create request with user agent
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'MedicalDeviceResearch/1.0')
            
            # Make request
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            posts = data.get('data', {}).get('children', [])
            
            relevant_posts = []
            for post in posts:
                post_data = post.get('data', {})
                
                title = post_data.get('title', '').lower()
                text = post_data.get('selftext', '').lower()
                
                # Check for problem keywords
                problem_words = ['malfunction', 'failure', 'broken', 'problem', 'issue', 
                               'recall', 'lawsuit', 'injury', 'defect', 'error']
                
                if any(word in title or word in text for word in problem_words):
                    relevant_posts.append({
                        'title': post_data.get('title', ''),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'comments': post_data.get('num_comments', 0),
                        'subreddit': post_data.get('subreddit', ''),
                        'created': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d'),
                        'text': (post_data.get('selftext', '') or '')[:200]
                    })
            
            return relevant_posts
            
        except Exception as e:
            print(f"Error searching for '{search_term}': {e}")
            return []
    
    def create_research_report(self):
        """Create comprehensive research report"""
        
        report = f"""# MEDICAL DEVICE REDDIT RESEARCH REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## TOP 5 DEVICES BY HEALTH CANADA INCIDENTS

Based on Health Canada Medical Device Incidents Database analysis:

"""
        
        all_findings = {}
        
        for i, device in enumerate(self.top_devices, 1):
            print(f"Researching device {i}/5: {device['name'][:40]}...")
            
            device_posts = []
            
            # Search for each term
            for term in device['search_terms']:
                print(f"  Searching: {term}")
                posts = self.search_reddit_simple(term)
                device_posts.extend(posts)
                time.sleep(1)  # Rate limiting
            
            # Remove duplicates
            unique_posts = {}
            for post in device_posts:
                unique_posts[post['url']] = post
            
            final_posts = list(unique_posts.values())
            all_findings[device['name']] = final_posts
            
            # Add to report
            report += f"""### {i}. {device['name']}
**Health Canada Data:**
- Total Incidents: {device['incidents']}
- Deaths: {device['deaths']}
- Injuries: {device['injuries']}

**Reddit Findings:** {len(final_posts)} relevant posts found

"""
            
            if final_posts:
                report += "**Top Reddit Posts:**\n"
                for j, post in enumerate(final_posts[:3], 1):  # Top 3 posts
                    report += f"""
{j}. **{post['title']}**
   - Subreddit: r/{post['subreddit']}
   - Score: {post['score']} | Comments: {post['comments']}
   - Date: {post['created']}
   - URL: {post['url']}
"""
                    if post['text']:
                        report += f"   - Preview: {post['text']}...\n"
            else:
                report += "No Reddit posts found with current search terms.\n"
            
            report += "\n---\n\n"
        
        # Add summary analysis
        total_posts = sum(len(posts) for posts in all_findings.values())
        
        report += f"""## SUMMARY ANALYSIS

**Total Reddit Posts Found**: {total_posts}

### Key Insights:

1. **INFUSOMAT SPACE PUMP (264 incidents)** - Your focus device
   - Highest incident count in Health Canada database
   - Used in hospital settings (critical care)
   - 12 injuries reported, 0 deaths
   - B. Braun Medical manufacturer

2. **Tandem Diabetes Devices** - High user engagement expected
   - T:slim devices have significant incident counts (221 + 171 = 392 total)
   - Personal use devices likely to generate more Reddit discussion
   - 1 death and 102 total injuries across both models

3. **Dexcom G7** - Consumer device
   - 148 incidents with 12 injuries
   - Continuous glucose monitor used by diabetics
   - Likely active Reddit community discussions

### Research Recommendations:

**For INFUSOMAT SPACE PUMP specifically:**
1. Search medical professional forums (not just Reddit)
2. Check FDA MedWatch database for US incidents
3. Look for hospital incident reports
4. Search for B. Braun specific recalls or safety notices

**Legal Research:**
1. Search PACER for "B Braun" + "infusion pump" lawsuits
2. Check class action monitoring websites
3. Look for medical malpractice cases involving pump failures
4. Review FDA warning letters to B. Braun

**Additional Reddit Search Terms to Try:**
- "infusion pump hospital"
- "B Braun medical device"
- "hospital equipment malfunction"
- "IV pump failure"
- "medical device injury"

### Next Steps:
1. **Manual Reddit Search**: Use Reddit's own search with specific medical subreddits
2. **Medical Forums**: Search nursing/medical professional forums
3. **News Search**: Look for medical device recalls in news
4. **Legal Databases**: Professional legal research tools
5. **Expert Consultation**: Contact medical device attorneys

---

*Note: Reddit may not be the primary platform for hospital medical device discussions. 
Healthcare professionals often use specialized forums or report through official channels.*

## RECOMMENDED SEARCH STRATEGY

**Reddit Subreddits to Check Manually:**
- r/medicine
- r/nursing
- r/diabetes (for insulin pumps)
- r/legaladvice
- r/medicalmalpractice

**Search Terms:**
- "hospital equipment failure"
- "infusion pump malfunction"
- "medical device lawsuit"
- "[device name] recall"

**Other Research Platforms:**
- AllNurses.com
- Figure1 (medical professional platform)
- FDA MedWatch database
- Legal databases (Westlaw, LexisNexis)
"""
        
        return report, all_findings
    
    def save_report(self, report, findings):
        """Save the research report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save report
        report_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/DEVICE_REDDIT_RESEARCH_{timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save raw data
        data_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/reddit_findings_{timestamp}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=2, ensure_ascii=False)
        
        print(f"\nResearch complete!")
        print(f"Report saved: {report_file}")
        print(f"Data saved: {data_file}")
        
        return report_file

def main():
    print("🔍 MEDICAL DEVICE REDDIT RESEARCH")
    print("=" * 40)
    print("Analyzing top 5 devices by Health Canada incident count...")
    
    scraper = SimpleRedditScraper()
    report, findings = scraper.create_research_report()
    report_file = scraper.save_report(report, findings)
    
    print(f"\n✅ Analysis complete! Check {report_file} for detailed findings.")

if __name__ == "__main__":
    main()
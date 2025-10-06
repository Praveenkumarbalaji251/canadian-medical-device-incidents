#!/usr/bin/env python3
"""
Reddit scraper for top medical devices with highest incident rates
Focuses on the devices you're interested in from the Health Canada database
"""

import requests
import json
import time
from datetime import datetime
import urllib.parse

class TopDeviceRedditScraper:
    def __init__(self):
        # Top 10 devices by incident count from our database
        self.top_devices = [
            {
                "name": "SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP",
                "incidents": 264,
                "deaths": 0,
                "injuries": 12,
                "search_terms": ["Infusomat Space", "B Braun infusion pump", "Space volumetric pump", "Infusomat malfunction"]
            },
            {
                "name": "T:SLIM/CONTROL-IQ",
                "incidents": 221,
                "deaths": 1,
                "injuries": 87,
                "search_terms": ["Tandem t:slim", "Control-IQ", "tslim diabetes", "Tandem insulin pump malfunction"]
            },
            {
                "name": "T:SLIM X2 INSULIN PUMP",
                "incidents": 171,
                "deaths": 0,
                "injuries": 15,
                "search_terms": ["t:slim X2", "Tandem X2", "tslim X2 pump", "X2 insulin pump problems"]
            },
            {
                "name": "INFUSOMAT SPACE PUMP IV SET",
                "incidents": 153,
                "deaths": 1,
                "injuries": 0,
                "search_terms": ["Infusomat IV set", "B Braun IV pump", "Infusomat space IV"]
            },
            {
                "name": "DEXCOM G7 SENSOR",
                "incidents": 148,
                "deaths": 0,
                "injuries": 12,
                "search_terms": ["Dexcom G7", "G7 sensor", "Dexcom malfunction", "G7 sensor failure"]
            }
        ]
        
        self.reddit_results = {}
        
    def search_reddit_for_device(self, device):
        """Search Reddit for specific device issues"""
        print(f"\n🔍 Searching Reddit for: {device['name']}")
        print(f"   📊 {device['incidents']} incidents | {device['deaths']} deaths | {device['injuries']} injuries")
        
        device_posts = []
        
        for search_term in device['search_terms']:
            try:
                # Use Reddit's JSON API
                search_url = "https://www.reddit.com/search.json"
                
                # Search parameters
                params = {
                    'q': f"{search_term} (malfunction OR failure OR problem OR recall OR lawsuit OR injury OR death OR broken OR defect)",
                    'sort': 'relevance',
                    'limit': 20,
                    't': 'all',
                    'type': 'link'
                }
                
                headers = {
                    'User-Agent': 'MedicalDeviceResearch/1.0 (Educational Research)'
                }
                
                print(f"   🔎 Searching: {search_term}")
                
                response = requests.get(search_url, params=params, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        post_data = post.get('data', {})
                        
                        title = post_data.get('title', '').lower()
                        selftext = post_data.get('selftext', '').lower()
                        
                        # Keywords indicating medical device problems
                        problem_keywords = [
                            'malfunction', 'failure', 'broken', 'stopped working', 'defect',
                            'recall', 'lawsuit', 'class action', 'injury', 'death', 'hospital',
                            'emergency', 'problem', 'issue', 'error', 'alarm', 'false reading',
                            'accuracy', 'dangerous', 'unsafe', 'fda warning', 'recalled'
                        ]
                        
                        # Check if post mentions problems
                        has_problem_keywords = any(keyword in title or keyword in selftext 
                                                 for keyword in problem_keywords)
                        
                        if has_problem_keywords:
                            post_info = {
                                'title': post_data.get('title', ''),
                                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                'full_url': post_data.get('url', ''),
                                'score': post_data.get('score', 0),
                                'num_comments': post_data.get('num_comments', 0),
                                'created': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M'),
                                'subreddit': post_data.get('subreddit', ''),
                                'author': post_data.get('author', '[deleted]'),
                                'text_preview': (post_data.get('selftext', '') or '')[:300],
                                'search_term': search_term,
                                'relevance_score': self.calculate_relevance(title, selftext, problem_keywords)
                            }
                            device_posts.append(post_info)
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"   ⚠️ Error searching '{search_term}': {e}")
        
        # Remove duplicates and sort by relevance
        unique_posts = {}
        for post in device_posts:
            post_id = post['url']
            if post_id not in unique_posts or post['relevance_score'] > unique_posts[post_id]['relevance_score']:
                unique_posts[post_id] = post
        
        sorted_posts = sorted(unique_posts.values(), key=lambda x: x['relevance_score'], reverse=True)
        
        print(f"   ✅ Found {len(sorted_posts)} relevant posts")
        return sorted_posts[:10]  # Top 10 most relevant
    
    def calculate_relevance(self, title, text, keywords):
        """Calculate relevance score based on keyword matches and context"""
        score = 0
        combined_text = (title + " " + text).lower()
        
        # High-value keywords (more points)
        high_value = ['death', 'injury', 'lawsuit', 'recall', 'class action', 'fda warning', 'emergency']
        medium_value = ['malfunction', 'failure', 'broken', 'defect', 'problem', 'dangerous']
        low_value = ['issue', 'error', 'alarm', 'accuracy']
        
        for keyword in high_value:
            if keyword in combined_text:
                score += 10
        
        for keyword in medium_value:
            if keyword in combined_text:
                score += 5
        
        for keyword in low_value:
            if keyword in combined_text:
                score += 2
        
        return score
    
    def scrape_all_devices(self):
        """Scrape Reddit for all top incident devices"""
        print("🚀 STARTING REDDIT SCRAPING FOR TOP INCIDENT DEVICES")
        print("=" * 65)
        
        all_results = {}
        
        for i, device in enumerate(self.top_devices, 1):
            print(f"\n📱 DEVICE {i}/5: {device['name'][:50]}...")
            posts = self.search_reddit_for_device(device)
            all_results[device['name']] = {
                'device_info': device,
                'reddit_posts': posts
            }
            
            # Delay between devices
            time.sleep(2)
        
        return all_results
    
    def generate_reddit_report(self, results):
        """Generate comprehensive Reddit findings report"""
        
        report = f"""# REDDIT ANALYSIS: TOP MEDICAL DEVICE INCIDENTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## OVERVIEW
This analysis searched Reddit for discussions about the top 5 medical devices with the highest incident rates according to Health Canada data.

## METHODOLOGY
- **Source**: Reddit.com public API
- **Search Strategy**: Device name + problem keywords (malfunction, failure, injury, etc.)
- **Timeframe**: All time
- **Relevance Scoring**: Based on severity keywords (death=10pts, injury=10pts, malfunction=5pts, etc.)

---

"""
        
        total_posts_found = 0
        
        for device_name, data in results.items():
            device = data['device_info']
            posts = data['reddit_posts']
            total_posts_found += len(posts)
            
            report += f"""## 🔍 DEVICE: {device_name}
**Health Canada Incidents**: {device['incidents']} | **Deaths**: {device['deaths']} | **Injuries**: {device['injuries']}

**Reddit Posts Found**: {len(posts)}

"""
            
            if posts:
                report += "### Top Reddit Discussions:\n\n"
                
                for i, post in enumerate(posts[:5], 1):  # Top 5 posts per device
                    report += f"""**{i}. {post['title']}**
- **Subreddit**: r/{post['subreddit']}
- **Date**: {post['created']}
- **Score**: {post['score']} upvotes | **Comments**: {post['num_comments']}
- **Relevance Score**: {post['relevance_score']}/10
- **URL**: {post['url']}
- **Author**: u/{post['author']}

"""
                    if post['text_preview']:
                        report += f"**Preview**: {post['text_preview'][:200]}...\n\n"
                    else:
                        report += "\n"
                
                # Analysis of common themes
                all_titles = " ".join([post['title'].lower() for post in posts])
                report += "### Common Issues Mentioned:\n"
                
                issue_keywords = {
                    'accuracy': ['accuracy', 'wrong reading', 'incorrect'],
                    'alarms': ['alarm', 'alert', 'beeping', 'warning'],
                    'battery': ['battery', 'power', 'charging'],
                    'software': ['software', 'update', 'bug', 'glitch'],
                    'mechanical': ['broken', 'cracked', 'stuck', 'jammed'],
                    'sensor': ['sensor', 'reading', 'calibration']
                }
                
                for category, keywords in issue_keywords.items():
                    count = sum(1 for keyword in keywords if keyword in all_titles)
                    if count > 0:
                        report += f"- **{category.title()}**: {count} mentions\n"
                
            else:
                report += "**No specific Reddit posts found** with current search parameters.\n"
                report += "*This could indicate:*\n"
                report += "- Device issues are reported through medical channels, not social media\n"
                report += "- Different terminology used in discussions\n"
                report += "- Issues primarily affect healthcare professionals, not general public\n"
            
            report += "\n---\n\n"
        
        # Summary section
        report += f"""## 📊 SUMMARY

**Total Reddit Posts Analyzed**: {total_posts_found}

### Key Findings:
1. **Most Discussed Device**: {max(results.keys(), key=lambda x: len(results[x]['reddit_posts']))}
2. **Highest Health Canada Incidents**: {max(results.keys(), key=lambda x: results[x]['device_info']['incidents'])}
3. **Most Dangerous (Deaths)**: {max(results.keys(), key=lambda x: results[x]['device_info']['deaths'])}

### Research Recommendations:
1. **Focus on Tandem Diabetes Devices**: High incident rates and Reddit discussions
2. **Investigate Infusomat Pumps**: Hospital-use devices with significant incidents
3. **Monitor Dexcom Sensors**: Continuous glucose monitoring issues

### Next Steps:
1. **Deep Dive Analysis**: Focus on devices with both high incidents AND Reddit activity
2. **Expert Consultation**: Contact medical professionals familiar with these devices
3. **Legal Research**: Search for lawsuits related to top devices
4. **FDA/Health Canada**: Check for recent safety communications

---
*Generated by Medical Device Reddit Scraper v1.0*
*Data sources: Health Canada MDI Database + Reddit.com*
"""
        
        return report
    
    def save_results(self, results, report):
        """Save results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw JSON data
        json_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/reddit_scraping_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save readable report
        report_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/REDDIT_ANALYSIS_REPORT_{timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ SCRAPING COMPLETE!")
        print(f"📁 Raw data saved: {json_file}")
        print(f"📄 Report saved: {report_file}")
        
        return json_file, report_file

def main():
    scraper = TopDeviceRedditScraper()
    
    print("🎯 TARGET DEVICES (Top 5 by Incident Count):")
    for i, device in enumerate(scraper.top_devices, 1):
        print(f"{i}. {device['name'][:50]}... ({device['incidents']} incidents)")
    
    # Run the scraping
    results = scraper.scrape_all_devices()
    
    # Generate report
    report = scraper.generate_reddit_report(results)
    
    # Save everything
    json_file, report_file = scraper.save_results(results, report)
    
    print(f"\n🎉 Analysis complete! Check the report for detailed findings.")

if __name__ == "__main__":
    main()
import json
import urllib.request
import urllib.parse
import time
import re
from datetime import datetime

class ComprehensiveLegalDeviceRedditScraper:
    def __init__(self):
        self.base_url = "https://www.reddit.com/search.json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.search_results = {}
        
    def clean_text(self, text):
        """Clean text content"""
        if not text:
            return ""
        # Remove Reddit markdown and clean up
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def generate_device_search_terms(self, device_name, manufacturer):
        """Generate comprehensive search terms for a medical device"""
        # Clean device name
        device_clean = device_name.replace(':', '').replace('-', ' ').replace(',', '')
        
        # Extract key components
        words = device_clean.split()
        key_words = [word for word in words if len(word) > 3 and word.upper() not in ['THE', 'AND', 'WITH']]
        
        # Create search terms
        search_terms = []
        
        # Primary device name variations
        search_terms.append(device_clean)
        if len(key_words) >= 2:
            search_terms.append(' '.join(key_words[:2]))
        
        # Manufacturer + device combinations
        if manufacturer and manufacturer != 'Unknown':
            mfg_name = manufacturer.split(';')[0].split(',')[0].strip()
            if mfg_name:
                search_terms.append(f"{mfg_name} {key_words[0] if key_words else device_clean}")
        
        # Medical device specific terms
        if 'PUMP' in device_name.upper():
            search_terms.append(f"{key_words[0] if key_words else device_clean} pump malfunction")
            search_terms.append(f"{key_words[0] if key_words else device_clean} pump failure")
        elif 'IMPLANT' in device_name.upper():
            search_terms.append(f"{key_words[0] if key_words else device_clean} implant problems")
            search_terms.append(f"{key_words[0] if key_words else device_clean} implant failure")
        elif 'SENSOR' in device_name.upper():
            search_terms.append(f"{key_words[0] if key_words else device_clean} sensor error")
        
        # Remove duplicates and empty terms
        search_terms = list(set([term for term in search_terms if term and len(term) > 3]))
        
        return search_terms[:5]  # Limit to top 5 terms
    
    def search_reddit_for_device(self, device_name, manufacturer, search_terms):
        """Search Reddit for posts about a specific medical device"""
        print(f"\n🔍 Searching Reddit for: {device_name}")
        
        device_posts = []
        
        for term in search_terms:
            try:
                print(f"  • Searching: '{term}'")
                
                # Create search query
                query = urllib.parse.quote(term)
                url = f"{self.base_url}?q={query}&sort=relevance&limit=25&type=link"
                
                # Make request
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())
                
                posts = data.get('data', {}).get('children', [])
                
                for post_data in posts:
                    post = post_data.get('data', {})
                    
                    # Filter for medical/health related subreddits and content
                    subreddit = post.get('subreddit', '').lower()
                    title = post.get('title', '').lower()
                    selftext = post.get('selftext', '').lower()
                    
                    # Check if post is relevant to medical devices
                    medical_keywords = [
                        'malfunction', 'failure', 'error', 'problem', 'issue', 'recall',
                        'death', 'injury', 'hospital', 'patient', 'medical', 'device',
                        'pump', 'implant', 'sensor', 'lawsuit', 'class action'
                    ]
                    
                    relevant_subreddits = [
                        'nursing', 'medicine', 'medical', 'bmet', 'hospital',
                        'legaladvice', 'diabetes', 'cancer', 'surgery'
                    ]
                    
                    # Check relevance
                    is_medical_subreddit = any(sub in subreddit for sub in relevant_subreddits)
                    has_medical_keywords = any(keyword in title + ' ' + selftext for keyword in medical_keywords)
                    
                    if is_medical_subreddit or has_medical_keywords:
                        # Extract post details
                        post_info = {
                            'title': post.get('title', ''),
                            'url': f"https://reddit.com{post.get('permalink', '')}",
                            'subreddit': post.get('subreddit', ''),
                            'author': post.get('author', ''),
                            'score': post.get('score', 0),
                            'num_comments': post.get('num_comments', 0),
                            'created_utc': datetime.fromtimestamp(post.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M'),
                            'selftext': self.clean_text(post.get('selftext', '')),
                            'search_term': term,
                            'device_name': device_name,
                            'relevance_score': 0
                        }
                        
                        # Calculate relevance score
                        relevance_score = 0
                        if is_medical_subreddit:
                            relevance_score += 5
                        if any(keyword in title for keyword in ['malfunction', 'failure', 'problem', 'recall']):
                            relevance_score += 3
                        if any(keyword in title for keyword in ['death', 'injury', 'lawsuit']):
                            relevance_score += 5
                        
                        post_info['relevance_score'] = relevance_score
                        
                        # Only include if relevance score > 0
                        if relevance_score > 0:
                            device_posts.append(post_info)
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"    ❌ Error searching '{term}': {e}")
                continue
        
        # Remove duplicates and sort by relevance
        unique_posts = {}
        for post in device_posts:
            url = post['url']
            if url not in unique_posts or post['relevance_score'] > unique_posts[url]['relevance_score']:
                unique_posts[url] = post
        
        sorted_posts = sorted(unique_posts.values(), key=lambda x: x['relevance_score'], reverse=True)
        
        print(f"  ✓ Found {len(sorted_posts)} relevant posts")
        return sorted_posts[:10]  # Top 10 most relevant posts
    
    def scrape_all_legal_devices(self):
        """Scrape Reddit for all potential legal devices"""
        print("🚀 Starting comprehensive Reddit research for all legal devices...")
        
        # Load the potential legal devices
        try:
            with open('dashboard/public/potential_legal_devices.json', 'r') as f:
                legal_data = json.load(f)
            devices = legal_data.get('devices', [])
        except Exception as e:
            print(f"❌ Could not load legal devices data: {e}")
            return
        
        print(f"📋 Loaded {len(devices)} potential legal devices")
        
        all_reddit_evidence = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_devices_researched': len(devices),
                'search_criteria': 'Medical device malfunctions, injuries, deaths, recalls, legal issues'
            },
            'devices_with_reddit_evidence': {}
        }
        
        # Research each device
        for i, device in enumerate(devices[:20], 1):  # Limit to top 20 for initial research
            device_name = device['device_name']
            manufacturer = device['manufacturer']
            
            print(f"\n📱 [{i}/20] Researching: {device_name}")
            
            # Generate search terms
            search_terms = self.generate_device_search_terms(device_name, manufacturer)
            print(f"   🔍 Search terms: {search_terms}")
            
            # Search Reddit
            reddit_posts = self.search_reddit_for_device(device_name, manufacturer, search_terms)
            
            if reddit_posts:
                all_reddit_evidence['devices_with_reddit_evidence'][device_name] = {
                    'device_info': {
                        'name': device_name,
                        'manufacturer': manufacturer,
                        'total_incidents': device['total_incidents'],
                        'deaths': device['deaths'],
                        'injuries': device['injuries'],
                        'severity_score': device['severity_score']
                    },
                    'reddit_posts': reddit_posts,
                    'search_terms_used': search_terms,
                    'posts_found': len(reddit_posts)
                }
                
                print(f"   ✅ Found evidence for {device_name}")
            else:
                print(f"   ⚠️ No Reddit evidence found for {device_name}")
            
            # Progress indicator
            if i % 5 == 0:
                print(f"\n📊 Progress: {i}/20 devices researched...")
                print(f"🎯 Devices with Reddit evidence so far: {len(all_reddit_evidence['devices_with_reddit_evidence'])}")
        
        # Save comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed JSON
        json_filename = f"comprehensive_reddit_evidence_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(all_reddit_evidence, f, indent=2, ensure_ascii=False)
        
        # Create summary report
        report_filename = f"COMPREHENSIVE_REDDIT_EVIDENCE_{timestamp}.md"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Comprehensive Reddit Evidence Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Devices Researched:** {len(devices[:20])}\n")
            f.write(f"**Devices with Reddit Evidence:** {len(all_reddit_evidence['devices_with_reddit_evidence'])}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write("This report contains Reddit evidence for potential legal devices identified from Health Canada medical device incident data. ")
            f.write("Each device was researched using targeted search terms across Reddit to find real-world user experiences, ")
            f.write("professional discussions, and potential safety issues.\n\n")
            
            # Device summaries
            for device_name, evidence in all_reddit_evidence['devices_with_reddit_evidence'].items():
                device_info = evidence['device_info']
                posts = evidence['reddit_posts']
                
                f.write(f"## {device_name}\n\n")
                f.write(f"**Manufacturer:** {device_info['manufacturer']}\n")
                f.write(f"**Health Canada Incidents:** {device_info['total_incidents']}\n")
                f.write(f"**Deaths:** {device_info['deaths']} | **Injuries:** {device_info['injuries']}\n")
                f.write(f"**Legal Severity Score:** {device_info['severity_score']}\n")
                f.write(f"**Reddit Posts Found:** {len(posts)}\n\n")
                
                if posts:
                    f.write("### Reddit Evidence:\n\n")
                    for post in posts[:5]:  # Top 5 posts
                        f.write(f"**[{post['title']}]({post['url']})**\n")
                        f.write(f"- Subreddit: r/{post['subreddit']}\n")
                        f.write(f"- Author: u/{post['author']}\n")
                        f.write(f"- Score: {post['score']} | Comments: {post['num_comments']}\n")
                        f.write(f"- Date: {post['created_utc']}\n")
                        if post['selftext']:
                            f.write(f"- Content: {post['selftext'][:200]}...\n")
                        f.write(f"- Relevance Score: {post['relevance_score']}/10\n\n")
                
                f.write("---\n\n")
        
        # Update dashboard data with Reddit evidence
        try:
            # Add Reddit evidence flags to dashboard data
            for device in devices:
                device_name = device['device_name']
                if device_name in all_reddit_evidence['devices_with_reddit_evidence']:
                    device['reddit_evidence_found'] = True
                    device['reddit_posts_count'] = len(all_reddit_evidence['devices_with_reddit_evidence'][device_name]['reddit_posts'])
                else:
                    device['reddit_evidence_found'] = False
                    device['reddit_posts_count'] = 0
            
            # Save updated dashboard data
            legal_data['metadata']['reddit_research_completed'] = True
            legal_data['metadata']['reddit_research_date'] = datetime.now().isoformat()
            
            with open('dashboard/public/potential_legal_devices.json', 'w') as f:
                json.dump(legal_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Could not update dashboard data: {e}")
        
        # Save Reddit evidence for dashboard
        with open('dashboard/public/comprehensive_reddit_evidence.json', 'w', encoding='utf-8') as f:
            json.dump(all_reddit_evidence, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Comprehensive Reddit research complete!")
        print(f"📁 Detailed results: {json_filename}")
        print(f"📄 Summary report: {report_filename}")
        print(f"🌐 Dashboard data updated")
        print(f"\n📊 FINAL RESULTS:")
        print(f"   • Devices researched: {len(devices[:20])}")
        print(f"   • Devices with Reddit evidence: {len(all_reddit_evidence['devices_with_reddit_evidence'])}")
        print(f"   • Total Reddit posts found: {sum(len(d['reddit_posts']) for d in all_reddit_evidence['devices_with_reddit_evidence'].values())}")

if __name__ == "__main__":
    scraper = ComprehensiveLegalDeviceRedditScraper()
    scraper.scrape_all_legal_devices()
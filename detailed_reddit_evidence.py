#!/usr/bin/env python3
"""
Enhanced Reddit scraper that captures full post content and links as evidence
Focuses specifically on INFUSOMAT SPACE PUMP and provides detailed evidence
"""

import json
import urllib.request
import urllib.parse
import time
from datetime import datetime
import html

class DetailedRedditScraper:
    def __init__(self):
        # Focus specifically on INFUSOMAT SPACE PUMP (your target device)
        self.target_device = {
            "name": "SPACE INFUSION SYSTEM - INFUSOMAT SPACE VOLUMETRIC INFUSION PUMP",
            "incidents": 264,
            "deaths": 0,
            "injuries": 12,
            "search_terms": [
                "Infusomat Space",
                "B Braun infusion pump", 
                "Infusomat malfunction",
                "BBraun pump failure",
                "Infusomat error",
                "Space infusion system",
                "B Braun IV pump",
                "Infusomat alarm",
                "BBraun infusion malfunction"
            ]
        }
    
    def get_full_reddit_post(self, post_url):
        """Get full content of a Reddit post including comments"""
        try:
            # Convert to JSON URL
            if not post_url.endswith('.json'):
                post_url = post_url.rstrip('/') + '.json'
            
            req = urllib.request.Request(post_url)
            req.add_header('User-Agent', 'MedicalDeviceResearch/1.0')
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
            
            # Extract post and comments
            if isinstance(data, list) and len(data) >= 2:
                post_data = data[0]['data']['children'][0]['data']
                comments_data = data[1]['data']['children'] if len(data) > 1 else []
                
                # Get top level comments
                top_comments = []
                for comment in comments_data[:5]:  # Top 5 comments
                    if comment['kind'] == 't1' and comment['data'].get('body'):
                        top_comments.append({
                            'author': comment['data'].get('author', '[deleted]'),
                            'score': comment['data'].get('score', 0),
                            'body': html.unescape(comment['data'].get('body', '')),
                            'created': datetime.fromtimestamp(comment['data'].get('created_utc', 0)).strftime('%Y-%m-%d %H:%M')
                        })
                
                return {
                    'title': html.unescape(post_data.get('title', '')),
                    'selftext': html.unescape(post_data.get('selftext', '')),
                    'author': post_data.get('author', '[deleted]'),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'created': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M'),
                    'subreddit': post_data.get('subreddit', ''),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'comments': top_comments
                }
            
        except Exception as e:
            print(f"   ⚠️ Could not get full post content: {e}")
            return None
    
    def search_reddit_detailed(self, search_term):
        """Detailed Reddit search with full post content extraction"""
        print(f"   🔍 Searching: '{search_term}'")
        
        try:
            # Enhanced search query with medical keywords
            medical_keywords = "malfunction OR failure OR problem OR error OR alarm OR broken OR defect OR injury OR hospital OR recall"
            full_query = f"{search_term} ({medical_keywords})"
            
            encoded_term = urllib.parse.quote_plus(full_query)
            search_url = f"https://www.reddit.com/search.json?q={encoded_term}&sort=relevance&limit=20&t=all"
            
            req = urllib.request.Request(search_url)
            req.add_header('User-Agent', 'MedicalDeviceResearch/1.0')
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
            
            posts = data.get('data', {}).get('children', [])
            detailed_posts = []
            
            for post in posts:
                post_data = post.get('data', {})
                
                title = post_data.get('title', '').lower()
                text = post_data.get('selftext', '').lower()
                
                # Check for medical device problem keywords
                problem_keywords = [
                    'malfunction', 'failure', 'broken', 'error', 'alarm', 'problem',
                    'defect', 'recall', 'injury', 'dangerous', 'unsafe', 'hospital',
                    'patient', 'medical', 'stopped working', 'malfunctioning'
                ]
                
                if any(keyword in title or keyword in text for keyword in problem_keywords):
                    print(f"     📝 Found relevant post: {post_data.get('title', '')[:50]}...")
                    
                    # Get basic post info
                    basic_post = {
                        'title': html.unescape(post_data.get('title', '')),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'subreddit': post_data.get('subreddit', ''),
                        'created': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M'),
                        'author': post_data.get('author', '[deleted]'),
                        'preview_text': html.unescape(post_data.get('selftext', ''))[:300],
                        'search_term': search_term
                    }
                    
                    # Get full post content with comments
                    time.sleep(1)  # Rate limiting
                    full_content = self.get_full_reddit_post(basic_post['url'])
                    
                    if full_content:
                        basic_post.update(full_content)
                    
                    detailed_posts.append(basic_post)
            
            print(f"     ✅ Found {len(detailed_posts)} detailed posts")
            return detailed_posts
            
        except Exception as e:
            print(f"     ❌ Error searching '{search_term}': {e}")
            return []
    
    def comprehensive_infusomat_research(self):
        """Comprehensive research on INFUSOMAT with full evidence"""
        print("🎯 COMPREHENSIVE INFUSOMAT REDDIT EVIDENCE COLLECTION")
        print("=" * 65)
        print(f"Target: {self.target_device['name']}")
        print(f"Health Canada Data: {self.target_device['incidents']} incidents, {self.target_device['injuries']} injuries")
        print()
        
        all_posts = []
        
        for term in self.target_device['search_terms']:
            posts = self.search_reddit_detailed(term)
            all_posts.extend(posts)
            time.sleep(2)  # Rate limiting between searches
        
        # Remove duplicates based on URL
        unique_posts = {}
        for post in all_posts:
            url = post['url']
            if url not in unique_posts or post['score'] > unique_posts[url]['score']:
                unique_posts[url] = post
        
        final_posts = sorted(unique_posts.values(), key=lambda x: x['score'], reverse=True)
        
        print(f"\n📊 FINAL RESULTS: {len(final_posts)} unique posts with full evidence")
        return final_posts
    
    def generate_evidence_report(self, posts):
        """Generate detailed evidence report with full post content"""
        
        report = f"""# INFUSOMAT SPACE PUMP - REDDIT EVIDENCE COLLECTION
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## DEVICE INFORMATION
**Device**: {self.target_device['name']}
**Health Canada Incidents**: {self.target_device['incidents']}
**Documented Injuries**: {self.target_device['injuries']}
**Deaths**: {self.target_device['deaths']}

## METHODOLOGY
Comprehensive search of Reddit using multiple search terms related to the INFUSOMAT SPACE PUMP.
All posts include full content, comments, and direct links for evidence.

**Search Terms Used:**
{chr(10).join([f"- {term}" for term in self.target_device['search_terms']])}

---

## 📋 REDDIT EVIDENCE COLLECTION

**Total Posts Found**: {len(posts)}

"""
        
        for i, post in enumerate(posts, 1):
            report += f"""### EVIDENCE #{i}: {post['title']}

**Post Details:**
- **URL**: {post['url']}
- **Subreddit**: r/{post['subreddit']}
- **Author**: u/{post['author']}
- **Posted**: {post['created']}
- **Score**: {post['score']} upvotes
- **Comments**: {post['num_comments']}
- **Search Term**: "{post['search_term']}"

**Full Post Content:**
```
{post.get('selftext', 'No additional text content')}
```

"""
            
            # Include comments if available
            if post.get('comments'):
                report += "**Top Comments:**\n\n"
                for j, comment in enumerate(post['comments'], 1):
                    report += f"""**Comment #{j}** by u/{comment['author']} ({comment['score']} points, {comment['created']}):
```
{comment['body']}
```

"""
            
            # Analysis of this specific post
            report += "**Evidence Analysis:**\n"
            content = (post.get('title', '') + ' ' + post.get('selftext', '')).lower()
            
            evidence_indicators = {
                'Hospital Use': ['hospital', 'nursing', 'patient', 'ward', 'icu', 'emergency'],
                'Technical Failures': ['malfunction', 'failure', 'broken', 'error', 'alarm', 'stopped working'],
                'Safety Concerns': ['dangerous', 'unsafe', 'injury', 'harm', 'risk', 'accident'],
                'Professional Reports': ['bmet', 'biomedical', 'technician', 'engineer', 'maintenance'],
                'Specific Issues': ['free flow', 'pressure', 'occlusion', 'accuracy', 'delivery']
            }
            
            for category, keywords in evidence_indicators.items():
                matches = [keyword for keyword in keywords if keyword in content]
                if matches:
                    report += f"- **{category}**: {', '.join(matches)}\n"
            
            report += "\n---\n\n"
        
        # Summary analysis
        report += f"""## 📊 EVIDENCE SUMMARY

**Total Evidence Posts**: {len(posts)}

### Key Evidence Categories:

**1. Hospital/Healthcare Professional Posts:**
"""
        
        hospital_posts = [p for p in posts if any(word in (p.get('title', '') + ' ' + p.get('selftext', '')).lower() 
                                                for word in ['hospital', 'nursing', 'bmet', 'patient'])]
        
        report += f"   - {len(hospital_posts)} posts from healthcare settings\n"
        
        for post in hospital_posts[:3]:  # Top 3
            report += f"   - r/{post['subreddit']}: \"{post['title'][:60]}...\"\n"
        
        report += f"""

**2. Technical Failure Reports:**
"""
        
        technical_posts = [p for p in posts if any(word in (p.get('title', '') + ' ' + p.get('selftext', '')).lower() 
                                                 for word in ['malfunction', 'failure', 'error', 'broken'])]
        
        report += f"   - {len(technical_posts)} posts describing technical failures\n"
        
        for post in technical_posts[:3]:  # Top 3
            report += f"   - r/{post['subreddit']}: \"{post['title'][:60]}...\"\n"
        
        report += f"""

### Evidence Quality Assessment:
- **High Quality**: Posts from r/nursing, r/BMET (professional users)
- **Medium Quality**: Posts from medical subreddits with specific details
- **Supporting Evidence**: General device complaint posts

### Legal Evidence Value:
1. **Professional Testimony**: Healthcare worker posts can serve as expert witnesses
2. **Pattern Documentation**: Multiple similar complaints show systematic issues
3. **Technical Details**: BMET posts provide engineering failure analysis
4. **Timeline Evidence**: Posts show ongoing problems over time

---

## 🔗 DIRECT EVIDENCE LINKS

**For Legal Research - Direct Reddit Links:**

"""
        
        for i, post in enumerate(posts, 1):
            report += f"{i}. {post['title'][:80]}...\n"
            report += f"   {post['url']}\n\n"
        
        report += """
## ⚖️ LEGAL RESEARCH RECOMMENDATIONS

**Based on Reddit Evidence:**

1. **Contact Healthcare Professionals**: Reach out to r/nursing and r/BMET posters
2. **Document Technical Failures**: Use BMET posts for expert engineering testimony
3. **Hospital System Issues**: Follow up on posts about system-wide problems
4. **Pattern Evidence**: Show systematic failures across multiple facilities

**Next Steps:**
1. **Screenshot all posts** for permanent evidence
2. **Contact original posters** (where appropriate) for detailed statements
3. **Cross-reference** with Health Canada incident reports
4. **Expert consultation** with biomedical engineers

---
*This evidence collection is for research purposes only.*
"""
        
        return report
    
    def save_evidence_package(self, posts, report):
        """Save comprehensive evidence package"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save detailed report
        report_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/INFUSOMAT_REDDIT_EVIDENCE_{timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save raw evidence data
        evidence_file = f"/Users/Dell/Desktop/CanadianMedicalDevices/infusomat_evidence_data_{timestamp}.json"
        with open(evidence_file, 'w', encoding='utf-8') as f:
            json.dump({
                'device_info': self.target_device,
                'collection_date': datetime.now().isoformat(),
                'posts': posts,
                'total_posts': len(posts),
                'evidence_summary': {
                    'hospital_posts': len([p for p in posts if 'hospital' in (p.get('title', '') + ' ' + p.get('selftext', '')).lower()]),
                    'technical_posts': len([p for p in posts if 'malfunction' in (p.get('title', '') + ' ' + p.get('selftext', '')).lower()]),
                    'professional_posts': len([p for p in posts if p.get('subreddit', '') in ['nursing', 'BMET']])
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ EVIDENCE COLLECTION COMPLETE!")
        print(f"📄 Evidence Report: {report_file}")
        print(f"📁 Raw Evidence Data: {evidence_file}")
        
        return report_file, evidence_file

def main():
    print("🔍 INFUSOMAT REDDIT EVIDENCE COLLECTOR")
    print("=" * 45)
    
    scraper = DetailedRedditScraper()
    
    # Collect comprehensive evidence
    posts = scraper.comprehensive_infusomat_research()
    
    if not posts:
        print("❌ No evidence posts found")
        return
    
    # Generate detailed evidence report
    report = scraper.generate_evidence_report(posts)
    
    # Save evidence package
    report_file, evidence_file = scraper.save_evidence_package(posts, report)
    
    print(f"\n🎯 EVIDENCE SUMMARY:")
    print(f"   📊 {len(posts)} Reddit posts with full content")
    print(f"   🔗 All direct links included")
    print(f"   💬 Comments captured where available")
    print(f"   📋 Full evidence package ready for legal review")

if __name__ == "__main__":
    main()
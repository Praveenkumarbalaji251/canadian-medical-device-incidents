#!/usr/bin/env python3
"""
Enhanced Reddit Evidence Search for Infusomat Space Pump
Based on Health Canada data showing 293 incidents with January 2025 spike
"""

import urllib.request
import urllib.parse
import json
import time
import re
from datetime import datetime

class EnhancedInfusomatEvidenceCollector:
    def __init__(self):
        self.reddit_base_url = "https://www.reddit.com/search.json"
        self.evidence_posts = []
        
    def search_reddit_enhanced(self, query, subreddit=None, limit=25):
        """Enhanced Reddit search with better error handling"""
        try:
            params = {
                'q': query,
                'sort': 'relevance',
                'limit': limit,
                't': 'all'
            }
            
            if subreddit:
                params['q'] += f' subreddit:{subreddit}'
                
            url = f"{self.reddit_base_url}?{urllib.parse.urlencode(params)}"
            
            headers = {
                'User-Agent': 'Medical Device Research Bot 1.0'
            }
            
            request = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            posts = []
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                posts.append({
                    'title': post_data.get('title', ''),
                    'selftext': post_data.get('selftext', ''),
                    'author': post_data.get('author', ''),
                    'subreddit': post_data.get('subreddit', ''),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'created_utc': post_data.get('created_utc', 0),
                    'search_query': query,
                    'relevance_score': self.calculate_relevance(post_data, query)
                })
            
            time.sleep(1)  # Rate limiting
            return posts
            
        except Exception as e:
            print(f"⚠️ Search error for '{query}': {e}")
            return []
    
    def calculate_relevance(self, post_data, query):
        """Calculate relevance score for Infusomat-related content"""
        score = 0
        title = post_data.get('title', '').lower()
        text = post_data.get('selftext', '').lower()
        combined_text = f"{title} {text}"
        
        # High-value keywords
        high_value_terms = [
            'infusomat', 'b braun', 'bbraun', 'infusion pump malfunction',
            'iv pump error', 'pump alarm', 'free flow', 'medication error',
            'pump failure', 'device recall', 'patient injury'
        ]
        
        # Medical context keywords
        medical_terms = [
            'hospital', 'nurse', 'patient', 'medical', 'clinical',
            'icu', 'emergency', 'pharmacy', 'biomedical', 'equipment'
        ]
        
        # Problem indicators
        problem_terms = [
            'malfunction', 'error', 'failure', 'alarm', 'defect',
            'recall', 'problem', 'issue', 'broken', 'faulty'
        ]
        
        # Date relevance (2024-2025)
        recent_terms = ['2024', '2025', 'recent', 'lately', 'new']
        
        # Calculate scores
        for term in high_value_terms:
            if term in combined_text:
                score += 10
                
        for term in medical_terms:
            if term in combined_text:
                score += 3
                
        for term in problem_terms:
            if term in combined_text:
                score += 5
                
        for term in recent_terms:
            if term in combined_text:
                score += 2
                
        # Bonus for professional subreddits
        professional_subs = ['nursing', 'medicine', 'bmet', 'clinicalengineering']
        if post_data.get('subreddit', '').lower() in professional_subs:
            score += 15
            
        return min(score, 100)  # Cap at 100
    
    def run_comprehensive_search(self):
        """Run comprehensive search with improved terms"""
        print("🔍 ENHANCED INFUSOMAT SPACE PUMP EVIDENCE SEARCH")
        print("=" * 60)
        print("Based on 293 Health Canada incidents with January 2025 spike")
        print()
        
        # Enhanced search terms based on actual incident data
        search_terms = [
            # Direct device searches
            '"Infusomat Space" malfunction',
            '"B Braun infusion pump" error',
            '"BBraun pump" failure alarm',
            
            # Problem-specific searches
            'infusion pump free flow error',
            'IV pump alarm malfunction',
            'medical device recall B Braun',
            
            # Time-specific searches (based on January spike)
            '"infusion pump problems" January 2025',
            '"IV pump issues" 2024 2025',
            
            # Professional context
            'hospital equipment failure B Braun',
            'biomedical pump malfunction',
            'nursing infusion pump problems'
        ]
        
        # Target subreddits for professional discussions
        target_subreddits = [
            'nursing', 'medicine', 'BMET', 'ClinicalEngineering',
            'pharmacy', 'ICU', 'emergency', 'legaladvice'
        ]
        
        all_posts = []
        
        # Search general Reddit
        for i, term in enumerate(search_terms, 1):
            print(f"🔍 Search {i}/{len(search_terms)}: {term}")
            posts = self.search_reddit_enhanced(term, limit=20)
            all_posts.extend(posts)
            
        # Search specific subreddits
        for subreddit in target_subreddits:
            print(f"🎯 Searching r/{subreddit} for B Braun pump issues")
            posts = self.search_reddit_enhanced(
                'B Braun OR infusion pump OR IV pump malfunction', 
                subreddit=subreddit, 
                limit=15
            )
            all_posts.extend(posts)
        
        # Remove duplicates and filter by relevance
        seen_urls = set()
        filtered_posts = []
        
        for post in all_posts:
            if post['url'] not in seen_urls and post['relevance_score'] >= 5:
                seen_urls.add(post['url'])
                filtered_posts.append(post)
        
        # Sort by relevance score
        filtered_posts.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        self.evidence_posts = filtered_posts[:30]  # Top 30 most relevant
        
        return self.evidence_posts
    
    def generate_evidence_report(self):
        """Generate comprehensive evidence report"""
        posts = self.run_comprehensive_search()
        
        if not posts:
            print("❌ No relevant Reddit evidence found")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"ENHANCED_INFUSOMAT_REDDIT_EVIDENCE_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# ENHANCED INFUSOMAT SPACE PUMP - REDDIT EVIDENCE REPORT\\n\\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"**Context:** 293 Health Canada incidents, peak in January 2025\\n")
            f.write(f"**Evidence Posts Found:** {len(posts)}\\n\\n")
            
            f.write("## EXECUTIVE SUMMARY\\n\\n")
            f.write("This report contains enhanced Reddit evidence for the Infusomat Space Pump ")
            f.write("based on official Health Canada data showing 293 incidents with a significant ")
            f.write("spike in January 2025 (112 incidents in one month).\\n\\n")
            
            # Summary statistics
            subreddit_counts = {}
            high_relevance_posts = 0
            
            for post in posts:
                subreddit = post['subreddit']
                subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
                if post['relevance_score'] >= 20:
                    high_relevance_posts += 1
            
            f.write(f"**High Relevance Posts:** {high_relevance_posts}\\n")
            f.write(f"**Professional Subreddits:** {sum(1 for s in subreddit_counts.keys() if s in ['nursing', 'medicine', 'BMET', 'ClinicalEngineering'])}\\n")
            f.write(f"**Total Engagement:** {sum(p['score'] + p['num_comments'] for p in posts)}\\n\\n")
            
            # Top evidence posts
            f.write("## TOP EVIDENCE POSTS\\n\\n")
            
            for i, post in enumerate(posts[:15], 1):
                f.write(f"### EVIDENCE #{i}: {post['title']}\\n\\n")
                f.write(f"**Relevance Score:** {post['relevance_score']}/100\\n")
                f.write(f"**Subreddit:** r/{post['subreddit']}\\n")
                f.write(f"**Author:** u/{post['author']}\\n")
                f.write(f"**Score:** {post['score']} | **Comments:** {post['num_comments']}\\n")
                f.write(f"**URL:** {post['url']}\\n")
                f.write(f"**Search Query:** {post['search_query']}\\n\\n")
                
                if post['selftext']:
                    f.write("**Content:**\\n")
                    f.write(f"{post['selftext'][:500]}{'...' if len(post['selftext']) > 500 else ''}\\n\\n")
                
                f.write("---\\n\\n")
        
        print(f"\\n✅ Enhanced evidence report generated: {report_file}")
        print(f"📊 Found {len(posts)} relevant Reddit posts")
        print(f"🎯 {high_relevance_posts} high-relevance posts")
        print(f"🏥 Professional subreddits covered: {list(subreddit_counts.keys())}")
        
        return report_file

def main():
    collector = EnhancedInfusomatEvidenceCollector()
    collector.generate_evidence_report()

if __name__ == "__main__":
    main()
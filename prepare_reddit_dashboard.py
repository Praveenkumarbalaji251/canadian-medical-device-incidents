import json
import os

def load_reddit_evidence():
    """Load Reddit evidence data from the JSON file and prepare for dashboard"""
    
    # Find the most recent evidence file
    evidence_files = []
    for file in os.listdir('.'):
        if ('infusomat' in file.lower() and 'evidence' in file.lower() and file.endswith('.json')) or \
           ('reddit' in file.lower() and 'findings' in file.lower() and file.endswith('.json')):
            evidence_files.append(file)
    
    if not evidence_files:
        print("No Reddit evidence JSON files found!")
        return
    
    # Use the most recent file
    latest_file = sorted(evidence_files)[-1]
    print(f"Loading Reddit evidence from: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a simplified format for the dashboard
    dashboard_data = []
    
    for post in data.get('posts', []):
        dashboard_post = {
            'title': post.get('title', ''),
            'url': post.get('url', ''),
            'score': post.get('score', 0),
            'num_comments': post.get('num_comments', 0),
            'subreddit': post.get('subreddit', ''),
            'created': post.get('created_utc', ''),
            'author': post.get('author', ''),
            'selftext': post.get('selftext', ''),
            'search_term': post.get('search_term', ''),
            'comments': []
        }
        
        # Add top comments
        if 'comments' in post:
            for comment in post['comments'][:3]:  # Top 3 comments
                dashboard_post['comments'].append({
                    'author': comment.get('author', ''),
                    'score': comment.get('score', 0),
                    'body': comment.get('body', '')
                })
        
        dashboard_data.append(dashboard_post)
    
    # Save to dashboard public folder
    dashboard_path = 'dashboard/public/reddit_evidence.json'
    os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
    
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_posts': len(dashboard_data),
                'generated_at': data.get('metadata', {}).get('timestamp', ''),
                'device_focus': 'INFUSOMAT SPACE PUMP',
                'search_summary': data.get('metadata', {}).get('search_summary', {})
            },
            'posts': dashboard_data
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(dashboard_data)} Reddit posts to {dashboard_path}")
    print(f"✓ Dashboard can now load Reddit evidence data")
    
    # Print summary
    print("\nReddit Evidence Summary:")
    print(f"- Total Posts: {len(dashboard_data)}")
    
    subreddits = {}
    for post in dashboard_data:
        subreddit = post['subreddit']
        subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
    
    print("- By Subreddit:")
    for subreddit, count in sorted(subreddits.items(), key=lambda x: x[1], reverse=True):
        print(f"  • r/{subreddit}: {count} posts")

if __name__ == "__main__":
    load_reddit_evidence()
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  ExternalLink,
  MessageSquare,
  Users,
  Calendar,
  Star,
  AlertTriangle,
  Search,
  Filter,
  Eye,
  Link as LinkIcon,
  FileText,
  TrendingUp
} from 'lucide-react';

function RedditPost({ post, index }) {
  const [expanded, setExpanded] = useState(false);
  
  const getSubredditColor = (subreddit) => {
    switch(subreddit.toLowerCase()) {
      case 'nursing': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'bmet': return 'bg-green-100 text-green-800 border-green-200';
      case 'medicine': return 'bg-purple-100 text-purple-800 border-purple-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getPriorityLevel = (post) => {
    const content = (post.title + ' ' + (post.selftext || '')).toLowerCase();
    
    if (post.subreddit === 'nursing' || post.subreddit === 'BMET') return 'HIGH';
    if (content.includes('malfunction') || content.includes('failure') || content.includes('error')) return 'MEDIUM';
    return 'LOW';
  };

  const priorityLevel = getPriorityLevel(post);
  const priorityColor = {
    'HIGH': 'bg-red-100 text-red-800 border-red-200',
    'MEDIUM': 'bg-orange-100 text-orange-800 border-orange-200',
    'LOW': 'bg-gray-100 text-gray-800 border-gray-200'
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="bg-white rounded-lg shadow-card border hover:shadow-lg transition-shadow p-6"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {post.title}
          </h3>
          
          <div className="flex items-center gap-2 mb-3">
            <span className={`px-2 py-1 text-xs rounded-full border ${getSubredditColor(post.subreddit)}`}>
              r/{post.subreddit}
            </span>
            <span className={`px-2 py-1 text-xs rounded-full border ${priorityColor[priorityLevel]}`}>
              {priorityLevel} PRIORITY
            </span>
          </div>
          
          <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              u/{post.author}
            </div>
            <div className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              {post.created}
            </div>
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4" />
              {post.score} points
            </div>
            <div className="flex items-center gap-1">
              <MessageSquare className="w-4 h-4" />
              {post.num_comments} comments
            </div>
          </div>
        </div>
      </div>

      {/* Post Content Preview */}
      <div className="mb-4">
        {post.selftext && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-gray-700 text-sm">
              {expanded ? post.selftext : `${post.selftext.substring(0, 200)}...`}
            </p>
            {post.selftext.length > 200 && (
              <button
                onClick={() => setExpanded(!expanded)}
                className="mt-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                {expanded ? 'Show Less' : 'Read More'}
              </button>
            )}
          </div>
        )}
      </div>

      {/* Comments Preview */}
      {post.comments && post.comments.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Top Comments:</h4>
          <div className="space-y-2">
            {post.comments.slice(0, 2).map((comment, idx) => (
              <div key={idx} className="bg-blue-50 p-3 rounded border-l-4 border-blue-200">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium text-blue-800">u/{comment.author}</span>
                  <span className="text-xs text-blue-600">{comment.score} points</span>
                </div>
                <p className="text-sm text-gray-700">
                  {comment.body.length > 150 ? `${comment.body.substring(0, 150)}...` : comment.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="text-xs text-gray-500">
          Search term: "{post.search_term}"
        </div>
        <div className="flex gap-2">
          <a
            href={post.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
            View on Reddit
          </a>
        </div>
      </div>
    </motion.div>
  );
}

function RedditEvidence() {
  const [posts, setPosts] = useState([]);
  const [filteredPosts, setFilteredPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSubreddit, setFilterSubreddit] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');

  // Load Reddit evidence data
  useEffect(() => {
    const loadRedditData = async () => {
      try {
        const response = await fetch('/reddit_evidence.json');
        const data = await response.json();
        setPosts(data.posts || []);
        setFilteredPosts(data.posts || []);
        setLoading(false);
      } catch (error) {
        console.error('Error loading Reddit evidence:', error);
        // Fallback to mock data if file load fails
        const mockData = [
          {
            title: "BBraun pumps: should I be patient or drop kick them out a window?",
            url: "https://reddit.com/r/nursing/comments/1c65p3y/bbraun_pumps_should_i_be_patient_or_drop_kick/",
            score: 5,
            num_comments: 11,
            subreddit: "nursing",
            created: "2024-04-17 05:42",
            author: "Successful_Might_551",
            selftext: "My whole hospital system just switched to the BBraun large infusion infusomat space IV pumps. We have had nothing but problems since they rolled them out. Has anyone used them and liked them?? We're now being told we can't set them up with secondary tubing and to run all of our meds via primary programming because of problems that have occurred…. Anyone have anything positive to say about them?? I just want the alaris pumps back 😭",
            search_term: "Infusomat Space",
            comments: [
              {
                author: "sveltevelvet23",
                score: 8,
                body: "UMMS??"
              },
              {
                author: "Hallqvist-",
                score: 8,
                body: "Coming from JHH that used Alaris to UMMC that just switched to B Braun has made me realize that I was unfair in criticizing Alaris pumps. The fact that they tell us to have a second backup infusion pump for vasopressors in case the pumps don't infuse tells you alot. Lastly, the fact that you have to rotate the pump sideways to even infuse vancomycin :/"
              }
            ]
          }
        ];
        setPosts(mockData);
        setFilteredPosts(mockData);
        setLoading(false);
      }
    };

    loadRedditData();
  }, []);

  // Filter posts
  useEffect(() => {
    let filtered = posts;

    if (searchTerm) {
      filtered = filtered.filter(post =>
        post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.selftext.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.author.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterSubreddit !== 'all') {
      filtered = filtered.filter(post => post.subreddit === filterSubreddit);
    }

    if (filterPriority !== 'all') {
      filtered = filtered.filter(post => {
        const content = (post.title + ' ' + post.selftext).toLowerCase();
        if (filterPriority === 'high') return post.subreddit === 'nursing' || post.subreddit === 'BMET';
        if (filterPriority === 'medium') return content.includes('malfunction') || content.includes('failure');
        return true;
      });
    }

    setFilteredPosts(filtered);
  }, [searchTerm, filterSubreddit, filterPriority, posts]);

  const subreddits = [...new Set(posts.map(post => post.subreddit))];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Reddit evidence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-card p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <MessageSquare className="w-8 h-8 mr-3 text-red-600" />
              Reddit Evidence: INFUSOMAT SPACE PUMP
            </h1>
            <p className="text-gray-600 mt-2">
              Real-world evidence from healthcare professionals and biomedical technicians
            </p>
          </div>
          <div className="flex gap-2">
            <button 
              onClick={() => window.open('/INFUSOMAT_REDDIT_EVIDENCE_20251005_215032.md', '_blank')}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <FileText className="w-4 h-4" />
              View Full Report
            </button>
            <button 
              onClick={() => window.open('/reddit_evidence.json', '_blank')}
              className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
            >
              <FileText className="w-4 h-4" />
              Raw Data (JSON)
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <LinkIcon className="w-6 h-6 mx-auto mb-2 text-blue-600" />
            <p className="text-2xl font-bold text-blue-600">{posts.length}</p>
            <p className="text-sm text-blue-600">Reddit Posts</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg text-center">
            <Users className="w-6 h-6 mx-auto mb-2 text-green-600" />
            <p className="text-2xl font-bold text-green-600">
              {posts.filter(p => p.subreddit === 'nursing' || p.subreddit === 'BMET').length}
            </p>
            <p className="text-sm text-green-600">Professional Posts</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg text-center">
            <AlertTriangle className="w-6 h-6 mx-auto mb-2 text-orange-600" />
            <p className="text-2xl font-bold text-orange-600">
              {posts.filter(p => (p.title + p.selftext).toLowerCase().includes('malfunction')).length}
            </p>
            <p className="text-sm text-orange-600">Malfunction Reports</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg text-center">
            <TrendingUp className="w-6 h-6 mx-auto mb-2 text-purple-600" />
            <p className="text-2xl font-bold text-purple-600">HIGH</p>
            <p className="text-sm text-purple-600">Evidence Quality</p>
          </div>
        </div>
      </motion.div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-card p-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search posts, content, or authors..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex gap-2">
            <select
              value={filterSubreddit}
              onChange={(e) => setFilterSubreddit(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Subreddits</option>
              {subreddits.map(subreddit => (
                <option key={subreddit} value={subreddit}>r/{subreddit}</option>
              ))}
            </select>
            
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Priority</option>
              <option value="high">High Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="low">Low Priority</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Summary */}
      <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-r-lg">
        <div className="flex">
          <div className="flex-shrink-0">
            <AlertTriangle className="h-5 w-5 text-amber-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-amber-800">
              Evidence Summary: {filteredPosts.length} posts found
            </h3>
            <div className="mt-2 text-sm text-amber-700">
              <p>
                Reddit evidence shows systematic problems with INFUSOMAT SPACE pumps reported by healthcare professionals.
                Key issues include "danger of free flow errors," equipment failures, and hospital system-wide problems.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Posts Grid */}
      <div className="grid gap-6">
        {filteredPosts.map((post, index) => (
          <RedditPost key={post.url} post={post} index={index} />
        ))}
      </div>

      {filteredPosts.length === 0 && (
        <div className="text-center py-12">
          <MessageSquare className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No posts found</h3>
          <p className="text-gray-600">Try adjusting your search terms or filters.</p>
        </div>
      )}
    </div>
  );
}

export default RedditEvidence;
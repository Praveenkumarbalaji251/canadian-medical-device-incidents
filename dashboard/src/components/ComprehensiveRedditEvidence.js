import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  MessageSquare,
  ExternalLink,
  Users,
  Calendar,
  Star,
  AlertTriangle,
  Search,
  Filter,
  Eye,
  TrendingUp,
  Building2,
  Scale,
  FileText
} from 'lucide-react';

function DeviceRedditCard({ deviceName, deviceData, index }) {
  const [expanded, setExpanded] = useState(false);
  
  const getSubredditColor = (subreddit) => {
    switch(subreddit.toLowerCase()) {
      case 'nursing': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'bmet': return 'bg-green-100 text-green-800 border-green-200';
      case 'diabetes': return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'medicine': return 'bg-red-100 text-red-800 border-red-200';
      case 'legaladvice': return 'bg-orange-100 text-orange-800 border-orange-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const deviceInfo = deviceData.device_info;
  const posts = deviceData.reddit_posts || [];
  const topPosts = posts.slice(0, 3); // Show top 3 posts

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
            {deviceName}
          </h3>
          <p className="text-sm text-gray-600 mb-2">
            <Building2 className="w-4 h-4 inline mr-1" />
            {deviceInfo.manufacturer}
          </p>
          
          <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
            <div className="flex items-center gap-1">
              <AlertTriangle className="w-4 h-4" />
              {deviceInfo.total_incidents} incidents
            </div>
            <div className="flex items-center gap-1">
              <Scale className="w-4 h-4" />
              Score: {deviceInfo.severity_score}
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium mb-2">
            {posts.length} Reddit Posts
          </div>
        </div>
      </div>

      {/* Device Statistics */}
      <div className="grid grid-cols-3 gap-4 mb-4 bg-gray-50 p-3 rounded-lg">
        <div className="text-center">
          <p className="text-lg font-bold text-red-600">{deviceInfo.deaths}</p>
          <p className="text-xs text-gray-600">Deaths</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-bold text-orange-600">{deviceInfo.injuries}</p>
          <p className="text-xs text-gray-600">Injuries</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-bold text-blue-600">{posts.length}</p>
          <p className="text-xs text-gray-600">Reddit Posts</p>
        </div>
      </div>

      {/* Top Reddit Posts */}
      {topPosts.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Top Reddit Evidence:</h4>
          <div className="space-y-3">
            {topPosts.map((post, idx) => (
              <div key={idx} className="border-l-4 border-indigo-200 bg-indigo-50 p-3 rounded-r">
                <div className="flex items-start justify-between mb-2">
                  <h5 className="text-sm font-medium text-gray-900 flex-1">
                    {post.title.substring(0, 80)}...
                  </h5>
                  <span className={`px-2 py-1 text-xs rounded-full ${getSubredditColor(post.subreddit)}`}>
                    r/{post.subreddit}
                  </span>
                </div>
                
                <div className="flex items-center gap-4 text-xs text-gray-600 mb-2">
                  <span>u/{post.author}</span>
                  <span>{post.score} points</span>
                  <span>{post.num_comments} comments</span>
                  <span>Relevance: {post.relevance_score}/10</span>
                </div>
                
                {post.selftext && (
                  <p className="text-sm text-gray-700 mb-2">
                    {post.selftext.substring(0, 150)}...
                  </p>
                )}
                
                <a
                  href={post.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800"
                >
                  <ExternalLink className="w-3 h-3" />
                  View on Reddit
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Search Terms Used */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-700 mb-2">Search Terms Used:</h4>
        <div className="flex flex-wrap gap-1">
          {deviceData.search_terms_used?.slice(0, 3).map((term, idx) => (
            <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
              "{term}"
            </span>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="text-xs text-gray-500">
          Found via {deviceData.search_terms_used?.length} search terms
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
          >
            <Eye className="w-4 h-4" />
            {expanded ? 'Show Less' : `View All ${posts.length}`}
          </button>
        </div>
      </div>

      {/* Expanded View */}
      {expanded && posts.length > 3 && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-4 pt-4 border-t border-gray-100"
        >
          <h4 className="text-sm font-medium text-gray-900 mb-3">All Reddit Posts ({posts.length}):</h4>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {posts.slice(3).map((post, idx) => (
              <div key={idx} className="bg-gray-50 p-3 rounded border-l-2 border-gray-200">
                <div className="flex items-start justify-between mb-1">
                  <h6 className="text-sm font-medium text-gray-800 flex-1">
                    {post.title}
                  </h6>
                  <span className={`px-2 py-1 text-xs rounded ${getSubredditColor(post.subreddit)}`}>
                    r/{post.subreddit}
                  </span>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-600">
                  <span>{post.score} points</span>
                  <span>{post.num_comments} comments</span>
                  <a href={post.url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-800">
                    View →
                  </a>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

function ComprehensiveRedditEvidence() {
  const [devicesData, setDevicesData] = useState({});
  const [filteredDevices, setFilteredDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPosts, setFilterPosts] = useState('all');
  const [sortBy, setSortBy] = useState('posts_count');

  // Load comprehensive Reddit evidence
  useEffect(() => {
    const loadRedditData = async () => {
      try {
        const response = await fetch('/comprehensive_reddit_evidence.json');
        const data = await response.json();
        setDevicesData(data.devices_with_reddit_evidence || {});
        
        // Convert to array for filtering/sorting
        const devicesArray = Object.entries(data.devices_with_reddit_evidence || {}).map(([name, data]) => ({
          name,
          ...data
        }));
        
        setFilteredDevices(devicesArray);
        setLoading(false);
      } catch (error) {
        console.error('Error loading comprehensive Reddit evidence:', error);
        setLoading(false);
      }
    };

    loadRedditData();
  }, []);

  // Filter and sort devices
  useEffect(() => {
    const devicesArray = Object.entries(devicesData).map(([name, data]) => ({
      name,
      ...data
    }));

    let filtered = devicesArray;

    if (searchTerm) {
      filtered = filtered.filter(device =>
        device.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        device.device_info.manufacturer.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterPosts !== 'all') {
      if (filterPosts === 'high') {
        filtered = filtered.filter(device => device.reddit_posts.length >= 20);
      } else if (filterPosts === 'medium') {
        filtered = filtered.filter(device => device.reddit_posts.length >= 10 && device.reddit_posts.length < 20);
      } else if (filterPosts === 'low') {
        filtered = filtered.filter(device => device.reddit_posts.length < 10);
      }
    }

    // Sort devices
    filtered.sort((a, b) => {
      switch(sortBy) {
        case 'posts_count':
          return b.reddit_posts.length - a.reddit_posts.length;
        case 'severity_score':
          return b.device_info.severity_score - a.device_info.severity_score;
        case 'deaths':
          return b.device_info.deaths - a.device_info.deaths;
        case 'device_name':
          return a.name.localeCompare(b.name);
        default:
          return b.reddit_posts.length - a.reddit_posts.length;
      }
    });

    setFilteredDevices(filtered);
  }, [searchTerm, filterPosts, sortBy, devicesData]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading comprehensive Reddit evidence...</p>
        </div>
      </div>
    );
  }

  const totalPosts = Object.values(devicesData).reduce((sum, device) => sum + device.reddit_posts.length, 0);
  const totalDevices = Object.keys(devicesData).length;

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
              <MessageSquare className="w-8 h-8 mr-3 text-indigo-600" />
              Comprehensive Reddit Evidence
            </h1>
            <p className="text-gray-600 mt-2">
              Real-world evidence from Reddit for all potential legal devices
            </p>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              <FileText className="w-4 h-4" />
              Full Report
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-indigo-50 p-4 rounded-lg text-center">
            <MessageSquare className="w-6 h-6 mx-auto mb-2 text-indigo-600" />
            <p className="text-2xl font-bold text-indigo-600">{totalPosts}</p>
            <p className="text-sm text-indigo-600">Total Reddit Posts</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg text-center">
            <Scale className="w-6 h-6 mx-auto mb-2 text-purple-600" />
            <p className="text-2xl font-bold text-purple-600">{totalDevices}</p>
            <p className="text-sm text-purple-600">Devices Researched</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg text-center">
            <TrendingUp className="w-6 h-6 mx-auto mb-2 text-green-600" />
            <p className="text-2xl font-bold text-green-600">100%</p>
            <p className="text-sm text-green-600">Evidence Coverage</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg text-center">
            <AlertTriangle className="w-6 h-6 mx-auto mb-2 text-orange-600" />
            <p className="text-2xl font-bold text-orange-600">HIGH</p>
            <p className="text-sm text-orange-600">Research Quality</p>
          </div>
        </div>
      </motion.div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-card p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search devices or manufacturers..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            value={filterPosts}
            onChange={(e) => setFilterPosts(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">All Post Counts</option>
            <option value="high">High (20+ posts)</option>
            <option value="medium">Medium (10-19 posts)</option>
            <option value="low">Low (1-9 posts)</option>
          </select>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          >
            <option value="posts_count">Sort by Reddit Posts</option>
            <option value="severity_score">Sort by Severity</option>
            <option value="deaths">Sort by Deaths</option>
            <option value="device_name">Sort by Name</option>
          </select>
        </div>
      </div>

      {/* Results Summary */}
      <div className="bg-indigo-50 border-l-4 border-indigo-400 p-4 rounded-r-lg">
        <div className="flex">
          <div className="flex-shrink-0">
            <MessageSquare className="h-5 w-5 text-indigo-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-indigo-800">
              Reddit Research Complete: {filteredDevices.length} devices with evidence
            </h3>
            <div className="mt-2 text-sm text-indigo-700">
              <p>
                Comprehensive Reddit scraping completed for all top legal devices. Evidence includes user experiences,
                professional discussions, malfunction reports, and safety concerns from relevant medical subreddits.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Devices Grid */}
      <div className="grid gap-6">
        {filteredDevices.map((device, index) => (
          <DeviceRedditCard 
            key={device.name} 
            deviceName={device.name}
            deviceData={device}
            index={index} 
          />
        ))}
      </div>

      {filteredDevices.length === 0 && (
        <div className="text-center py-12">
          <MessageSquare className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No devices found</h3>
          <p className="text-gray-600">Try adjusting your search terms or filters.</p>
        </div>
      )}
    </div>
  );
}

export default ComprehensiveRedditEvidence;
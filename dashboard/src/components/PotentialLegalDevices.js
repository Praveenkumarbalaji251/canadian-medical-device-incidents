import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  AlertTriangle,
  Skull,
  UserX,
  Wrench,
  TrendingUp,
  Building2,
  Calendar,
  Scale,
  Search,
  Filter,
  Eye,
  BarChart3,
  FileText,
  ExternalLink,
  MessageSquare
} from 'lucide-react';

function DeviceCard({ device, index }) {
  const getRiskColor = (level) => {
    switch(level) {
      case 'HIGH': return 'border-red-500 bg-red-50';
      case 'MEDIUM': return 'border-orange-500 bg-orange-50';
      case 'LOW': return 'border-yellow-500 bg-yellow-50';
      default: return 'border-gray-500 bg-gray-50';
    }
  };

  const getRiskTextColor = (level) => {
    switch(level) {
      case 'HIGH': return 'text-red-800';
      case 'MEDIUM': return 'text-orange-800';
      case 'LOW': return 'text-yellow-800';
      default: return 'text-gray-800';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className={`bg-white rounded-lg shadow-card border-l-4 ${getRiskColor(device.risk_level)} p-6 hover:shadow-lg transition-shadow`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {device.device_name}
          </h3>
          <p className="text-sm text-gray-600 mb-2">
            <Building2 className="w-4 h-4 inline mr-1" />
            {device.manufacturer}
          </p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskColor(device.risk_level)} ${getRiskTextColor(device.risk_level)}`}>
          {device.risk_level} RISK
        </div>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            <AlertTriangle className="w-4 h-4 text-gray-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">{device.total_incidents}</p>
          <p className="text-xs text-gray-600">Total Incidents</p>
        </div>
        
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            <Skull className="w-4 h-4 text-red-600" />
          </div>
          <p className="text-2xl font-bold text-red-600">{device.deaths}</p>
          <p className="text-xs text-gray-600">Deaths</p>
        </div>
        
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            <UserX className="w-4 h-4 text-orange-600" />
          </div>
          <p className="text-2xl font-bold text-orange-600">{device.injuries}</p>
          <p className="text-xs text-gray-600">Injuries</p>
        </div>
        
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            <Wrench className="w-4 h-4 text-blue-600" />
          </div>
          <p className="text-2xl font-bold text-blue-600">{device.malfunctions}</p>
          <p className="text-xs text-gray-600">Malfunctions</p>
        </div>
      </div>

      {/* Severity Score */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Legal Severity Score</span>
          <span className="text-lg font-bold text-purple-600">{device.severity_score}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-purple-600 h-2 rounded-full" 
            style={{ width: `${Math.min((device.severity_score / 1500) * 100, 100)}%` }}
          ></div>
        </div>
      </div>

      {/* Legal Merit Reasons */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Legal Merit:</h4>
        <div className="space-y-1">
          {device.legal_merit.map((reason, idx) => (
            <div key={idx} className="flex items-center text-sm text-gray-600">
              <Scale className="w-3 h-3 mr-2 text-purple-600" />
              {reason}
            </div>
          ))}
        </div>
      </div>

      {/* Key Problems */}
      {device.key_problems && device.key_problems.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Key Problems:</h4>
          <div className="flex flex-wrap gap-1">
            {device.key_problems.slice(0, 3).map((problem, idx) => (
              <span key={idx} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">
                {problem.substring(0, 20)}...
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Death Causes */}
      {device.death_causes && device.death_causes.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Death Patterns:</h4>
          <div className="space-y-1">
            {device.death_causes.slice(0, 2).map((cause, idx) => (
              <div key={idx} className="text-xs text-red-700 bg-red-50 p-2 rounded">
                • {cause}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="text-xs text-gray-500">
          Class Action Status: {device.class_action_status}
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-1 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
            <MessageSquare className="w-4 h-4" />
            Reddit Research
          </button>
          <button className="flex items-center gap-1 px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors">
            <Scale className="w-4 h-4" />
            Legal Analysis
          </button>
        </div>
      </div>
    </motion.div>
  );
}

function PotentialLegalDevices() {
  const [devices, setDevices] = useState([]);
  const [filteredDevices, setFilteredDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  const [filterDeaths, setFilterDeaths] = useState('all');
  const [sortBy, setSortBy] = useState('severity_score');

  // Load potential legal devices data
  useEffect(() => {
    const loadDevicesData = async () => {
      try {
        const response = await fetch('/potential_legal_devices.json');
        const data = await response.json();
        setDevices(data.devices || []);
        setFilteredDevices(data.devices || []);
        setLoading(false);
      } catch (error) {
        console.error('Error loading devices data:', error);
        setLoading(false);
      }
    };

    loadDevicesData();
  }, []);

  // Filter and sort devices
  useEffect(() => {
    let filtered = devices;

    if (searchTerm) {
      filtered = filtered.filter(device =>
        device.device_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        device.manufacturer.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterRisk !== 'all') {
      filtered = filtered.filter(device => device.risk_level === filterRisk);
    }

    if (filterDeaths !== 'all') {
      if (filterDeaths === 'with_deaths') {
        filtered = filtered.filter(device => device.deaths > 0);
      } else if (filterDeaths === 'multiple_deaths') {
        filtered = filtered.filter(device => device.deaths >= 5);
      }
    }

    // Sort devices
    filtered.sort((a, b) => {
      switch(sortBy) {
        case 'severity_score':
          return b.severity_score - a.severity_score;
        case 'total_incidents':
          return b.total_incidents - a.total_incidents;
        case 'deaths':
          return b.deaths - a.deaths;
        case 'device_name':
          return a.device_name.localeCompare(b.device_name);
        default:
          return b.severity_score - a.severity_score;
      }
    });

    setFilteredDevices(filtered);
  }, [searchTerm, filterRisk, filterDeaths, sortBy, devices]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyzing potential legal devices...</p>
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
              <Scale className="w-8 h-8 mr-3 text-purple-600" />
              Potential Legal Devices
            </h1>
            <p className="text-gray-600 mt-2">
              Medical devices with similar injury patterns and no existing class actions
            </p>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
              <FileText className="w-4 h-4" />
              Full Legal Report
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-purple-50 p-4 rounded-lg text-center">
            <Scale className="w-6 h-6 mx-auto mb-2 text-purple-600" />
            <p className="text-2xl font-bold text-purple-600">{devices.length}</p>
            <p className="text-sm text-purple-600">Legal Candidates</p>
          </div>
          <div className="bg-red-50 p-4 rounded-lg text-center">
            <Skull className="w-6 h-6 mx-auto mb-2 text-red-600" />
            <p className="text-2xl font-bold text-red-600">
              {devices.reduce((sum, device) => sum + device.deaths, 0)}
            </p>
            <p className="text-sm text-red-600">Total Deaths</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg text-center">
            <UserX className="w-6 h-6 mx-auto mb-2 text-orange-600" />
            <p className="text-2xl font-bold text-orange-600">
              {devices.reduce((sum, device) => sum + device.injuries, 0)}
            </p>
            <p className="text-sm text-orange-600">Total Injuries</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <AlertTriangle className="w-6 h-6 mx-auto mb-2 text-blue-600" />
            <p className="text-2xl font-bold text-blue-600">
              {devices.reduce((sum, device) => sum + device.total_incidents, 0)}
            </p>
            <p className="text-sm text-blue-600">Total Incidents</p>
          </div>
        </div>
      </motion.div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-card p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search devices or manufacturers..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          >
            <option value="all">All Risk Levels</option>
            <option value="HIGH">High Risk</option>
            <option value="MEDIUM">Medium Risk</option>
            <option value="LOW">Low Risk</option>
          </select>
          
          <select
            value={filterDeaths}
            onChange={(e) => setFilterDeaths(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          >
            <option value="all">All Devices</option>
            <option value="with_deaths">With Deaths</option>
            <option value="multiple_deaths">5+ Deaths</option>
          </select>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          >
            <option value="severity_score">Sort by Severity</option>
            <option value="total_incidents">Sort by Incidents</option>
            <option value="deaths">Sort by Deaths</option>
            <option value="device_name">Sort by Name</option>
          </select>
        </div>
      </div>

      {/* Results Summary */}
      <div className="bg-purple-50 border-l-4 border-purple-400 p-4 rounded-r-lg">
        <div className="flex">
          <div className="flex-shrink-0">
            <AlertTriangle className="h-5 w-5 text-purple-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-purple-800">
              Legal Analysis Results: {filteredDevices.length} devices found
            </h3>
            <div className="mt-2 text-sm text-purple-700">
              <p>
                Devices analyzed for similar injury patterns, repeated malfunctions, and absence of existing class action lawsuits.
                Sorted by legal severity score (deaths×10 + injuries×2 + malfunctions×0.5).
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Devices Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-1">
        {filteredDevices.map((device, index) => (
          <DeviceCard key={device.device_name} device={device} index={index} />
        ))}
      </div>

      {filteredDevices.length === 0 && (
        <div className="text-center py-12">
          <Scale className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No devices found</h3>
          <p className="text-gray-600">Try adjusting your search terms or filters.</p>
        </div>
      )}
    </div>
  );
}

export default PotentialLegalDevices;
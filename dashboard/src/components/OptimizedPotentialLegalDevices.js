import React, { useState, useEffect, useMemo, useCallback, memo } from 'react';
import { motion } from 'framer-motion';
import {
  AlertTriangle,
  Skull,
  UserX,
  Wrench,
  TrendingUp,
  Building2,
  Scale,
  Search,
  Filter,
  MessageSquare,
  BarChart3
} from 'lucide-react';

// Memoized device card for better performance
const OptimizedDeviceCard = memo(({ device, index }) => {
  const getRiskColor = useCallback((level) => {
    switch(level) {
      case 'HIGH': return 'border-red-500 bg-red-50';
      case 'MEDIUM': return 'border-orange-500 bg-orange-50';
      case 'LOW': return 'border-yellow-500 bg-yellow-50';
      default: return 'border-gray-500 bg-gray-50';
    }
  }, []);

  const getRiskTextColor = useCallback((level) => {
    switch(level) {
      case 'HIGH': return 'text-red-800';
      case 'MEDIUM': return 'text-orange-800';
      case 'LOW': return 'text-yellow-800';
      default: return 'text-gray-800';
    }
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, delay: Math.min(index * 0.02, 0.5) }}
      className={`bg-white rounded-lg shadow-sm border-l-4 ${getRiskColor(device.risk_level)} p-6 hover:shadow-md transition-shadow duration-200`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 mb-2 truncate">
            {device.device_name}
          </h3>
          <p className="text-sm text-gray-600 mb-2 flex items-center">
            <Building2 className="w-4 h-4 inline mr-1 flex-shrink-0" />
            <span className="truncate">{device.manufacturer}</span>
          </p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ${getRiskColor(device.risk_level)} ${getRiskTextColor(device.risk_level)}`}>
          {device.risk_level} RISK
        </div>
      </div>

      {/* Statistics Grid - Optimized */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        <div className="text-center">
          <AlertTriangle className="w-4 h-4 mx-auto mb-1 text-gray-600" />
          <p className="text-lg font-bold text-gray-900">{device.total_incidents}</p>
          <p className="text-xs text-gray-600">Total</p>
        </div>
        <div className="text-center">
          <Skull className="w-4 h-4 mx-auto mb-1 text-red-600" />
          <p className="text-lg font-bold text-red-600">{device.deaths}</p>
          <p className="text-xs text-gray-600">Deaths</p>
        </div>
        <div className="text-center">
          <UserX className="w-4 h-4 mx-auto mb-1 text-orange-600" />
          <p className="text-lg font-bold text-orange-600">{device.injuries}</p>
          <p className="text-xs text-gray-600">Injuries</p>
        </div>
        <div className="text-center">
          <Wrench className="w-4 h-4 mx-auto mb-1 text-blue-600" />
          <p className="text-lg font-bold text-blue-600">{device.malfunctions}</p>
          <p className="text-xs text-gray-600">Malfunctions</p>
        </div>
      </div>

      {/* Severity Score - Simplified */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Severity Score</span>
          <span className="text-lg font-bold text-purple-600">{device.severity_score}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-purple-600 h-2 rounded-full transition-all duration-300" 
            style={{ width: `${Math.min((device.severity_score / 1500) * 100, 100)}%` }}
          />
        </div>
      </div>

      {/* Legal Merit - Truncated */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Legal Merit:</h4>
        <div className="space-y-1">
          {device.legal_merit?.slice(0, 2).map((reason, idx) => (
            <div key={idx} className="flex items-center text-sm text-gray-600">
              <Scale className="w-3 h-3 mr-2 text-purple-600 flex-shrink-0" />
              <span className="truncate">{reason}</span>
            </div>
          ))}
          {device.legal_merit?.length > 2 && (
            <div className="text-xs text-gray-500">
              +{device.legal_merit.length - 2} more reasons
            </div>
          )}
        </div>
      </div>

      {/* Actions - Simplified */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="text-xs text-gray-500">
          Status: {device.class_action_status}
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-1 px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors duration-200">
            <MessageSquare className="w-4 h-4" />
            Reddit
          </button>
          <button className="flex items-center gap-1 px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors duration-200">
            <Scale className="w-4 h-4" />
            Legal
          </button>
        </div>
      </div>
    </motion.div>
  );
});

// Optimized statistics card
const StatsCard = memo(({ icon: Icon, value, label, color }) => (
  <div className={`${color} p-4 rounded-lg text-center`}>
    <Icon className="w-6 h-6 mx-auto mb-2" />
    <p className="text-2xl font-bold">{value}</p>
    <p className="text-sm">{label}</p>
  </div>
));

function OptimizedPotentialLegalDevices() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  const [filterDeaths, setFilterDeaths] = useState('all');
  const [sortBy, setSortBy] = useState('severity_score');

  // Load devices data with error handling
  useEffect(() => {
    const loadDevicesData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/potential_legal_devices.json');
        if (!response.ok) throw new Error('Failed to load legal devices data');
        
        const data = await response.json();
        setDevices(data.devices || []);
      } catch (error) {
        console.error('Error loading devices data:', error);
        setDevices([]);
      } finally {
        setLoading(false);
      }
    };

    loadDevicesData();
  }, []);

  // Memoized filtering and sorting
  const filteredDevices = useMemo(() => {
    if (!devices.length) return [];

    let filtered = devices.filter(device => {
      const searchMatch = !searchTerm || 
        device.device_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        device.manufacturer.toLowerCase().includes(searchTerm.toLowerCase());

      const riskMatch = filterRisk === 'all' || device.risk_level === filterRisk;

      let deathMatch = true;
      if (filterDeaths === 'with_deaths') {
        deathMatch = device.deaths > 0;
      } else if (filterDeaths === 'multiple_deaths') {
        deathMatch = device.deaths >= 5;
      }

      return searchMatch && riskMatch && deathMatch;
    });

    // Sort devices
    return filtered.sort((a, b) => {
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
  }, [devices, searchTerm, filterRisk, filterDeaths, sortBy]);

  // Memoized statistics
  const stats = useMemo(() => {
    if (!devices.length) return { totalDevices: 0, totalDeaths: 0, totalInjuries: 0, totalIncidents: 0 };

    return devices.reduce((acc, device) => ({
      totalDevices: acc.totalDevices + 1,
      totalDeaths: acc.totalDeaths + device.deaths,
      totalInjuries: acc.totalInjuries + device.injuries,
      totalIncidents: acc.totalIncidents + device.total_incidents
    }), { totalDevices: 0, totalDeaths: 0, totalInjuries: 0, totalIncidents: 0 });
  }, [devices]);

  // Optimized handlers
  const handleSearchChange = useCallback((e) => {
    setSearchTerm(e.target.value);
  }, []);

  const handleRiskFilterChange = useCallback((value) => {
    setFilterRisk(value);
  }, []);

  const handleDeathsFilterChange = useCallback((value) => {
    setFilterDeaths(value);
  }, []);

  const handleSortChange = useCallback((value) => {
    setSortBy(value);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading legal devices...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Optimized Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <Scale className="w-8 h-8 mr-3 text-purple-600" />
              Legal Device Candidates
            </h1>
            <p className="text-gray-600 mt-2">
              {filteredDevices.length} devices with legal potential
            </p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors duration-200">
            <BarChart3 className="w-4 h-4" />
            Legal Report
          </button>
        </div>

        {/* Optimized Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatsCard
            icon={Scale}
            value={stats.totalDevices}
            label="Legal Candidates"
            color="bg-purple-50 text-purple-600"
          />
          <StatsCard
            icon={Skull}
            value={stats.totalDeaths}
            label="Total Deaths"
            color="bg-red-50 text-red-600"
          />
          <StatsCard
            icon={UserX}
            value={stats.totalInjuries}
            label="Total Injuries"
            color="bg-orange-50 text-orange-600"
          />
          <StatsCard
            icon={AlertTriangle}
            value={stats.totalIncidents}
            label="Total Incidents"
            color="bg-blue-50 text-blue-600"
          />
        </div>
      </div>

      {/* Optimized Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search devices..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
              value={searchTerm}
              onChange={handleSearchChange}
            />
          </div>
          
          <select
            value={filterRisk}
            onChange={(e) => handleRiskFilterChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 transition-all duration-200"
          >
            <option value="all">All Risk Levels</option>
            <option value="HIGH">High Risk</option>
            <option value="MEDIUM">Medium Risk</option>
            <option value="LOW">Low Risk</option>
          </select>
          
          <select
            value={filterDeaths}
            onChange={(e) => handleDeathsFilterChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 transition-all duration-200"
          >
            <option value="all">All Devices</option>
            <option value="with_deaths">With Deaths</option>
            <option value="multiple_deaths">5+ Deaths</option>
          </select>
          
          <select
            value={sortBy}
            onChange={(e) => handleSortChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 transition-all duration-200"
          >
            <option value="severity_score">By Severity</option>
            <option value="total_incidents">By Incidents</option>
            <option value="deaths">By Deaths</option>
            <option value="device_name">By Name</option>
          </select>
        </div>
      </div>

      {/* Results Summary */}
      {filteredDevices.length > 0 && (
        <div className="bg-purple-50 border-l-4 border-purple-400 p-4 rounded-r-lg">
          <div className="flex">
            <AlertTriangle className="h-5 w-5 text-purple-400 flex-shrink-0" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-purple-800">
                Found {filteredDevices.length} legal candidates
              </h3>
              <p className="mt-1 text-sm text-purple-700">
                Devices analyzed for similar injury patterns and absence of existing class actions.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Optimized Devices Grid */}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {filteredDevices.map((device, index) => (
          <OptimizedDeviceCard key={device.device_name} device={device} index={index} />
        ))}
      </div>

      {/* No results state */}
      {filteredDevices.length === 0 && !loading && (
        <div className="text-center py-12">
          <Scale className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No devices found</h3>
          <p className="text-gray-600">Try adjusting your search terms or filters.</p>
        </div>
      )}
    </div>
  );
}

export default OptimizedPotentialLegalDevices;
import React, { useState, useEffect, useMemo, useCallback, memo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertTriangle,
  Search,
  Filter,
  Skull,
  Activity,
  Calendar,
  Building,
  ChevronLeft,
  ChevronRight,
  Grid,
  List,
  Download,
  TrendingUp,
  Users,
  UserX
} from 'lucide-react';

// Memoized incident card component for better performance
const IncidentCard = memo(({ incident, index }) => {
  const getSeverityColor = useCallback((severity) => {
    if (severity?.includes('DEATH') || severity?.includes('MORT')) return 'border-red-500 bg-red-50';
    if (severity?.includes('INJURY') || severity?.includes('BLESSURE')) return 'border-orange-500 bg-orange-50';
    return 'border-yellow-500 bg-yellow-50';
  }, []);

  const getSeverityIcon = useCallback((severity) => {
    if (severity?.includes('DEATH') || severity?.includes('MORT')) return <Skull className="w-5 h-5 text-red-600" />;
    if (severity?.includes('INJURY') || severity?.includes('BLESSURE')) return <UserX className="w-5 h-5 text-orange-600" />;
    return <Activity className="w-5 h-5 text-yellow-600" />;
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, delay: Math.min(index * 0.01, 0.3) }}
      className={`bg-white rounded-lg shadow-sm border-l-4 hover:shadow-md transition-shadow duration-200 p-4 ${getSeverityColor(incident.HAZARD_SEVERITY_CODE_E)}`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          {getSeverityIcon(incident.HAZARD_SEVERITY_CODE_E)}
          <span className="text-sm font-medium text-gray-900">
            ID: {incident.INCIDENT_ID}
          </span>
        </div>
        <span className="text-xs text-gray-500">
          {incident.RECEIPT_DT}
        </span>
      </div>

      <div className="space-y-2">
        <div className="flex items-center text-sm text-gray-600">
          <Building className="w-4 h-4 mr-2" />
          <span className="font-medium">{incident.TRADE_NAME || 'Unknown Device'}</span>
        </div>
        
        <div className="flex items-center text-sm text-gray-600">
          <Calendar className="w-4 h-4 mr-2" />
          <span>Incident: {incident.INCIDENT_DT}</span>
        </div>

        {incident.COMPANY_NAME && (
          <div className="text-xs text-gray-500 truncate">
            Company: {incident.COMPANY_NAME}
          </div>
        )}
      </div>

      <div className="mt-3 pt-3 border-t border-gray-100">
        <div className="flex justify-between items-center">
          <span className="text-xs font-medium text-gray-700">
            {incident.HAZARD_SEVERITY_CODE_E}
          </span>
          <span className="text-xs text-gray-500">
            Risk: {incident.RISK_CLASSIFICATION || 'N/A'}
          </span>
        </div>
      </div>
    </motion.div>
  );
});

// Optimized table row component
const IncidentTableRow = memo(({ incident, index }) => {
  const getSeverityColor = useCallback((severity) => {
    if (severity?.includes('DEATH') || severity?.includes('MORT')) return 'text-red-600 bg-red-50';
    if (severity?.includes('INJURY') || severity?.includes('BLESSURE')) return 'text-orange-600 bg-orange-50';
    return 'text-yellow-600 bg-yellow-50';
  }, []);

  return (
    <motion.tr
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2, delay: Math.min(index * 0.005, 0.1) }}
      className="hover:bg-gray-50 transition-colors duration-150"
    >
      <td className="px-4 py-3 text-sm text-gray-900">{incident.INCIDENT_ID}</td>
      <td className="px-4 py-3 text-sm text-gray-600">{incident.TRADE_NAME || 'Unknown'}</td>
      <td className="px-4 py-3 text-sm text-gray-600">{incident.COMPANY_NAME || 'Unknown'}</td>
      <td className="px-4 py-3 text-sm text-gray-600">{incident.INCIDENT_DT}</td>
      <td className="px-4 py-3">
        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(incident.HAZARD_SEVERITY_CODE_E)}`}>
          {incident.HAZARD_SEVERITY_CODE_E}
        </span>
      </td>
      <td className="px-4 py-3 text-sm text-gray-600">{incident.RISK_CLASSIFICATION || 'N/A'}</td>
    </motion.tr>
  );
});

// Virtual pagination component for better performance
const VirtualPagination = memo(({ currentPage, totalPages, onPageChange, itemsPerPage, totalItems }) => {
  const getVisiblePages = useMemo(() => {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];

    for (let i = Math.max(2, currentPage - delta); i <= Math.min(totalPages - 1, currentPage + delta); i++) {
      range.push(i);
    }

    if (currentPage - delta > 2) {
      rangeWithDots.push(1, '...');
    } else {
      rangeWithDots.push(1);
    }

    rangeWithDots.push(...range);

    if (currentPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else {
      rangeWithDots.push(totalPages);
    }

    return rangeWithDots;
  }, [currentPage, totalPages]);

  return (
    <div className="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200 sm:px-6">
      <div className="flex justify-between flex-1 sm:hidden">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
        >
          Previous
        </button>
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="relative ml-3 inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
        >
          Next
        </button>
      </div>
      
      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-gray-700">
            Showing <span className="font-medium">{(currentPage - 1) * itemsPerPage + 1}</span> to{' '}
            <span className="font-medium">{Math.min(currentPage * itemsPerPage, totalItems)}</span> of{' '}
            <span className="font-medium">{totalItems}</span> results
          </p>
        </div>
        
        <div>
          <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
            <button
              onClick={() => onPageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            
            {getVisiblePages.map((page, index) => (
              <button
                key={index}
                onClick={() => typeof page === 'number' && onPageChange(page)}
                disabled={page === '...'}
                className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                  page === currentPage
                    ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                    : page === '...'
                    ? 'border-gray-300 bg-white text-gray-500 cursor-default'
                    : 'border-gray-300 bg-white text-gray-500 hover:bg-gray-50'
                }`}
              >
                {page}
              </button>
            ))}
            
            <button
              onClick={() => onPageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  );
});

function OptimizedAllIncidents() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [severityFilter, setSeverityFilter] = useState('all');
  const [viewMode, setViewMode] = useState('card');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(50); // Increased for better performance

  // Load incidents data with error handling
  useEffect(() => {
    const loadIncidents = async () => {
      try {
        setLoading(true);
        const response = await fetch('/dashboard_data.json');
        if (!response.ok) throw new Error('Failed to load data');
        
        const data = await response.json();
        setIncidents(data || []);
      } catch (error) {
        console.error('Error loading incidents:', error);
        setIncidents([]);
      } finally {
        setLoading(false);
      }
    };

    loadIncidents();
  }, []);

  // Memoized filtering and search logic
  const filteredIncidents = useMemo(() => {
    if (!incidents.length) return [];

    return incidents.filter(incident => {
      // Search filter
      const searchMatch = !searchTerm || 
        incident.TRADE_NAME?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.COMPANY_NAME?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.INCIDENT_ID?.toString().includes(searchTerm);

      // Severity filter
      const severityMatch = severityFilter === 'all' || 
        incident.HAZARD_SEVERITY_CODE_E?.includes(severityFilter.toUpperCase());

      return searchMatch && severityMatch;
    });
  }, [incidents, searchTerm, severityFilter]);

  // Memoized pagination
  const paginatedIncidents = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredIncidents.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredIncidents, currentPage, itemsPerPage]);

  const totalPages = Math.ceil(filteredIncidents.length / itemsPerPage);

  // Memoized statistics
  const stats = useMemo(() => {
    if (!filteredIncidents.length) return { total: 0, deaths: 0, injuries: 0, other: 0 };

    return filteredIncidents.reduce((acc, incident) => {
      acc.total++;
      const severity = incident.HAZARD_SEVERITY_CODE_E || '';
      if (severity.includes('DEATH') || severity.includes('MORT')) acc.deaths++;
      else if (severity.includes('INJURY') || severity.includes('BLESSURE')) acc.injuries++;
      else acc.other++;
      return acc;
    }, { total: 0, deaths: 0, injuries: 0, other: 0 });
  }, [filteredIncidents]);

  // Optimized search handler with debouncing
  const handleSearchChange = useCallback((e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  }, []);

  const handleSeverityFilterChange = useCallback((value) => {
    setSeverityFilter(value);
    setCurrentPage(1);
  }, []);

  const handlePageChange = useCallback((page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading incidents...</p>
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
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <AlertTriangle className="w-6 h-6 mr-3 text-red-600" />
              All Medical Device Incidents
            </h1>
            <p className="text-gray-600 mt-1">Complete database of Health Canada incidents</p>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setViewMode('card')}
              className={`p-2 rounded-lg transition-colors ${viewMode === 'card' ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <Grid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-2 rounded-lg transition-colors ${viewMode === 'table' ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <List className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Optimized Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <AlertTriangle className="w-5 h-5 mx-auto mb-2 text-blue-600" />
            <p className="text-2xl font-bold text-blue-600">{stats.total}</p>
            <p className="text-sm text-blue-600">Total Incidents</p>
          </div>
          <div className="bg-red-50 p-4 rounded-lg text-center">
            <Skull className="w-5 h-5 mx-auto mb-2 text-red-600" />
            <p className="text-2xl font-bold text-red-600">{stats.deaths}</p>
            <p className="text-sm text-red-600">Deaths</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg text-center">
            <UserX className="w-5 h-5 mx-auto mb-2 text-orange-600" />
            <p className="text-2xl font-bold text-orange-600">{stats.injuries}</p>
            <p className="text-sm text-orange-600">Injuries</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg text-center">
            <Activity className="w-5 h-5 mx-auto mb-2 text-yellow-600" />
            <p className="text-2xl font-bold text-yellow-600">{stats.other}</p>
            <p className="text-sm text-yellow-600">Other</p>
          </div>
        </div>
      </div>

      {/* Optimized Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search incidents, devices, or companies..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={searchTerm}
              onChange={handleSearchChange}
            />
          </div>
          
          <select
            value={severityFilter}
            onChange={(e) => handleSeverityFilterChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Severities</option>
            <option value="death">Deaths Only</option>
            <option value="injury">Injuries Only</option>
            <option value="potential">Potential Issues</option>
          </select>
        </div>
      </div>

      {/* Optimized Content */}
      <div className="bg-white rounded-lg shadow-sm">
        {viewMode === 'card' ? (
          <div className="p-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              <AnimatePresence>
                {paginatedIncidents.map((incident, index) => (
                  <IncidentCard key={incident.INCIDENT_ID} incident={incident} index={index} />
                ))}
              </AnimatePresence>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {paginatedIncidents.map((incident, index) => (
                  <IncidentTableRow key={incident.INCIDENT_ID} incident={incident} index={index} />
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Optimized Pagination */}
        {totalPages > 1 && (
          <VirtualPagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={handlePageChange}
            itemsPerPage={itemsPerPage}
            totalItems={filteredIncidents.length}
          />
        )}
      </div>

      {/* No results state */}
      {filteredIncidents.length === 0 && !loading && (
        <div className="text-center py-12">
          <AlertTriangle className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No incidents found</h3>
          <p className="text-gray-600">Try adjusting your search terms or filters.</p>
        </div>
      )}
    </div>
  );
}

export default OptimizedAllIncidents;
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
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
  Download,
  Eye,
  SortAsc,
  SortDesc
} from 'lucide-react';

function IncidentCard({ incident, index }) {
  const getSeverityColor = (severity) => {
    if (incident.isDeath) return 'bg-red-100 border-red-500 text-red-800';
    if (incident.isInjury) return 'bg-orange-100 border-orange-500 text-orange-800';
    if (incident.isPotentialHarm) return 'bg-yellow-100 border-yellow-500 text-yellow-800';
    return 'bg-gray-100 border-gray-500 text-gray-800';
  };

  const getSeverityIcon = () => {
    if (incident.isDeath) return <Skull className="w-4 h-4" />;
    if (incident.isInjury) return <AlertTriangle className="w-4 h-4" />;
    return <Activity className="w-4 h-4" />;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.02 }}
      className={`p-4 rounded-lg border-l-4 shadow-sm hover:shadow-md transition-shadow ${getSeverityColor()}`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            {getSeverityIcon()}
            <span className="text-xs font-medium">
              Incident #{incident.id}
            </span>
            <span className="text-xs bg-white bg-opacity-50 px-2 py-1 rounded">
              Class {incident.riskClass}
            </span>
          </div>
          
          <h3 className="font-semibold text-sm mb-1">
            {incident.deviceName}
          </h3>
          
          <p className="text-xs opacity-75 mb-2">
            Code: {incident.deviceCode} | {incident.company}
          </p>
          
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              {new Date(incident.incidentDate).toLocaleDateString()}
            </div>
            <div className="flex items-center gap-1">
              <Building className="w-3 h-3" />
              Reported: {new Date(incident.receiptDate).toLocaleDateString()}
            </div>
          </div>
          
          <div className="mt-2 text-xs font-medium">
            {incident.severityCode}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function IncidentTable({ incidents, currentPage, itemsPerPage, onSort, sortConfig }) {
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentIncidents = incidents.slice(startIndex, startIndex + itemsPerPage);

  const getSortIcon = (columnKey) => {
    if (sortConfig.key === columnKey) {
      return sortConfig.direction === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />;
    }
    return null;
  };

  const getSeverityBadge = (incident) => {
    if (incident.isDeath) return <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">DEATH</span>;
    if (incident.isInjury) return <span className="px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded-full">INJURY</span>;
    if (incident.isPotentialHarm) return <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded-full">POTENTIAL HARM</span>;
    return <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">OTHER</span>;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => onSort('id')}
              >
                <div className="flex items-center gap-1">
                  ID {getSortIcon('id')}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => onSort('deviceName')}
              >
                <div className="flex items-center gap-1">
                  Device {getSortIcon('deviceName')}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => onSort('company')}
              >
                <div className="flex items-center gap-1">
                  Company {getSortIcon('company')}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => onSort('incidentDate')}
              >
                <div className="flex items-center gap-1">
                  Incident Date {getSortIcon('incidentDate')}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => onSort('severityCode')}
              >
                <div className="flex items-center gap-1">
                  Severity {getSortIcon('severityCode')}
                </div>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {currentIncidents.map((incident, index) => (
              <motion.tr
                key={incident.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.2, delay: index * 0.01 }}
                className="hover:bg-gray-50"
              >
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  #{incident.id}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  <div>
                    <div className="font-medium">{incident.deviceName}</div>
                    <div className="text-xs text-gray-500">Code: {incident.deviceCode}</div>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  {incident.company}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {new Date(incident.incidentDate).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  <div className="text-xs">{incident.severityCode}</div>
                  <div className="text-xs text-gray-500">Class {incident.riskClass}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getSeverityBadge(incident)}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AllIncidents() {
  const [incidents, setIncidents] = useState([]);
  const [filteredIncidents, setFilteredIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);
  const [viewMode, setViewMode] = useState('table'); // 'table' or 'cards'
  const [sortConfig, setSortConfig] = useState({ key: 'receiptDate', direction: 'desc' });
  const [filterConfig, setFilterConfig] = useState({
    severity: 'all',
    dateRange: 'all',
    riskClass: 'all'
  });

  // Load all incident data
  useEffect(() => {
    fetch('/comprehensive_dashboard_data.json')
      .then(response => response.json())
      .then(data => {
        const sortedIncidents = data.incidents.sort((a, b) => new Date(b.receiptDate) - new Date(a.receiptDate));
        setIncidents(sortedIncidents);
        setFilteredIncidents(sortedIncidents);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading incident data:', error);
        setLoading(false);
      });
  }, []);

  // Search functionality
  useEffect(() => {
    let filtered = incidents;

    // Apply search
    if (searchTerm) {
      filtered = filtered.filter(incident =>
        incident.deviceName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.id.includes(searchTerm) ||
        incident.deviceCode.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Apply filters
    if (filterConfig.severity !== 'all') {
      if (filterConfig.severity === 'death') {
        filtered = filtered.filter(incident => incident.isDeath);
      } else if (filterConfig.severity === 'injury') {
        filtered = filtered.filter(incident => incident.isInjury);
      } else if (filterConfig.severity === 'potential') {
        filtered = filtered.filter(incident => incident.isPotentialHarm);
      }
    }

    if (filterConfig.riskClass !== 'all') {
      filtered = filtered.filter(incident => incident.riskClass === filterConfig.riskClass);
    }

    setFilteredIncidents(filtered);
    setCurrentPage(1); // Reset to first page when filtering
  }, [searchTerm, filterConfig, incidents]);

  const handleSort = (key) => {
    let direction = 'desc';
    if (sortConfig.key === key && sortConfig.direction === 'desc') {
      direction = 'asc';
    }
    setSortConfig({ key, direction });

    const sorted = [...filteredIncidents].sort((a, b) => {
      let aVal = a[key];
      let bVal = b[key];

      // Handle date sorting
      if (key === 'incidentDate' || key === 'receiptDate') {
        aVal = new Date(aVal);
        bVal = new Date(bVal);
      }

      if (direction === 'asc') {
        return aVal > bVal ? 1 : -1;
      }
      return aVal < bVal ? 1 : -1;
    });
    setFilteredIncidents(sorted);
  };

  // Calculate pagination
  const totalPages = Math.ceil(filteredIncidents.length / itemsPerPage);
  const totalDeaths = filteredIncidents.filter(i => i.isDeath).length;
  const totalInjuries = filteredIncidents.filter(i => i.isInjury).length;
  const totalPotentialHarms = filteredIncidents.filter(i => i.isPotentialHarm).length;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading all 6,970 incidents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Statistics */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-card p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <AlertTriangle className="w-8 h-8 mr-3 text-red-600" />
              All Medical Device Incidents
            </h1>
            <p className="text-gray-600 mt-2">
              Complete database of {incidents.length} reported incidents (Sept 2024 - April 2025)
            </p>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Download className="w-4 h-4" />
              Export
            </button>
          </div>
        </div>

        {/* Critical Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <Activity className="w-6 h-6 mx-auto mb-2 text-blue-600" />
            <p className="text-2xl font-bold text-blue-600">{filteredIncidents.length}</p>
            <p className="text-sm text-blue-600">Total Incidents</p>
          </div>
          <div className="bg-red-50 p-4 rounded-lg text-center">
            <Skull className="w-6 h-6 mx-auto mb-2 text-red-600" />
            <p className="text-2xl font-bold text-red-600">{totalDeaths}</p>
            <p className="text-sm text-red-600">Deaths</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg text-center">
            <AlertTriangle className="w-6 h-6 mx-auto mb-2 text-orange-600" />
            <p className="text-2xl font-bold text-orange-600">{totalInjuries}</p>
            <p className="text-sm text-orange-600">Injuries</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg text-center">
            <Activity className="w-6 h-6 mx-auto mb-2 text-yellow-600" />
            <p className="text-2xl font-bold text-yellow-600">{totalPotentialHarms}</p>
            <p className="text-sm text-yellow-600">Potential Harms</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg text-center">
            <Calendar className="w-6 h-6 mx-auto mb-2 text-gray-600" />
            <p className="text-2xl font-bold text-gray-600">{totalPages}</p>
            <p className="text-sm text-gray-600">Pages</p>
          </div>
        </div>
      </motion.div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-card p-6">
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search incidents by device, company, ID, or device code..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="flex gap-2">
            <select
              value={filterConfig.severity}
              onChange={(e) => setFilterConfig({...filterConfig, severity: e.target.value})}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Severities</option>
              <option value="death">Deaths Only</option>
              <option value="injury">Injuries Only</option>
              <option value="potential">Potential Harms</option>
            </select>
            <select
              value={filterConfig.riskClass}
              onChange={(e) => setFilterConfig({...filterConfig, riskClass: e.target.value})}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Risk Classes</option>
              <option value="1">Class 1</option>
              <option value="2">Class 2</option>
              <option value="3">Class 3</option>
              <option value="4">Class 4</option>
            </select>
          </div>
        </div>

        {/* View Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-gray-700">View:</span>
            <div className="flex rounded-lg border border-gray-300">
              <button
                onClick={() => setViewMode('table')}
                className={`px-4 py-2 text-sm font-medium rounded-l-lg ${
                  viewMode === 'table' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                Table
              </button>
              <button
                onClick={() => setViewMode('cards')}
                className={`px-4 py-2 text-sm font-medium rounded-r-lg ${
                  viewMode === 'cards' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                Cards
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Show:</span>
            <select
              value={itemsPerPage}
              onChange={(e) => setItemsPerPage(parseInt(e.target.value))}
              className="px-3 py-1 border border-gray-300 rounded text-sm"
            >
              <option value={25}>25</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
              <option value={200}>200</option>
            </select>
            <span className="text-sm text-gray-600">per page</span>
          </div>
        </div>
      </div>

      {/* Incidents Display */}
      {viewMode === 'table' ? (
        <IncidentTable 
          incidents={filteredIncidents}
          currentPage={currentPage}
          itemsPerPage={itemsPerPage}
          onSort={handleSort}
          sortConfig={sortConfig}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredIncidents
            .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
            .map((incident, index) => (
              <IncidentCard key={incident.id} incident={incident} index={index} />
            ))}
        </div>
      )}

      {/* Pagination */}
      <div className="bg-white rounded-lg shadow-card p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Showing {((currentPage - 1) * itemsPerPage) + 1} to {Math.min(currentPage * itemsPerPage, filteredIncidents.length)} of {filteredIncidents.length} incidents
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="p-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-3 py-1 text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="p-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AllIncidents;
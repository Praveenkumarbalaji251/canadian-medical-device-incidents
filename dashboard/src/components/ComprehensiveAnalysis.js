import React, { useState, useEffect, useMemo } from 'react';
import { Search, Filter, SortAsc, SortDesc, AlertTriangle, Users, Calendar, Building } from 'lucide-react';

const ComprehensiveAnalysis = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('devices');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'desc' });
  const [filters, setFilters] = useState({
    severity: 'all',
    riskClass: 'all',
    dateRange: 'all'
  });

  useEffect(() => {
    fetch('/comprehensive_dashboard_data.json')
      .then(response => response.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading comprehensive data:', error);
        setLoading(false);
      });
  }, []);

  const handleSort = (key) => {
    let direction = 'desc';
    if (sortConfig.key === key && sortConfig.direction === 'desc') {
      direction = 'asc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (columnKey) => {
    if (sortConfig.key === columnKey) {
      return sortConfig.direction === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />;
    }
    return null;
  };

  const filteredAndSortedDevices = useMemo(() => {
    if (!data?.devices) return [];
    
    let filtered = data.devices.filter(device => {
      const matchesSearch = device.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           device.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           device.primaryCompany.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesSearch;
    });

    if (sortConfig.key) {
      filtered.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        
        if (typeof aValue === 'string') {
          return sortConfig.direction === 'asc' 
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        }
        
        return sortConfig.direction === 'asc' 
          ? aValue - bValue
          : bValue - aValue;
      });
    }

    return filtered;
  }, [data?.devices, searchTerm, sortConfig]);

  const filteredAndSortedCompanies = useMemo(() => {
    if (!data?.companies) return [];
    
    let filtered = data.companies.filter(company => {
      const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesSearch;
    });

    if (sortConfig.key) {
      filtered.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        
        if (typeof aValue === 'string') {
          return sortConfig.direction === 'asc' 
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        }
        
        return sortConfig.direction === 'asc' 
          ? aValue - bValue
          : bValue - aValue;
      });
    }

    return filtered;
  }, [data?.companies, searchTerm, sortConfig]);

  const filteredIncidents = useMemo(() => {
    if (!data?.incidents) return [];
    
    return data.incidents.filter(incident => {
      const matchesSearch = incident.deviceName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           incident.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           incident.severityCode.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesSeverity = filters.severity === 'all' || 
                             (filters.severity === 'death' && incident.isDeath) ||
                             (filters.severity === 'injury' && incident.isInjury) ||
                             (filters.severity === 'potential' && incident.isPotentialHarm);
      
      return matchesSearch && matchesSeverity;
    });
  }, [data?.incidents, searchTerm, filters]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center text-red-600 p-8">
        <AlertTriangle className="w-16 h-16 mx-auto mb-4" />
        <h3 className="text-xl font-semibold mb-2">Error Loading Data</h3>
        <p>Unable to load comprehensive analysis data.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Comprehensive Medical Device Analysis
        </h1>
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Data Coverage: 8 Months Only
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>
                  This analysis covers <strong>September 2024 - April 2025</strong> ({data.summary.monthsOfData} months) 
                  with {data.summary.totalIncidents.toLocaleString()} incidents. 
                  <strong> Missing: May-October 2025 data</strong> due to Health Canada reporting delays.
                </p>
              </div>
            </div>
          </div>
        </div>
        <p className="text-gray-600 mb-6">
          Detailed analysis of {data.summary.totalIncidents.toLocaleString()} medical device incidents 
          from {data.summary.dateRange.start} to {data.summary.dateRange.end} (Most recent available data)
        </p>
        
        {/* Key Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-red-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-red-600">Deaths</p>
                <p className="text-2xl font-bold text-red-900">{data.summary.totalDeaths}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Injuries</p>
                <p className="text-2xl font-bold text-orange-900">{data.summary.totalInjuries.toLocaleString()}</p>
              </div>
              <Users className="w-8 h-8 text-orange-500" />
            </div>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Unique Devices</p>
                <p className="text-2xl font-bold text-blue-900">{data.summary.uniqueDevices.toLocaleString()}</p>
              </div>
              <Calendar className="w-8 h-8 text-blue-500" />
            </div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Companies</p>
                <p className="text-2xl font-bold text-green-900">{data.summary.uniqueCompanies}</p>
              </div>
              <Building className="w-8 h-8 text-green-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search devices, companies, or severity..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex gap-4">
            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={filters.severity}
              onChange={(e) => setFilters({...filters, severity: e.target.value})}
            >
              <option value="all">All Severities</option>
              <option value="death">Deaths Only</option>
              <option value="injury">Injuries Only</option>
              <option value="potential">Potential Harm</option>
            </select>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'devices', label: 'Device Analysis', count: data.devices.length },
              { id: 'companies', label: 'Company Analysis', count: data.companies.length },
              { id: 'incidents', label: 'Incident Details', count: data.incidents.length }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label} ({tab.count.toLocaleString()})
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'devices' && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('name')}
                  >
                    <div className="flex items-center gap-1">
                      Device Name {getSortIcon('name')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('totalIncidents')}
                  >
                    <div className="flex items-center gap-1">
                      Total Incidents {getSortIcon('totalIncidents')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('deaths')}
                  >
                    <div className="flex items-center gap-1">
                      Deaths {getSortIcon('deaths')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('injuries')}
                  >
                    <div className="flex items-center gap-1">
                      Injuries {getSortIcon('injuries')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('riskScore')}
                  >
                    <div className="flex items-center gap-1">
                      Risk Score {getSortIcon('riskScore')}
                    </div>
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Primary Company
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredAndSortedDevices.slice(0, 50).map((device, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{device.name}</div>
                        <div className="text-sm text-gray-500">Code: {device.code}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {device.totalIncidents.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                      {device.deaths}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-orange-600 font-medium">
                      {device.injuries}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        device.riskScore > 50 ? 'bg-red-100 text-red-800' :
                        device.riskScore > 20 ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {device.riskScore.toFixed(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                      {device.primaryCompany}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'companies' && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('name')}
                  >
                    <div className="flex items-center gap-1">
                      Company Name {getSortIcon('name')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('totalIncidents')}
                  >
                    <div className="flex items-center gap-1">
                      Total Incidents {getSortIcon('totalIncidents')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('deaths')}
                  >
                    <div className="flex items-center gap-1">
                      Deaths {getSortIcon('deaths')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('injuries')}
                  >
                    <div className="flex items-center gap-1">
                      Injuries {getSortIcon('injuries')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('uniqueDevices')}
                  >
                    <div className="flex items-center gap-1">
                      Unique Devices {getSortIcon('uniqueDevices')}
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('riskScore')}
                  >
                    <div className="flex items-center gap-1">
                      Risk Score {getSortIcon('riskScore')}
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredAndSortedCompanies.slice(0, 50).map((company, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 max-w-xs">
                      <div className="truncate" title={company.name}>
                        {company.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {company.totalIncidents.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                      {company.deaths}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-orange-600 font-medium">
                      {company.injuries}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {company.uniqueDevices}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        company.riskScore > 100 ? 'bg-red-100 text-red-800' :
                        company.riskScore > 50 ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {company.riskScore.toFixed(1)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'incidents' && (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              Showing {Math.min(filteredIncidents.length, 100).toLocaleString()} of {filteredIncidents.length.toLocaleString()} incidents
            </p>
            <div className="grid gap-4">
              {filteredIncidents.slice(0, 100).map((incident, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-medium text-gray-900">{incident.deviceName}</h4>
                      <p className="text-sm text-gray-600">{incident.company}</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        incident.isDeath ? 'bg-red-100 text-red-800' :
                        incident.isInjury ? 'bg-orange-100 text-orange-800' :
                        incident.isPotentialHarm ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {incident.severityCode}
                      </span>
                    </div>
                  </div>
                  <div className="flex justify-between text-sm text-gray-500">
                    <span>ID: {incident.id}</span>
                    <span>Receipt: {incident.receiptDate}</span>
                    <span>Risk Class: {incident.riskClass}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ComprehensiveAnalysis;
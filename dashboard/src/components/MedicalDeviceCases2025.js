import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { 
  Heart, 
  AlertTriangle, 
  ExternalLink, 
  Calendar,
  Activity,
  Stethoscope,
  FileText,
  Search,
  Filter,
  BarChart3,
  TrendingUp
} from 'lucide-react';

// Load the 2025 Canadian Medical Device Incidents Data
const medicalDeviceCases2025 = require('../dashboard_data_2025_20251007_163751.json');

const MedicalDeviceCases2025 = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const casesPerPage = 20;

  const filteredCases = useMemo(() => {
    return medicalDeviceCases2025.filter(caseData => {
      const matchesSearch = searchTerm === '' || 
        Object.values(caseData).some(value => 
          value.toString().toLowerCase().includes(searchTerm.toLowerCase())
        );
      
      const matchesSeverity = selectedSeverity === 'all' || 
        (selectedSeverity === 'injury' && caseData.severity === 'INJURY') ||
        (selectedSeverity === 'potential' && caseData.severity === 'POTENTIAL FOR DEATH/INJURY') ||
        (selectedSeverity === 'minimal' && caseData.severity === 'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES');
      
      return matchesSearch && matchesSeverity;
    });
  }, [searchTerm, selectedSeverity]);

  // Pagination
  const totalPages = Math.ceil(filteredCases.length / casesPerPage);
  const startIndex = (currentPage - 1) * casesPerPage;
  const paginatedCases = filteredCases.slice(startIndex, startIndex + casesPerPage);

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'INJURY': return 'bg-red-100 text-red-800 border-red-200';
      case 'POTENTIAL FOR DEATH/INJURY': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'INJURY': return <AlertTriangle className="w-4 h-4 text-red-600" />;
      case 'POTENTIAL FOR DEATH/INJURY': return <Heart className="w-4 h-4 text-orange-600" />;
      default: return <Activity className="w-4 h-4 text-yellow-600" />;
    }
  };

  // Calculate comprehensive statistics
  const stats = useMemo(() => {
    const severityStats = medicalDeviceCases2025.reduce((acc, case_) => {
      acc[case_.severity] = (acc[case_.severity] || 0) + 1;
      return acc;
    }, {});

    const deviceStats = medicalDeviceCases2025.reduce((acc, case_) => {
      const deviceName = case_.deviceName;
      acc[deviceName] = (acc[deviceName] || 0) + 1;
      return acc;
    }, {});

    const topDevices = Object.entries(deviceStats)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 20);

    // Category analysis
    const categories = {
      'INFUSION/PUMP': ['INFUSION', 'PUMP', 'INFUSOMAT'],
      'INSULIN': ['INSULIN', 'T:SLIM'],
      'DIALYSIS': ['DIALYSIS', 'BVM'],
      'SURGICAL': ['SURGICAL', 'CLIP', 'IOL'],
      'IMPLANT': ['IMPLANT', 'BREAST'],
      'CARDIAC': ['CARDIAC', 'HEART', 'PACEMAKER'],
      'MONITORING': ['MONITOR', 'SENSOR'],
      'RESPIRATORY': ['VENTILATOR', 'CPAP', 'OXYGEN']
    };

    const categoryStats = {};
    Object.keys(categories).forEach(cat => categoryStats[cat] = 0);

    Object.entries(deviceStats).forEach(([deviceName, count]) => {
      const deviceUpper = deviceName.toUpperCase();
      for (const [category, keywords] of Object.entries(categories)) {
        if (keywords.some(keyword => deviceUpper.includes(keyword))) {
          categoryStats[category] += count;
          break;
        }
      }
    });

    const sortedCategories = Object.entries(categoryStats)
      .sort(([,a], [,b]) => b - a)
      .filter(([,count]) => count > 0);

    // Statistical summary
    const counts = Object.values(deviceStats);
    const totalDevices = Object.keys(deviceStats).length;
    const totalCases = medicalDeviceCases2025.length;
    const mean = totalCases / totalDevices;
    const median = counts.sort((a, b) => a - b)[Math.floor(counts.length / 2)];
    const max = Math.max(...counts);
    const min = Math.min(...counts);
    const over10 = counts.filter(c => c > 10).length;
    const over50 = counts.filter(c => c > 50).length;
    const over100 = counts.filter(c => c > 100).length;

    return { 
      severityStats, 
      topDevices, 
      categoryStats: sortedCategories,
      summary: {
        totalDevices,
        totalCases,
        mean: mean.toFixed(1),
        median,
        max,
        min,
        over10,
        over50,
        over100
      }
    };
  }, []);

  const Pagination = () => (
    <div className="flex items-center justify-center space-x-2 mt-8">
      <button
        onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
        disabled={currentPage === 1}
        className="px-3 py-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
      >
        Previous
      </button>
      
      <span className="px-4 py-2 text-sm text-gray-600">
        Page {currentPage} of {totalPages} ({filteredCases.length} cases)
      </span>
      
      <button
        onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
        disabled={currentPage === totalPages}
        className="px-3 py-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
      >
        Next
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center mb-4">
            <Stethoscope className="w-8 h-8 text-indigo-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-800">
              Canadian Medical Device Incidents - 2025
            </h1>
          </div>
          <p className="text-xl text-gray-600 mb-2">
            Comprehensive Analysis of All Medical Device Incidents
          </p>
          <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
            <span className="flex items-center">
              <Calendar className="w-4 h-4 mr-1" />
              Data Source: Health Canada Medical Device Incidents Database
            </span>
            <span className="flex items-center">
              <FileText className="w-4 h-4 mr-1" />
              Total Cases: {medicalDeviceCases2025.length}
            </span>
            <span className="flex items-center">
              <TrendingUp className="w-4 h-4 mr-1" />
              Year: 2025
            </span>
          </div>
        </motion.div>

        {/* Search and Filter Controls */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-md p-6 mb-6"
        >
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search by device, company, outcome, evidence..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <select
                value={selectedSeverity}
                onChange={(e) => {
                  setSelectedSeverity(e.target.value);
                  setCurrentPage(1);
                }}
                className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
              >
                <option value="all">All Severities</option>
                <option value="injury">Injury Cases</option>
                <option value="potential">Potential Death/Injury</option>
                <option value="minimal">Minimal/No Consequences</option>
              </select>
            </div>
          </div>
        </motion.div>

        {/* Statistics Cards */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          {['INJURY', 'POTENTIAL FOR DEATH/INJURY', 'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES'].map((severity) => {
            const count = stats.severityStats[severity] || 0;
            const percentage = ((count / medicalDeviceCases2025.length) * 100).toFixed(1);
            
            return (
              <div key={severity} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{severity.replace(/_/g, ' ')}</p>
                    <p className="text-2xl font-bold text-gray-900">{count}</p>
                    <p className="text-sm text-gray-500">{percentage}% of cases</p>
                  </div>
                  <div className="text-3xl">
                    {getSeverityIcon(severity)}
                  </div>
                </div>
              </div>
            );
          })}
        </motion.div>

        {/* Device Categories Analysis */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-md p-6 mb-8"
        >
          <div className="flex items-center mb-4">
            <BarChart3 className="w-5 h-5 text-indigo-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Device Categories Analysis</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {stats.categoryStats.map(([category, count], index) => {
              const percentage = ((count / medicalDeviceCases2025.length) * 100).toFixed(1);
              return (
                <div key={category} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <span className="font-medium text-gray-800">{category}</span>
                    <div className="text-sm text-gray-600">{percentage}% of cases</div>
                  </div>
                  <div className="text-lg font-bold text-indigo-600">{count}</div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Top 20 Devices Ranking */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-md p-6 mb-8"
        >
          <div className="flex items-center mb-4">
            <TrendingUp className="w-5 h-5 text-red-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Top 20 Medical Devices by Incident Count</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">Rank</th>
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">Cases</th>
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">%</th>
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">Device Name</th>
                </tr>
              </thead>
              <tbody>
                {stats.topDevices.map(([device, count], index) => {
                  const percentage = ((count / medicalDeviceCases2025.length) * 100).toFixed(1);
                  const displayDevice = device.length > 60 ? device.substring(0, 60) + '...' : device;
                  return (
                    <tr key={device} className={`border-b border-gray-100 ${index < 3 ? 'bg-red-50' : index < 10 ? 'bg-orange-50' : ''}`}>
                      <td className="py-2 px-3 font-medium">{index + 1}</td>
                      <td className="py-2 px-3 font-bold text-red-600">{count}</td>
                      <td className="py-2 px-3 text-gray-600">{percentage}%</td>
                      <td className="py-2 px-3 text-gray-800">{displayDevice}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Statistical Summary */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-md p-6 mb-8"
        >
          <div className="flex items-center mb-4">
            <Activity className="w-5 h-5 text-green-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Statistical Summary</h3>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{stats.summary.totalDevices}</div>
              <div className="text-sm text-gray-600">Total Devices</div>
            </div>
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{stats.summary.mean}</div>
              <div className="text-sm text-gray-600">Mean Cases/Device</div>
            </div>
            <div className="text-center p-3 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">{stats.summary.median}</div>
              <div className="text-sm text-gray-600">Median Cases</div>
            </div>
            <div className="text-center p-3 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{stats.summary.max}</div>
              <div className="text-sm text-gray-600">Max Cases</div>
            </div>
            <div className="text-center p-3 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{stats.summary.over100}</div>
              <div className="text-sm text-gray-600">Devices {'>'}100 Cases</div>
            </div>
            <div className="text-center p-3 bg-indigo-50 rounded-lg">
              <div className="text-2xl font-bold text-indigo-600">{stats.summary.over50}</div>
              <div className="text-sm text-gray-600">Devices {'>'}50 Cases</div>
            </div>
            <div className="text-center p-3 bg-pink-50 rounded-lg">
              <div className="text-2xl font-bold text-pink-600">{stats.summary.over10}</div>
              <div className="text-sm text-gray-600">Devices {'>'}10 Cases</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-600">{stats.summary.min}</div>
              <div className="text-sm text-gray-600">Min Cases</div>
            </div>
          </div>
        </motion.div>

        {/* Cases Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {paginatedCases.map((caseData, index) => (
            <motion.div
              key={caseData.caseId}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      {getSeverityIcon(caseData.severity)}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Case #{caseData.caseId}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Incident ID: {caseData.mdrNumber}
                      </p>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getSeverityColor(caseData.severity)}`}>
                    Score: {caseData.severityScore}/10
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center text-sm">
                    <Calendar className="w-4 h-4 text-gray-400 mr-2 flex-shrink-0" />
                    <span className="text-gray-600">Event Date:</span>
                    <span className="ml-2 font-medium">{caseData.eventDate}</span>
                  </div>
                  
                  <div className="flex items-start text-sm">
                    <Stethoscope className="w-4 h-4 text-gray-400 mr-2 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="text-gray-600">Device:</span>
                      <span className="ml-2 font-medium block">{caseData.deviceName}</span>
                    </div>
                  </div>

                  <div className="flex items-start text-sm">
                    <AlertTriangle className="w-4 h-4 text-gray-400 mr-2 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="text-gray-600">Malfunction:</span>
                      <span className="ml-2 block text-gray-900">{caseData.malfunction}</span>
                    </div>
                  </div>

                  <div className="flex items-start text-sm">
                    <Heart className="w-4 h-4 text-gray-400 mr-2 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="text-gray-600">Outcome:</span>
                      <span className="ml-2 block font-medium text-red-600">{caseData.outcome}</span>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="flex items-start text-sm">
                      <FileText className="w-4 h-4 text-gray-400 mr-2 flex-shrink-0 mt-0.5" />
                      <div>
                        <span className="text-gray-600 font-medium">Evidence:</span>
                        <p className="mt-1 text-gray-700 leading-relaxed">{caseData.evidence}</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-xs text-gray-500">
                    <div>
                      <span className="font-medium">Device Code:</span>
                      <br />{caseData.deviceCode}
                    </div>
                    <div>
                      <span className="font-medium">Risk Class:</span>
                      <br />{caseData.riskClass}
                    </div>
                    <div>
                      <span className="font-medium">Report Type:</span>
                      <br />{caseData.reportType}
                    </div>
                    <div>
                      <span className="font-medium">Usage:</span>
                      <br />{caseData.usage}
                    </div>
                  </div>

                  <div className="pt-3 border-t border-gray-200">
                    <a
                      href={caseData.fdaLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-800 transition-colors duration-200"
                    >
                      <ExternalLink className="w-4 h-4 mr-1" />
                      View Canadian Medical Device Incident Report
                    </a>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <Pagination />

        {/* Summary Footer */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 bg-white rounded-lg shadow-md p-6 text-center"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            2025 Canadian Medical Device Incidents - Comprehensive Analysis
          </h3>
          <p className="text-gray-600 max-w-4xl mx-auto">
            This dashboard presents {medicalDeviceCases2025.length} medical device incidents from {stats.summary.totalDevices} different 
            devices in the Canadian Medical Device Incidents database for 2025. The analysis reveals that INFUSION/PUMP 
            devices account for {stats.categoryStats.length > 0 ? ((stats.categoryStats[0][1] / medicalDeviceCases2025.length) * 100).toFixed(1) : '0'}% of all incidents, 
            with the SPACE INFUSION SYSTEM leading at {stats.topDevices.length > 0 ? stats.topDevices[0][1] : '0'} cases. 
            Each case includes detailed evidence of device malfunctions and clinical outcomes.
          </p>
          <div className="mt-4 text-sm text-gray-500">
            <p>Data Source: Health Canada Medical Device Incidents Database</p>
            <p>Analysis Date: {new Date().toLocaleDateString()}</p>
            <p>Showing {filteredCases.length} of {medicalDeviceCases2025.length} total cases across {stats.summary.totalDevices} device types</p>
            <p>Top Risk Category: INFUSION/PUMP devices ({stats.categoryStats.length > 0 ? stats.categoryStats[0][1] : '0'} incidents)</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default MedicalDeviceCases2025;
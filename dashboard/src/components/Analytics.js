import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  BarChart3,
  PieChart,
  TrendingUp,
  Filter,
  Download,
  Calendar,
  Search,
  RefreshCw
} from 'lucide-react';
import { Bar, Line, Scatter } from 'react-chartjs-2';

function FilterPanel({ filters, setFilters, onApply }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-card p-6 mb-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          <Filter className="w-5 h-5 mr-2" />
          Filters & Analysis Options
        </h3>
        <button
          onClick={onApply}
          className="btn-primary"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Apply Filters
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Date Range
          </label>
          <select
            value={filters.dateRange}
            onChange={(e) => setFilters({...filters, dateRange: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Time</option>
            <option value="last3months">Last 3 Months</option>
            <option value="last6months">Last 6 Months</option>
            <option value="lastyear">Last Year</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Severity Level
          </label>
          <select
            value={filters.severity}
            onChange={(e) => setFilters({...filters, severity: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Severities</option>
            <option value="DEATH">Death</option>
            <option value="INJURY">Injury</option>
            <option value="POTENTIAL">Potential for Death/Injury</option>
            <option value="MINIMAL">Minimal/No Consequences</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Device Category
          </label>
          <select
            value={filters.deviceCategory}
            onChange={(e) => setFilters({...filters, deviceCategory: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Categories</option>
            <option value="GENERAL HOSPITAL">General Hospital</option>
            <option value="CARDIOVASCULAR">Cardiovascular</option>
            <option value="ORTHOPAEDICS">Orthopaedics</option>
            <option value="SURGERY">Surgery</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Report Type
          </label>
          <select
            value={filters.reportType}
            onChange={(e) => setFilters({...filters, reportType: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Types</option>
            <option value="mandatory">Mandatory Reports</option>
            <option value="voluntary">Voluntary Reports</option>
            <option value="recall">Recall Related</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Company Search
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              value={filters.companySearch}
              onChange={(e) => setFilters({...filters, companySearch: e.target.value})}
              placeholder="Search companies..."
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function StatisticalSummary() {
  const stats = [
    {
      title: "Average Incidents per Month",
      value: "871",
      change: "+8.2%",
      trend: "up"
    },
    {
      title: "Most Common Severity",
      value: "Injury",
      subtitle: "37.3% of all incidents"
    },
    {
      title: "Peak Incident Month",
      value: "January 2025",
      subtitle: "1,179 incidents"
    },
    {
      title: "Fatality Rate",
      value: "1.8%",
      change: "-0.3%",
      trend: "down"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white rounded-lg shadow-card p-6"
        >
          <h4 className="text-sm font-medium text-gray-600">{stat.title}</h4>
          <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
          {stat.change && (
            <p className={`text-sm mt-1 ${stat.trend === 'up' ? 'text-red-600' : 'text-green-600'}`}>
              {stat.change}
            </p>
          )}
          {stat.subtitle && (
            <p className="text-sm text-gray-500 mt-1">{stat.subtitle}</p>
          )}
        </motion.div>
      ))}
    </div>
  );
}

function AdvancedCharts() {
  // Correlation Analysis Chart
  const correlationData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
    datasets: [
      {
        label: 'High-Risk Devices',
        data: [65, 78, 82, 91, 87, 95, 102, 88],
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        yAxisID: 'y',
      },
      {
        label: 'Incident Severity Score',
        data: [3.2, 3.8, 4.1, 4.5, 4.2, 4.7, 5.1, 4.4],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        yAxisID: 'y1',
      }
    ],
  };

  const correlationOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Month'
        }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Number of High-Risk Devices'
        }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Average Severity Score'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
    plugins: {
      title: {
        display: true,
        text: 'Correlation: High-Risk Devices vs Incident Severity'
      }
    }
  };

  // Device Category Analysis
  const categoryData = {
    labels: [
      'General Hospital',
      'Cardiovascular',
      'Orthopaedics',
      'Surgery',
      'Gastroenterology',
      'Anesthesiology',
      'Chemistry',
      'Ophthalmology'
    ],
    datasets: [
      {
        label: 'Incidents',
        data: [2274, 1044, 895, 1374, 699, 296, 277, 123],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(139, 92, 246, 0.8)',
          'rgba(236, 72, 153, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(251, 146, 60, 0.8)'
        ],
        borderColor: [
          'rgba(59, 130, 246, 1)',
          'rgba(16, 185, 129, 1)',
          'rgba(245, 158, 11, 1)',
          'rgba(239, 68, 68, 1)',
          'rgba(139, 92, 246, 1)',
          'rgba(236, 72, 153, 1)',
          'rgba(34, 197, 94, 1)',
          'rgba(251, 146, 60, 1)'
        ],
        borderWidth: 2
      }
    ]
  };

  const categoryOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Incidents by Device Category'
      },
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Number of Incidents'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Device Category'
        }
      }
    }
  };

  // Risk Assessment Scatter Plot
  const riskData = {
    datasets: [
      {
        label: 'Device Risk Profile',
        data: [
          { x: 291, y: 4.2 }, // Space Infusion System
          { x: 224, y: 3.8 }, // T:SLIM Control-IQ
          { x: 176, y: 3.1 }, // Infusomat Space Pump
          { x: 171, y: 4.0 }, // T:SLIM X2
          { x: 170, y: 2.9 }, // Prismax Control
          { x: 148, y: 3.5 }, // Dexcom G7
          { x: 132, y: 2.7 }, // Lifeline Beta
          { x: 114, y: 2.4 }, // Novum IQ
          { x: 110, y: 4.8 }, // Breast Implant
          { x: 105, y: 3.2 }  // Legion Pressfit
        ],
        backgroundColor: 'rgba(239, 68, 68, 0.6)',
        borderColor: 'rgba(239, 68, 68, 1)',
        pointRadius: 8,
        pointHoverRadius: 10
      }
    ]
  };

  const riskOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Device Risk Assessment (Incidents vs Severity)'
      },
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Number of Incidents'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Average Severity Score (1-5)'
        },
        min: 0,
        max: 5
      }
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <div className="bg-white rounded-lg shadow-card p-6 h-96">
        <Line data={correlationData} options={correlationOptions} />
      </div>
      <div className="bg-white rounded-lg shadow-card p-6 h-96">
        <Scatter data={riskData} options={riskOptions} />
      </div>
      <div className="lg:col-span-2 bg-white rounded-lg shadow-card p-6 h-96">
        <Bar data={categoryData} options={categoryOptions} />
      </div>
    </div>
  );
}

function DataInsights() {
  const insights = [
    {
      title: "Seasonal Pattern Detected",
      description: "January shows consistently higher incident rates, possibly due to increased hospital activity post-holidays.",
      type: "trend",
      confidence: "High",
      impact: "Medium"
    },
    {
      title: "Device Category Risk Correlation",
      description: "General hospital devices account for 32.6% of all incidents, suggesting need for enhanced monitoring.",
      type: "correlation",
      confidence: "High",
      impact: "High"
    },
    {
      title: "Manufacturer Concentration",
      description: "Top 5 companies account for 35% of all incidents, indicating potential systematic issues.",
      type: "concentration",
      confidence: "Medium",
      impact: "High"
    },
    {
      title: "Severity Improvement Trend",
      description: "Death rate has decreased by 0.3% compared to previous period, showing improving safety measures.",
      type: "improvement",
      confidence: "High",
      impact: "Low"
    }
  ];

  const getInsightColor = (type) => {
    switch (type) {
      case 'trend': return 'border-blue-200 bg-blue-50';
      case 'correlation': return 'border-purple-200 bg-purple-50';
      case 'concentration': return 'border-red-200 bg-red-50';
      case 'improvement': return 'border-green-200 bg-green-50';
      default: return 'border-gray-200 bg-gray-50';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Insights & Recommendations</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {insights.map((insight, index) => (
          <motion.div
            key={insight.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`border rounded-lg p-4 ${getInsightColor(insight.type)}`}
          >
            <h4 className="font-medium text-gray-900 mb-2">{insight.title}</h4>
            <p className="text-sm text-gray-700 mb-3">{insight.description}</p>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <span className="text-xs text-gray-600">
                  Confidence: <span className="font-medium">{insight.confidence}</span>
                </span>
                <span className="text-xs text-gray-600">
                  Impact: <span className="font-medium">{insight.impact}</span>
                </span>
              </div>
              <span className="text-xs px-2 py-1 bg-white rounded-full border">
                {insight.type}
              </span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function Analytics() {
  const [filters, setFilters] = useState({
    dateRange: 'all',
    severity: 'all',
    deviceCategory: 'all',
    reportType: 'all',
    companySearch: ''
  });

  const handleApplyFilters = () => {
    // In a real app, this would trigger data refetch with new filters
    console.log('Applying filters:', filters);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Advanced Analytics</h1>
          <p className="text-gray-600 mt-1">
            Deep dive into medical device incident patterns and correlations
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary">
            <Download className="w-4 h-4 mr-2" />
            Export Analysis
          </button>
          <button className="btn-primary">
            <BarChart3 className="w-4 h-4 mr-2" />
            Custom Report
          </button>
        </div>
      </div>

      {/* Filters */}
      <FilterPanel 
        filters={filters} 
        setFilters={setFilters} 
        onApply={handleApplyFilters} 
      />

      {/* Statistical Summary */}
      <StatisticalSummary />

      {/* Advanced Charts */}
      <AdvancedCharts />

      {/* Data Insights */}
      <DataInsights />
    </div>
  );
}

export default Analytics;
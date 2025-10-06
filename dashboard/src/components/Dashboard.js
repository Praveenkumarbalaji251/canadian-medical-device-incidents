import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Activity,
  AlertTriangle,
  TrendingUp,
  Calendar,
  Users,
  Building2,
  Stethoscope,
  Shield,
  ArrowUp,
  ArrowDown,
  Minus
} from 'lucide-react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// Mock data - in a real app, this would come from your API
const mockData = {
  totalIncidents: 6970,
  monthlyGrowth: 8.5,
  criticalIncidents: 124,
  activeDevices: 8175,
  companiesInvolved: 16067,
  averageResolutionTime: "14 days",
  monthlyData: [
    { month: '2024-09', incidents: 627, deaths: 12, injuries: 245 },
    { month: '2024-10', incidents: 882, deaths: 18, injuries: 332 },
    { month: '2024-11', incidents: 854, deaths: 15, injuries: 298 },
    { month: '2024-12', incidents: 822, deaths: 14, injuries: 287 },
    { month: '2025-01', incidents: 1179, deaths: 23, injuries: 421 },
    { month: '2025-02', incidents: 872, deaths: 16, injuries: 314 },
    { month: '2025-03', incidents: 936, deaths: 19, injuries: 342 },
    { month: '2025-04', incidents: 798, deaths: 7, injuries: 288 }
  ],
  severityData: {
    'DEATH': 124,
    'INJURY': 2597,
    'POTENTIAL FOR DEATH/INJURY': 2386,
    'MINIMAL/NO ADVERSE HEALTH CONSEQUENCES': 1450,
    'UNASSIGNED': 413
  },
  topDevices: [
    { name: 'SPACE INFUSION SYSTEM', incidents: 291, trend: 'up' },
    { name: 'T:SLIM/CONTROL-IQ', incidents: 224, trend: 'down' },
    { name: 'INFUSOMAT SPACE PUMP', incidents: 176, trend: 'up' },
    { name: 'T:SLIM X2 INSULIN PUMP', incidents: 171, trend: 'stable' },
    { name: 'PRISMAX CONTROL UNIT', incidents: 170, trend: 'up' }
  ],
  topCompanies: [
    { name: 'TANDEM DIABETES CARE', incidents: 731, severity: 'high' },
    { name: 'JOHNSON & JOHNSON MEDTECH', incidents: 614, severity: 'medium' },
    { name: 'ABBVIE CORPORATION', incidents: 542, severity: 'medium' },
    { name: 'BOSTON SCIENTIFIC', incidents: 416, severity: 'low' },
    { name: 'MEDTRONIC CANADA', incidents: 397, severity: 'low' }
  ]
};

function MetricCard({ title, value, subtitle, icon: Icon, trend, color = "blue" }) {
  const colorClasses = {
    blue: "from-blue-500 to-blue-600",
    green: "from-green-500 to-green-600",
    red: "from-red-500 to-red-600",
    yellow: "from-yellow-500 to-yellow-600",
    purple: "from-purple-500 to-purple-600",
    indigo: "from-indigo-500 to-indigo-600"
  };

  const getTrendIcon = () => {
    if (trend === 'up') return <ArrowUp className="w-4 h-4 text-green-500" />;
    if (trend === 'down') return <ArrowDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="metric-card"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {subtitle && (
            <div className="flex items-center mt-2">
              {trend && getTrendIcon()}
              <p className="text-sm text-gray-500 ml-1">{subtitle}</p>
            </div>
          )}
        </div>
        <div className={`w-12 h-12 bg-gradient-to-r ${colorClasses[color]} rounded-lg flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </motion.div>
  );
}

function TrendChart() {
  const chartData = {
    labels: mockData.monthlyData.map(d => d.month),
    datasets: [
      {
        label: 'Total Incidents',
        data: mockData.monthlyData.map(d => d.incidents),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: 'rgb(59, 130, 246)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6,
      },
      {
        label: 'Deaths',
        data: mockData.monthlyData.map(d => d.deaths),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderWidth: 2,
        fill: false,
        tension: 0.4,
        pointBackgroundColor: 'rgb(239, 68, 68)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20
        }
      },
      title: {
        display: true,
        text: 'Monthly Incident Trends',
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    }
  };

  return (
    <div className="chart-container h-80">
      <Line data={chartData} options={options} />
    </div>
  );
}

function SeverityChart() {
  const chartData = {
    labels: Object.keys(mockData.severityData),
    datasets: [
      {
        data: Object.values(mockData.severityData),
        backgroundColor: [
          '#dc2626', // DEATH - Red
          '#f59e0b', // INJURY - Orange
          '#eab308', // POTENTIAL - Yellow
          '#22c55e', // MINIMAL - Green
          '#6b7280'  // UNASSIGNED - Gray
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true
        }
      },
      title: {
        display: true,
        text: 'Incidents by Severity Level',
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    }
  };

  return (
    <div className="chart-container h-80">
      <Doughnut data={chartData} options={options} />
    </div>
  );
}

function TopDevicesList() {
  return (
    <div className="chart-container">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Devices by Incidents</h3>
      <div className="space-y-4">
        {mockData.topDevices.map((device, index) => (
          <motion.div
            key={device.name}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-sm font-bold text-blue-600">{index + 1}</span>
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">{device.name}</p>
                <p className="text-xs text-gray-500">{device.incidents} incidents</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {device.trend === 'up' && <ArrowUp className="w-4 h-4 text-red-500" />}
              {device.trend === 'down' && <ArrowDown className="w-4 h-4 text-green-500" />}
              {device.trend === 'stable' && <Minus className="w-4 h-4 text-gray-400" />}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function TopCompaniesList() {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="chart-container">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Companies by Incidents</h3>
      <div className="space-y-4">
        {mockData.topCompanies.map((company, index) => (
          <motion.div
            key={company.name}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <span className="text-sm font-bold text-purple-600">{index + 1}</span>
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">{company.name}</p>
                <p className="text-xs text-gray-500">{company.incidents} incidents</p>
              </div>
            </div>
            <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getSeverityColor(company.severity)}`}>
              {company.severity}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function RecentAlerts() {
  const alerts = [
    {
      id: 1,
      type: 'critical',
      title: 'High-risk device incident reported',
      description: 'T:SLIM insulin pump malfunction resulted in patient hospitalization',
      time: '2 hours ago'
    },
    {
      id: 2,
      type: 'warning',
      title: 'Increased incidents for device category',
      description: 'Infusion pumps showing 15% increase in reported incidents',
      time: '4 hours ago'
    },
    {
      id: 3,
      type: 'info',
      title: 'Monthly report available',
      description: 'April 2025 incident summary report is ready for review',
      time: '1 day ago'
    }
  ];

  const getAlertIcon = (type) => {
    switch (type) {
      case 'critical': return <AlertTriangle className="w-5 h-5 text-red-500" />;
      case 'warning': return <Shield className="w-5 h-5 text-yellow-500" />;
      default: return <Activity className="w-5 h-5 text-blue-500" />;
    }
  };

  const getAlertStyle = (type) => {
    switch (type) {
      case 'critical': return 'border-l-red-500 bg-red-50';
      case 'warning': return 'border-l-yellow-500 bg-yellow-50';
      default: return 'border-l-blue-500 bg-blue-50';
    }
  };

  return (
    <div className="chart-container">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h3>
      <div className="space-y-3">
        {alerts.map((alert, index) => (
          <motion.div
            key={alert.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`border-l-4 p-4 rounded-r-lg ${getAlertStyle(alert.type)}`}
          >
            <div className="flex items-start space-x-3">
              {getAlertIcon(alert.type)}
              <div className="flex-1">
                <h4 className="text-sm font-medium text-gray-900">{alert.title}</h4>
                <p className="text-sm text-gray-600 mt-1">{alert.description}</p>
                <p className="text-xs text-gray-500 mt-2">{alert.time}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Data Coverage Warning */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-r-lg"
      >
        <div className="flex">
          <div className="flex-shrink-0">
            <AlertTriangle className="h-5 w-5 text-amber-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-amber-800">
              Data Coverage: 8 Months Available (Missing Recent Data)
            </h3>
            <div className="mt-2 text-sm text-amber-700">
              <p>
                Analysis covers <strong>September 2024 - April 2025</strong> only. 
                Missing: <strong>May-October 2025</strong> due to Health Canada reporting delays.
                See comprehensive analysis for complete explanation.
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
          <p className="text-gray-600 mt-1">
            Medical Device Incidents • September 2024 - April 2025 (8 Months Available)
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary">
            <Calendar className="w-4 h-4 mr-2" />
            8 Months Data
          </button>
          <button className="btn-primary">
            <TrendingUp className="w-4 h-4 mr-2" />
            Generate Report
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Incidents"
          value={mockData.totalIncidents.toLocaleString()}
          subtitle={`+${mockData.monthlyGrowth}% from last month`}
          icon={Activity}
          trend="up"
          color="blue"
        />
        <MetricCard
          title="Critical Incidents"
          value={mockData.criticalIncidents}
          subtitle="Deaths reported"
          icon={AlertTriangle}
          color="red"
        />
        <MetricCard
          title="Devices Involved"
          value={mockData.activeDevices.toLocaleString()}
          subtitle="Active medical devices"
          icon={Stethoscope}
          color="purple"
        />
        <MetricCard
          title="Companies Involved"
          value={mockData.companiesInvolved.toLocaleString()}
          subtitle="Reporting entities"
          icon={Building2}
          color="green"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TrendChart />
        <SeverityChart />
      </div>

      {/* Lists and Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <TopDevicesList />
        <TopCompaniesList />
        <RecentAlerts />
      </div>
    </div>
  );
}

export default Dashboard;
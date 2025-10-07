import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  AlertTriangle, 
  BarChart3, 
  Calendar, 
  Download, 
  Filter,
  Heart,
  Home,
  Settings,
  TrendingUp,
  Users,
  Building2,
  Stethoscope,
  Shield,
  MessageSquare,
  Scale
} from 'lucide-react';

// Import components
import Dashboard from './components/Dashboard';
import Analytics from './components/Analytics';
import DeviceAnalysis from './components/DeviceAnalysis';
import OptimizedAllIncidents from './components/OptimizedAllIncidents';
import ComprehensiveAnalysis from './components/ComprehensiveAnalysis';
import CompanyAnalysis from './components/CompanyAnalysis';
import TrendAnalysis from './components/TrendAnalysis';
import SeverityAnalysis from './components/SeverityAnalysis';
import DataUpload from './components/DataUpload';
import RedditEvidence from './components/RedditEvidence';
import OptimizedPotentialLegalDevices from './components/OptimizedPotentialLegalDevices';
import ComprehensiveRedditEvidence from './components/ComprehensiveRedditEvidence';
import CardiacArrestCases from './components/CardiacArrestCases';

// Navigation items
const navigationItems = [
  { name: 'Dashboard', href: '/', icon: Home, color: 'text-blue-600' },
  { name: 'All Incidents', href: '/incidents', icon: AlertTriangle, color: 'text-red-600' },
  { name: 'Cardiac Arrest Deaths', href: '/cardiac-deaths', icon: Heart, color: 'text-red-700' },
  { name: 'Legal Devices', href: '/legal', icon: Scale, color: 'text-purple-600' },
  { name: 'All Reddit Evidence', href: '/reddit-all', icon: MessageSquare, color: 'text-indigo-600' },
  { name: 'Reddit Evidence', href: '/reddit', icon: MessageSquare, color: 'text-indigo-500' },
  { name: 'Comprehensive', href: '/comprehensive', icon: BarChart3, color: 'text-emerald-600' },
  { name: 'Analytics', href: '/analytics', icon: TrendingUp, color: 'text-green-600' },
  { name: 'Device Analysis', href: '/devices', icon: Stethoscope, color: 'text-purple-600' },
  { name: 'Company Analysis', href: '/companies', icon: Building2, color: 'text-orange-600' },
  { name: 'Severity Analysis', href: '/severity', icon: Shield, color: 'text-gray-600' },
];

function Navigation() {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className={`bg-white shadow-lg transition-all duration-300 ${isCollapsed ? 'w-16' : 'w-64'}`}>
      <div className="p-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          {!isCollapsed && (
            <div>
              <h1 className="text-lg font-bold text-gray-900">MDI Dashboard</h1>
              <p className="text-xs text-gray-500">Medical Device Incidents</p>
            </div>
          )}
        </div>
        
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="mt-4 w-full flex items-center justify-center p-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <Filter className="w-5 h-5" />
        </button>
      </div>

      <nav className="mt-8">
        <div className="px-4 space-y-2">
          {navigationItems.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <item.icon
                  className={`flex-shrink-0 w-5 h-5 ${
                    isActive ? item.color : 'text-gray-400 group-hover:text-gray-600'
                  }`}
                />
                {!isCollapsed && (
                  <span className="ml-3 truncate">{item.name}</span>
                )}
                {isActive && !isCollapsed && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="ml-auto w-2 h-2 bg-blue-600 rounded-full"
                  />
                )}
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}

function Header() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            Medical Device Incidents Dashboard
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Real-time analysis of Canadian medical device incident data
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <p className="text-sm font-medium text-gray-900">
              {currentTime.toLocaleDateString('en-CA')}
            </p>
            <p className="text-xs text-gray-500">
              {currentTime.toLocaleTimeString('en-CA')}
            </p>
          </div>
          
          <div className="flex items-center space-x-2">
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
              <Download className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => setIsLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-primary rounded-full flex items-center justify-center mb-4 mx-auto">
            <Heart className="w-8 h-8 text-white animate-pulse" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Loading Dashboard
          </h2>
          <p className="text-gray-600">
            Preparing your medical device incidents data...
          </p>
          <div className="mt-4 w-64 h-2 bg-gray-200 rounded-full mx-auto overflow-hidden">
            <div className="h-full bg-gradient-primary rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex">
        <Navigation />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          
          <main className="flex-1 overflow-auto">
            <div className="p-6">
              <AnimatePresence mode="wait">
                <motion.div
                  key={window.location.pathname}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/incidents" element={<OptimizedAllIncidents />} />
                    <Route path="/cardiac-deaths" element={<CardiacArrestCases />} />
                    <Route path="/legal" element={<OptimizedPotentialLegalDevices />} />
                    <Route path="/reddit-all" element={<ComprehensiveRedditEvidence />} />
                    <Route path="/reddit" element={<RedditEvidence />} />
                    <Route path="/comprehensive" element={<ComprehensiveAnalysis />} />
                    <Route path="/analytics" element={<Analytics />} />
                    <Route path="/devices" element={<DeviceAnalysis />} />
                    <Route path="/companies" element={<CompanyAnalysis />} />
                    <Route path="/trends" element={<TrendAnalysis />} />
                    <Route path="/severity" element={<SeverityAnalysis />} />
                    <Route path="/upload" element={<DataUpload />} />
                  </Routes>
                </motion.div>
              </AnimatePresence>
            </div>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
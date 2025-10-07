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
  Filter
} from 'lucide-react';

// Cardiac Arrest Death Cases Data
const cardiacArrestCases = [
  {
    caseId: 1,
    mdrNumber: "20852645",
    eventDate: "05-28-2024",
    deviceName: "INFUSOMAT (B. BRAUN MEDICAL INC.)",
    medication: "Norepinephrine",
    malfunction: "Air in line alarm malfunction",
    outcome: "Patient died after cardiac arrest unrelated to IV pump issue",
    severityScore: 8,
    evidence: "Air alarm system failed during critical vasopressor delivery, interrupting life-sustaining medication flow",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=20852645"
  },
  {
    caseId: 2,
    mdrNumber: "20860983",
    eventDate: "06-26-2024",
    deviceName: "INFUSOMAT® (B. BRAUN AVITUM AG)",
    medication: "Norepinephrine",
    malfunction: "Upstream occlusion alarm during vasopressor infusion",
    outcome: "Cardiac arrest, survived arrest but died next day",
    severityScore: 8,
    evidence: "Occlusion detection malfunction stopped norepinephrine delivery during critical care, leading to hemodynamic collapse",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=20860983"
  },
  {
    caseId: 3,
    mdrNumber: "19745909",
    eventDate: "05-17-2024",
    deviceName: "INFUSOMAT® (B. BRAUN AVITUM AG)",
    medication: "Levophed (norepinephrine)",
    malfunction: "Repetitive air bubble alarms and occlusion alarms",
    outcome: "Cardiac arrest, cardiogenic shock, multiorgan failure, death",
    severityScore: 10,
    evidence: "Multiple false alarms caused repeated interruption of vasopressor therapy, resulting in cardiovascular collapse",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=19745909"
  },
  {
    caseId: 4,
    mdrNumber: "19533326",
    eventDate: "05-18-2024",
    deviceName: "INFUSOMAT® (B. BRAUN AVITUM AG)",
    medication: "Norepinephrine",
    malfunction: "Air-in-line alarms",
    outcome: "Heart rate and BP dropped, unable to resuscitate",
    severityScore: 8,
    evidence: "Air detection system malfunction interrupted continuous vasopressor infusion, causing immediate hemodynamic instability",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=19533326"
  },
  {
    caseId: 5,
    mdrNumber: "19172359",
    eventDate: "03-04-2024",
    deviceName: "INFUSOMAT® (B. BRAUN MEDICAL INC.)",
    medication: "Epinephrine",
    malfunction: "Delay in programming and locking mechanism issue",
    outcome: "7-minute delay in traumatic cardiac arrest, patient died in OR",
    severityScore: 8,
    evidence: "Device programming failure caused critical 7-minute delay in epinephrine administration during cardiac arrest",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=19172359"
  },
  {
    caseId: 6,
    mdrNumber: "19078060",
    eventDate: "No date provided",
    deviceName: "INFUSOMAT® (B. BRAUN AVITUM AG)",
    medication: "Norepinephrine and Vasopressin",
    malfunction: "Alarm malfunction leading to medication delivery interruption",
    outcome: "Patient arrived in cardiac arrest, died at 0233 hours",
    severityScore: 9,
    evidence: "Alarm system failure interrupted dual vasopressor therapy, preventing hemodynamic support during critical transport",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=19078060"
  },
  {
    caseId: 7,
    mdrNumber: "18948564",
    eventDate: "11-20-2023",
    deviceName: "INFUSOMAT ® (B. BRAUN MELSUNGEN AG)",
    medication: "Noradrenaline",
    malfunction: "Medication underflow due to device malfunction",
    outcome: "Patient passed away, case raised as coroner's case",
    severityScore: 8,
    evidence: "Pump underdelivery of noradrenaline resulted in inadequate vasopressor support, case escalated to coroner investigation",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=18948564"
  },
  {
    caseId: 8,
    mdrNumber: "18845790",
    eventDate: "02-05-2024",
    deviceName: "INFUSOMAT® (B. BRAUN AVITUM AG)",
    medication: "Unspecified critical medication",
    malfunction: "Unidentified problem leading to device failure",
    outcome: "13 pumps with unidentified problem, patient passed away",
    severityScore: 10,
    evidence: "Simultaneous failure of 13 infusion pumps with unknown etiology, causing complete loss of critical care medication delivery",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=18845790"
  },
  {
    caseId: 9,
    mdrNumber: "18521112",
    eventDate: "12-17-2023",
    deviceName: "INFUSOMAT ® (B. BRAUN MELSUNGEN AG)",
    medication: "Noradrenaline",
    malfunction: "Pressure alarms leading to infusion interruption",
    outcome: "CPR performed, pump found dysfunctional, patient died",
    severityScore: 8,
    evidence: "Pressure alarm malfunction stopped noradrenaline infusion during code blue event, pump confirmed non-functional post-mortem",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=18521112"
  },
  {
    caseId: 10,
    mdrNumber: "18411458",
    eventDate: "12-14-2023",
    deviceName: "INFUSOMAT® (B. BRAUN AVITUM AG)",
    medication: "Epinephrine and Dopamine",
    malfunction: "Intermittent pump failures and air-in-line alarms",
    outcome: "Code blue, multiple CPR rounds, care withdrawn",
    severityScore: 9,
    evidence: "Intermittent device failures disrupted continuous inotropic support, requiring multiple resuscitation attempts before care withdrawal",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=18411458"
  },
  {
    caseId: 11,
    mdrNumber: "15340971",
    eventDate: "08-17-2022",
    deviceName: "INFUSOMAT SPACE (B. BRAUN AVITUM AG)",
    medication: "Vasoactive amines (vasopressors)",
    malfunction: "Device stopped working without alarm",
    outcome: "Cardiorespiratory arrest, asystole, patient died",
    severityScore: 10,
    evidence: "Silent pump failure with no alarm notification, complete cessation of vasopressor delivery leading to asystolic arrest",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=15340971"
  },
  {
    caseId: 12,
    mdrNumber: "12706566",
    eventDate: "09-23-2021",
    deviceName: "INFUSOMAT (B. BRAUN MEDICAL INC.)",
    medication: "Vasopressor",
    malfunction: "Pump failure during vasopressor infusion",
    outcome: "Device stopped working, cardiac arrest, death",
    severityScore: 9,
    evidence: "Complete pump failure during continuous vasopressor therapy, immediate hemodynamic collapse and cardiac arrest",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=12706566"
  },
  {
    caseId: 13,
    mdrNumber: "12061340",
    eventDate: "06-08-2021",
    deviceName: "INFUSOMAT (B. BRAUN MEDICAL INC.)",
    medication: "Noradrenaline",
    malfunction: "Overinfusion of medication (100ml/h vs prescribed rate)",
    outcome: "Cardiac arrest at 8:30 PM, patient died from overinfusion",
    severityScore: 9,
    evidence: "Rate control failure delivered 100ml/h noradrenaline instead of prescribed dose, causing fatal drug overdose and cardiac arrest",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=12061340"
  },
  {
    caseId: 14,
    mdrNumber: "5701644",
    eventDate: "05-04-2016",
    deviceName: "INFUSOMAT SPACE (B. BRAUN MEDICAL INC.)",
    medication: "Norepinephrine",
    malfunction: "Medication infusion error leading to over-infusion",
    outcome: "Over-infusion, respiratory and cardiac code, patient expired",
    severityScore: 9,
    evidence: "Infusion rate error caused norepinephrine overdose, triggering respiratory failure followed by cardiac arrest",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=5701644"
  },
  {
    caseId: 15,
    mdrNumber: "5050444",
    eventDate: "01-27-2015",
    deviceName: "INFUSOMAT SPACE (B. BRAUN MEDICAL INC.)",
    medication: "Total Parenteral Nutrition (TPN)",
    malfunction: "Medication infusion rate discrepancy",
    outcome: "10-hour infusion finished in 1 hour, 'too few drops' alarm, cardiac arrest, death",
    severityScore: 9,
    evidence: "Rate control malfunction delivered 10-hour TPN infusion in 1 hour, causing massive fluid overload and cardiac arrest",
    fdaLink: "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=5050444"
  }
];

const CardiacArrestCases = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [selectedDevice, setSelectedDevice] = useState('all');

  // Filter and search logic
  const filteredCases = useMemo(() => {
    return cardiacArrestCases.filter(case_ => {
      const matchesSearch = 
        case_.mdrNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        case_.deviceName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        case_.medication.toLowerCase().includes(searchTerm.toLowerCase()) ||
        case_.malfunction.toLowerCase().includes(searchTerm.toLowerCase()) ||
        case_.evidence.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesSeverity = selectedSeverity === 'all' || case_.severityScore.toString() === selectedSeverity;
      
      const matchesDevice = selectedDevice === 'all' || case_.deviceName.includes(selectedDevice);
      
      return matchesSearch && matchesSeverity && matchesDevice;
    });
  }, [searchTerm, selectedSeverity, selectedDevice]);

  // Get unique devices for filter
  const uniqueDevices = [...new Set(cardiacArrestCases.map(case_ => {
    if (case_.deviceName.includes('INFUSOMAT SPACE')) return 'INFUSOMAT SPACE';
    if (case_.deviceName.includes('INFUSOMAT')) return 'INFUSOMAT';
    return case_.deviceName;
  }))];

  const getSeverityColor = (score) => {
    if (score >= 9) return 'bg-red-100 text-red-800 border-red-200';
    if (score >= 7) return 'bg-orange-100 text-orange-800 border-orange-200';
    return 'bg-yellow-100 text-yellow-800 border-yellow-200';
  };

  const getOutcomeColor = (outcome) => {
    if (outcome.toLowerCase().includes('died') || outcome.toLowerCase().includes('death') || outcome.toLowerCase().includes('expired')) {
      return 'bg-red-50 text-red-900 border-red-200';
    }
    return 'bg-gray-50 text-gray-900 border-gray-200';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <Heart className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Cardiac Arrest Death Cases</h1>
              <p className="text-gray-600">FDA MAUDE Database Analysis - Device-Related Fatalities</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <AlertTriangle className="w-8 h-8 text-red-500" />
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{cardiacArrestCases.length}</p>
                <p className="text-gray-600">Fatal Cases</p>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <Stethoscope className="w-8 h-8 text-blue-500" />
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{uniqueDevices.length}</p>
                <p className="text-gray-600">Device Types</p>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <Activity className="w-8 h-8 text-orange-500" />
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">
                  {(cardiacArrestCases.reduce((sum, case_) => sum + case_.severityScore, 0) / cardiacArrestCases.length).toFixed(1)}
                </p>
                <p className="text-gray-600">Avg Severity</p>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <Calendar className="w-8 h-8 text-green-500" />
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">2015-2024</p>
                <p className="text-gray-600">Date Range</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white p-6 rounded-lg shadow-sm border mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search MDR, device, medication, evidence..."
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-full"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Severity Score</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value)}
              >
                <option value="all">All Severities</option>
                <option value="10">Critical (10)</option>
                <option value="9">Severe (9)</option>
                <option value="8">High (8)</option>
                <option value="7">Moderate (7)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Device Type</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={selectedDevice}
                onChange={(e) => setSelectedDevice(e.target.value)}
              >
                <option value="all">All Devices</option>
                {uniqueDevices.map(device => (
                  <option key={device} value={device}>{device}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Cases List */}
        <div className="space-y-6">
          {filteredCases.map((case_, index) => (
            <motion.div
              key={case_.caseId}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-red-100 rounded-lg">
                      <Heart className="w-5 h-5 text-red-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Death Case #{case_.caseId} - MDR {case_.mdrNumber}
                      </h3>
                      <p className="text-gray-600">{case_.eventDate}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getSeverityColor(case_.severityScore)}`}>
                      Severity {case_.severityScore}/10
                    </span>
                    <a
                      href={case_.fdaLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="View FDA MAUDE Report"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                        <Stethoscope className="w-4 h-4 mr-2 text-blue-500" />
                        Device Information
                      </h4>
                      <p className="text-gray-700 bg-blue-50 p-3 rounded-lg border">
                        {case_.deviceName}
                      </p>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Medication</h4>
                      <p className="text-gray-700 bg-gray-50 p-3 rounded-lg border">
                        {case_.medication}
                      </p>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Device Malfunction</h4>
                      <p className="text-gray-700 bg-orange-50 p-3 rounded-lg border border-orange-200">
                        {case_.malfunction}
                      </p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                        <FileText className="w-4 h-4 mr-2 text-green-500" />
                        Evidence
                      </h4>
                      <p className="text-gray-700 bg-green-50 p-3 rounded-lg border border-green-200">
                        {case_.evidence}
                      </p>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Patient Outcome</h4>
                      <p className={`p-3 rounded-lg border ${getOutcomeColor(case_.outcome)}`}>
                        {case_.outcome}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {filteredCases.length === 0 && (
          <div className="text-center py-12">
            <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No cases found</h3>
            <p className="text-gray-600">Try adjusting your search criteria</p>
          </div>
        )}

        {/* Footer Note */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Data Source:</strong> FDA MAUDE Database | <strong>Analysis:</strong> OpenAI GPT-3.5-turbo | 
            <strong>Note:</strong> All cases verified with direct FDA report links. Evidence column contains detailed analysis of device failure mechanisms.
          </p>
        </div>
      </div>
    </div>
  );
};

export default CardiacArrestCases;
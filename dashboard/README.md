# Medical Device Incidents Dashboard

A modern, interactive React dashboard for analyzing Canadian Medical Device Incidents data with advanced visualizations and insights.

## 🚀 Features

- **Interactive Dashboard**: Real-time overview of medical device incidents
- **Advanced Analytics**: Deep dive into patterns, correlations, and trends
- **Device Analysis**: Comprehensive device risk assessment and incident tracking
- **Company Analysis**: Risk profiles and compliance metrics for manufacturers
- **Trend Analysis**: Seasonal patterns and predictive modeling
- **Severity Analysis**: In-depth analysis of incident severity and outcomes
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Built with React, Tailwind CSS, and Framer Motion

## 🛠 Technology Stack

- **Frontend**: React 18, React Router 6
- **Styling**: Tailwind CSS 3
- **Charts**: Chart.js, React-ChartJS-2, Recharts
- **Animation**: Framer Motion
- **Icons**: Lucide React, Heroicons
- **Build Tool**: Create React App

## 📊 Dashboard Sections

### 1. Main Dashboard
- Key metrics overview
- Monthly incident trends
- Severity distribution
- Top devices and companies
- Real-time alerts

### 2. Advanced Analytics
- Statistical analysis
- Correlation studies
- Risk assessment matrices
- Data insights and recommendations

### 3. Device Analysis
- Device risk profiles
- Incident patterns by device type
- Manufacturer comparisons
- Common failure modes

### 4. Company Analysis
- Manufacturer risk scores
- Compliance tracking
- Incident reporting patterns
- Industry benchmarking

### 5. Trend Analysis
- Seasonal patterns
- Growth trajectories
- Predictive analytics
- Forecasting models

### 6. Severity Analysis
- Fatality rates
- Injury classifications
- Risk stratification
- Outcome predictions

## 🚀 Getting Started

### Prerequisites

- Node.js 16.0 or higher
- npm or yarn package manager

### Installation

1. **Navigate to the dashboard directory**:
   ```bash
   cd /Users/Dell/Desktop/CanadianMedicalDevices/dashboard
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## 📁 Project Structure

```
dashboard/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Dashboard.js          # Main dashboard overview
│   │   ├── Analytics.js          # Advanced analytics
│   │   ├── DeviceAnalysis.js     # Device-specific analysis
│   │   ├── CompanyAnalysis.js    # Company analysis
│   │   ├── TrendAnalysis.js      # Trend analysis
│   │   ├── SeverityAnalysis.js   # Severity analysis
│   │   └── DataUpload.js         # Data upload interface
│   ├── App.js                    # Main application component
│   ├── index.js                  # Application entry point
│   └── index.css                 # Global styles
├── package.json
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Design System

### Color Palette

- **Primary**: Blue (#3B82F6) - Used for main actions and navigation
- **Health**: Green (#22C55E) - Used for positive indicators
- **Danger**: Red (#EF4444) - Used for critical incidents and high-risk items
- **Warning**: Yellow/Orange (#F59E0B) - Used for medium-risk items
- **Gray**: Various shades for text, borders, and backgrounds

### Typography

- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800, 900

### Components

- **Cards**: White background with subtle shadows
- **Buttons**: Primary (blue) and secondary (gray) variants
- **Charts**: Consistent color scheme across all visualizations
- **Forms**: Clean, accessible input styling

## 📊 Data Integration

The dashboard is designed to work with the medical device incidents data extracted from Health Canada. To integrate real data:

1. **CSV Data**: Place your CSV files in the `public/data/` directory
2. **API Integration**: Modify the data fetching logic in components
3. **Real-time Updates**: Implement WebSocket connections for live data

### Expected Data Format

```javascript
{
  incidents: [
    {
      id: "incident_id",
      date: "2025-04-29",
      severity: "INJURY",
      deviceName: "Device Name",
      manufacturer: "Company Name",
      category: "GENERAL HOSPITAL",
      description: "Incident description"
    }
  ]
}
```

## 🔧 Customization

### Adding New Charts

1. Import Chart.js components:
   ```javascript
   import { Line, Bar, Doughnut } from 'react-chartjs-2';
   ```

2. Create chart data and options:
   ```javascript
   const chartData = {
     labels: ['Jan', 'Feb', 'Mar'],
     datasets: [{ /* dataset config */ }]
   };
   ```

3. Render the chart:
   ```javascript
   <Line data={chartData} options={chartOptions} />
   ```

### Modifying Color Scheme

Edit `tailwind.config.js` to customize colors:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom primary colors
      }
    }
  }
}
```

### Adding New Pages

1. Create a new component in `src/components/`
2. Add the route in `App.js`
3. Update the navigation in `App.js`

## 🚀 Deployment

### Netlify

1. Build the project: `npm run build`
2. Deploy the `build` folder to Netlify

### Vercel

1. Connect your GitHub repository
2. Vercel will automatically build and deploy

### Traditional Hosting

1. Build the project: `npm run build`
2. Upload the `build` folder to your web server

## 📱 Mobile Responsiveness

The dashboard is fully responsive and optimized for:

- **Desktop**: Full-featured experience with side navigation
- **Tablet**: Adaptive layout with collapsible navigation
- **Mobile**: Touch-optimized interface with mobile navigation

## 🔒 Security Considerations

- Input validation for all user inputs
- XSS protection through React's built-in escaping
- HTTPS recommended for production
- API authentication for data access
- Data privacy compliance (GDPR, PIPEDA)

## 🧪 Testing

Run tests with:

```bash
npm test
```

For end-to-end testing, consider adding:
- Cypress for full application testing
- Jest for unit testing
- React Testing Library for component testing

## 📈 Performance Optimization

- **Code Splitting**: Implemented with React.lazy()
- **Image Optimization**: Use WebP format for images
- **Bundle Analysis**: Run `npm run build` and analyze bundle size
- **Caching**: Implement service workers for offline functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the documentation
- Review existing issues and discussions

## 🔮 Future Enhancements

- Real-time data streaming
- Machine learning predictions
- Advanced filtering and search
- Export functionality for all charts
- Multi-language support
- Dark mode theme
- Mobile app version
- API documentation
- Advanced user permissions
- Integration with other health databases
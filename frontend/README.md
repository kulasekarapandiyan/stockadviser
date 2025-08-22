# ⚛️ Stock Advisor Frontend

React-based frontend for the Stock Advisor application, providing an intuitive and responsive user interface for stock analysis and portfolio management.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn package manager
- Backend API running on `http://localhost:8000`

### Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm start
   # or
   yarn start
   ```

The application will open in your browser at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/                    # Static assets
│   ├── index.html            # Main HTML file
│   └── favicon.ico           # App icon
├── src/                      # Source code
│   ├── components/           # Reusable UI components
│   │   ├── Navbar.js         # Navigation component
│   │   ├── StockChart.js     # Stock chart component
│   │   ├── TechnicalPanel.js # Technical analysis panel
│   │   ├── FundamentalPanel.js # Fundamental analysis panel
│   │   └── PortfolioCard.js  # Portfolio display component
│   ├── pages/                # Page components
│   │   ├── Dashboard.js      # Main dashboard page
│   │   ├── StockAnalysis.js  # Stock analysis page
│   │   ├── Portfolio.js      # Portfolio management page
│   │   └── MarketOverview.js # Market overview page
│   ├── services/             # API services
│   │   ├── api.js            # API client configuration
│   │   ├── stockService.js   # Stock-related API calls
│   │   └── portfolioService.js # Portfolio API calls
│   ├── utils/                # Utility functions
│   │   ├── formatters.js     # Data formatting utilities
│   │   └── validators.js     # Input validation
│   ├── hooks/                # Custom React hooks
│   │   ├── useStockData.js   # Stock data fetching hook
│   │   └── usePortfolio.js   # Portfolio management hook
│   ├── App.js                # Main application component
│   ├── index.js              # Application entry point
│   └── App.css               # Global styles
├── package.json              # Dependencies and scripts
├── tailwind.config.js        # Tailwind CSS configuration
└── README.md                 # This file
```

## 🎨 UI Components

### Core Components

#### Navbar
- Responsive navigation with mobile menu
- Active route highlighting
- Brand logo and navigation links

#### StockChart
- Interactive stock price charts
- Multiple timeframe selection
- Technical indicator overlays
- Pattern highlighting

#### TechnicalPanel
- Technical indicator values
- Signal generation display
- Pattern recognition results
- Buy/sell recommendations

#### FundamentalPanel
- Financial ratios and metrics
- Scoring system display
- Peer comparison charts
- Valuation models

#### PortfolioCard
- Portfolio overview display
- Position management
- Performance tracking
- Risk assessment

## 📱 Pages

### Dashboard (`/`)
- Stock search functionality
- Popular stocks display
- Feature highlights
- Quick navigation

### Stock Analysis (`/stock/:symbol`)
- Comprehensive stock analysis
- Technical and fundamental data
- Interactive charts
- Recommendation summary

### Portfolio (`/portfolio`)
- Portfolio management
- Position tracking
- Performance analytics
- Risk assessment

### Market Overview (`/market`)
- Market indices display
- Sector performance
- Market sentiment
- Economic indicators

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```bash
# API Configuration
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=10000

# Feature Flags
REACT_APP_ENABLE_REAL_TIME=true
REACT_APP_ENABLE_NOTIFICATIONS=true

# Chart Configuration
REACT_APP_CHART_THEME=light
REACT_APP_DEFAULT_TIMEFRAME=1d
```

### Tailwind CSS Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        success: {
          500: '#10b981',
          600: '#059669',
        },
        warning: {
          500: '#f59e0b',
          600: '#d97706',
        },
        danger: {
          500: '#ef4444',
          600: '#dc2626',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

## 🚀 Development

### Available Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject from Create React App
npm run eject

# Start with HTTPS
HTTPS=true npm start
```

### Development Workflow

1. **Component Development**
   - Create components in `src/components/`
   - Use Tailwind CSS for styling
   - Follow React best practices

2. **Page Development**
   - Create pages in `src/pages/`
   - Implement routing logic
   - Handle API calls and state management

3. **API Integration**
   - Create services in `src/services/`
   - Use axios for HTTP requests
   - Implement error handling and loading states

4. **Styling**
   - Use Tailwind CSS utility classes
   - Create custom components for complex UI
   - Maintain consistent design system

### Code Quality

#### ESLint Configuration
```json
{
  "extends": [
    "react-app",
    "react-app/jest"
  ],
  "rules": {
    "no-unused-vars": "warn",
    "prefer-const": "error"
  }
}
```

#### Prettier Configuration
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

## 📊 State Management

### React Hooks

#### useStockData
```javascript
const { data, loading, error, refetch } = useStockData(symbol, period);
```

#### usePortfolio
```javascript
const { portfolios, addPortfolio, updatePortfolio } = usePortfolio();
```

### Context API

```javascript
// StockContext.js
const StockContext = createContext();

export const StockProvider = ({ children }) => {
  const [selectedStock, setSelectedStock] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  
  return (
    <StockContext.Provider value={{
      selectedStock,
      setSelectedStock,
      analysisData,
      setAnalysisData
    }}>
      {children}
    </StockContext.Provider>
  );
};
```

## 🔌 API Integration

### API Client Configuration

```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  timeout: process.env.REACT_APP_API_TIMEOUT || 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Service Functions

```javascript
// services/stockService.js
import api from './api';

export const stockService = {
  // Get comprehensive stock analysis
  getStockAnalysis: async (symbol, period = '1y', interval = '1d') => {
    const response = await api.get(`/api/stocks/${symbol}`, {
      params: { period, interval }
    });
    return response.data;
  },

  // Get technical analysis
  getTechnicalAnalysis: async (symbol, period = '1y') => {
    const response = await api.get(`/api/stocks/${symbol}/technical`, {
      params: { period }
    });
    return response.data;
  },

  // Get fundamental analysis
  getFundamentalAnalysis: async (symbol) => {
    const response = await api.get(`/api/stocks/${symbol}/fundamental`);
    return response.data;
  },

  // Get buy/sell signals
  getSignals: async (symbol, period = '1y') => {
    const response = await api.get(`/api/stocks/${symbol}/signals`, {
      params: { period }
    });
    return response.data;
  }
};
```

## 🎨 UI/UX Features

### Responsive Design
- Mobile-first approach
- Breakpoint-based layouts
- Touch-friendly interactions

### Dark/Light Theme
```javascript
const [theme, setTheme] = useState('light');

const toggleTheme = () => {
  const newTheme = theme === 'light' ? 'dark' : 'light';
  setTheme(newTheme);
  document.documentElement.classList.toggle('dark');
};
```

### Loading States
```javascript
const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>
);
```

### Error Handling
```javascript
const ErrorBoundary = ({ children }) => {
  const [hasError, setHasError] = useState(false);

  if (hasError) {
    return (
      <div className="text-center p-8">
        <h2 className="text-xl font-semibold text-red-600 mb-4">
          Something went wrong
        </h2>
        <button 
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Reload Page
        </button>
      </div>
    );
  }

  return children;
};
```

## 📱 Mobile Optimization

### Touch Interactions
```javascript
const useTouchGesture = () => {
  const [startX, setStartX] = useState(0);
  const [startY, setStartY] = useState(0);

  const handleTouchStart = (e) => {
    setStartX(e.touches[0].clientX);
    setStartY(e.touches[0].clientY);
  };

  const handleTouchEnd = (e) => {
    const endX = e.changedTouches[0].clientX;
    const endY = e.changedTouches[0].clientY;
    
    const deltaX = endX - startX;
    const deltaY = endY - startY;
    
    // Handle swipe gestures
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      if (deltaX > 50) {
        // Swipe right
      } else if (deltaX < -50) {
        // Swipe left
      }
    }
  };

  return { handleTouchStart, handleTouchEnd };
};
```

### Responsive Charts
```javascript
const useResponsiveChart = () => {
  const [chartDimensions, setChartDimensions] = useState({
    width: 800,
    height: 400
  });

  useEffect(() => {
    const updateDimensions = () => {
      const container = document.getElementById('chart-container');
      if (container) {
        setChartDimensions({
          width: container.offsetWidth,
          height: Math.min(400, container.offsetWidth * 0.5)
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  return chartDimensions;
};
```

## 🧪 Testing

### Testing Setup

```bash
# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false
```

### Component Testing

```javascript
// components/__tests__/StockChart.test.js
import { render, screen } from '@testing-library/react';
import StockChart from '../StockChart';

test('renders stock chart with symbol', () => {
  render(<StockChart symbol="AAPL" />);
  expect(screen.getByText('AAPL')).toBeInTheDocument();
});

test('shows loading state initially', () => {
  render(<StockChart symbol="AAPL" />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

### Mock API Calls

```javascript
// __mocks__/api.js
export const mockStockData = {
  symbol: 'AAPL',
  current_price: 150.25,
  price_change: 2.50,
  price_change_percent: 1.69
};

jest.mock('../services/api', () => ({
  getStockAnalysis: jest.fn(() => Promise.resolve(mockStockData))
}));
```

## 🚀 Production Build

### Build Process

```bash
# Create production build
npm run build

# Test production build locally
npx serve -s build -l 3000
```

### Build Optimization

```javascript
// webpack.config.js (if ejecting)
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
};
```

### Environment-Specific Builds

```bash
# Development
npm run start

# Staging
REACT_APP_ENV=staging npm run build

# Production
REACT_APP_ENV=production npm run build
```

## 📊 Performance Optimization

### Code Splitting

```javascript
// Lazy load components
const StockAnalysis = lazy(() => import('./pages/StockAnalysis'));
const Portfolio = lazy(() => import('./pages/Portfolio'));

// Suspense wrapper
<Suspense fallback={<LoadingSpinner />}>
  <Routes>
    <Route path="/stock/:symbol" element={<StockAnalysis />} />
    <Route path="/portfolio" element={<Portfolio />} />
  </Routes>
</Suspense>
```

### Memoization

```javascript
const MemoizedStockChart = memo(StockChart, (prevProps, nextProps) => {
  return prevProps.symbol === nextProps.symbol && 
         prevProps.period === nextProps.period;
});
```

### Bundle Analysis

```bash
# Install bundle analyzer
npm install --save-dev webpack-bundle-analyzer

# Analyze bundle
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
```

## 🔒 Security

### Security Best Practices

- **Input Validation**: Validate all user inputs
- **XSS Prevention**: Use React's built-in XSS protection
- **CSRF Protection**: Implement CSRF tokens for forms
- **Content Security Policy**: Set appropriate CSP headers

### Environment Variables

```bash
# Never commit sensitive data
REACT_APP_API_KEY=your_api_key
REACT_APP_SECRET=your_secret

# Use .env.local for local development
# Use .env.production for production builds
```

## 📱 Progressive Web App (PWA)

### PWA Configuration

```json
// public/manifest.json
{
  "name": "Stock Advisor",
  "short_name": "StockAdvisor",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#3b82f6",
  "background_color": "#ffffff",
  "icons": [
    {
      "src": "icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

### Service Worker

```javascript
// src/serviceWorker.js
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js');
  });
}
```

## 🚀 Deployment

### Static Hosting

```bash
# Build the application
npm run build

# Deploy to various platforms
# Netlify, Vercel, AWS S3, etc.
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Frontend
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: npm ci
      - run: npm run build
      - run: npm run test
      - name: Deploy to production
        run: # deployment commands
```

## 🤝 Contributing

### Development Guidelines

1. **Code Style**: Follow ESLint and Prettier configurations
2. **Component Structure**: Use functional components with hooks
3. **State Management**: Prefer local state over global state when possible
4. **Testing**: Write tests for new components and features
5. **Documentation**: Update README and component documentation

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

2. **API Connection Issues**
   - Verify backend is running
   - Check CORS configuration
   - Verify API endpoints

3. **Performance Issues**
   - Use React DevTools Profiler
   - Check bundle size
   - Implement code splitting

### Getting Help

- Check the console for error messages
- Review React and Tailwind CSS documentation
- Create an issue in the repository
- Check browser compatibility

---

**Happy coding! 🚀**

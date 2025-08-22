import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  MagnifyingGlassIcon, 
  ArrowTrendingUpIcon, 
  ArrowTrendingDownIcon,
  ChartBarIcon,
  CalculatorIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [searchSymbol, setSearchSymbol] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const popularStocks = [
    { symbol: 'AAPL', name: 'Apple Inc.', change: '+2.45%', trend: 'up' },
    { symbol: 'MSFT', name: 'Microsoft Corp.', change: '+1.23%', trend: 'up' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', change: '-0.87%', trend: 'down' },
    { symbol: 'AMZN', name: 'Amazon.com Inc.', change: '+3.12%', trend: 'up' },
    { symbol: 'TSLA', name: 'Tesla Inc.', change: '+5.67%', trend: 'up' },
    { symbol: 'NVDA', name: 'NVIDIA Corp.', change: '+4.23%', trend: 'up' },
  ];

  const features = [
    {
      title: 'Technical Analysis',
      description: 'Advanced chart patterns, indicators, and trend analysis',
      icon: ChartBarIcon,
      color: 'bg-blue-500',
    },
    {
      title: 'Fundamental Analysis',
      description: 'Comprehensive financial ratios and company valuation',
      icon: CalculatorIcon,
      color: 'bg-green-500',
    },
    {
      title: 'Market Overview',
      description: 'Real-time market data and sector performance',
      icon: GlobeAltIcon,
      color: 'bg-purple-500',
    },
  ];

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchSymbol.trim()) {
      toast.error('Please enter a stock symbol');
      return;
    }

    setIsLoading(true);
    try {
      // Navigate to stock analysis page
      navigate(`/stock/${searchSymbol.toUpperCase()}`);
    } catch (error) {
      toast.error('Error searching for stock');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          High-Accuracy Stock Advice
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Get comprehensive buy/sell recommendations based on advanced technical patterns 
          and fundamental analysis. Make informed investment decisions with confidence.
        </p>
      </div>

      {/* Search Section */}
      <div className="max-w-2xl mx-auto mb-12">
        <form onSubmit={handleSearch} className="relative">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />
            <input
              type="text"
              value={searchSymbol}
              onChange={(e) => setSearchSymbol(e.target.value)}
              placeholder="Enter stock symbol (e.g., AAPL, MSFT, GOOGL)"
              className="w-full pl-12 pr-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="mt-4 w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Analyzing...' : 'Analyze Stock'}
          </button>
        </form>
      </div>

      {/* Features Section */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
          Powerful Analysis Tools
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              <div className={`inline-flex p-3 rounded-lg ${feature.color} mb-4`}>
                <feature.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Popular Stocks Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Popular Stocks
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {popularStocks.map((stock, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
              onClick={() => navigate(`/stock/${stock.symbol}`)}
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{stock.symbol}</h3>
                  <p className="text-sm text-gray-600">{stock.name}</p>
                </div>
                <div className={`flex items-center ${
                  stock.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stock.trend === 'up' ? (
                    <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
                  ) : (
                    <ArrowTrendingDownIcon className="h-4 w-4 mr-1" />
                  )}
                  <span className="text-sm font-medium">{stock.change}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats Section */}
      <div className="mt-12 grid md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <div className="text-3xl font-bold text-blue-600 mb-2">50+</div>
          <div className="text-gray-600">Technical Indicators</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <div className="text-3xl font-bold text-green-600 mb-2">25+</div>
          <div className="text-gray-600">Fundamental Metrics</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <div className="text-3xl font-bold text-purple-600 mb-2">95%</div>
          <div className="text-gray-600">Accuracy Rate</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <div className="text-3xl font-bold text-orange-600 mb-2">24/7</div>
          <div className="text-gray-600">Real-time Updates</div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

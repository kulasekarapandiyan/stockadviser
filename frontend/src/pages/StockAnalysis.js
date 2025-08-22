import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { 
  ChartBarIcon, 
  CalculatorIcon, 
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

const StockAnalysis = () => {
  const { symbol } = useParams();
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchStockData();
  }, [symbol]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/stocks/${symbol}`);
      if (!response.ok) {
        throw new Error('Failed to fetch stock data');
      }
      const data = await response.json();
      setStockData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <InformationCircleIcon className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">{error}</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!stockData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">No data available</h2>
        </div>
      </div>
    );
  }

  const { current_price, price_change, price_change_percent, overall_recommendation } = stockData;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {symbol} Stock Analysis
        </h1>
        <div className="flex items-center space-x-4">
          <span className="text-2xl font-semibold">${current_price?.toFixed(2) || 'N/A'}</span>
          <div className={`flex items-center ${
            price_change >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {price_change >= 0 ? (
              <ArrowTrendingUpIcon className="h-5 w-5 mr-1" />
            ) : (
              <ArrowTrendingDownIcon className="h-5 w-5 mr-1" />
            )}
            <span className="font-medium">
              {price_change >= 0 ? '+' : ''}{price_change?.toFixed(2) || 'N/A'} 
              ({price_change_percent >= 0 ? '+' : ''}{price_change_percent?.toFixed(2) || 'N/A'}%)
            </span>
          </div>
        </div>
      </div>

      {/* Recommendation Banner */}
      {overall_recommendation && (
        <div className="mb-8 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Overall Recommendation</h2>
          <div className="flex items-center justify-between">
            <div>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                overall_recommendation.signal === 'buy' ? 'bg-green-100 text-green-800' :
                overall_recommendation.signal === 'sell' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {overall_recommendation.signal.toUpperCase()}
              </span>
              <p className="mt-2 text-gray-600">{overall_recommendation.reason}</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(overall_recommendation.strength * 100)}%
              </div>
              <div className="text-sm text-gray-500">Confidence</div>
            </div>
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'overview', name: 'Overview', icon: ChartBarIcon },
            { id: 'technical', name: 'Technical Analysis', icon: ChartBarIcon },
            { id: 'fundamental', name: 'Fundamental Analysis', icon: CalculatorIcon },
            { id: 'signals', name: 'Signals', icon: TrendingUpIcon }
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
              <tab.icon className="h-5 w-5 inline mr-2" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-lg shadow-md p-6">
        {activeTab === 'overview' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Stock Overview</h3>
            <p className="text-gray-600">
              Comprehensive analysis of {symbol} including technical indicators, 
              fundamental metrics, and trading signals.
            </p>
          </div>
        )}

        {activeTab === 'technical' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Technical Analysis</h3>
            <p className="text-gray-600">
              Technical indicators, patterns, and signals for {symbol}.
            </p>
          </div>
        )}

        {activeTab === 'fundamental' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Fundamental Analysis</h3>
            <p className="text-gray-600">
              Financial ratios, valuation metrics, and company fundamentals for {symbol}.
            </p>
          </div>
        )}

        {activeTab === 'signals' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Trading Signals</h3>
            <p className="text-gray-600">
              Buy/sell signals and recommendations for {symbol}.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StockAnalysis;

import React, { useState, useEffect } from 'react';
import { 
  GlobeAltIcon, 
  ArrowTrendingUpIcon, 
  ArrowTrendingDownIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const MarketOverview = () => {
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMarketData();
  }, []);

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/market/overview');
      if (response.ok) {
        const data = await response.json();
        setMarketData(data);
      } else {
        throw new Error('Failed to fetch market data');
      }
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
          <h3 className="text-sm font-medium text-red-800">Error</h3>
          <div className="mt-2 text-sm text-red-700">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Market Overview</h1>
        <p className="text-gray-600">Real-time market data and sector performance</p>
      </div>

      {/* Market Indices */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Major Indices</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {marketData?.market_indices ? (
            Object.entries(marketData.market_indices).map(([name, data]) => (
              <div key={name} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">{name}</h3>
                  <GlobeAltIcon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">
                  {data.current_value?.toLocaleString() || 'N/A'}
                </div>
                <div className={`flex items-center ${
                  data.change_percent >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {data.change_percent >= 0 ? (
                    <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
                  ) : (
                    <ArrowTrendingDownIcon className="h-4 w-4 mr-1" />
                  )}
                  <span className="font-medium">
                    {data.change_percent >= 0 ? '+' : ''}{data.change_percent?.toFixed(2) || 'N/A'}%
                  </span>
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  Volume: {data.volume?.toLocaleString() || 'N/A'}
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full text-center py-8">
              <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No market data</h3>
              <p className="mt-1 text-sm text-gray-500">
                Market data is currently unavailable.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Sector Performance */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Sector Performance</h2>
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">YTD Performance by Sector</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {marketData?.sector_performance ? (
              Object.entries(marketData.sector_performance).map(([sector, data]) => (
                <div key={sector} className="px-6 py-4 flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-blue-500 mr-3"></div>
                    <div>
                      <div className="text-sm font-medium text-gray-900">{sector}</div>
                      <div className="text-sm text-gray-500">{data.etf}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-sm font-medium ${
                      data.ytd_return >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {data.ytd_return >= 0 ? '+' : ''}{data.ytd_return?.toFixed(2) || 'N/A'}%
                    </div>
                    <div className="text-sm text-gray-500">
                      ${data.current_price?.toFixed(2) || 'N/A'}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="px-6 py-8 text-center">
                <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No sector data</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Sector performance data is currently unavailable.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Market Summary */}
      <div className="grid gap-6 md:grid-cols-3">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ArrowTrendingUpIcon className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Market Trend</h3>
              <p className="text-sm text-gray-500">Overall market direction</p>
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-bold text-green-600">Bullish</div>
            <div className="text-sm text-gray-500">Based on major indices</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ChartBarIcon className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Volatility</h3>
              <p className="text-sm text-gray-500">Market volatility index</p>
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-bold text-blue-600">Normal</div>
            <div className="text-sm text-gray-500">VIX at normal levels</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <GlobeAltIcon className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Trading Volume</h3>
              <p className="text-sm text-gray-500">Market activity level</p>
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-bold text-purple-600">High</div>
            <div className="text-sm text-gray-500">Above average volume</div>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      {marketData?.last_updated && (
        <div className="mt-8 text-center text-sm text-gray-500">
          Last updated: {new Date(marketData.last_updated).toLocaleString()}
        </div>
      )}
    </div>
  );
};

export default MarketOverview;

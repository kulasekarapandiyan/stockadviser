import React, { useState, useEffect } from 'react';
import { 
  PlusIcon, 
  ChartBarIcon, 
  CurrencyDollarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';

const Portfolio = () => {
  const [portfolios, setPortfolios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newPortfolio, setNewPortfolio] = useState({ name: '', description: '' });

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const fetchPortfolios = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/portfolios');
      if (response.ok) {
        const data = await response.json();
        setPortfolios(data.portfolios || []);
      }
    } catch (error) {
      console.error('Error fetching portfolios:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePortfolio = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/portfolios', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newPortfolio),
      });

      if (response.ok) {
        setNewPortfolio({ name: '', description: '' });
        setShowCreateForm(false);
        fetchPortfolios();
      }
    } catch (error) {
      console.error('Error creating portfolio:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Portfolio Management</h1>
        <p className="text-gray-600">Track your investments and analyze performance</p>
      </div>

      {/* Create Portfolio Button */}
      <div className="mb-8">
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Create Portfolio
        </button>
      </div>

      {/* Create Portfolio Form */}
      {showCreateForm && (
        <div className="mb-8 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Portfolio</h3>
          <form onSubmit={handleCreatePortfolio} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Portfolio Name
              </label>
              <input
                type="text"
                id="name"
                value={newPortfolio.name}
                onChange={(e) => setNewPortfolio({ ...newPortfolio, name: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                id="description"
                value={newPortfolio.description}
                onChange={(e) => setNewPortfolio({ ...newPortfolio, description: e.target.value })}
                rows={3}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div className="flex space-x-3">
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Create Portfolio
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Portfolios List */}
      {portfolios.length === 0 ? (
        <div className="text-center py-12">
          <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No portfolios</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating your first portfolio.
          </p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {portfolios.map((portfolio) => (
            <div
              key={portfolio.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">{portfolio.name}</h3>
                <ChartBarIcon className="h-6 w-6 text-gray-400" />
              </div>
              <p className="text-gray-600 mb-4">{portfolio.description}</p>
              <div className="border-t pt-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Created</span>
                  <span className="text-gray-900">
                    {new Date(portfolio.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Portfolio Stats */}
      {portfolios.length > 0 && (
        <div className="mt-12 grid gap-6 md:grid-cols-4">
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <CurrencyDollarIcon className="mx-auto h-8 w-8 text-blue-600 mb-2" />
            <div className="text-2xl font-bold text-gray-900">{portfolios.length}</div>
            <div className="text-gray-600">Total Portfolios</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <ArrowTrendingUpIcon className="mx-auto h-8 w-8 text-green-600 mb-2" />
            <div className="text-2xl font-bold text-gray-900">$0</div>
            <div className="text-gray-600">Total Value</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <ChartBarIcon className="mx-auto h-8 w-8 text-purple-600 mb-2" />
            <div className="text-2xl font-bold text-gray-900">0</div>
            <div className="text-gray-600">Total Positions</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <ArrowTrendingDownIcon className="mx-auto h-8 w-8 text-red-600 mb-2" />
            <div className="text-2xl font-bold text-gray-900">0%</div>
            <div className="text-gray-600">Total Return</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Portfolio;

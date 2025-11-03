import { useState, useEffect } from 'react';
import { analyticsAPI, metadataAPI } from '../services/api';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { TrendingUp, ShoppingCart, Users, DollarSign, Clock, Package } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [productRanking, setProductRanking] = useState([]);
  const [channelPerformance, setChannelPerformance] = useState([]);
  const [storePerformance, setStorePerformance] = useState([]);
  const [timeSeries, setTimeSeries] = useState([]);
  const [deliveryPerformance, setDeliveryPerformance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [metadata, setMetadata] = useState({ stores: [], channels: [] });
  const [selectedStore, setSelectedStore] = useState('');
  const [selectedChannel, setSelectedChannel] = useState('');

  useEffect(() => {
    loadDashboardData();
    loadMetadata();
  }, [selectedStore, selectedChannel]);

  const loadMetadata = async () => {
    try {
      const response = await metadataAPI.getMetadata();
      setMetadata(response.data);
    } catch (error) {
      console.error('Error loading metadata:', error);
    }
  };

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedStore) params.store_ids = selectedStore;
      if (selectedChannel) params.channel_ids = selectedChannel;

      const [
        overviewRes,
        productsRes,
        channelsRes,
        storesRes,
        timeSeriesRes,
        deliveryRes,
      ] = await Promise.all([
        analyticsAPI.getOverview(params),
        analyticsAPI.getProductRanking({ ...params, limit: 10 }),
        analyticsAPI.getChannelPerformance(params),
        analyticsAPI.getStorePerformance(params),
        analyticsAPI.getTimeSeries({ ...params, period: 'daily' }),
        analyticsAPI.getDeliveryPerformance(params),
      ]);

      setOverview(overviewRes.data);
      setProductRanking(productsRes.data.products);
      setChannelPerformance(channelsRes.data.channels);
      setStorePerformance(storesRes.data.stores);
      setTimeSeries(timeSeriesRes.data.data);
      setDeliveryPerformance(deliveryRes.data.performance);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  if (loading && !overview) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando dados...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Analytics Dashboard
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Plataforma de analytics para restaurantes
          </p>
        </div>
      </header>

      {/* Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Filtrar por Loja
              </label>
              <select
                value={selectedStore}
                onChange={(e) => setSelectedStore(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todas as Lojas</option>
                {metadata.stores.map((store) => (
                  <option key={store.id} value={store.id}>
                    {store.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Filtrar por Canal
              </label>
              <select
                value={selectedChannel}
                onChange={(e) => setSelectedChannel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todos os Canais</option>
                {metadata.channels.map((channel) => (
                  <option key={channel.id} value={channel.id}>
                    {channel.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {/* Overview Cards */}
        {overview && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <MetricCard
              title="Vendas Totais"
              value={formatNumber(overview.total_sales)}
              icon={<ShoppingCart className="h-6 w-6" />}
              color="blue"
            />
            <MetricCard
              title="Faturamento Total"
              value={formatCurrency(overview.total_revenue)}
              icon={<DollarSign className="h-6 w-6" />}
              color="green"
            />
            <MetricCard
              title="Ticket Médio"
              value={formatCurrency(overview.average_ticket)}
              icon={<TrendingUp className="h-6 w-6" />}
              color="purple"
            />
            <MetricCard
              title="Vendas Completas"
              value={formatNumber(overview.completed_sales)}
              subtitle={`${((overview.completed_sales / overview.total_sales) * 100).toFixed(1)}% de sucesso`}
              icon={<Package className="h-6 w-6" />}
              color="green"
            />
            <MetricCard
              title="Total Descontos"
              value={formatCurrency(overview.total_discount)}
              icon={<DollarSign className="h-6 w-6" />}
              color="orange"
            />
            <MetricCard
              title="Taxa de Entrega"
              value={formatCurrency(overview.total_delivery_fee)}
              icon={<Clock className="h-6 w-6" />}
              color="blue"
            />
          </div>
        )}

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Products Ranking */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Top 10 Produtos</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={productRanking}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="product_name" 
                    angle={-45}
                    textAnchor="end"
                    height={100}
                    interval={0}
                    tick={{ fontSize: 10 }}
                  />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="total_quantity" fill="#3b82f6" name="Quantidade Vendida" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Channel Performance */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Performance por Canal</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={channelPerformance}
                    dataKey="total_revenue"
                    nameKey="channel_name"
                    cx="50%"
                    cy="50%"
                    label={(entry) => `${entry.channel_name}: ${entry.revenue_percentage.toFixed(1)}%`}
                    labelLine={false}
                  >
                    {channelPerformance.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value) => formatCurrency(value)}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Time Series */}
        {timeSeries.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">Evolução de Vendas</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={timeSeries}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tick={{ fontSize: 10 }}
                  />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Line 
                    yAxisId="left"
                    type="monotone" 
                    dataKey="sales_count" 
                    stroke="#3b82f6" 
                    name="Vendas"
                  />
                  <Line 
                    yAxisId="right"
                    type="monotone" 
                    dataKey="revenue" 
                    stroke="#10b981" 
                    name="Faturamento"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Tables Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Store Performance */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Performance por Loja</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Loja</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendas</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Faturamento</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {storePerformance.slice(0, 5).map((store) => (
                    <tr key={store.store_id}>
                      <td className="px-4 py-3 text-sm text-gray-900">{store.store_name}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{formatNumber(store.total_sales)}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(store.total_revenue)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Delivery Performance */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Performance de Entrega</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Região</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Entregas</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tempo Médio</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {deliveryPerformance.slice(0, 5).map((delivery, idx) => (
                    <tr key={idx}>
                      <td className="px-4 py-3 text-sm text-gray-900">
                        {delivery.neighborhood || 'N/A'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900">
                        {formatNumber(delivery.total_deliveries)}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900">
                        {delivery.total_delivery_time_minutes.toFixed(0)} min
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function MetricCard({ title, value, subtitle, icon, color = 'blue' }) {
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-gray-900">{value}</p>
          {subtitle && (
            <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
          )}
        </div>
        <div className={`${colorClasses[color]} p-3 rounded-lg text-white`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, AreaChart, Area, PieChart, Pie, Cell,
  ComposedChart, ResponsiveContainer
} from 'recharts';

// Sample data - In real implementation, this would come from your database
const generateData = () => {
  const now = new Date();
  return Array.from({ length: 24 }, (_, i) => {
    const time = new Date(now - (23 - i) * 3600000);
    return {
      hour: time.getHours(),
      transactions: Math.floor(Math.random() * 50) + 10,
      amount: Math.random() * 1000 + 500,
      networkLoad: Math.random() * 100,
      successRate: Math.random() * 20 + 80,
    };
  });
};

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const DashboardCard = ({ title, children }) => (
  <div className="bg-white rounded-lg shadow p-4 m-2">
    <h3 className="text-lg font-semibold mb-4 text-gray-700">{title}</h3>
    {children}
  </div>
);

const Analytics = () => {
  const [data] = useState(generateData());
  
  const formatHour = (hour) => `${hour}:00`;
  
  // Calculate summary statistics
  const totalTransactions = data.reduce((sum, d) => sum + d.transactions, 0);
  const averageAmount = data.reduce((sum, d) => sum + d.amount, 0) / data.length;
  const averageLoad = data.reduce((sum, d) => sum + d.networkLoad, 0) / data.length;
  
  // Distribution data for pie chart
  const distributionData = [
    { name: '0-250', value: Math.random() * 100 },
    { name: '251-500', value: Math.random() * 100 },
    { name: '501-750', value: Math.random() * 100 },
    { name: '751+', value: Math.random() * 100 },
  ];

  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Transaction Analytics Dashboard</h1>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-500 text-white rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Total Transactions</h3>
          <p className="text-3xl">{totalTransactions}</p>
        </div>
        <div className="bg-green-500 text-white rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Average Amount</h3>
          <p className="text-3xl">${averageAmount.toFixed(2)}</p>
        </div>
        <div className="bg-purple-500 text-white rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Network Load</h3>
          <p className="text-3xl">{averageLoad.toFixed(1)}%</p>
        </div>
      </div>

      {/* Transaction Volume Over Time */}
      <DashboardCard title="Transaction Volume Over Time">
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="hour" tickFormatter={formatHour} />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip />
            <Legend />
            <Bar yAxisId="left" dataKey="transactions" fill="#8884d8" name="Transactions" />
            <Line yAxisId="right" type="monotone" dataKey="amount" stroke="#82ca9d" name="Amount ($)" />
          </ComposedChart>
        </ResponsiveContainer>
      </DashboardCard>

      {/* Network Load */}
      <DashboardCard title="Network Load Analysis">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="hour" tickFormatter={formatHour} />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="networkLoad" fill="#8884d8" stroke="#8884d8" name="Load (%)" />
          </AreaChart>
        </ResponsiveContainer>
      </DashboardCard>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Success Rate */}
        <DashboardCard title="Transaction Success Rate">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" tickFormatter={formatHour} />
              <YAxis domain={[60, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="successRate" stroke="#82ca9d" name="Success Rate (%)" />
            </LineChart>
          </ResponsiveContainer>
        </DashboardCard>

        {/* Amount Distribution */}
        <DashboardCard title="Transaction Amount Distribution">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={distributionData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label
              >
                {distributionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </DashboardCard>
      </div>
    </div>
  );
};

export default Analytics;

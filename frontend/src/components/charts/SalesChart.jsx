import React from 'react';
import { motion } from 'framer-motion';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

export function SalesChart({ results }) {
  if (!results) return null;

  // Prepare chart data by combining historical and forecast
  const getChartData = () => {
    const hist = results.historical.map(item => ({
      name: item.Date,
      Historical: item.Sales,
      Forecast: null
    }));
    
    const fore = results.forecast.map(item => ({
      name: item.Date,
      Historical: null,
      Forecast: item.Sales
    }));
    
    // Link the last historical point to the first forecast point visually
    if (hist.length > 0 && fore.length > 0) {
      fore[0].Historical = hist[hist.length - 1].Historical;
    }
    
    return [...hist, ...fore];
  };

  const chartData = getChartData();
  const today = results.historical[results.historical.length - 1]?.Date;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 }}
      className="card p-6 h-[400px] mb-8"
    >
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-base font-semibold text-primary">Sales Trajectory</h2>
          <p className="text-xs text-muted mt-1">Historical vs Expected Forecast</p>
        </div>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={chartData} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="colorHistorical" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#52525b" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#52525b" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#27272a" />
          <XAxis 
            dataKey="name" 
            stroke="#a1a1aa" 
            tick={{fill: '#a1a1aa', fontSize: 11}}
            tickLine={false}
            axisLine={false}
            minTickGap={40}
            dy={10}
          />
          <YAxis 
            stroke="#a1a1aa" 
            tick={{fill: '#a1a1aa', fontSize: 11}} 
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `$${value}`}
            dx={-10}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#111111', borderColor: '#27272a', borderRadius: '8px', color: '#fff', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            itemStyle={{ color: '#fff', fontSize: '13px' }}
            labelStyle={{ color: '#a1a1aa', fontSize: '12px', marginBottom: '4px' }}
          />
          {today && <ReferenceLine x={today} stroke="#52525b" strokeDasharray="4 4" label={{ position: 'top', value: 'Today', fill: '#a1a1aa', fontSize: 11 }} />}
          
          <Area type="monotone" dataKey="Historical" stroke="#a1a1aa" strokeWidth={2} fillOpacity={1} fill="url(#colorHistorical)" isAnimationActive={false} />
          <Area type="monotone" dataKey="Forecast" stroke="#3b82f6" strokeWidth={2} strokeDasharray="5 5" fillOpacity={1} fill="url(#colorForecast)" />
        </AreaChart>
      </ResponsiveContainer>
    </motion.div>
  );
}

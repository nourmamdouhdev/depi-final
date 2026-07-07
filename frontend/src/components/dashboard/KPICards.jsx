import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, DollarSign, Calendar, Activity } from 'lucide-react';

const Card = ({ title, value, icon: Icon, trend, prefix = '', delay }) => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="card p-5 flex flex-col justify-between"
    >
      <div className="flex justify-between items-start mb-4">
        <p className="text-sm font-medium text-muted">{title}</p>
        <div className="p-2 bg-white/5 rounded-md text-muted">
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div>
        <h3 className="text-2xl font-bold text-primary tracking-tight">
          {prefix}{value}
        </h3>
        {trend !== undefined && (
          <p className={`text-xs font-medium mt-2 flex items-center ${trend >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
            <TrendingUp className={`w-3 h-3 mr-1 ${trend < 0 ? 'rotate-180' : ''}`} />
            {trend > 0 ? '+' : ''}{trend}% from previous period
          </p>
        )}
      </div>
    </motion.div>
  );
};

export function KPICards({ summary }) {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <Card 
        title="Historical Revenue" 
        value={summary.total_historical_revenue.toLocaleString()} 
        icon={DollarSign}
        prefix="$"
        delay={0.1}
      />
      <Card 
        title="Projected Revenue" 
        value={summary.projected_revenue.toLocaleString()} 
        icon={Activity}
        prefix="$"
        delay={0.2}
      />
      <Card 
        title="Historical Avg Daily" 
        value={summary.historical_avg_daily_sales.toLocaleString()} 
        icon={Calendar}
        prefix="$"
        delay={0.3}
      />
      <Card 
        title="Projected Avg Daily" 
        value={summary.projected_avg_daily_sales.toLocaleString()} 
        icon={TrendingUp}
        prefix="$"
        trend={summary.historical_monthly_growth_rate_pct}
        delay={0.4}
      />
    </div>
  );
}

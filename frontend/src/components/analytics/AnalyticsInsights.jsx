import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

export function AnalyticsInsights({ summary }) {
  if (!summary) return null;

  const growth = summary.historical_monthly_growth_rate_pct;
  const isPositive = growth > 0;
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.6 }}
      className="card p-6 mb-8 bg-gradient-to-br from-surface to-[#151515] border-l-2 border-l-accent"
    >
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-accent" />
        <h2 className="text-base font-semibold text-primary">AI Forecast Insights</h2>
      </div>
      <div className="space-y-3">
        <p className="text-sm text-muted">
          <strong className="text-primary font-medium">Revenue Outlook: </strong>
          Sales are projected to generate <span className="text-emerald-400 font-medium">${summary.projected_revenue.toLocaleString()}</span> over the next {summary.forecast_days} days.
        </p>
        <p className="text-sm text-muted">
          <strong className="text-primary font-medium">Growth Analysis: </strong>
          Historical trends show a {isPositive ? 'positive' : 'negative'} growth trajectory of <span className={`${isPositive ? 'text-emerald-400' : 'text-red-400'} font-medium`}>{Math.abs(growth)}%</span> month-over-month.
        </p>
        <p className="text-sm text-muted">
          <strong className="text-primary font-medium">Daily Averages: </strong>
          The model predicts an average of <span className="text-accent font-medium">${summary.projected_avg_daily_sales.toLocaleString()}</span> in daily sales during the forecast horizon.
        </p>
      </div>
    </motion.div>
  );
}

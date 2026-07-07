import React from 'react';
import { motion } from 'framer-motion';
import { Download, Share2 } from 'lucide-react';

export function ExportData({ forecast, horizon }) {
  if (!forecast) return null;

  const downloadCSV = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + "Date,Forecasted Sales\n" 
      + forecast.map(e => `${e.Date},${e.Sales}`).join("\n");
      
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `forecast_${horizon}d.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.7 }}
      className="flex items-center gap-3"
    >
      <button onClick={downloadCSV} className="btn-secondary flex items-center gap-2 text-sm">
        <Download className="w-4 h-4" /> Export CSV
      </button>
      <button className="btn-secondary flex items-center gap-2 text-sm">
        <Share2 className="w-4 h-4" /> Share Report
      </button>
    </motion.div>
  );
}

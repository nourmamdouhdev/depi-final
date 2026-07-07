import React, { useState } from 'react';
import { DashboardLayout } from './layouts/DashboardLayout';
import { Hero } from './components/dashboard/Hero';
import { FileUploader } from './components/upload/FileUploader';
import { KPICards } from './components/dashboard/KPICards';
import { SalesChart } from './components/charts/SalesChart';
import { AnalyticsInsights } from './components/analytics/AnalyticsInsights';
import { ExportData } from './components/export/ExportData';
import { useForecast } from './hooks/useForecast';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const {
    file,
    setFile,
    horizon,
    setHorizon,
    loading,
    error,
    results,
    processForecast
  } = useForecast();

  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <DashboardLayout activeTab={activeTab} setActiveTab={setActiveTab}>
      <div id="dashboard">
        <Hero />
      </div>

      <div id="upload" className="flex flex-col lg:flex-row gap-6 mb-6">
        <div className="w-full lg:w-2/3">
          <FileUploader 
            file={file} 
            setFile={setFile} 
            loading={loading}
            onUpload={() => processForecast(file, horizon)} 
          />
        </div>
        <div className="w-full lg:w-1/3 flex flex-col justify-end pb-8">
          <label className="block text-sm font-medium text-primary mb-2">
            Forecast Horizon (Days)
          </label>
          <select 
            className="input-field"
            value={horizon}
            onChange={(e) => setHorizon(Number(e.target.value))}
            disabled={loading}
          >
            <option value={7}>Next 7 Days</option>
            <option value={30}>Next 30 Days</option>
            <option value={90}>Next Quarter (90 Days)</option>
            <option value={365}>Next Year (365 Days)</option>
          </select>
        </div>
      </div>

      <AnimatePresence>
        {error && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg mb-8 text-sm"
          >
            {error}
          </motion.div>
        )}
      </AnimatePresence>

      {results ? (
        <div className="space-y-6">
          <div id="export" className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-primary">Forecast Overview</h2>
            <ExportData forecast={results.forecast} horizon={horizon} />
          </div>
          
          <div id="forecast">
            <KPICards summary={results.summary} />
            <SalesChart results={results} />
          </div>
          
          <div id="analytics">
            <AnalyticsInsights summary={results.summary} />
          </div>
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="border border-dashed border-border rounded-xl p-16 flex flex-col items-center justify-center text-center mt-8"
        >
          <div className="w-16 h-16 rounded-full bg-surface border border-border flex items-center justify-center mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-muted"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
          </div>
          <h3 className="text-lg font-medium text-primary mb-2">No Data Generated Yet</h3>
          <p className="text-sm text-muted max-w-sm">
            Upload a CSV file containing historical sales data to generate predictive insights and visualizations.
          </p>
        </motion.div>
      )}
    </DashboardLayout>
  );
}

export default App;

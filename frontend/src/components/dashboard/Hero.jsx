import React from 'react';
import { motion } from 'framer-motion';

export function Hero() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="mb-10"
    >
      <h1 className="text-3xl font-semibold text-primary tracking-tight mb-2">
        Sales Intelligence
      </h1>
      <p className="text-muted max-w-2xl text-sm leading-relaxed">
        Transform historical sales data into actionable future insights using our proprietary machine learning models. 
        Upload your dataset to generate a high-confidence forecast immediately.
      </p>
    </motion.div>
  );
}

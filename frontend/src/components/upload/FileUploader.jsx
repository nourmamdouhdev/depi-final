import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { UploadCloud, File, X, Loader2 } from 'lucide-react';

export function FileUploader({ file, setFile, onUpload, loading }) {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, [setFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    maxFiles: 1
  });

  return (
    <div className="card p-6 mb-8">
      <h2 className="text-sm font-semibold mb-4 text-primary">Upload Dataset</h2>
      
      {!file ? (
        <div 
          {...getRootProps()} 
          className={`border border-dashed rounded-lg p-10 text-center cursor-pointer transition-all duration-200 ${
            isDragActive ? 'border-accent bg-accent/5' : 'border-border hover:border-muted hover:bg-white/5'
          }`}
        >
          <input {...getInputProps()} />
          <div className="w-10 h-10 rounded-full bg-surface border border-border flex items-center justify-center mx-auto mb-3">
            <UploadCloud className="w-5 h-5 text-muted" />
          </div>
          <p className="text-sm font-medium text-primary mb-1">
            Click to upload or drag and drop
          </p>
          <p className="text-xs text-muted">
            CSV files only. Must contain 'Date' and 'Sales' columns.
          </p>
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          className="border border-border rounded-lg p-4 flex items-center justify-between bg-surface"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded bg-accent/10 flex items-center justify-center">
              <File className="w-5 h-5 text-accent" />
            </div>
            <div>
              <p className="text-sm font-medium text-primary">{file.name}</p>
              <p className="text-xs text-muted">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {!loading && (
              <button 
                onClick={() => setFile(null)}
                className="p-2 text-muted hover:text-red-400 transition-colors rounded hover:bg-white/5"
              >
                <X className="w-4 h-4" />
              </button>
            )}
            <button 
              onClick={onUpload}
              disabled={loading}
              className="btn-primary flex items-center gap-2 text-sm ml-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
              {loading ? 'Processing...' : 'Generate Forecast'}
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}

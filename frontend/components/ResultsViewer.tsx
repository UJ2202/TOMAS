'use client';

import { CheckCircle, Download, RefreshCw } from 'lucide-react';

interface ResultsViewerProps {
  results: any;
  onNewExecution: () => void;
}

export default function ResultsViewer({ results, onNewExecution }: ResultsViewerProps) {
  const renderValue = (value: any): React.ReactNode => {
    if (typeof value === 'string') {
      return <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: value.replace(/\n/g, '<br />') }} />;
    } else if (Array.isArray(value)) {
      return (
        <ul className="list-disc pl-5 space-y-1">
          {value.map((item, i) => (
            <li key={i}>{renderValue(item)}</li>
          ))}
        </ul>
      );
    } else if (typeof value === 'object' && value !== null) {
      return (
        <div className="space-y-2">
          {Object.entries(value).map(([k, v]) => (
            <div key={k}>
              <span className="font-semibold">{k}: </span>
              {renderValue(v)}
            </div>
          ))}
        </div>
      );
    }
    return String(value);
  };

  return (
    <div className="space-y-6">
      {/* Success Header */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
        <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
        <h3 className="text-2xl font-bold text-green-900 mb-2">Task Completed!</h3>
        <p className="text-green-700">
          {results.message || 'Your task has been executed successfully.'}
        </p>
      </div>

      {/* Results */}
      <div className="space-y-4">
        <h4 className="text-lg font-semibold text-slate-900">Results</h4>
        
        {Object.entries(results).map(([key, value]) => {
          if (key === 'status' || key === 'message') return null;
          
          return (
            <div key={key} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
              <h5 className="font-semibold text-slate-900 mb-2 capitalize">
                {key.replace(/_/g, ' ')}
              </h5>
              <div className="text-slate-700">
                {renderValue(value)}
              </div>
            </div>
          );
        })}
      </div>

      {/* Actions */}
      <div className="flex space-x-4">
        <button
          onClick={onNewExecution}
          className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 font-semibold flex items-center justify-center"
        >
          <RefreshCw className="w-5 h-5 mr-2" />
          New Execution
        </button>
        <button
          onClick={() => {
            const dataStr = JSON.stringify(results, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'results.json';
            link.click();
          }}
          className="flex-1 bg-slate-600 text-white py-3 px-4 rounded-md hover:bg-slate-700 font-semibold flex items-center justify-center"
        >
          <Download className="w-5 h-5 mr-2" />
          Download Results
        </button>
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import { TranslationResult } from '../types/translation';

interface DemoTranscriptProps {
  translationHistory: TranslationResult[];
  supportedLanguages: Record<string, string>;
  onClear: () => void;
}

const DemoTranscript: React.FC<DemoTranscriptProps> = ({
  translationHistory,
  supportedLanguages,
  onClear,
}) => {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(
    translationHistory.length > 0 ? translationHistory.length - 1 : null
  );

  const toggleExpand = (idx: number) => {
    setExpandedIdx(expandedIdx === idx ? null : idx);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">📝 Meeting Transcript</h2>
        {translationHistory.length > 0 && (
          <button
            onClick={onClear}
            className="py-2 px-4 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
          >
            🗑️ Clear Transcript
          </button>
        )}
      </div>

      {translationHistory.length > 0 ? (
        <div className="space-y-2">
          {translationHistory.map((item, idx) => (
            <div
              key={idx}
              className="border border-gray-200 rounded-lg overflow-hidden"
            >
              {/* Header - Always Visible */}
              <button
                onClick={() => toggleExpand(idx)}
                className="w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 transition-colors text-left flex justify-between items-center"
              >
                <span className="font-medium text-gray-800">
                  {idx + 1}. {(item as any).speaker || 'Speaker'} -{' '}
                  {new Date(item.timestamp).toLocaleTimeString()}
                </span>
                <span className="text-gray-500">
                  {expandedIdx === idx ? '▼' : '▶'}
                </span>
              </button>

              {/* Content - Expandable */}
              {expandedIdx === idx && (
                <div className="px-4 py-3 bg-white">
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">Original:</p>
                    <p className="text-gray-800">{item.original_text}</p>
                  </div>

                  {item.detected_language && (
                    <p className="text-sm text-gray-600 mb-3">
                      Language: {supportedLanguages[item.detected_language] || item.detected_language}
                    </p>
                  )}

                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">Translations:</p>
                    {Object.entries(item.translations).length > 0 ? (
                      <ul className="space-y-2">
                        {Object.entries(item.translations).map(([lang, text]) => (
                          <li key={lang} className="text-gray-800">
                            <strong className="text-blue-600">
                              {supportedLanguages[lang] || lang}:
                            </strong>{' '}
                            {text}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-500 text-sm">Translation not available</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-gray-600">Meeting transcript will appear here as the demo runs</p>
        </div>
      )}
    </div>
  );
};

export default DemoTranscript;

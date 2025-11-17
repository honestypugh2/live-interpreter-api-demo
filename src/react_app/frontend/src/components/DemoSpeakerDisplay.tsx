import React from 'react';

interface DemoSpeakerDisplayProps {
  speaker: string;
  lang: string;
  text: string;
  supportedLanguages: Record<string, string>;
  demoRunning: boolean;
  autoAdvance: boolean;
  onManualAdvance: () => void;
}

const DemoSpeakerDisplay: React.FC<DemoSpeakerDisplayProps> = ({
  speaker,
  lang,
  text,
  supportedLanguages,
  demoRunning,
  autoAdvance,
  onManualAdvance,
}) => {
  const getLanguageFlag = (langCode: string): string => {
    const flags: Record<string, string> = {
      'en-US': '🇺🇸',
      'es-ES': '🇪🇸',
      'es-MX': '🇲🇽',
      'fr-FR': '🇫🇷',
      'de-DE': '🇩🇪',
      'it-IT': '🇮🇹',
      'pt-BR': '🇧🇷',
      'zh-CN': '🇨🇳',
      'ja-JP': '🇯🇵',
      'ko-KR': '🇰🇷',
    };
    return flags[langCode] || '🌐';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">🗣️ Current Speaker</h2>

      {demoRunning ? (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-bold text-lg text-gray-800 mb-2">{speaker}</h3>

          {/* Language Indicator */}
          <div className="flex items-center space-x-2 text-sm text-gray-600 mb-3">
            <span className="text-2xl">{getLanguageFlag(lang)}</span>
            <span>Speaking in: {supportedLanguages[lang] || lang}</span>
          </div>

          {/* Original Text */}
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <p className="text-lg leading-relaxed text-gray-800">{text}</p>
          </div>

          {/* Manual Advance Button */}
          {!autoAdvance && (
            <button
              onClick={onManualAdvance}
              className="w-full py-3 px-4 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              ➡️ Next Line
            </button>
          )}
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-gray-600">👆 Click 'Start Demo' to begin</p>
        </div>
      )}
    </div>
  );
};

export default DemoSpeakerDisplay;

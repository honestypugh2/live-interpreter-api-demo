import React from 'react';
import { TranslationResult } from '../types/translation';

interface DemoTranslationDisplayProps {
  translationHistory: TranslationResult[];
  supportedLanguages: Record<string, string>;
  enableAudioPlayback: boolean;
}

const DemoTranslationDisplay: React.FC<DemoTranslationDisplayProps> = ({
  translationHistory,
  supportedLanguages,
  enableAudioPlayback,
}) => {
  const [playingLang, setPlayingLang] = React.useState<string | null>(null);

  const handlePlayAudio = async (text: string, language: string) => {
    if (!window.speechSynthesis) {
      alert('Speech synthesis not supported in this browser');
      return;
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    setPlayingLang(language);

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Map language codes to speech synthesis language codes
    const langMap: Record<string, string> = {
      'en-US': 'en-US',
      'es-ES': 'es-ES',
      'es-MX': 'es-MX',
      'fr-FR': 'fr-FR',
      'de-DE': 'de-DE',
      'it-IT': 'it-IT',
      'pt-BR': 'pt-BR',
      'zh-CN': 'zh-CN',
      'ja-JP': 'ja-JP',
      'ko-KR': 'ko-KR',
    };
    
    utterance.lang = langMap[language] || 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onend = () => setPlayingLang(null);
    utterance.onerror = () => {
      console.error('Speech synthesis error');
      setPlayingLang(null);
    };

    window.speechSynthesis.speak(utterance);
  };

  const latest = translationHistory.length > 0 ? translationHistory[translationHistory.length - 1] : null;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">💬 Live Translations</h2>

      {latest ? (
        <div>
          <p className="font-medium text-gray-700 mb-3">Latest Translation:</p>
          
          <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4 mb-4">
            {/* Speaker */}
            {(latest as any).speaker && (
              <h3 className="font-bold text-lg text-gray-800 mb-2">
                {(latest as any).speaker}
              </h3>
            )}

            {/* Original Text */}
            <div className="mb-3">
              <p className="font-medium text-gray-700 text-sm mb-1">Original:</p>
              <p className="text-gray-800">{latest.original_text}</p>
            </div>

            {/* Detected Language */}
            {latest.detected_language && (
              <p className="text-sm text-gray-600 mb-3">
                Detected: {supportedLanguages[latest.detected_language] || latest.detected_language}
              </p>
            )}

            {/* Translations */}
            <div className="mb-3">
              <p className="font-medium text-gray-700 text-sm mb-2">Translations:</p>
              {Object.entries(latest.translations).map(([lang, text]) => (
                <div key={lang} className="bg-white rounded p-3 mb-2">
                  <p className="text-sm text-gray-600 mb-1">
                    🌐 <strong>{supportedLanguages[lang] || lang}:</strong>
                  </p>
                  <p className="text-gray-800">{text}</p>
                </div>
              ))}
            </div>

            {/* Timestamp */}
            <p className="text-xs text-gray-500">
              ⏱️ {new Date(latest.timestamp).toLocaleTimeString()}
            </p>
          </div>

          {/* Audio Playback */}
          {enableAudioPlayback && (
            <div className="mt-4">
              <p className="font-medium text-gray-700 text-sm mb-2">🔊 Audio Playback:</p>
              <div className="grid grid-cols-2 gap-2">
                {/* Original Audio */}
                {latest.detected_language && (
                  <button
                    onClick={() => handlePlayAudio(latest.original_text, latest.detected_language!)}
                    disabled={playingLang === latest.detected_language}
                    className={`py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
                      playingLang === latest.detected_language
                        ? 'bg-green-400 text-white cursor-not-allowed'
                        : 'bg-green-600 text-white hover:bg-green-700'
                    }`}
                  >
                    {playingLang === latest.detected_language ? '🔊 Playing...' : '▶️ Play'} {supportedLanguages[latest.detected_language] || 'Original'}
                  </button>
                )}

                {/* Translated Audio */}
                {Object.entries(latest.translations).map(([lang, text]) => (
                  <button
                    key={lang}
                    onClick={() => handlePlayAudio(text, lang)}
                    disabled={playingLang === lang}
                    className={`py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
                      playingLang === lang
                        ? 'bg-blue-400 text-white cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {playingLang === lang ? '🔊 Playing...' : '▶️ Play'} {supportedLanguages[lang] || lang}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-gray-600">Translations will appear here as the demo progresses</p>
        </div>
      )}
    </div>
  );
};

export default DemoTranslationDisplay;

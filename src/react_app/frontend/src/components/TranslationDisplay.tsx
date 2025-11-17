import { TranslationResult } from '../types/translation';
import { useState, useEffect } from 'react';

interface Props {
  translations: TranslationResult[];
  interimText?: string;
  interimTranslations?: Record<string, string>;
  isRecording?: boolean;
}

const LANGUAGES: Record<string, string> = {
  'en-US': 'English (US)',
  'es-ES': 'Spanish (Spain)',
  'es-MX': 'Spanish (Mexico)',
  'fr-FR': 'French',
  'de-DE': 'German',
  'it-IT': 'Italian',
  'pt-BR': 'Portuguese',
  'zh-CN': 'Chinese',
  'ja-JP': 'Japanese',
  'ko-KR': 'Korean',
};

const TranslationDisplay = ({ translations, interimText, interimTranslations, isRecording }: Props) => {
  const [playingAudio, setPlayingAudio] = useState<string | null>(null);

  // Debug logging
  useEffect(() => {
    if (translations[0]) {
      console.log('Latest translation:', translations[0]);
      console.log('Has synthesized_audio:', !!translations[0].synthesized_audio);
      console.log('Synthesized audio keys:', translations[0].synthesized_audio ? Object.keys(translations[0].synthesized_audio) : []);
    }
  }, [translations]);

  const playAudio = (audioBase64: string, lang: string) => {
    setPlayingAudio(lang);
    try {
      // Decode base64 to binary
      const binaryString = atob(audioBase64);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      
      // Create audio blob and play
      const blob = new Blob([bytes], { type: 'audio/wav' });
      const audio = new Audio(URL.createObjectURL(blob));
      
      audio.onended = () => {
        setPlayingAudio(null);
      };
      
      audio.onerror = () => {
        console.error('Audio playback error');
        setPlayingAudio(null);
      };
      
      audio.play().catch(err => {
        console.error('Playback failed:', err);
        setPlayingAudio(null);
      });
    } catch (error) {
      console.error('Error playing audio:', error);
      setPlayingAudio(null);
    }
  };

  if (translations.length === 0) {
    return (
      <div className="card h-full flex items-center justify-center">
        <div className="text-center text-gray-500 dark:text-gray-400">
          <div className="text-6xl mb-4">🎤</div>
          <p className="text-lg mb-2">No translations yet</p>
          <p className="text-sm">Start recording to see translations appear here</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        💬 Translations
      </h3>

      {/* Interim Results (Continuous Mode) */}
      {isRecording && interimText && (
        <div className="card bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-300 dark:border-yellow-700 border-dashed">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="animate-pulse text-red-500">🔴</div>
              <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                Recognizing... (interim)
              </span>
            </div>
            
            <div>
              <div className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                🗣️ Speaking
              </div>
              <p className="text-base text-gray-800 dark:text-gray-200">
                {interimText}
              </p>
            </div>

            {interimTranslations && Object.keys(interimTranslations).length > 0 && (
              <div className="border-t border-yellow-300 dark:border-yellow-700 pt-3">
                <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                  🌐 Translating...
                </div>
                {Object.entries(interimTranslations).map(([lang, text]) => (
                  <div key={lang} className="mb-2 last:mb-0">
                    <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
                      {LANGUAGES[lang] || lang}:
                    </span>
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                      {text}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Latest Translation - Highlighted */}
      {translations[0] && (
        <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-2 border-blue-300 dark:border-blue-700">
          <div className="space-y-4">
            {/* Original Text */}
            <div>
              <div className="flex items-center mb-2">
                <span className="text-sm font-semibold text-gray-600 dark:text-gray-300">
                  🗣️ Original
                </span>
                {translations[0].detected_language && (
                  <span className="ml-2 text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                    {LANGUAGES[translations[0].detected_language] || translations[0].detected_language}
                  </span>
                )}
              </div>
              <p className="text-lg text-gray-900 dark:text-white">
                {translations[0].original_text}
              </p>
            </div>

            {/* Translations */}
            <div className="border-t border-gray-300 dark:border-gray-600 pt-4">
              <div className="text-sm font-semibold text-gray-600 dark:text-gray-300 mb-3">
                🌐 Translations
              </div>
              {Object.entries(translations[0].translations).map(([lang, text]) => (
                <div key={lang} className="mb-3 last:mb-0">
                  <div className="flex justify-between items-center mb-1">
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {LANGUAGES[lang] || lang}
                    </div>
                    {/* Audio playback button */}
                    {translations[0].synthesized_audio && translations[0].synthesized_audio[lang] && (
                      <button
                        onClick={() => playAudio(translations[0].synthesized_audio![lang], lang)}
                        disabled={playingAudio === lang}
                        className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
                      >
                        {playingAudio === lang ? '⏸️ Playing...' : '▶️ Play'}
                      </button>
                    )}
                  </div>
                  <p className="text-base text-gray-800 dark:text-gray-100">
                    {text}
                  </p>
                </div>
              ))}
            </div>

            {/* Metadata */}
            <div className="text-xs text-gray-500 dark:text-gray-400 flex justify-between border-t border-gray-300 dark:border-gray-600 pt-2">
              <span>⏱️ {new Date(translations[0].timestamp).toLocaleTimeString()}</span>
              <span>⏲️ {translations[0].duration_ms}ms</span>
            </div>
          </div>
        </div>
      )}

      {/* Translation History */}
      {translations.length > 1 && (
        <div>
          <h4 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-3">
            📝 History
          </h4>
          <div className="space-y-3">
            {translations.slice(1).map((translation, index) => (
              <div
                key={index}
                className="card bg-white dark:bg-gray-800 hover:shadow-md transition-shadow"
              >
                <div className="space-y-2">
                  <div className="flex justify-between items-start">
                    <p className="text-sm text-gray-800 dark:text-gray-200 flex-1">
                      {translation.original_text}
                    </p>
                    <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">
                      {new Date(translation.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  {Object.entries(translation.translations).map(([lang, text]) => (
                    <div key={lang} className="text-xs text-gray-600 dark:text-gray-400">
                      <span className="font-medium">{LANGUAGES[lang]}:</span> {text}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslationDisplay;

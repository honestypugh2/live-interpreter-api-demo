import { LanguageConfig } from '../types/translation';

interface Props {
  config: LanguageConfig;
  onConfigChange: (config: LanguageConfig) => void;
}

const LANGUAGES = {
  'en-US': 'English (US)',
  'en-GB': 'English (UK)',
  'es-ES': 'Spanish (Spain)',
  'es-MX': 'Spanish (Mexico)',
  'fr-FR': 'French (France)',
  'fr-CA': 'French (Canada)',
  'de-DE': 'German',
  'it-IT': 'Italian',
  'pt-BR': 'Portuguese (Brazil)',
  'zh-CN': 'Chinese (Mandarin)',
  'ja-JP': 'Japanese',
  'ko-KR': 'Korean',
};

const NEURAL_VOICES: Record<string, string[]> = {
  'en-US': ['en-US-JennyNeural', 'en-US-GuyNeural', 'en-US-AriaNeural', 'en-US-DavisNeural'],
  'en-GB': ['en-GB-SoniaNeural', 'en-GB-RyanNeural'],
  'es-ES': ['es-ES-ElviraNeural', 'es-ES-AlvaroNeural'],
  'es-MX': ['es-MX-DaliaNeural', 'es-MX-JorgeNeural'],
  'fr-FR': ['fr-FR-DeniseNeural', 'fr-FR-HenriNeural'],
  'de-DE': ['de-DE-KatjaNeural', 'de-DE-ConradNeural'],
  'it-IT': ['it-IT-ElsaNeural', 'it-IT-DiegoNeural'],
  'pt-BR': ['pt-BR-FranciscaNeural', 'pt-BR-AntonioNeural'],
  'zh-CN': ['zh-CN-XiaoxiaoNeural', 'zh-CN-YunxiNeural'],
  'ja-JP': ['ja-JP-NanamiNeural', 'ja-JP-KeitaNeural'],
  'ko-KR': ['ko-KR-SunHiNeural', 'ko-KR-InJoonNeural'],
};

const formatVoiceName = (voice: string, lang: string): string => {
  return voice.replace('Neural', '').replace(`${lang}-`, '');
};

const LanguageSelector = ({ config, onConfigChange }: Props) => {
  const handleTargetLanguageChange = (index: number, value: string) => {
    const newTargetLangs = [...config.target_languages];
    if (value === '') {
      // Remove language
      newTargetLangs.splice(index, 1);
    } else {
      newTargetLangs[index] = value;
    }
    onConfigChange({ ...config, target_languages: newTargetLangs });
  };

  const handleAddTargetLanguage = () => {
    if (config.target_languages.length < 3) {
      onConfigChange({ 
        ...config, 
        target_languages: [...config.target_languages, 'fr-FR'] 
      });
    }
  };

  const handleVoiceChange = (lang: string, voice: string) => {
    const newVoicePrefs = { ...(config.voice_preferences || {}) };
    newVoicePrefs[lang] = voice;
    onConfigChange({ ...config, voice_preferences: newVoicePrefs });
  };

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        ⚙️ Language Configuration
      </h3>

      {/* Live Interpreter Toggle */}
      <div className="mb-4">
        <label className="flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={config.use_live_interpreter}
            onChange={(e) =>
              onConfigChange({ ...config, use_live_interpreter: e.target.checked })
            }
            className="w-4 h-4 text-azure-blue border-gray-300 rounded focus:ring-azure-blue"
          />
          <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
            Use Live Interpreter
          </span>
        </label>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-6">
          Auto-detects language with personal voice
        </p>
      </div>

      {/* Continuous Mode Toggle */}
      {config.use_live_interpreter && (
        <div className="mb-4">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={config.use_continuous_mode !== false}
              onChange={(e) =>
                onConfigChange({ ...config, use_continuous_mode: e.target.checked })
              }
              className="w-4 h-4 text-azure-blue border-gray-300 rounded focus:ring-azure-blue"
            />
            <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
              Continuous Mode (Real-time)
            </span>
          </label>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-6">
            Translates in real-time as you speak
          </p>
        </div>
      )}

      {/* Source Language */}
      {!config.use_live_interpreter && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Source Language
          </label>
          <select
            value={config.source_language || 'en-US'}
            onChange={(e) =>
              onConfigChange({ ...config, source_language: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            {Object.entries(LANGUAGES).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Target Languages (up to 3) */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Target Languages (up to 3)
        </label>
        {config.target_languages.map((lang, index) => (
          <div key={index} className="mb-2">
            <div className="flex gap-2">
              <select
                value={lang}
                onChange={(e) => handleTargetLanguageChange(index, e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
              >
                {Object.entries(LANGUAGES).map(([code, name]) => (
                  <option key={code} value={code}>
                    {name}
                  </option>
                ))}
              </select>
              {config.target_languages.length > 1 && (
                <button
                  onClick={() => handleTargetLanguageChange(index, '')}
                  className="px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
                >
                  ✕
                </button>
              )}
            </div>
            {/* Voice selection for this language */}
            {NEURAL_VOICES[lang] && (
              <select
                value={config.voice_preferences?.[lang] || NEURAL_VOICES[lang][0]}
                onChange={(e) => handleVoiceChange(lang, e.target.value)}
                className="w-full mt-1 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-xs"
              >
                {NEURAL_VOICES[lang].map((voice) => (
                  <option key={voice} value={voice}>
                    🎤 {formatVoiceName(voice, lang)}
                  </option>
                ))}
              </select>
            )}
          </div>
        ))}
        {config.target_languages.length < 3 && (
          <button
            onClick={handleAddTargetLanguage}
            className="mt-2 w-full px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
          >
            + Add Target Language
          </button>
        )}
      </div>

      {/* Info */}
      {config.use_live_interpreter && (
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded border border-blue-200 dark:border-blue-800">
          <p className="text-xs text-blue-700 dark:text-blue-300">
            ✨ Automatic language detection active. Supports 100+ languages.
          </p>
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;

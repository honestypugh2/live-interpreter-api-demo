import { useState, useEffect } from 'react';
import './App.css';
import { TranslationResult } from './types/translation';
import DemoControls from './components/DemoControls';
import DemoSpeakerDisplay from './components/DemoSpeakerDisplay';
import DemoTranslationDisplay from './components/DemoTranslationDisplay';
import DemoTranscript from './components/DemoTranscript';

export interface SimulatedLine {
  speaker: string;
  lang: string;
  text: string;
}

// Simulated transcript - Council meeting about community park
const SIMULATED_TRANSCRIPT: SimulatedLine[] = [
  {
    speaker: "Council Chair (English)",
    lang: "en-US",
    text: "Good afternoon, everyone. Thank you for joining today's meeting. We'll discuss the new community park project and its budget allocation."
  },
  {
    speaker: "Council Member (Spanish)",
    lang: "es-ES",
    text: "Buenas tardes. Este proyecto es muy importante para nuestra comunidad. Queremos asegurarnos de que el diseño incluya áreas verdes y espacios para niños."
  },
  {
    speaker: "Council Chair (English)",
    lang: "en-US",
    text: "I completely agree. We also need to consider accessibility for seniors and people with disabilities. The design should be inclusive."
  },
  {
    speaker: "Council Member (Spanish)",
    lang: "es-ES",
    text: "Perfecto. También necesitamos considerar el mantenimiento a largo plazo. ¿Cuál es el presupuesto anual propuesto?"
  },
  {
    speaker: "Council Chair (English)",
    lang: "en-US",
    text: "The proposed budget is two hundred fifty thousand dollars for construction, with an annual maintenance budget of thirty thousand dollars."
  },
  {
    speaker: "Council Member (Spanish)",
    lang: "es-ES",
    text: "¿Cuándo planeamos comenzar la construcción? La comunidad está muy emocionada por este proyecto."
  },
  {
    speaker: "Council Chair (English)",
    lang: "en-US",
    text: "The goal is to start in early spring, once the budget is approved. We should have completion by next fall."
  },
  {
    speaker: "Council Member (Spanish)",
    lang: "es-ES",
    text: "Excelente. Propongo que votemos hoy para aprobar el presupuesto y podamos avanzar con el proyecto."
  },
];

const SUPPORTED_LANGUAGES: Record<string, string> = {
  'en-US': 'English (US)',
  'es-ES': 'Spanish (Spain)',
  'es-MX': 'Spanish (Mexico)',
  'fr-FR': 'French (France)',
  'de-DE': 'German (Germany)',
  'it-IT': 'Italian (Italy)',
  'pt-BR': 'Portuguese (Brazil)',
  'zh-CN': 'Chinese (Mandarin)',
  'ja-JP': 'Japanese',
  'ko-KR': 'Korean',
};

function AppDemo() {
  const [demoRunning, setDemoRunning] = useState(false);
  const [demoPaused, setDemoPaused] = useState(false);
  const [currentLineIdx, setCurrentLineIdx] = useState(0);
  const [translationHistory, setTranslationHistory] = useState<TranslationResult[]>([]);
  const [autoAdvance, setAutoAdvance] = useState(true);
  const [delaySeconds, setDelaySeconds] = useState(3);
  const [enableAudioPlayback, setEnableAudioPlayback] = useState(true);

  // Auto-advance logic
  useEffect(() => {
    if (!demoRunning || demoPaused || !autoAdvance) return;
    if (currentLineIdx >= SIMULATED_TRANSCRIPT.length) {
      setDemoRunning(false);
      return;
    }

    const timer = setTimeout(() => {
      processCurrentLine();
    }, delaySeconds * 1000);

    return () => clearTimeout(timer);
  }, [demoRunning, demoPaused, currentLineIdx, autoAdvance, delaySeconds]);

  // Cleanup speech synthesis on unmount
  useEffect(() => {
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const processCurrentLine = async () => {
    if (currentLineIdx >= SIMULATED_TRANSCRIPT.length) {
      setDemoRunning(false);
      return;
    }

    const currentLine = SIMULATED_TRANSCRIPT[currentLineIdx];
    
    // Simulate translation
    const result = await simulateTranslation(currentLine);
    setTranslationHistory(prev => [...prev, result]);

    // Play audio if enabled - use Web Speech API
    if (enableAudioPlayback && window.speechSynthesis) {
      // Play original language
      await speakText(currentLine.text, currentLine.lang);
      
      // Play translations
      for (const [lang, text] of Object.entries(result.translations)) {
        await speakText(text, lang);
      }
    }

    // Advance to next line
    setCurrentLineIdx(prev => prev + 1);
  };

  // Helper function to speak text using Web Speech API
  const speakText = (text: string, language: string): Promise<void> => {
    return new Promise((resolve) => {
      if (!window.speechSynthesis) {
        console.warn('Speech synthesis not supported');
        resolve();
        return;
      }

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
      utterance.rate = 0.9; // Slightly slower for clarity
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      utterance.onend = () => resolve();
      utterance.onerror = () => {
        console.error('Speech synthesis error');
        resolve();
      };

      window.speechSynthesis.speak(utterance);
    });
  };

  const simulateTranslation = async (line: SimulatedLine): Promise<TranslationResult> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    const translations: Record<string, string> = {};
    
    // Simple translation simulation
    if (line.lang === 'en-US') {
      translations['es-ES'] = getSpanishTranslation(line.text);
    } else if (line.lang === 'es-ES') {
      translations['en-US'] = getEnglishTranslation(line.text);
    }

    return {
      original_text: line.text,
      detected_language: line.lang,
      translations,
      timestamp: new Date().toISOString(),
      duration_ms: 500,
      synthesized_audio: {
        [line.lang]: 'simulated_audio_data',
        ...Object.keys(translations).reduce((acc, lang) => ({ ...acc, [lang]: 'simulated_audio_data' }), {})
      },
      speaker: line.speaker
    } as TranslationResult & { speaker: string };
  };

  const getSpanishTranslation = (text: string): string => {
    // Real translation would come from Azure API
    const translations: Record<string, string> = {
      "Good afternoon, everyone. Thank you for joining today's meeting. We'll discuss the new community park project and its budget allocation.": 
        "Buenas tardes a todos. Gracias por unirse a la reunión de hoy. Discutiremos el nuevo proyecto del parque comunitario y su asignación presupuestaria.",
      "I completely agree. We also need to consider accessibility for seniors and people with disabilities. The design should be inclusive.":
        "Estoy completamente de acuerdo. También debemos considerar la accesibilidad para personas mayores y personas con discapacidades. El diseño debe ser inclusivo.",
      "The proposed budget is two hundred fifty thousand dollars for construction, with an annual maintenance budget of thirty thousand dollars.":
        "El presupuesto propuesto es de doscientos cincuenta mil dólares para la construcción, con un presupuesto de mantenimiento anual de treinta mil dólares.",
      "The goal is to start in early spring, once the budget is approved. We should have completion by next fall.":
        "El objetivo es comenzar a principios de la primavera, una vez que se apruebe el presupuesto. Deberíamos tener la finalización para el próximo otoño."
    };
    return translations[text] || "[Translation from Azure would appear here]";
  };

  const getEnglishTranslation = (text: string): string => {
    // Real translation would come from Azure API
    const translations: Record<string, string> = {
      "Buenas tardes. Este proyecto es muy importante para nuestra comunidad. Queremos asegurarnos de que el diseño incluya áreas verdes y espacios para niños.":
        "Good afternoon. This project is very important for our community. We want to make sure the design includes green areas and spaces for children.",
      "Perfecto. También necesitamos considerar el mantenimiento a largo plazo. ¿Cuál es el presupuesto anual propuesto?":
        "Perfect. We also need to consider long-term maintenance. What is the proposed annual budget?",
      "¿Cuándo planeamos comenzar la construcción? La comunidad está muy emocionada por este proyecto.":
        "When do we plan to start construction? The community is very excited about this project.",
      "Excelente. Propongo que votemos hoy para aprobar el presupuesto y podamos avanzar con el proyecto.":
        "Excellent. I propose that we vote today to approve the budget so we can move forward with the project."
    };
    return translations[text] || "[Translation from Azure would appear here]";
  };

  const handleStartDemo = () => {
    setDemoRunning(true);
    setDemoPaused(false);
    setCurrentLineIdx(0);
    setTranslationHistory([]);
  };

  const handlePauseResume = () => {
    setDemoPaused(!demoPaused);
  };

  const handleStop = () => {
    setDemoRunning(false);
    setDemoPaused(false);
    setCurrentLineIdx(0);
    
    // Cancel any ongoing speech
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  };

  const handleManualAdvance = () => {
    processCurrentLine();
  };

  const handleClearTranscript = () => {
    setTranslationHistory([]);
  };

  const currentLine = currentLineIdx < SIMULATED_TRANSCRIPT.length 
    ? SIMULATED_TRANSCRIPT[currentLineIdx] 
    : null;

  const progress = SIMULATED_TRANSCRIPT.length > 0 
    ? currentLineIdx / SIMULATED_TRANSCRIPT.length 
    : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-center mb-2">
            🌐 Azure Live Interpreter Demo
          </h1>
          <p className="text-center text-blue-100 text-lg">
            Simulated Council Meeting - Real-time Translation Demo
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Info Banner */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <p className="text-blue-800 font-medium">
              📋 <strong>Demo Mode:</strong> Simulated council meeting with English ⇄ Spanish translation
            </p>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column: Controls & Current Speaker */}
          <div className="space-y-6">
            <DemoControls
              demoRunning={demoRunning}
              demoPaused={demoPaused}
              progress={progress}
              currentLine={currentLineIdx + 1}
              totalLines={SIMULATED_TRANSCRIPT.length}
              autoAdvance={autoAdvance}
              delaySeconds={delaySeconds}
              enableAudioPlayback={enableAudioPlayback}
              onStart={handleStartDemo}
              onPauseResume={handlePauseResume}
              onStop={handleStop}
              onAutoAdvanceChange={setAutoAdvance}
              onDelayChange={setDelaySeconds}
              onAudioPlaybackChange={setEnableAudioPlayback}
            />

            <DemoSpeakerDisplay
              speaker={currentLine?.speaker || ''}
              lang={currentLine?.lang || 'en-US'}
              text={currentLine?.text || ''}
              supportedLanguages={SUPPORTED_LANGUAGES}
              demoRunning={demoRunning}
              autoAdvance={autoAdvance}
              onManualAdvance={handleManualAdvance}
            />

            {!demoRunning && translationHistory.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-800">✅ Demo completed. Review translations on the right →</p>
              </div>
            )}
          </div>

          {/* Right Column: Live Translations */}
          <div>
            <DemoTranslationDisplay
              translationHistory={translationHistory}
              supportedLanguages={SUPPORTED_LANGUAGES}
              enableAudioPlayback={enableAudioPlayback}
            />
          </div>
        </div>

        {/* Transcript Section */}
        <div className="mt-8">
          <DemoTranscript
            translationHistory={translationHistory}
            supportedLanguages={SUPPORTED_LANGUAGES}
            onClear={handleClearTranscript}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
          <p className="font-medium">Powered by Azure Speech Service | Live Interpreter Demo</p>
          <p className="text-sm mt-1">Simulated council meeting with real-time English ⇄ Spanish translation</p>
        </div>
      </footer>
    </div>
  );
}

export default AppDemo;

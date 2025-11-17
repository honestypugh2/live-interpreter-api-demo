import { useState, useEffect } from 'react';
import './App.css';
import { useWebSocket } from './hooks/useWebSocket';
import { LanguageConfig, TranslationResult, RecordingStatus } from './types/translation';
import ConnectionStatus from './components/ConnectionStatus';
import AudioRecorder from './components/AudioRecorder';
import LanguageSelector from './components/LanguageSelector';
import TranslationDisplay from './components/TranslationDisplay';

function App() {
  const { connectionStatus, lastMessage, sendMessage } = useWebSocket();
  const [recordingStatus, setRecordingStatus] = useState<RecordingStatus>('idle');
  const [translations, setTranslations] = useState<TranslationResult[]>([]);
  const [interimText, setInterimText] = useState<string>('');
  const [interimTranslations, setInterimTranslations] = useState<Record<string, string>>({});
  const [config, setConfig] = useState<LanguageConfig>({
    source_language: 'en-US',
    target_languages: ['es-ES'],
    use_live_interpreter: true,
    use_continuous_mode: true,
    voice_preferences: {},
  });

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (!lastMessage) return;

    switch (lastMessage.type) {
      case 'connected':
        console.log('Connected to server:', lastMessage.data.message);
        // Send initial config
        sendMessage({ type: 'config', data: config });
        break;

      case 'config_confirmed':
        console.log('Config confirmed:', lastMessage.data);
        break;

      case 'recognizing':
        // Interim results - update UI with partial translations
        console.log('Recognizing:', lastMessage.data);
        setInterimText(lastMessage.data.original_text || '');
        setInterimTranslations(lastMessage.data.translations || {});
        break;

      case 'recognized':
        // Final result
        const result: TranslationResult = lastMessage.data;
        setTranslations((prev) => [result, ...prev]);
        setInterimText('');
        setInterimTranslations({});
        console.log('Translation complete:', result);
        break;

      case 'started':
        setRecordingStatus('recording');
        break;

      case 'stopped':
        setRecordingStatus('idle');
        break;

      case 'error':
        console.error('Error from server:', lastMessage.data.message);
        setRecordingStatus('idle');
        break;
    }
  }, [lastMessage, sendMessage, config]);

  const handleStartRecording = () => {
    if (connectionStatus !== 'connected') {
      alert('Not connected to server');
      return;
    }
    sendMessage({ type: 'start_recording', data: {} });
    setRecordingStatus('recording');
  };

  const handleStopRecording = () => {
    sendMessage({ type: 'stop_recording', data: {} });
    setRecordingStatus('processing');
  };

  const handleConfigChange = (newConfig: LanguageConfig) => {
    setConfig(newConfig);
    if (connectionStatus === 'connected') {
      sendMessage({ type: 'config', data: newConfig });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-azure-blue dark:text-blue-400 mb-2">
            🌐 Azure Live Interpreter
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Real-time speech translation powered by Azure Speech Service
          </p>
        </header>

        {/* Connection Status */}
        <ConnectionStatus status={connectionStatus} />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          {/* Left Column - Controls */}
          <div className="lg:col-span-1 space-y-6">
            {/* Language Configuration */}
            <LanguageSelector config={config} onConfigChange={handleConfigChange} />

            {/* Audio Recorder */}
            <AudioRecorder
              recordingStatus={recordingStatus}
              onStartRecording={handleStartRecording}
              onStopRecording={handleStopRecording}
              disabled={connectionStatus !== 'connected'}
            />

            {/* Info Card */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                📖 Quick Guide
              </h3>
              <ul className="text-left text-sm text-gray-600 dark:text-gray-300 space-y-2">
                <li>✓ Select languages</li>
                <li>✓ Click Start Recording</li>
                <li>✓ Speak clearly</li>
                <li>✓ Click Stop when done</li>
                <li>✓ View translations</li>
              </ul>
            </div>
          </div>

          {/* Right Column - Translations */}
          <div className="lg:col-span-2">
            <TranslationDisplay 
              translations={translations}
              interimText={interimText}
              interimTranslations={interimTranslations}
              isRecording={recordingStatus === 'recording'}
            />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600 dark:text-gray-400 text-sm">
          <p>Built with React + TypeScript + Azure Speech Service</p>
          <p className="mt-1">For council meetings, conferences, and multilingual events</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

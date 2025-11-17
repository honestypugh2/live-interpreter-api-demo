import React from 'react';

interface DemoControlsProps {
  demoRunning: boolean;
  demoPaused: boolean;
  progress: number;
  currentLine: number;
  totalLines: number;
  autoAdvance: boolean;
  delaySeconds: number;
  enableAudioPlayback: boolean;
  onStart: () => void;
  onPauseResume: () => void;
  onStop: () => void;
  onAutoAdvanceChange: (enabled: boolean) => void;
  onDelayChange: (seconds: number) => void;
  onAudioPlaybackChange: (enabled: boolean) => void;
}

const DemoControls: React.FC<DemoControlsProps> = ({
  demoRunning,
  demoPaused,
  progress,
  currentLine,
  totalLines,
  autoAdvance,
  delaySeconds,
  enableAudioPlayback,
  onStart,
  onPauseResume,
  onStop,
  onAutoAdvanceChange,
  onDelayChange,
  onAudioPlaybackChange,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-4 border-red-500">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">🎬 Demo Controls</h2>
      <div className="bg-blue-200 p-2 mb-2 text-center font-bold">
        DEMO CONTROLS COMPONENT IS RENDERING
      </div>

      {/* Status Indicator */}
      <div
        className={`p-4 rounded-lg mb-4 ${
          demoRunning
            ? 'bg-blue-50 border-l-4 border-blue-500'
            : 'bg-gray-100 border-l-4 border-gray-400'
        }`}
      >
        <p className="font-medium text-gray-800">
          Status: <span className="font-bold">{demoRunning ? 'Active' : 'Idle'}</span>
        </p>
      </div>

      {/* Control Buttons */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <button
          onClick={onStart}
          disabled={demoRunning}
          className={`py-3 px-4 rounded-lg font-medium transition-colors ${
            demoRunning
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-600 text-white hover:bg-green-700'
          }`}
        >
          ▶️ Start
        </button>

        <button
          onClick={onPauseResume}
          disabled={!demoRunning}
          className={`py-3 px-4 rounded-lg font-medium transition-colors ${
            !demoRunning
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : demoPaused
              ? 'bg-green-600 text-white hover:bg-green-700'
              : 'bg-yellow-600 text-white hover:bg-yellow-700'
          }`}
        >
          {demoPaused ? '▶️ Resume' : '⏸️ Pause'}
        </button>

        <button
          onClick={onStop}
          disabled={!demoRunning}
          className={`py-3 px-4 rounded-lg font-medium transition-colors ${
            !demoRunning
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-red-600 text-white hover:bg-red-700'
          }`}
        >
          ⏹️ Stop
        </button>
      </div>

      {/* Progress Bar */}
      {demoRunning && (
        <div>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-2 overflow-hidden">
            <div
              className="bg-blue-600 h-3 rounded-full transition-all duration-300"
              style={{ width: `${progress * 100}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 text-center">
            Line {currentLine} of {totalLines}
          </p>

          {!demoPaused && (
            <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-blue-800 text-sm">
                🎙️ <strong>Demo in progress...</strong> Watch translations appear in real-time →
              </p>
            </div>
          )}
        </div>
      )}

      {/* Audio Settings */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">🔊 Audio Settings</h3>
        
        <div className="space-y-3">
          {/* Enable Audio Playback */}
          <label className="flex items-center space-x-3 cursor-pointer">
            <input
              type="checkbox"
              checked={enableAudioPlayback}
              onChange={(e) => onAudioPlaybackChange(e.target.checked)}
              className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
            />
            <span className="text-sm font-medium text-gray-700">
              Play translated audio
            </span>
          </label>

          {/* Auto-advance */}
          <label className="flex items-center space-x-3 cursor-pointer">
            <input
              type="checkbox"
              checked={autoAdvance}
              onChange={(e) => onAutoAdvanceChange(e.target.checked)}
              className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
            />
            <span className="text-sm font-medium text-gray-700">
              Auto-advance lines
            </span>
          </label>

          {/* Delay Slider (only shown when auto-advance is enabled) */}
          {autoAdvance && (
            <div className="ml-7 mt-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Delay: {delaySeconds}s
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={delaySeconds}
                onChange={(e) => onDelayChange(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>1s</span>
                <span>5s</span>
                <span>10s</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Demo Info */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">ℹ️ Demo Information</h3>
        <div className="bg-gray-50 rounded-lg p-4 space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Mode:</span>
            <span className="font-medium text-gray-800">Simulated (No Backend)</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Languages:</span>
            <span className="font-medium text-gray-800">English ⇄ Spanish</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Total Lines:</span>
            <span className="font-medium text-gray-800">{totalLines}</span>
          </div>
        </div>
        <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
          <p className="text-xs text-blue-800">
            💡 <strong>Tip:</strong> This demo runs entirely in your browser with simulated data. 
            No microphone or Azure API required!
          </p>
        </div>
      </div>
    </div>
  );
};

export default DemoControls;

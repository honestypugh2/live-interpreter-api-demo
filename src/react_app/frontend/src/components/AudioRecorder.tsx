import { RecordingStatus } from '../types/translation';

interface Props {
  recordingStatus: RecordingStatus;
  onStartRecording: () => void;
  onStopRecording: () => void;
  disabled: boolean;
}

const AudioRecorder = ({ recordingStatus, onStartRecording, onStopRecording, disabled }: Props) => {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        🎤 Audio Recording
      </h3>

      {/* Status Display */}
      <div className="mb-4">
        {recordingStatus === 'idle' && (
          <div className="text-gray-600 dark:text-gray-300 text-sm">
            Ready to record
          </div>
        )}
        {recordingStatus === 'recording' && (
          <div className="text-red-600 dark:text-red-400 text-sm font-semibold animate-pulse">
            🔴 Recording in progress...
          </div>
        )}
        {recordingStatus === 'processing' && (
          <div className="text-blue-600 dark:text-blue-400 text-sm">
            ⏳ Processing translation...
          </div>
        )}
      </div>

      {/* Control Buttons */}
      <div className="space-y-3">
        <button
          onClick={onStartRecording}
          disabled={disabled || recordingStatus !== 'idle'}
          className="btn-danger w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {recordingStatus === 'recording' ? '🔴 Recording...' : '🎙️ Start Recording'}
        </button>

        <button
          onClick={onStopRecording}
          disabled={recordingStatus !== 'recording'}
          className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ⏹️ Stop & Translate
        </button>
      </div>

      {/* Visual Indicator */}
      {recordingStatus === 'recording' && (
        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded border border-red-200 dark:border-red-800">
          <p className="text-xs text-red-700 dark:text-red-300">
            💡 Speak clearly into your microphone
          </p>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;

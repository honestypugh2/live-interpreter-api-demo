/**
 * Translation-related TypeScript types
 */

export interface TranslationResult {
  original_text: string;
  detected_language?: string;
  translations: Record<string, string>;
  timestamp: string;
  duration_ms: number;
  synthesized_audio?: Record<string, string>;  // Base64 encoded audio per language
}

export interface LanguageConfig {
  source_language?: string;
  target_languages: string[];
  use_live_interpreter: boolean;
  use_continuous_mode?: boolean;
  voice_preferences?: Record<string, string>;
}

export interface WebSocketMessage {
  type: 'connected' | 'config_confirmed' | 'recognizing' | 'recognized' | 'audio' | 'started' | 'stopped' | 'error' | 'pong';
  data: any;
}

export interface AudioData {
  audio: string; // base64 encoded
  format: string;
  sample_rate: number;
}

export interface ServerConfig {
  source_language: string;
  target_languages: string[];
  voice_name: string;
  region: string;
  live_interpreter_enabled: boolean;
  auto_detect_enabled: boolean;
}

export interface HealthStatus {
  status: string;
  version: string;
  azure_region: string;
  live_interpreter_enabled: boolean;
}

export type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error';
export type RecordingStatus = 'idle' | 'recording' | 'processing';

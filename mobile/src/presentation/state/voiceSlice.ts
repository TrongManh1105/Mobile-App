export type VoiceStateStatus =
  | 'Idle'
  | 'Listening'
  | 'Processing'
  | 'Recognized'
  | 'Error';

export interface VoiceState {
  status: VoiceStateStatus;
  amplitude: number;             // 0.0 to 1.0 for real-time waveform visualizer
  liveTranscript: string;
  confidenceScore: number;
  detectedIntent: string | null;
  errorMessage: string | null;
  canRetry: boolean;
}

export const initialVoiceState: VoiceState = {
  status: 'Idle',
  amplitude: 0.0,
  liveTranscript: '',
  confidenceScore: 1.0,
  detectedIntent: null,
  errorMessage: null,
  canRetry: true
};

// Pure Reducer Logic
export function voiceReducer(
  state: VoiceState = initialVoiceState,
  action: { type: string; payload?: any }
): VoiceState {
  switch (action.type) {
    case 'voice/startListening':
      return {
        ...state,
        status: 'Listening',
        amplitude: 0.1,
        liveTranscript: '',
        detectedIntent: null,
        errorMessage: null
      };

    case 'voice/updateAmplitude':
      return {
        ...state,
        amplitude: action.payload
      };

    case 'voice/setProcessing':
      return {
        ...state,
        status: 'Processing',
        liveTranscript: action.payload?.transcript || state.liveTranscript
      };

    case 'voice/intentRecognized':
      return {
        ...state,
        status: 'Recognized',
        detectedIntent: action.payload.intent,
        confidenceScore: action.payload.confidenceScore,
        liveTranscript: action.payload.rawTranscript
      };

    case 'voice/setError':
      return {
        ...state,
        status: 'Error',
        errorMessage: action.payload.message,
        canRetry: action.payload.canRetry ?? true
      };

    case 'voice/resetIdle':
      return {
        ...initialVoiceState
      };

    default:
      return state;
  }
}


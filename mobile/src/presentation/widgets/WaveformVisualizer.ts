export interface WaveformBar {
  index: number;
  heightPercentage: number; // 10% to 100%
}

export class WaveformVisualizer {
  /**
   * Generates dynamic height values for 16 bars representing the audio frequency waveform.
   * Modulated by the live amplitude (0.0 to 1.0).
   */
  public static calculateBars(amplitude: number, barCount: number = 16): WaveformBar[] {
    const clampedAmp = Math.max(0.05, Math.min(amplitude, 1.0));
    const bars: WaveformBar[] = [];

    for (let i = 0; i < barCount; i++) {
      // Bell-curve shape in middle + amplitude modulation
      const normalizedPosition = i / (barCount - 1);
      const bellCurve = Math.sin(normalizedPosition * Math.PI);
      const randomJitter = (Math.sin(i * 3.5 + Date.now() / 150) + 1.0) * 0.2;
      const height = Math.min(100, Math.max(15, (bellCurve * 70 + randomJitter * 20) * clampedAmp));

      bars.push({
        index: i,
        heightPercentage: Math.round(height)
      });
    }

    return bars;
  }
}


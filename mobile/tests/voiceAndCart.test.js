import test from 'node:test';
import assert from 'node:assert/strict';

import { voiceReducer, initialVoiceState } from '../src/presentation/state/voiceSlice.ts';
import { cartReducer, initialCartState } from '../src/presentation/state/cartSlice.ts';
import { trackingReducer, initialTrackingState } from '../src/presentation/state/orderTrackingSlice.ts';
import { DeepLinkLauncher } from '../src/core/utils/deepLinkLauncher.ts';
import { WaveformVisualizer } from '../src/presentation/widgets/WaveformVisualizer.ts';

test('Voice State Machine transitions through 5 states correctly', () => {
  // 1. Initial State: Idle
  assert.equal(initialVoiceState.status, 'Idle');

  // 2. Start Listening
  const listeningState = voiceReducer(initialVoiceState, { type: 'voice/startListening' });
  assert.equal(listeningState.status, 'Listening');
  assert.equal(listeningState.amplitude, 0.1);

  // 3. Update Amplitude (for Waveform Visualizer)
  const ampState = voiceReducer(listeningState, { type: 'voice/updateAmplitude', payload: 0.85 });
  assert.equal(ampState.amplitude, 0.85);

  // 4. Processing
  const processingState = voiceReducer(ampState, {
    type: 'voice/setProcessing',
    payload: { transcript: 'Cho 2 phở bò tái' }
  });
  assert.equal(processingState.status, 'Processing');
  assert.equal(processingState.liveTranscript, 'Cho 2 phở bò tái');

  // 5. Intent Recognized
  const recognizedState = voiceReducer(processingState, {
    type: 'voice/intentRecognized',
    payload: {
      intent: 'AddToCart',
      confidenceScore: 0.94,
      rawTranscript: 'Cho 2 phở bò tái'
    }
  });
  assert.equal(recognizedState.status, 'Recognized');
  assert.equal(recognizedState.detectedIntent, 'AddToCart');

  // 6. Error State with fallback
  const errorState = voiceReducer(recognizedState, {
    type: 'voice/setError',
    payload: { message: 'Không thể kết nối micro', canRetry: true }
  });
  assert.equal(errorState.status, 'Error');
  assert.equal(errorState.errorMessage, 'Không thể kết nối micro');
  assert.equal(errorState.canRetry, true);

  // 7. Reset back to Idle
  const resetState = voiceReducer(errorState, { type: 'voice/resetIdle' });
  assert.equal(resetState.status, 'Idle');
});

test('Cart Reducer handles adding items, calculating totals and updating quantities', () => {
  // Add first dish: 2 x Phở Bò (65.000đ)
  const state1 = cartReducer(initialCartState, {
    type: 'cart/addItem',
    payload: {
      dishId: 'pho_01',
      dishName: 'Phở Bò Tái Nạm',
      quantity: 2,
      unitPrice: 65000,
      note: 'Nhiều hành'
    }
  });
  assert.equal(state1.items.length, 1);
  assert.equal(state1.items[0].quantity, 2);
  assert.equal(state1.totalAmount, 130000);

  // Add complementary side: 2 x Quẩy Giòn (10.000đ)
  const state2 = cartReducer(state1, {
    type: 'cart/addItem',
    payload: {
      dishId: 'side_01',
      dishName: 'Quẩy Giòn',
      quantity: 2,
      unitPrice: 10000
    }
  });
  assert.equal(state2.items.length, 2);
  assert.equal(state2.totalAmount, 150000);

  // Add existing dish again -> Increments quantity
  const state3 = cartReducer(state2, {
    type: 'cart/addItem',
    payload: {
      dishId: 'pho_01',
      dishName: 'Phở Bò Tái Nạm',
      quantity: 1,
      unitPrice: 65000
    }
  });
  assert.equal(state3.items[0].quantity, 3);
  assert.equal(state3.totalAmount, 215000);

  // Remove dish from cart
  const state4 = cartReducer(state3, {
    type: 'cart/removeItem',
    payload: 'side_01'
  });
  assert.equal(state4.items.length, 1);
  assert.equal(state4.totalAmount, 195000);
});

test('Order Tracking Reducer handles timers and state transitions', () => {
  const dummyOrder = {
    orderId: 'ORD-123',
    customerPhone: '0912345678',
    customerName: 'Test User',
    merchantPhone: '0987654321',
    status: 'CONFIRMED',
    totalAmount: 130000,
    estimatedPrepTimeMinutes: 15,
    deliveryType: 'DineIn',
    addressOrTable: 'Bàn 1',
    whatsappUrl: 'https://wa.me/test',
    smsUrl: 'sms:test',
    createdAt: new Date().toISOString(),
    items: []
  };

  const state1 = trackingReducer(initialTrackingState, {
    type: 'tracking/setOrder',
    payload: dummyOrder
  });
  assert.equal(state1.status, 'CONFIRMED');
  assert.equal(state1.remainingSeconds, 900); // 15 mins * 60

  // Decrement timer
  const state2 = trackingReducer(state1, { type: 'tracking/decrementTimer' });
  assert.equal(state2.remainingSeconds, 899);

  // Transition to PREPARING
  const state3 = trackingReducer(state2, {
    type: 'tracking/updateStatus',
    payload: { status: 'PREPARING', message: 'Bếp bắt đầu nấu' }
  });
  assert.equal(state3.status, 'PREPARING');
  assert.equal(state3.statusNotification, 'Bếp bắt đầu nấu');
});

test('DeepLinkLauncher falls back gracefully to SMS when WhatsApp is unavailable', async () => {
  const wa = 'https://wa.me/84987654321?text=OrderPayload';
  const sms = 'sms:0987654321?body=OrderPayload';

  // Device has WhatsApp
  const resultWA = await DeepLinkLauncher.dispatchOrder(wa, sms, true);
  assert.equal(resultWA.channel, 'WhatsApp');
  assert.equal(resultWA.url, wa);

  // Device does not have WhatsApp
  const resultSMS = await DeepLinkLauncher.dispatchOrder(wa, sms, false);
  assert.equal(resultSMS.channel, 'SMS');
  assert.equal(resultSMS.url, sms);
});

test('WaveformVisualizer generates 16 modulated frequency bars', () => {
  const bars = WaveformVisualizer.calculateBars(0.8, 16);
  assert.equal(bars.length, 16);
  for (const bar of bars) {
    assert.ok(bar.heightPercentage >= 10 && bar.heightPercentage <= 100);
  }
});

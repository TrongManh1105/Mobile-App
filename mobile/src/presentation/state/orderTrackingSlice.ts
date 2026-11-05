import type { OrderEntity, OrderStatus } from '../../domain/entities/order.ts';
import type { NearbyPOIEntity } from '../../domain/entities/poi.ts';

export interface OrderTrackingState {
  currentOrder: OrderEntity | null;
  status: OrderStatus | null;
  remainingSeconds: number;
  nearbyPOIs: NearbyPOIEntity[];
  statusNotification: string | null;
}

export const initialTrackingState: OrderTrackingState = {
  currentOrder: null,
  status: null,
  remainingSeconds: 0,
  nearbyPOIs: [],
  statusNotification: null
};

export function trackingReducer(
  state: OrderTrackingState = initialTrackingState,
  action: { type: string; payload?: any }
): OrderTrackingState {
  switch (action.type) {
    case 'tracking/setOrder': {
      const order: OrderEntity = action.payload;
      return {
        ...state,
        currentOrder: order,
        status: order.status,
        remainingSeconds: (order.estimatedPrepTimeMinutes || 15) * 60
      };
    }

    case 'tracking/updateStatus': {
      const { status, message }: { status: OrderStatus; message?: string } = action.payload;
      return {
        ...state,
        status,
        statusNotification: message || `Đơn hàng chuyển sang trạng thái: ${status}`
      };
    }

    case 'tracking/decrementTimer': {
      return {
        ...state,
        remainingSeconds: Math.max(state.remainingSeconds - 1, 0)
      };
    }

    case 'tracking/setNearbyPOIs': {
      return {
        ...state,
        nearbyPOIs: action.payload
      };
    }

    default:
      return state;
  }
}

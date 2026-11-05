import type { CartItemEntity } from '../../domain/entities/order.ts';

export interface CartState {
  items: CartItemEntity[];
  totalAmount: number;
}

export const initialCartState: CartState = {
  items: [],
  totalAmount: 0
};

export function calculateCartTotal(items: CartItemEntity[]): number {
  return items.reduce((sum, it) => sum + it.quantity * it.unitPrice, 0);
}

export function cartReducer(
  state: CartState = initialCartState,
  action: { type: string; payload?: any }
): CartState {
  switch (action.type) {
    case 'cart/addItem': {
      const newItem: CartItemEntity = action.payload;
      const existingIdx = state.items.findIndex(it => it.dishId === newItem.dishId);
      let updatedItems: CartItemEntity[];

      if (existingIdx >= 0) {
        updatedItems = state.items.map((it, idx) =>
          idx === existingIdx
            ? { ...it, quantity: it.quantity + (newItem.quantity || 1) }
            : it
        );
      } else {
        updatedItems = [...state.items, { ...newItem, quantity: newItem.quantity || 1 }];
      }

      return {
        items: updatedItems,
        totalAmount: calculateCartTotal(updatedItems)
      };
    }

    case 'cart/removeItem': {
      const dishIdToRemove: string = action.payload;
      const updatedItems = state.items.filter(it => it.dishId !== dishIdToRemove);
      return {
        items: updatedItems,
        totalAmount: calculateCartTotal(updatedItems)
      };
    }

    case 'cart/updateQuantity': {
      const { dishId, quantity }: { dishId: string; quantity: number } = action.payload;
      let updatedItems: CartItemEntity[];
      if (quantity <= 0) {
        updatedItems = state.items.filter(it => it.dishId !== dishId);
      } else {
        updatedItems = state.items.map(it =>
          it.dishId === dishId ? { ...it, quantity } : it
        );
      }
      return {
        items: updatedItems,
        totalAmount: calculateCartTotal(updatedItems)
      };
    }

    case 'cart/clearCart':
      return initialCartState;

    default:
      return state;
  }
}

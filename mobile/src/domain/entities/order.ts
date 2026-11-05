export interface CartItemEntity {
  dishId: string;
  dishName: string;
  quantity: number;
  unitPrice: number;
  note?: string;
}

export type OrderStatus =
  | 'CREATED'
  | 'CONFIRMED'
  | 'PREPARING'
  | 'READY'
  | 'COMPLETED'
  | 'CANCELLED';

export interface OrderEntity {
  orderId: string;
  customerPhone: string;
  customerName: string;
  merchantPhone: string;
  status: OrderStatus;
  totalAmount: number;
  estimatedPrepTimeMinutes: number;
  deliveryType: 'DineIn' | 'Takeaway' | 'Delivery';
  addressOrTable: string;
  orderNotes?: string;
  whatsappUrl: string;
  smsUrl: string;
  createdAt: string;
  items: CartItemEntity[];
}


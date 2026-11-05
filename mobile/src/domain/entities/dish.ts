export interface DishEntity {
  id: string;
  name: string;
  category: string;
  price: number;
  prepTimeMinutes: number;
  flavorTags: string[];
  mealTypes: string[];
  isVegetarian: boolean;
  isAvailable: boolean;
  imageUrl?: string;
}

export interface ComboEntity {
  comboId: string;
  comboName: string;
  primaryDishId: string;
  complementaryDish: DishEntity;
  discountRate: number;
  originalTotal: number;
  discountedTotal: number;
}


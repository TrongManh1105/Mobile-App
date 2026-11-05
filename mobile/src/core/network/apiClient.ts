export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://127.0.0.1:8000/api/v1') {
    this.baseUrl = baseUrl;
  }

  async getDishes(category?: string, isVegetarian?: boolean): Promise<any[]> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (isVegetarian !== undefined) params.append('is_vegetarian', String(isVegetarian));

    const response = await fetch(`${this.baseUrl}/dishes/?${params.toString()}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  }

  async getRecommendations(cartDishIds: string[], currentHour: number = 12): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/recommendations/dishes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cart_dish_ids: cartDishIds,
        current_time_hour: currentHour,
        limit: 4
      })
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  }

  async getNearbyPOIs(waitMinutes: number = 20): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/poi/nearby?available_wait_minutes=${waitMinutes}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  }

  async createOrder(orderPayload: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/orders/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderPayload)
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  }
}

export const apiClient = new ApiClient();


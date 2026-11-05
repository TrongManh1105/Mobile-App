export interface NearbyPOIEntity {
  id: string;
  name: string;
  category: 'Park' | 'Bookstore' | 'Cafe' | 'Landmark';
  latitude: number;
  longitude: number;
  distanceMeters: number;
  walkingDurationMinutes: number;
  suggestedVisitMinutes: number;
  thumbnailUrl?: string;
  googleMapsUrl?: string;
  description?: string;
}


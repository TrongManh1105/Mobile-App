import asyncio
from app.core.database import AsyncSessionLocal, init_db
from app.infrastructure.db.models import Dish, Combo, NearbyPOI, User

SAMPLE_DISHES = [
    # --- PHỞ (NOODLES) ---
    {
        "id": "pho_01",
        "name": "Phở Bò Tái Nạm",
        "category": "Pho",
        "price": 65000,
        "prep_time_minutes": 8,
        "flavor_tags": ["dam_da", "nong", "thanh"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.8, 0.1, 0.9, 0.65],
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=500"
    },
    {
        "id": "pho_02",
        "name": "Phở Bò Sốt Vang",
        "category": "Pho",
        "price": 75000,
        "prep_time_minutes": 10,
        "flavor_tags": ["dam_da", "beo_ngay", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.9, 0.2, 0.9, 0.75],
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=500"
    },
    {
        "id": "pho_03",
        "name": "Phở Gà Ta Thảo Mộc",
        "category": "Pho",
        "price": 60000,
        "prep_time_minutes": 8,
        "flavor_tags": ["thanh", "nong", "thom"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.9, 0.60],
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=500"
    },
    {
        "id": "pho_04",
        "name": "Phở Chay Nấm Hương Rong Biển",
        "category": "Pho",
        "price": 50000,
        "prep_time_minutes": 7,
        "flavor_tags": ["thanh", "nong", "ngot_diu"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.8, 0.50],
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=500"
    },

    # --- CƠM (RICE DISHES) ---
    {
        "id": "com_01",
        "name": "Cơm Tấm Sườn Bì Chả",
        "category": "Com",
        "price": 65000,
        "prep_time_minutes": 10,
        "flavor_tags": ["dam_da", "beo_ngay", "chua_ngot"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.85, 0.3, 0.7, 0.65],
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"
    },
    {
        "id": "com_02",
        "name": "Cơm Gà Xối Mỡ Giòn Da",
        "category": "Com",
        "price": 60000,
        "prep_time_minutes": 12,
        "flavor_tags": ["gion", "beo_ngay", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.8, 0.4, 0.7, 0.60],
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"
    },
    {
        "id": "com_03",
        "name": "Cơm Rang Dưa Bò",
        "category": "Com",
        "price": 55000,
        "prep_time_minutes": 9,
        "flavor_tags": ["chua_nhe", "dam_da", "nong"],
        "meal_types": ["lunch", "dinner", "late_night"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.75, 0.2, 0.8, 0.55],
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"
    },
    {
        "id": "com_04",
        "name": "Cơm Niêu Chay Đậu Hũ Sốt Cà",
        "category": "Com",
        "price": 45000,
        "prep_time_minutes": 10,
        "flavor_tags": ["thanh", "chua_ngot", "nong"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.5, 0.1, 0.7, 0.45],
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"
    },

    # --- BÚN / MÌ (BUN & NOODLES) ---
    {
        "id": "bun_01",
        "name": "Bún Bò Huế Cốt Đậm",
        "category": "Bun",
        "price": 65000,
        "prep_time_minutes": 8,
        "flavor_tags": ["cay", "dam_da", "thom_xa", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.8, 0.0, 0.8, 0.0, 0.95, 0.8, 0.9, 0.65],
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500"
    },
    {
        "id": "bun_02",
        "name": "Bún Chả Hà Nội Nướng Than Hoa",
        "category": "Bun",
        "price": 60000,
        "prep_time_minutes": 10,
        "flavor_tags": ["chua_ngot", "thom_khoi", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.6, 0.0, 0.9, 0.0, 0.7, 0.2, 0.6, 0.60],
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500"
    },
    {
        "id": "bun_03",
        "name": "Bún Đậu Mắm Tôm Đầy Đủ",
        "category": "Bun",
        "price": 70000,
        "prep_time_minutes": 10,
        "flavor_tags": ["dam_da", "chua_cay", "gion"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.5, 0.0, 0.9, 0.0, 0.9, 0.5, 0.5, 0.70],
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500"
    },
    {
        "id": "bun_04",
        "name": "Mì Quảng Tôm Thịt",
        "category": "Bun",
        "price": 55000,
        "prep_time_minutes": 8,
        "flavor_tags": ["dam_da", "thom_dau_phung", "nhe_nuoc"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.7, 0.0, 0.8, 0.0, 0.75, 0.3, 0.6, 0.55],
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500"
    },

    # --- ĐỒ ĂN KÈM (COMPLEMENTARY / SIDES) ---
    {
        "id": "side_01",
        "name": "Quẩy Giòn Phở",
        "category": "DoAnKem",
        "price": 10000,
        "prep_time_minutes": 1,
        "flavor_tags": ["gion", "xop"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.3, 0.0, 0.0, 0.0, 0.2, 0.0, 0.1, 0.10],
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500"
    },
    {
        "id": "side_02",
        "name": "Trứng Chần Nước Béo",
        "category": "DoAnKem",
        "price": 10000,
        "prep_time_minutes": 3,
        "flavor_tags": ["beo_ngay", "ngot_thom", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.4, 0.0, 0.0, 0.0, 0.6, 0.0, 0.5, 0.10],
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500"
    },
    {
        "id": "side_03",
        "name": "Canh Khổ Qua Nhồi Thịt",
        "category": "DoAnKem",
        "price": 25000,
        "prep_time_minutes": 5,
        "flavor_tags": ["thanh_nhiet", "dang_nhe", "nong"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.2, 0.4, 0.0, 0.0, 0.4, 0.0, 0.7, 0.25],
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=500"
    },
    {
        "id": "side_04",
        "name": "Chả Cốm Chiên Giòn",
        "category": "DoAnKem",
        "price": 25000,
        "prep_time_minutes": 5,
        "flavor_tags": ["gion", "thom_com", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.1, 0.1, 0.5, 0.0, 0.6, 0.1, 0.4, 0.25],
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=500"
    },

    # --- ĐỒ UỐNG (BEVERAGES) ---
    {
        "id": "drink_01",
        "name": "Trà Đá Thảo Mộc",
        "category": "DoUong",
        "price": 5000,
        "prep_time_minutes": 1,
        "flavor_tags": ["mat_lanh", "thanh", "giai_nhiet"],
        "meal_types": ["breakfast", "lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.1, 0.0, 0.0, 0.05],
        "image_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=500"
    },
    {
        "id": "drink_02",
        "name": "Trà Chanh Mật Ong Giã Tay",
        "category": "DoUong",
        "price": 25000,
        "prep_time_minutes": 3,
        "flavor_tags": ["chua_ngot", "mat_lanh", "thom_chanh"],
        "meal_types": ["lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.4, 0.0, 0.0, 0.25],
        "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"
    },
    {
        "id": "drink_03",
        "name": "Cà Phê Sữa Đá Sài Gòn",
        "category": "DoUong",
        "price": 30000,
        "prep_time_minutes": 3,
        "flavor_tags": ["dam_da", "dang_ngot", "beo", "tinh_tao"],
        "meal_types": ["breakfast", "lunch", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.8, 0.0, 0.1, 0.30],
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"
    },
    {
        "id": "drink_04",
        "name": "Nước Mơ Chùa Hương Ướp Lạnh",
        "category": "DoUong",
        "price": 20000,
        "prep_time_minutes": 2,
        "flavor_tags": ["chua_ngot", "mat_lanh", "thanh_nhiet"],
        "meal_types": ["lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.35, 0.0, 0.0, 0.20],
        "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"
    },

    # --- TRÁNG MIỆNG (DESSERT) ---
    {
        "id": "dessert_01",
        "name": "Chè Bưởi An Giang",
        "category": "TrangMieng",
        "price": 25000,
        "prep_time_minutes": 2,
        "flavor_tags": ["ngot_thanh", "beo_nuoc_cot_dua", "gion"],
        "meal_types": ["afternoon_snack", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.1, 0.25],
        "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=500"
    },
    {
        "id": "dessert_02",
        "name": "Sữa Chua Nếp Cẩm Phố Cổ",
        "category": "TrangMieng",
        "price": 25000,
        "prep_time_minutes": 2,
        "flavor_tags": ["chua_ngot", "beo_ngay", "mat_lanh"],
        "meal_types": ["lunch", "afternoon_snack", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 0.5, 0.45, 0.0, 0.0, 0.25],
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500"
    }
]

SAMPLE_COMBOS = [
    {
        "id": "combo_01",
        "primary_dish_id": "pho_01",
        "complementary_dish_id": "side_01",
        "discount_rate": 0.10,
        "combo_name": "Combo Phở Bò Tái & Quẩy Giòn"
    },
    {
        "id": "combo_02",
        "primary_dish_id": "pho_01",
        "complementary_dish_id": "drink_01",
        "discount_rate": 0.10,
        "combo_name": "Combo Phở Bò Tái & Trà Đá Thảo Mộc"
    },
    {
        "id": "combo_03",
        "primary_dish_id": "com_01",
        "complementary_dish_id": "side_03",
        "discount_rate": 0.15,
        "combo_name": "Combo Cơm Tấm & Canh Khổ Qua Nhồi Thịt"
    },
    {
        "id": "combo_04",
        "primary_dish_id": "com_01",
        "complementary_dish_id": "drink_02",
        "discount_rate": 0.10,
        "combo_name": "Combo Cơm Tấm & Trà Chanh Mật Ong"
    },
    {
        "id": "combo_05",
        "primary_dish_id": "bun_01",
        "complementary_dish_id": "drink_01",
        "discount_rate": 0.10,
        "combo_name": "Combo Bún Bò Huế Cay Nồng & Trà Đá Thanh Nhiệt"
    },
    {
        "id": "combo_06",
        "primary_dish_id": "bun_03",
        "complementary_dish_id": "drink_04",
        "discount_rate": 0.15,
        "combo_name": "Combo Bún Đậu Mắm Tôm & Nước Mơ Chùa Hương"
    }
]

SAMPLE_POIS = [
    {
        "id": "poi_01",
        "name": "Công Viên Bách Thảo Hà Nội",
        "category": "Park",
        "latitude": 21.0368,
        "longitude": 105.8285,
        "suggested_visit_minutes": 15,
        "walking_duration_minutes": 5,
        "thumbnail_url": "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0368,105.8285",
        "description": "Không gian cây xanh mát mẻ, hồ nước yên bình lý tưởng đi dạo ngắn 15 phút."
    },
    {
        "id": "poi_02",
        "name": "Nhà Sách Phố Đinh Lễ",
        "category": "Bookstore",
        "latitude": 21.0267,
        "longitude": 105.8532,
        "suggested_visit_minutes": 20,
        "walking_duration_minutes": 4,
        "thumbnail_url": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0267,105.8532",
        "description": "Phố sách lâu đời, nhiều sách hay và không khí tĩnh lặng thư giãn."
    },
    {
        "id": "poi_03",
        "name": "Quán Trà Nhài Yên Tĩnh",
        "category": "Cafe",
        "latitude": 21.0305,
        "longitude": 105.8505,
        "suggested_visit_minutes": 20,
        "walking_duration_minutes": 3,
        "thumbnail_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0305,105.8505",
        "description": "Không gian máy lạnh thưởng trà hoa nhài thư giãn trong lúc chờ món."
    },
    {
        "id": "poi_04",
        "name": "Hồ Hoàn Kiếm & Cầu Thê Húc",
        "category": "Landmark",
        "latitude": 21.0287,
        "longitude": 105.8524,
        "suggested_visit_minutes": 25,
        "walking_duration_minutes": 6,
        "thumbnail_url": "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0287,105.8524",
        "description": "Biểu tượng thủ đô, không gian lộng gió cho một vòng đi bộ ngắm cảnh."
    }
]

async def seed_database():
    print("Initializing database schema...")
    await init_db()
    async with AsyncSessionLocal() as session:
        # Check if already seeded
        from sqlalchemy import select
        result = await session.execute(select(Dish))
        existing_dishes = result.scalars().all()
        if existing_dishes:
            print(f"Database already contains {len(existing_dishes)} dishes. Skipping seed.")
            return

        print(f"Seeding {len(SAMPLE_DISHES)} dishes...")
        for dish_data in SAMPLE_DISHES:
            session.add(Dish(**dish_data))

        print(f"Seeding {len(SAMPLE_COMBOS)} combos...")
        for combo_data in SAMPLE_COMBOS:
            session.add(Combo(**combo_data))

        print(f"Seeding {len(SAMPLE_POIS)} POIs...")
        for poi_data in SAMPLE_POIS:
            session.add(NearbyPOI(**poi_data))

        await session.commit()
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    async def main():
        await seed_database()
        await engine.dispose()
    asyncio.run(main())


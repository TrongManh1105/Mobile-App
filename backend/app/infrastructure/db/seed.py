import asyncio
from sqlalchemy import select, delete
from app.core.database import AsyncSessionLocal, init_db, engine
from app.infrastructure.db.models import Dish, Combo, NearbyPOI, User

SAMPLE_DISHES = [
    # --- PHỞ (PHO NOODLES) ---
    {
        "id": "pho_01",
        "name": "Phở Bò Tái Lăn Hà Nội",
        "category": "Pho",
        "price": 65000,
        "prep_time_minutes": 8,
        "flavor_tags": ["dam_da", "thom_toi", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.85, 0.1, 0.9, 0.65],
        "image_url": "/static/images/pho_01.jpg"
    },
    {
        "id": "pho_02",
        "name": "Phở Bò Sốt Vang Ngũ Vị",
        "category": "Pho",
        "price": 75000,
        "prep_time_minutes": 10,
        "flavor_tags": ["dam_da", "beo_ngay", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.9, 0.2, 0.9, 0.75],
        "image_url": "/static/images/pho_02.jpg"
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
        "image_url": "/static/images/pho_03.jpg"
    },
    {
        "id": "pho_04",
        "name": "Phở Chay Nấm Hương Hạt Sen",
        "category": "Pho",
        "price": 50000,
        "prep_time_minutes": 7,
        "flavor_tags": ["thanh", "nong", "ngot_diu"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.8, 0.50],
        "image_url": "/static/images/pho_04.jpg"
    },

    # --- CƠM (RICE DISHES) ---
    {
        "id": "com_01",
        "name": "Cơm Tấm Sườn Bì Chả Đặc Biệt",
        "category": "Com",
        "price": 68000,
        "prep_time_minutes": 10,
        "flavor_tags": ["dam_da", "beo_ngay", "chua_ngot"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.85, 0.3, 0.7, 0.68],
        "image_url": "/static/images/com_01.jpg"
    },
    {
        "id": "com_02",
        "name": "Cơm Gà Xối Mỡ Giòn Da",
        "category": "Com",
        "price": 65000,
        "prep_time_minutes": 12,
        "flavor_tags": ["gion", "beo_ngay", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.8, 0.4, 0.7, 0.65],
        "image_url": "/static/images/com_02.jpg"
    },
    {
        "id": "com_03",
        "name": "Cơm Gà Hải Nam Luộc Da Vàng",
        "category": "Com",
        "price": 60000,
        "prep_time_minutes": 10,
        "flavor_tags": ["thanh", "thom_gwon", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.7, 0.1, 0.7, 0.60],
        "image_url": "/static/images/com_03.jpg"
    },
    {
        "id": "com_04",
        "name": "Cơm Rang Dưa Bò Phố Cổ",
        "category": "Com",
        "price": 55000,
        "prep_time_minutes": 9,
        "flavor_tags": ["chua_nhe", "dam_da", "nong"],
        "meal_types": ["lunch", "dinner", "late_night"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.75, 0.2, 0.8, 0.55],
        "image_url": "/static/images/com_04.jpg"
    },
    {
        "id": "com_05",
        "name": "Cơm Niêu Chay Đậu Hũ Sốt Nấm",
        "category": "Com",
        "price": 48000,
        "prep_time_minutes": 10,
        "flavor_tags": ["thanh", "chua_ngot", "nong"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.5, 0.1, 0.7, 0.48],
        "image_url": "/static/images/com_05.jpg"
    },

    # --- BÚN / MÌ (BUN & NOODLES) ---
    {
        "id": "bun_01",
        "name": "Bún Bò Huế Cốt Đậm Sa Tế",
        "category": "Bun",
        "price": 68000,
        "prep_time_minutes": 8,
        "flavor_tags": ["cay", "dam_da", "thom_xa", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.8, 0.0, 0.8, 0.0, 0.95, 0.8, 0.9, 0.68],
        "image_url": "/static/images/bun_01.jpg"
    },
    {
        "id": "bun_02",
        "name": "Bún Chả Hà Nội Nướng Than Hoa",
        "category": "Bun",
        "price": 62000,
        "prep_time_minutes": 10,
        "flavor_tags": ["chua_ngot", "thom_khoi", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.6, 0.0, 0.9, 0.0, 0.7, 0.2, 0.6, 0.62],
        "image_url": "/static/images/bun_02.jpg"
    },
    {
        "id": "bun_03",
        "name": "Bún Đậu Mắm Tôm Mẹt Đầy Đủ",
        "category": "Bun",
        "price": 75000,
        "prep_time_minutes": 10,
        "flavor_tags": ["dam_da", "chua_cay", "gion"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.5, 0.0, 0.9, 0.0, 0.9, 0.5, 0.5, 0.75],
        "image_url": "/static/images/bun_03.jpg"
    },
    {
        "id": "bun_04",
        "name": "Bún Thịt Nướng Chả Giò Giòn",
        "category": "Bun",
        "price": 58000,
        "prep_time_minutes": 9,
        "flavor_tags": ["chua_ngot", "gion", "thom"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.6, 0.0, 0.8, 0.0, 0.7, 0.3, 0.6, 0.58],
        "image_url": "/static/images/bun_04.jpg"
    },
    {
        "id": "bun_05",
        "name": "Mì Quảng Tôm Thịt Trứng Cút",
        "category": "Bun",
        "price": 55000,
        "prep_time_minutes": 8,
        "flavor_tags": ["dam_da", "thom_dau_phung", "nhe_nuoc"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.7, 0.0, 0.8, 0.0, 0.75, 0.3, 0.6, 0.55],
        "image_url": "/static/images/bun_05.jpg"
    },

    # --- BÁNH MÌ (VIETNAMESE BAGUETTES) ---
    {
        "id": "bm_01",
        "name": "Bánh Mì Chảo Xíu Mại Pate Trứng",
        "category": "BanhMi",
        "price": 52000,
        "prep_time_minutes": 7,
        "flavor_tags": ["beo_ngay", "dam_da", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.3, 0.0, 0.0, 0.0, 0.85, 0.2, 0.8, 0.52],
        "image_url": "/static/images/bm_01.jpg"
    },
    {
        "id": "bm_02",
        "name": "Bánh Mì Thịt Nướng Pate Giòn",
        "category": "BanhMi",
        "price": 35000,
        "prep_time_minutes": 5,
        "flavor_tags": ["gion", "dam_da", "chua_ngot"],
        "meal_types": ["breakfast", "lunch", "afternoon_snack"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.2, 0.0, 0.0, 0.0, 0.75, 0.3, 0.6, 0.35],
        "image_url": "/static/images/bm_02.jpg"
    },

    # --- ĐỒ ĂN KÈM (COMPLEMENTARY / SIDES) ---
    {
        "id": "side_01",
        "name": "Nem Rán Hà Nội Giòn Rụm",
        "category": "DoAnKem",
        "price": 30000,
        "prep_time_minutes": 5,
        "flavor_tags": ["gion", "dam_da", "thom"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.2, 0.2, 0.6, 0.0, 0.7, 0.1, 0.5, 0.30],
        "image_url": "/static/images/side_01.jpg"
    },
    {
        "id": "side_02",
        "name": "Quẩy Giòn Phở Vàng Ươm",
        "category": "DoAnKem",
        "price": 10000,
        "prep_time_minutes": 1,
        "flavor_tags": ["gion", "xop"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.3, 0.0, 0.0, 0.0, 0.2, 0.0, 0.1, 0.10],
        "image_url": "/static/images/side_02.jpg"
    },
    {
        "id": "side_03",
        "name": "Trứng Chần Nước Béo",
        "category": "DoAnKem",
        "price": 12000,
        "prep_time_minutes": 3,
        "flavor_tags": ["beo_ngay", "ngot_thom", "nong"],
        "meal_types": ["breakfast", "lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.4, 0.0, 0.0, 0.0, 0.6, 0.0, 0.5, 0.12],
        "image_url": "/static/images/side_03.jpg"
    },
    {
        "id": "side_04",
        "name": "Canh Khổ Qua Nhồi Thịt",
        "category": "DoAnKem",
        "price": 25000,
        "prep_time_minutes": 5,
        "flavor_tags": ["thanh_nhiet", "dang_nhe", "nong"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.2, 0.4, 0.0, 0.0, 0.4, 0.0, 0.7, 0.25],
        "image_url": "/static/images/side_04.jpg"
    },
    {
        "id": "side_05",
        "name": "Chả Cốm Chiên Giòn Mùa Thu",
        "category": "DoAnKem",
        "price": 25000,
        "prep_time_minutes": 5,
        "flavor_tags": ["gion", "thom_com", "dam_da"],
        "meal_types": ["lunch", "dinner"],
        "is_vegetarian": False,
        "is_available": True,
        "feature_vector": [0.1, 0.1, 0.5, 0.0, 0.6, 0.1, 0.4, 0.25],
        "image_url": "/static/images/side_05.jpg"
    },

    # --- ĐỒ UỐNG (BEVERAGES) ---
    {
        "id": "drink_01",
        "name": "Trà Đào Cam Sả Tươi",
        "category": "DoUong",
        "price": 28000,
        "prep_time_minutes": 3,
        "flavor_tags": ["chua_ngot", "thom_dao", "mat_lanh"],
        "meal_types": ["lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.45, 0.0, 0.0, 0.28],
        "image_url": "/static/images/drink_01.jpg"
    },
    {
        "id": "drink_02",
        "name": "Cà Phê Muối Xứ Huế",
        "category": "DoUong",
        "price": 32000,
        "prep_time_minutes": 3,
        "flavor_tags": ["beo_ngay", "dam_da", "tinh_tao"],
        "meal_types": ["breakfast", "lunch", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.85, 0.0, 0.1, 0.32],
        "image_url": "/static/images/drink_02.jpg"
    },
    {
        "id": "drink_03",
        "name": "Cà Phê Sữa Đá Sài Gòn",
        "category": "DoUong",
        "price": 30000,
        "prep_time_minutes": 3,
        "flavor_tags": ["dam_da", "dang_ngot", "beo"],
        "meal_types": ["breakfast", "lunch", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.8, 0.0, 0.1, 0.30],
        "image_url": "/static/images/drink_03.jpg"
    },
    {
        "id": "drink_04",
        "name": "Trà Chanh Mật Ong Giã Tay",
        "category": "DoUong",
        "price": 22000,
        "prep_time_minutes": 3,
        "flavor_tags": ["chua_ngot", "mat_lanh", "thom_chanh"],
        "meal_types": ["lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.4, 0.0, 0.0, 0.22],
        "image_url": "/static/images/drink_04.jpg"
    },
    {
        "id": "drink_05",
        "name": "Trà Đá Thảo Mộc",
        "category": "DoUong",
        "price": 5000,
        "prep_time_minutes": 1,
        "flavor_tags": ["mat_lanh", "thanh", "giai_nhiet"],
        "meal_types": ["breakfast", "lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.1, 0.0, 0.0, 0.05],
        "image_url": "/static/images/drink_05.jpg"
    },
    {
        "id": "drink_06",
        "name": "Nước Mơ Chùa Hương Ướp Lạnh",
        "category": "DoUong",
        "price": 20000,
        "prep_time_minutes": 2,
        "flavor_tags": ["chua_ngot", "mat_lanh"],
        "meal_types": ["lunch", "dinner", "afternoon_snack"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.35, 0.0, 0.0, 0.20],
        "image_url": "/static/images/drink_06.jpg"
    },

    # --- TRÁNG MIỆNG (DESSERT) ---
    {
        "id": "dessert_01",
        "name": "Chè Bưởi An Giang Nước Cốt Dừa",
        "category": "TrangMieng",
        "price": 25000,
        "prep_time_minutes": 2,
        "flavor_tags": ["ngot_thanh", "beo_nuoc_cot_dua", "gion"],
        "meal_types": ["afternoon_snack", "dinner"],
        "is_vegetarian": True,
        "is_available": True,
        "feature_vector": [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.1, 0.25],
        "image_url": "/static/images/dessert_01.jpg"
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
        "image_url": "/static/images/dessert_02.jpg"
    }
]

SAMPLE_COMBOS = [
    {
        "id": "combo_01",
        "primary_dish_id": "pho_01",
        "complementary_dish_id": "side_02",
        "discount_rate": 0.10,
        "combo_name": "Combo Phở Bò Tái Lăn & Quẩy Giòn"
    },
    {
        "id": "combo_02",
        "primary_dish_id": "pho_01",
        "complementary_dish_id": "drink_05",
        "discount_rate": 0.10,
        "combo_name": "Combo Phở Bò & Trà Đá Thảo Mộc"
    },
    {
        "id": "combo_03",
        "primary_dish_id": "com_02",
        "complementary_dish_id": "drink_01",
        "discount_rate": 0.15,
        "combo_name": "Combo Cơm Gà Xối Mỡ & Trà Đào Cam Sả"
    },
    {
        "id": "combo_04",
        "primary_dish_id": "com_01",
        "complementary_dish_id": "side_04",
        "discount_rate": 0.15,
        "combo_name": "Combo Cơm Tấm & Canh Khổ Qua Nhồi Thịt"
    },
    {
        "id": "combo_05",
        "primary_dish_id": "bun_01",
        "complementary_dish_id": "drink_05",
        "discount_rate": 0.10,
        "combo_name": "Combo Bún Bò Huế & Trà Đá Giải Nhiệt"
    },
    {
        "id": "combo_06",
        "primary_dish_id": "bun_03",
        "complementary_dish_id": "side_01",
        "discount_rate": 0.12,
        "combo_name": "Combo Bún Đậu & Nem Rán Hà Nội"
    },
    {
        "id": "combo_07",
        "primary_dish_id": "bm_01",
        "complementary_dish_id": "drink_02",
        "discount_rate": 0.15,
        "combo_name": "Combo Bánh Mì Chảo & Cà Phê Muối Huế"
    }
]

SAMPLE_POIS = [
    {
        "id": "poi_01",
        "name": "Vườn Hoa Lý Thái Tổ",
        "category": "Công viên",
        "latitude": 21.0278,
        "longitude": 105.8548,
        "suggested_visit_minutes": 10,
        "walking_duration_minutes": 2,
        "thumbnail_url": "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0278,105.8548",
        "description": "Không gian xanh thoáng mát chỉ cách 100m, lý tưởng dạo bộ thư giãn trong lúc chờ món."
    },
    {
        "id": "poi_02",
        "name": "Hồ Hoàn Kiếm & Cầu Thê Húc",
        "category": "Danh thắng",
        "latitude": 21.0287,
        "longitude": 105.8524,
        "suggested_visit_minutes": 15,
        "walking_duration_minutes": 3,
        "thumbnail_url": "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0287,105.8524",
        "description": "Biểu tượng thủ đô, đi bộ 3 phút ngắm tháp Rùa và cầu Thê Húc rực rỡ."
    },
    {
        "id": "poi_03",
        "name": "Phố Sách & Cafe Đinh Lễ",
        "category": "Nhà sách",
        "latitude": 21.0267,
        "longitude": 105.8532,
        "suggested_visit_minutes": 15,
        "walking_duration_minutes": 3,
        "thumbnail_url": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0267,105.8532",
        "description": "Góc phố sách cổ kính, nhiều đầu sách hay và không gian yên tĩnh."
    },
    {
        "id": "poi_04",
        "name": "Quán Trà Ô Long Yên Tĩnh",
        "category": "Quán Trà",
        "latitude": 21.0295,
        "longitude": 105.8515,
        "suggested_visit_minutes": 15,
        "walking_duration_minutes": 4,
        "thumbnail_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=500",
        "google_maps_url": "https://maps.google.com/?q=21.0295,105.8515",
        "description": "Thưởng thức trà thảo mộc mát lạnh hoặc mang về trong thời gian bếp chuẩn bị."
    }
]

async def seed_database():
    print("Initializing database schema...")
    await init_db()
    async with AsyncSessionLocal() as session:
        # Check current dish count; if matches updated count, skip
        result = await session.execute(select(Dish))
        existing_dishes = result.scalars().all()
        if len(existing_dishes) == len(SAMPLE_DISHES):
            needs_update = any(not (d.image_url and d.image_url.startswith("/static/images/")) for d in existing_dishes)
            if not needs_update:
                print(f"Database already up to date with {len(existing_dishes)} dishes. Skipping seed.")
                return

        # Refresh dataset with new dishes, images and POIs
        print("Refreshing database with updated dishes, images, and POIs...")
        await session.execute(delete(Combo))
        await session.execute(delete(Dish))
        await session.execute(delete(NearbyPOI))
        await session.commit()

        print(f"Seeding {len(SAMPLE_DISHES)} distinctive dishes...")
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

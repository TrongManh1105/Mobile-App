from sqlalchemy import Column, String, Float, ForeignKey
from app.core.database import Base

class Combo(Base):
    __tablename__ = "combos"

    id = Column(String, primary_key=True, index=True)
    primary_dish_id = Column(String, ForeignKey("dishes.id"), nullable=False)
    complementary_dish_id = Column(String, ForeignKey("dishes.id"), nullable=False)
    discount_rate = Column(Float, default=0.10)  # 10% discount when ordered together
    combo_name = Column(String, nullable=True)


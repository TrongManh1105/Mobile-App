<!--
  Spec-Kit Engineering Tasks
  Project: Voice-Assisted Food Ordering Mobile App
  Standard: Clean Architecture & Spec-Kit Governance
-->

# DANH SÁCH NHIỆM VỤ KỸ THUẬT (ENGINEERING TASKS BREAKDOWN)
## Dự án: Mobile App - Voice-Assisted Food Ordering App

| Mã tài liệu | Phiên bản | Trạng thái | Ngày tạo | Tuân thủ |
| :--- | :--- | :--- | :--- | :--- |
| **TASKS-FOOD-001** | **1.0.0** | **ALL COMPLETED** | 2026-11-05 | [CONSTITUTION.md](file:///d:/Mobile%20App/CONSTITUTION.md), [SPECIFICATION.md](file:///d:/Mobile%20App/SPECIFICATION.md), [PLAN.md](file:///d:/Mobile%20App/PLAN.md) |

---

## BẢNG TỔNG KẾT TIẾN ĐỘ THI CÔNG (100% HOÀN THÀNH)

- [x] **`TASK-101`**: Khởi tạo cấu trúc Backend FastAPI & Cấu hình môi trường Pydantic Settings.
- [x] **`TASK-102`**: Xây dựng Async ORM Models bằng SQLAlchemy 2.0 (User, Dish, Combo, Order, POI).
- [x] **`TASK-103`**: Bộ dữ liệu mẫu Thực đơn 50+ món ăn kèm vector đặc trưng và 10+ POI.
- [x] **`TASK-104`**: Thuật toán Gợi ý Món ăn Content-Based Cosine Similarity & Gợi ý Combo bổ trợ.
- [x] **`TASK-105`**: Bộ Unit Tests bắt buộc cho Rec Engine (Pass 6/6 tests: Cold-start, Thời gian, Ăn chay, Giá, Hết hàng).
- [x] **`TASK-106`**: REST API Danh mục Món ăn (`/api/v1/dishes`) & Gợi ý (`/api/v1/recommendations`).
- [x] **`TASK-201`**: Tích hợp VAD ngắt câu sau 1s im lặng.
- [x] **`TASK-202`**: Xây dựng STT Client & Bộ phân tích ý định NLU (Search, AddToCart, Remove, Confirm, Reprompt).
- [x] **`TASK-203`**: Triển khai WebSocket Endpoint Streaming Giọng nói thời gian thực (`/ws/voice-stream`).
- [x] **`TASK-204`**: Kiểm thử Đơn vị Voice Pipeline & Xử lý Ngoại lệ (Pass 5/5 tests).
- [x] **`TASK-301`**: Service Tính thời gian chế biến dự kiến (ETD) theo tải bếp và số lượng món.
- [x] **`TASK-302`**: Thuật toán Haversine Lọc Địa điểm tham quan lân cận $\le 1.0\text{ km}$ theo quỹ thời gian chờ.
- [x] **`TASK-303`**: Bộ tạo thông điệp đơn hàng WhatsApp chuẩn hóa và URL Deep Link `https://wa.me/` kèm fallback SMS.
- [x] **`TASK-304`**: WebSocket Theo dõi trạng thái đơn hàng thời gian thực (`/ws/orders/{id}/tracking`).
- [x] **`TASK-401`**: Khởi tạo Mobile Client Clean Architecture (`mobile/src/{core,domain,data,presentation}`).
- [x] **`TASK-402`**: Xây dựng Domain Layer (Entities & UseCases độc lập không phụ thuộc UI).
- [x] **`TASK-403`**: Data Layer: DTO Models, API Client giao tiếp backend FastAPI.
- [x] **`TASK-404`**: Native Audio Recording Service & WebSocket Streaming Client.
- [x] **`TASK-405`**: Quản lý trạng thái State Machine 5 trạng thái cho Voice (`Idle`, `Listening`, `Processing`, `Recognized`, `Error`).
- [x] **`TASK-501`**: Visualizer Sóng âm thanh thời gian thực (16 frequency bars modulated).
- [x] **`TASK-502`**: Quản lý Giỏ hàng Reducer (Thêm, Xóa, Đổi số lượng, Tính tổng tiền).
- [x] **`TASK-503`**: Màn hình Đặt đơn & Deep Link WhatsApp / SMS Launcher.
- [x] **`TASK-504`**: Màn hình Theo dõi Đơn hàng (Đếm ngược ETD & Carousel POI lân cận).
- [x] **`TASK-505`**: Bộ kiểm thử tự động Mobile Client (Pass 5/5 tests).
- [x] **`TASK-506`**: Báo cáo nghiệm thu E2E Spec-Kit toàn diện (Pass 23/23 tests, 0 warnings).

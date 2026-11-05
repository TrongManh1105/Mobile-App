# 🎙️ Voice-Assisted Food Ordering & Recommendation System
### *Hệ Thống Đặt Món Ăn Bằng Giọng Nói & Đề Xuất Thông Minh Dựa Trên Học Máy*

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/trongmanh1105/voice-food-app)
[![Tests](https://img.shields.io/badge/Tests-23%2F23%20Passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## 📖 1. Giới Thiệu & Nguồn Gốc Nghiên Cứu (Research Background)

Dự án được xây dựng và phát triển dựa trên cơ sở khoa học từ công trình nghiên cứu quốc tế:
> **VOCALICIOUS - Voice-Assisted Food Ordering Web Application**  
> *Tác giả:* Jishma Murali, G. S. Ananthu, Sreejith S., Nandana S., S. Shajahan  
> *Tạp chí:* **International Journal for Research in Applied Science & Engineering Technology (IJRASET)**  
> *Chỉ số & Thời gian xuất bản:* ISSN: 2321-9653, Volume 11, Issue V, May 2023  
> *DOI:* [10.22214/ijraset.2023.52445](https://doi.org/10.22214/ijraset.2023.52445) | [Bài báo gốc tại IJRASET](https://www.ijraset.com/research-paper/voice-assisted-food-ordering-web-application)

### 🔬 Bảng So Sánh Cải Tiến Giữa Bài Báo & Sản Phẩm Thực Tế

| Tiêu Chí | Nghiên Cứu Gốc (IJRASET 2023) | Sản Phẩm Nâng Cấp Trong Dự Án Này |
| :--- | :--- | :--- |
| **Công Nghệ Giọng Nói** | Web Speech API (Tiếng Anh cơ bản) | Web Speech API + Bộ bóc tách thực thể NLU Tiếng Việt (Ý định, Tên món, Số lượng, Ghi chú) |
| **Âm Thanh Phản Hồi** | Thông báo văn bản tĩnh | Web Audio API tổng hợp âm báo chimes đa tần số (Start chime 520Hz/650Hz, Success 880Hz, Error 300Hz) |
| **Hệ Thống Đề Xuất** | Lọc danh mục cố định | **Content-Based Filtering (Scikit-learn TF-IDF & Cosine Similarity)** theo sở thích, vị giác, độ cay |
| **Ước Lượng Thời Gian (ETD)** | Thời gian giả định tĩnh | Thuật toán ước tính tải bếp thực tế: $T_{est} = T_{base} + \sum t_i \times \text{queue\_factor}$ |
| **Trải Nghiệm Chờ Đợi** | Chỉ hiển thị vòng quay chờ | **Định vị điểm tham quan POI lân cận (< 1km)** qua công thức Haversine để khách dạo chơi |
| **Xác Nhận & Đặt Hàng** | Gửi email đơn thuần | **Deep Link WhatsApp & SMS** tự động định dạng hóa đơn Markdown gửi thẳng tới chủ quán |
| **Kiến Trúc Ứng Dụng** | Web PHP / JS truyền thống | **Clean Architecture (Hexagonal)**, FastAPI Async, TypeScript Domain Layer, Docker Containerized |

---

## ✨ 2. Các Tính Năng Trọng Tâm

* 🎙️ **Voice AI Assistant Tiếng Việt:** 
  * Nhận diện khẩu lệnh tức thì: *"Cho tôi 2 phở bò tái và 1 trà đào ít đá"* -> Tự động trích xuất món ăn, số lượng và thuộc tính kèm theo.
  * Hỗ trợ các lệnh điều khiển luồng: *"Thêm vào giỏ"*, *"Xóa giỏ hàng"*, *"Thanh toán đơn"*, *"Xem gợi ý"*.
  * Hiệu ứng sóng âm động (Dynamic Waveform 16 bars) phản hồi tương tác thời gian thực.
* 🧠 **Hệ Thống Gợi Ý Học Máy (ML Recommendation Engine):**
  * Sử dụng giải thuật **Cosine Similarity** tính toán khoảng cách vector đặc trưng giữa các món ăn (hương vị, độ cay, danh mục, giá tiền) để gợi ý combo/món kèm phù hợp nhất.
* ⏱️ **Ước Tính Thời Gian Chế Biến (Kitchen Load ETD):**
  * Tự động tính toán tổng thời gian nấu dựa trên độ phức tạp của từng món và số lượng đơn hàng đang chờ trong bếp.
* 📍 **Gợi Ý Điểm Đến Xung Quanh (Nearby POIs Discovery):**
  * Ứng dụng công thức **Haversine** tính toán khoảng cách địa lý chính xác, gợi ý quán cà phê, công viên, nhà sách trong bán kính dưới 1km giúp khách hàng thư giãn khi chờ món.
* 💬 **Chốt Đơn Đa Kênh Tức Thì (WhatsApp & SMS Deep Linking):**
  * Tạo đường dẫn trực tiếp mở ứng dụng WhatsApp với nội dung đơn hàng được định dạng chi tiết, giúp việc chốt đơn không phụ thuộc vào hạ tầng SMS trả phí.

---

## 🏛️ 3. Kiến Trúc Hệ Thống (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                    │
│   Mobile App Mockup (HTML5 / Tailwind CSS / Vanilla JS)     │
│   Web Speech API (STT) + Web Audio API (Chimes Feedback)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / WebSocket REST API
┌──────────────────────────────▼──────────────────────────────┐
│                  FASTAPI APPLICATION LAYER                  │
│  ┌───────────────────────┬───────────────────────────────┐  │
│  │ Voice NLU Pipeline    │ Recommendation Engine (ML)    │  │
│  │ - Intent Classifier   │ - TF-IDF Vectorizer           │  │
│  │ - Slot & Entity Parser│ - Cosine Similarity (Sklearn) │  │
│  ├───────────────────────┼───────────────────────────────┤  │
│  │ ETD Calculator        │ Haversine POI Geo-Locator     │  │
│  │ WhatsApp Link Builder │ Async Order Tracking State    │  │
│  └───────────────────────┴───────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Async SQLAlchemy 2.0 ORM
┌──────────────────────────────▼──────────────────────────────┐
│                  INFRASTRUCTURE & PERSISTENCE               │
│      SQLite + aiosqlite (Async Engine) / PostgreSQL         │
│          Dishes | Categories | Orders | Combos | POIs       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 4. Cấu Trúc Thư Mục (Project Structure)

```text
Mobile-App/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/       # REST API Endpoints (dishes, voice, orders, poi, ...)
│   │   ├── core/                   # Cấu hình hệ thống (config, logging)
│   │   ├── domain/services/        # Nghiệp vụ lõi (NLU, ML RecSys, ETD, Haversine, WhatsApp)
│   │   ├── infrastructure/db/      # SQLAlchemy Models & Seed Data
│   │   ├── schemas/                # Pydantic v2 DTOs & Request/Response Models
│   │   ├── static/                 # Giao diện Mobile App Mockup (index.html)
│   │   └── main.py                 # FastAPI Application Gateway
│   ├── requirements.txt            # Thư viện Python
│   └── tests/                      # Bộ kiểm thử Pytest tự động (18 unit/integration tests)
├── mobile/
│   ├── src/
│   │   ├── domain/entities/        # TypeScript Domain Entities (Dish, Order, Cart)
│   │   ├── infrastructure/         # Web Audio Synthesizer, Deep Linking
│   │   └── presentation/store/     # Redux Toolkit Slices (Cart, Order Tracking)
│   ├── tests/                      # Kiểm thử Redux & Business Logic (5 tests)
│   └── package.json
├── .specify/                       # Đặc tả kỹ thuật theo chuẩn Spec-Kit (Memory & Specs)
├── Dockerfile                      # Khởi tạo Docker Container
├── docker-compose.yml              # Quản lý triển khai đa vùng / môi trường
├── render.yaml                     # Cấu hình triển khai tự động 1-click Render.com
├── CONSTITUTION.md                 # Quy chuẩn chất lượng kiến trúc
├── SPECIFICATION.md                # Bản đặc tả kỹ thuật chi tiết
├── PLAN.md                         # Kế hoạch phát triển
├── TASKS.md                        # Danh mục công việc & trạng thái
└── CONVERGENCE.md                  # Báo cáo nghiệm thu & độ khớp mục tiêu
```

---

## 🚀 5. Hướng Dẫn Chạy Cục Bộ (Local Quickstart)

### Điều Kiện Tiên Quyết
* Python >= 3.12
* Node.js >= 20.0 (Tùy chọn nếu chạy mobile tests)
* Docker & Docker Desktop (Tùy chọn nếu chạy container)

### Bước 1: Khởi Tạo Môi Trường Python
```bash
# Clone dự án về máy
git clone https://github.com/TrongManh1105/Mobile-App.git
cd Mobile-App

# Tạo và kích hoạt môi trường ảo
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# Cài đặt toàn bộ thư viện
pip install -r backend/requirements.txt
```

### Bước 2: Nạp Dữ Liệu Khởi Tạo & Chạy Máy Chủ
```bash
# Nạp 22 món ăn, 6 combo đề xuất và các POI lân cận
python -m backend.app.infrastructure.db.seed

# Khởi chạy server FastAPI (mặc định cổng 8000)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Bước 3: Trải Nghiệm Ứng Dụng
* **Giao diện App Mobile:** Mở trình duyệt truy cập `http://localhost:8000/app` (Tối ưu giao diện chuẩn khung iPhone 16 Pro).
* **Tài liệu API Swagger:** Mở `http://localhost:8000/docs`.

---

## 🐳 6. Đóng Gói & Chạy Bằng Docker / Docker Hub

Hình ảnh Docker chính thức của dự án đã được tối ưu hóa nhiều tầng (Multi-stage/Slim) và cấu hình sẵn:

### Chạy Nhanh Từ Docker Hub
```bash
# Kéo image từ Docker Hub
docker pull trongmanh1105/voice-food-app:latest

# Khởi chạy container
docker run -d -p 8000:8000 --name voice-food-app trongmanh1105/voice-food-app:latest

# Truy cập ngay tại http://localhost:8000/app
```

### Tự Build Image & Chạy Bằng Docker Compose
```bash
# Build image cục bộ
docker build -t trongmanh1105/voice-food-app:latest .

# Khởi chạy bằng Docker Compose
docker-compose up -d

# Xem log hoạt động
docker-compose logs -f
```

---

## ☁️ 7. Triển Khai 24/7 Miễn Phí (Cloud Deployment Guide)

Để gửi sản phẩm cho giảng viên hoặc người dùng trải nghiệm thực tế mọi lúc mọi nơi kèm hỗ trợ micro (HTTPS):

### Cách 1: Triển Khai Lên Render.com (Khuyên dùng - Hoàn Toàn Miễn Phí)
1. Đăng nhập vào [Render.com](https://render.com) (bằng tài khoản GitHub).
2. Chọn **New +** -> **Web Service** -> Chọn Repository **`TrongManh1105/Mobile-App`**.
3. Cấu hình dịch vụ:
   * **Name:** `voice-food-app`
   * **Language / Runtime:** `Python`
   * **Build Command:** `pip install -r backend/requirements.txt`
   * **Start Command:** `python -m app.infrastructure.db.seed && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   * **Environment Variables:**
     * `PYTHONPATH` = `backend`
     * `DATABASE_URL` = `sqlite+aiosqlite:///./food_app.db`
4. Bấm **Create Web Service**. Sau ~2 phút, Render sẽ cung cấp đường dẫn HTTPS dạng:  
   `https://voice-food-app.onrender.com/app`  
   *(Có sẵn chứng chỉ SSL giúp micro Web Speech API hoạt động hoàn hảo trên điện thoại di động).*

### Cách 2: Triển Khai Nhanh Qua Cloudflare Tunnel (Chạy từ máy tính 24/7 có HTTPS)
Nếu muốn chạy trực tiếp từ server cá nhân hoặc laptop:
```bash
# Cài đặt cloudflared và khởi tạo đường hầm HTTPS
cloudflared tunnel --url http://localhost:8000
```
Hệ thống sẽ cấp một đường link công khai `https://xxx.trycloudflare.com/app` có đầy đủ chứng chỉ bảo mật.

---

## 🧪 8. Kiểm Thử Hệ Thống (Automated Testing)

Dự án áp dụng quy trình kiểm thử nghiêm ngặt bao phủ toàn bộ luồng nghiệp vụ:

### Kiểm Thử Backend (Pytest - 18 Tests)
```bash
pytest backend/tests -v
```
*Kết quả:*
* `test_voice_intent_and_slot_extraction`: Đạt chuẩn bóc tách tiếng Việt.
* `test_recommendation_cosine_similarity`: Đạt chuẩn độ tương đồng Scikit-learn.
* `test_etd_calculator_under_varying_loads`: Đạt chuẩn dự báo thời gian tải bếp.
* `test_haversine_poi_filter_under_1km`: Đạt chuẩn lọc địa lý lân cận.
* `test_whatsapp_deep_link_formatting`: Đạt chuẩn mã hóa ký tự URL WhatsApp.

### Kiểm Thử Mobile Clean Architecture (Node.js - 5 Tests)
```bash
node --experimental-strip-types mobile/tests/voiceAndCart.test.js
```
*Kết quả:* **23/23 Tests toàn diện PASSED (100%)**.

---

## 👨‍💻 9. Tác Giả & Bản Quyền

* **Tác Giả:** Trọng Mạnh ([@TrongManh1105](https://github.com/TrongManh1105))
* **Mã Nguồn:** [https://github.com/TrongManh1105/Mobile-App](https://github.com/TrongManh1105/Mobile-App)
* **Docker Image:** [https://hub.docker.com/r/trongmanh1105/voice-food-app](https://hub.docker.com/r/trongmanh1105/voice-food-app)
* **Giấy Phép:** Phân phối dưới giấy phép [MIT License](LICENSE).

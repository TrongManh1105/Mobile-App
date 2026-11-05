<!--
  Project Constitution: Voice-Driven Food Ordering Mobile Application
  Established under Spec-Kit / Clean Architecture Governance
-->

# HIẾN CHƯƠNG DỰ ÁN (PROJECT CONSTITUTION)
## Ứng Dụng Di Động Đặt Đồ Ăn Bằng Giọng Nói (Voice-Driven Food Delivery App)

| Phiên bản | Trạng thái | Ngày hiệu lực | Phạm vi |
| :--- | :--- | :--- | :--- |
| **1.0.0** | **APPROVED & ACTIVE** | 2026-11-05 | Toàn bộ hệ thống Mobile Client & Backend AI Engine |

---

## TỔNG QUAN & NGUYÊN TẮC BẤT KHẢ XÂM PHẠM (NON-NEGOTIABLES)

Tài liệu này đóng vai trò là **Hiến chương Kỹ thuật (Constitution)** tối cao của dự án. Mọi thành viên đội ngũ phát triển, quy trình sinh mã AI, mã nguồn, pull request (PR) và quyết định kiến trúc bắt buộc phải tuân thủ nghiêm ngặt 5 nguyên tắc cốt lõi dưới đây. Mọi vi phạm nguyên tắc sẽ bị chặn tại tầng CI/CD pipeline và Code Review.

```
+-------------------------------------------------------------------------------+
|                           KIẾN TRÚC TỔNG THỂ HỆ THỐNG                         |
+-------------------------------------------------------------------------------+
|                                                                               |
|   [ Mobile Client (Flutter / React Native) ]                                  |
|   +-----------------------------------------------------------------------+   |
|   | Presentation Layer (UI Widgets / Screens, Blocs / Redux Slices)       |   |
|   +-----------------------------------------------------------------------+   |
|                               | (Uses / Dispatches)                           |
|                               v                                               |
|   +-----------------------------------------------------------------------+   |
|   | Domain Layer (Entities, UseCases, Repository Interfaces - Pure Logic) |   |
|   +-----------------------------------------------------------------------+   |
|                               ^ (Implements)                                  |
|                               |                                               |
|   +-----------------------------------------------------------------------+   |
|   | Data Layer (DTOs, Mappers, Repositories, REST / WebSocket Clients)    |   |
|   +-----------------------------------------------------------------------+   |
|                               ^                                               |
|                               | Real-time WebSocket / gRPC / HTTPS            |
|                               v                                               |
|   [ Backend AI Engine (Python FastAPI) ]                                      |
|   +-----------------------------------------------------------------------+   |
|   | API & Gateway (Routers, WebSocket Stream Handlers, Auth Middleware)   |   |
|   +-----------------------------------------------------------------------+   |
|   | Domain Services (Voice Pipeline, NLU / Slot-filling, Recommendation)  |   |
|   +-----------------------------------------------------------------------+   |
|   | AI & Data Adapters (Whisper/STT, FastSpeech/TTS, Vector DB, RDBMS)    |   |
|   +-----------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------+
```

---

## ĐIỀU I: KIẾN TRÚC HỆ THỐNG - TUÂN THỦ CLEAN ARCHITECTURE

### 1. Phân tầng Mobile Client (Clean Architecture)
Mã nguồn ứng dụng di động bắt buộc phân chia thành 3 tầng độc lập, tuân thủ nguyên tắc đảo ngược phụ thuộc (Dependency Inversion Principle - DIP):

1. **Tầng Presentation (Giao diện & Tương tác người dùng):**
   - **Thành phần:** Screens, Components/Widgets, State Holders (Bloc/Cubit hoặc Redux Slices), Audio Visualizers (Waveform, mic status indicator).
   - **Quy tắc:**
     - Tuyệt đối **không** chứa logic nghiệp vụ (business logic) hoặc gọi trực tiếp API/Database.
     - Tầng Presentation chỉ nhận dữ liệu từ Domain UseCases dưới dạng UI State và gửi các Events/Actions phản hồi từ người dùng.
     - Giao diện phản hồi giọng nói phải hỗ trợ 5 trạng thái trực quan: `Idle`, `Listening` (đang ghi âm), `Processing` (AI đang phân tích), `Recognized/Confirmed` (đã nhận diện món), và `Error/Fallback` (lỗi nhận diện).

2. **Tầng Domain (Nghiệp vụ cốt lõi - Trọng tâm dự án):**
   - **Thành phần:** Business Entities, UseCases / Interactors, Value Objects, Repository Interfaces (Contracts).
   - **Quy tắc:**
     - Là tầng độc lập hoàn toàn, **không phụ thuộc** vào bất kỳ framework bên ngoài nào (không import Flutter UI, React Native native bridge, HTTP client, hay cơ sở dữ liệu).
     - Mọi luồng xử lý (ví dụ: `ProcessVoiceOrderUseCase`, `GetRecommendedDishesUseCase`, `ConfirmCartUseCase`) phải được đóng gói thành các UseCase đơn chức năng (Single Responsibility Principle).

3. **Tầng Data (Dữ liệu & Tích hợp hạ tầng):**
   - **Thành phần:** Models (DTOs - Data Transfer Objects), Data Sources (RemoteDataSource via WebSocket/REST, LocalDataSource via SQLite/Hive/AsyncStorage), Repository Implementations.
   - **Quy tắc:**
     - Hiện thực hóa (implement) các Repository Interfaces được định nghĩa tại Domain Layer.
     - Chịu trách nhiệm chuyển đổi (mapping) qua lại giữa Network/DB Models và Domain Entities.
     - Quản lý việc lưu trữ tạm thời (caching), audio buffering trước khi đẩy lên server.

### 2. Phân tầng Backend AI Engine (Python FastAPI)
1. **API / Routing Layer:** Nhận request HTTP REST và duy trì kết nối WebSocket thời gian thực cho audio streaming. Kiểm tra định dạng dữ liệu qua Pydantic Schemas.
2. **Domain / Service Layer:** Chứa logic nghiệp vụ cốt lõi: Voice Pipeline Coordinator, NLU & Intent Extraction, Slot Filling (món ăn, số lượng, ghi chú, địa chỉ), và Food Recommendation Engine.
3. **Infrastructure / AI Adapter Layer:** Tích hợp các mô hình STT (Speech-to-Text), LLM/NLP Engine, Text-to-Speech (TTS), Vector Database (gợi ý món ăn), RDBMS (PostgreSQL/MongoDB).

---

## ĐIỀU II: TIÊU CHUẨN CÔNG NGHỆ & NGÔN NGỮ

### 1. Cross-Platform Mobile Client
*Đội ngũ lựa chọn một trong hai phương án công nghệ sau và áp dụng tiêu chuẩn tương ứng:*

| Tiêu chuẩn | Lựa chọn A: Flutter | Lựa chọn B: React Native |
| :--- | :--- | :--- |
| **Ngôn ngữ** | Dart 3.x (Bật Sound Null Safety tuyệt đối) | TypeScript 5.x (Strict Mode: `"strict": true`) |
| **Style Guide** | Chuẩn Linting: `flutter_lints` / `very_good_analysis` | ESLint + Prettier + TypeScript-ESLint |
| **Audio Capture** | `record` hoặc `sound_stream` (truy xuất raw PCM 16kHz) | `react-native-live-audio-stream` / `react-native-audio-recorder-player` |
| **Dependency Injection** | `get_it` + `injectable` | `tsyringe` hoặc InversifyJS |
| **Network Client** | `dio` (kèm Interceptors ghi log, retry, refresh token) | `axios` kèm Axios Interceptors |

### 2. Backend AI Engine (Python FastAPI)
- **Runtime:** Python 3.11+ (Tận dụng cải tiến tốc độ và Async TaskGroups).
- **Web Framework:** FastAPI (Asynchronous ASGI với Uvicorn/Gunicorn).
- **Data Validation & Typing:** `pydantic` v2, Type Hints bắt buộc 100% trên hàm và method.
- **Async Framework:** `asyncio`, `aiohttp`, `websockets`.
- **Packaging & Dependency Management:** `poetry` hoặc `uv` (có khóa phiên bản chặt chẽ qua file lock).

---

## ĐIỀU III: QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)

### 1. Đối với dự án sử dụng Flutter (BLoC / Provider)
- **Mô hình bắt buộc:** BLoC (Business Logic Component) thông qua thư viện `flutter_bloc`.
- **Cấu trúc luồng dữ liệu:**
  $$\text{User Event / Voice Input} \longrightarrow \text{BLoC} \longrightarrow \text{Domain UseCase} \longrightarrow \text{Immutable State} \longrightarrow \text{UI Re-render}$$
- **Trạng thái Voice Interaction State Machine:**
  - `VoiceState`: Base abstract class (sử dụng `freezed` hoặc `equatable`).
  - Các state dẫn xuất bắt buộc:
    - `VoiceInitialState`: Trạng thái ban đầu, mic sẵn sàng.
    - `VoiceListeningState(amplitude, duration)`: Đang thu âm, phát tín hiệu biên độ sóng âm theo thời gian thực.
    - `VoiceProcessingState(transcriptPreview)`: Đang phân tích âm thanh, hiển thị transcript sơ bộ.
    - `VoiceOrderRecognizedState(orderProposal, confidenceScore)`: Nhận dạng thành công món ăn kèm độ tin cậy.
    - `VoiceErrorState(errorCode, userFriendlyMessage, canRetry)`: Gặp lỗi, cung cấp hành động khắc phục.
- **Nguyên tắc State:** Toàn bộ State là **Immutable**. Cập nhật thông qua phương thức `copyWith`.

### 2. Đối với dự án sử dụng React Native (Redux Toolkit)
- **Mô hình bắt buộc:** Redux Toolkit (RTK) kết hợp RTK Query cho fetching API.
- **Slice Architecture:** Phân tách rõ ràng các slice độc lập:
  - `voiceSlice`: Quản lý trạng thái micro, streaming audio chunk, live transcript, session ID.
  - `recommendationSlice`: Quản lý danh sách món gợi ý, ngữ cảnh thời gian, điểm số relevance.
  - `cartSlice`: Quản lý giỏ hàng, tính toán đơn giá, thuế, voucher.
- **Middleware:** Sử dụng Redux Middleware hoặc Custom Event Listeners để điều phối WebSocket Voice Stream, không đưa side-effects trực tiếp vào reducers.

---

## ĐIỀU IV: MODULE GIỌNG NÓI & XỬ LÝ THỜI GIAN THỰC (VOICE ENGINE)

### 1. Xử lý Tín hiệu Thoại (Audio Signal Processing)
- **Định dạng Audio chuẩn:**
  - Sample Rate: **16,000 Hz (16 kHz)**.
  - Bit Depth: **16-bit Linear PCM**, Mono Channel.
  - Frame Duration: Gửi chunk âm thanh từ 100ms - 250ms qua WebSocket để giảm thiểu độ trễ (latency budget mục tiêu: $\le 800\text{ ms}$ cho phản hồi AI).
- **VAD (Voice Activity Detection):**
  - Tích hợp bộ phát hiện khoảng lặng (VAD) phía client để tự động nhận biết khi người dùng dứt lời (silence duration > 1.2s), tự động gửi gói cờ kết thúc thoại (`END_OF_SPEECH`) lên server thay vì bắt người dùng bấm nút dừng.
- **Khử nhiễu & Chuẩn hóa:** Bật sẵn các cờ hệ thống: `echoCancellation: true`, `noiseSuppression: true`, `autoGainControl: true`.

### 2. Khả năng Chịu lỗi & Xử lý Ngoại lệ (Resilience & Exception Handling)

```
+-----------------------------------------------------------------------------------------+
|                    MA TRẬN XỬ LÝ SỰ CỐ MODULE GIỌNG NÓI                                 |
+--------------------------+------------------------------+-------------------------------+
| Kịch bản sự cố           | Hành vi Hệ thống             | Phản hồi Người dùng (UX/Voice)|
+--------------------------+------------------------------+-------------------------------+
| Mất kết nối mạng         | - Lưu audio buffer vào bộ nhớ| - Thông báo popup nhẹ & audio:|
| đột ngột khi nói         |   đệm cục bộ (tối đa 15s).   |   "Mất kết nối mạng. Bạn có   |
|                          | - Thử kết nối lại 3 lần theo |   muốn thử lại khi có mạng?"  |
|                          |   Exponential Backoff.       | - Chuyển sang nút tìm kiếm tay|
+--------------------------+------------------------------+-------------------------------+
| Không nhận dạng được     | - Kiểm tra Confidence Score. | - Gợi ý bằng giọng nói: "Tôi  |
| âm thanh (Tạp âm lớn     | - Nếu Score < 0.65: Hủy phân |   chưa nghe rõ, bạn có thể nói|
| hoặc nói quá nhỏ)        |   tích lệnh đặt món.         |   lại tên món ăn được không?" |
|                          | - Log telemetry ẩn danh.     | - Hiển thị các chip món ăn hot|
+--------------------------+------------------------------+-------------------------------+
| Nhận dạng mơ hồ          | - Hệ thống trích xuất Top-N  | - Hỏi xác nhận: "Ý bạn là Phở |
| (Ví dụ: "Cho 1 phở")     |   khả năng cao nhất.         |   Bò Tái hay Phở Gà?"         |
|                          | - Chờ phản hồi voice xác nhận| - Hiển thị 2 lựa chọn trên màn|
+--------------------------+------------------------------+-------------------------------+
| Server AI quá tải /      | - Circuit Breaker kích hoạt  | - Fallback sang tìm kiếm text |
| Timeout (> 3000ms)       |   sau 3 lần timeout liên tiếp|   hoặc hiển thị Menu thông    |
|                          |                              |   thường mà không làm đơ App. |
+--------------------------+------------------------------+-------------------------------+
```

---

## ĐIỀU V: CHẤT LƯỢNG MÃ NGUỒN, KIỂM THỬ & XỬ LÝ BẤT ĐỒNG BỘ

### 1. Quy chuẩn Kiểm thử Đơn vị (Unit Testing Mandates)
- **Chỉ tiêu Coverage:** Tối thiểu **80% Code Coverage** cho Domain Layer (UseCases), Repository Implementation, State Handlers (Blocs/Reducers) và AI Recommendation Engine.
- **Bắt buộc Unit Test cho Thuật toán Gợi ý Món ăn (Food Recommendation Engine):**
  Thuật toán gợi ý là trái tim nâng cao doanh số và trải nghiệm, bắt buộc phải có bộ Unit Test bao quát 100% các ca kiểm thử sau:
  1. **Cold-start User Test:** Kiểm tra gợi ý đối với người dùng mới (chưa có lịch sử) -> Phải trả về danh sách món thịnh hành (Trending/Popular) theo vị trí địa lý.
  2. **Context-aware Time Test:**
     - 06:00 - 09:00: Ưu tiên món ăn sáng (bún, phở, cà phê, bánh mì).
     - 11:00 - 13:00: Ưu tiên cơm trưa, combo văn phòng.
     - 14:00 - 16:30: Ưu tiên trà sữa, đồ ăn vặt, tráng miệng.
     - 18:00 - 21:00: Ưu tiên bữa tối gia đình, lẩu, món nhậu.
  3. **Dietary & Preference Filter Test:** Người dùng khai báo ăn chay (`vegetarian: true`) hoặc dị ứng hải sản -> Thuật toán **tuyệt đối không** được đưa món thịt/hải sản vào danh sách gợi ý.
  4. **Budget Constraint Test:** Lệnh giọng nói có điều kiện giá ("Tìm món dưới 50k") -> Mọi món gợi ý phải có $\text{Price} \le 50,000\text{ VND}$.
  5. **Out-of-Stock Exclusion Test:** Món ăn đã hết hàng tại quán (`is_available: false`) phải bị loại bỏ lập tức khỏi danh sách đề xuất.

### 2. Quy chuẩn Xử lý Bất đồng bộ (Async/Await & Concurrency)
- **Quy tắc 1 - Không bao giờ bỏ quên lỗi (Zero Unhandled Rejections):**
  Mọi tác vụ bất đồng bộ (`Future` trong Dart hoặc `Promise` trong TypeScript, `async def` trong Python) bắt buộc phải nằm trong khối `try/catch/finally` hoặc sử dụng Result Monad Pattern (`Either<Failure, Success>`).
- **Quy tắc 2 - Giải phóng tài nguyên triệt để (Resource Cleanup):**
  - Mọi Stream Subscription, WebSocket Channel, Audio Recorder session, Controller phải được đóng/hủy trong lifecycle teardown (`dispose()` trong Flutter, cleanup callback trong React `useEffect`, hoặc context manager `async with` trong Python).
  - Không được để rò rỉ bộ nhớ (Memory Leak) do audio buffer còn đọng lại khi người dùng rời màn hình.
- **Quy tắc 3 - Cơ chế Hủy tác vụ (Cancellation Tokens / AbortController):**
  Khi người dùng hủy lệnh nói hoặc nhấn nút hủy, ứng dụng phải lập tức kích hoạt `CancellationToken` (Dart) / `AbortController` (JS) / `asyncio.Task.cancel()` (Python) để chấm dứt ngay lập tức kết nối streaming và các tác vụ AI đang tính toán, tránh lãng phí GPU server và pin thiết bị.
- **Quy tắc 4 - Debounce & Anti-Spam:**
  Nút bấm ghi âm và sự kiện giọng nói phải áp dụng debounce tối thiểu 300ms để ngăn chặn việc người dùng nhấn liên tục gây xung đột thiết bị thu âm phần cứng.

---

## BẢNG KIỂM TRA CHẤT LƯỢNG PULL REQUEST (PR REVIEW CHECKLIST)

Mọi Pull Request trước khi merge vào nhánh chính (`main` / `develop`) bắt buộc phải được đánh dấu tích đầy đủ các tiêu chí:

- [ ] **Kiến trúc:** Mã nguồn tuân thủ đúng vị trí phân tầng Clean Architecture (Presentation, Domain, Data). Không import chéo vi phạm DIP.
- [ ] **State:** Không mutate trực tiếp state; State machine cho Voice interaction phản ánh đúng trạng thái thực tế.
- [ ] **Xử lý ngoại lệ:** Có kịch bản xử lý khi mất mạng và khi AI không hiểu giọng nói. Không để xảy ra crash ứng dụng.
- [ ] **Unit Tests:** Đã viết Unit Test cho toàn bộ UseCases liên quan và logic tính toán gợi ý món ăn. Kiểm tra test pass 100%.
- [ ] **Bất đồng bộ:** Sử dụng `async/await` an toàn, có `try/catch`, có hủy listeners / stream / controller khi unmount.
- [ ] **Hiệu năng:** Không gây drop frame (< 60fps) trên thiết bị di động khi render sóng âm thanh thời gian thực.


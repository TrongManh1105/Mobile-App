# Product

<!-- impeccable:product-schema 1 -->

## Platform

adaptive

## Users

Khách hàng cá nhân hoặc nhóm nhỏ ăn tại quán hoặc mua mang về (Dine-in / Takeaway) tại các quán ăn Việt Nam (phở, bún, cơm, bánh mì, đồ ăn kèm, đồ uống, tráng miệng). Họ đang trong trạng thái bận tay, muốn gọi món nhanh chóng mà không phải tìm đọc danh mục phức tạp hay gõ chữ trên màn hình nhỏ. Trong thời gian chờ bếp chuẩn bị, họ muốn biết chính xác khi nào món xong và khám phá các địa điểm thú vị quanh quán để dạo chơi thư giãn thay vì ngồi chờ sốt ruột.

## Product Purpose

Vocalicious cung cấp giải pháp gọi món bằng giọng nói tiếng Việt tự nhiên và hỗ trợ trải nghiệm chờ món thông minh. Sản phẩm loại bỏ ma sát đặt món truyền thống bằng cách bóc tách chính xác ý định, số lượng, ghi chú tùy biến (như "ít cay", "không hành", "nhiều đá", "không đường"), tự động gợi ý combo tương thích khẩu vị bằng máy học, đồng thời hiển thị thời gian chế biến ước tính (ETD) và các điểm tham quan (POIs) trong bán kính đi bộ (< 1km). Thành công được đo bằng tốc độ hoàn tất đơn hàng (< 30 giây), độ chính xác nhận diện giọng nói, và mức độ hài lòng trong thời gian chờ nhận món.

## Positioning

Trải nghiệm Voice-First ẩm thực Việt Nam khép kín từ khâu tiếp nhận khẩu lệnh đến đồng bộ hóa đơn thực tế. Khác với các ứng dụng đặt món chỉ có thanh tìm kiếm giọng nói đơn giản hoặc ứng dụng giao hàng cồng kềnh, Vocalicious kết hợp:
1. NLU giọng nói tiếng Việt chuyên sâu hiểu ngữ cảnh ẩm thực (lượng từ, từ lóng, ghi chú vị giác).
2. Hệ thống gợi ý combo tương đồng Cosine Similarity dựa trên vector đặc trưng món ăn.
3. Dự báo tải bếp động (Kitchen Load ETD) kết nối bán kính dạo bộ Haversine (< 1km).
4. Đồng bộ hóa đơn trực tiếp qua WhatsApp Deep Linking tới chủ quán với chi phí vận hành 0đ phí SMS gateway.

## Operating Context

- **Môi trường sử dụng:** Quán ăn thực tế với tiếng ồn xung quanh vừa phải, kết nối mạng di động 4G/Wi-Fi, thiết bị cầm tay (smartphone Android / iOS qua trình duyệt di động hoặc ứng dụng Android).
- **Hành vi tương tác:** Người dùng chạm mic và nói tự nhiên một câu ngắn (ví dụ: "Cho 2 bát phở bò tái lăn ít cay và 1 trà đá"), hệ thống phản hồi âm thanh chime đa tần số và cập nhật giỏ hàng trực quan tức thì.
- **Quy trình xử lý:** Gọi món bằng giọng nói $\rightarrow$ AI gợi ý combo đi kèm $\rightarrow$ Xác nhận đơn $\rightarrow$ Chuyển hóa đơn sang WhatsApp chủ quán $\rightarrow$ Màn hình theo dõi tiến độ bếp & bản đồ điểm dạo chơi lân cận.

## Capabilities and Constraints

- **Khả năng đã xác thực:**
  - Nhận diện giọng nói tiếng Việt qua Web Speech API / WebSocket backend pipeline với bộ bóc tách NLU loại bỏ tiền tố ghép ("cho tôi thêm", "gọi thêm") và hậu tố đệm ("gì đó", "nữa nhé").
  - Thuật toán Cosine Similarity đề xuất combo món chính + món kèm/đồ uống theo hương vị và danh mục.
  - Bộ tính toán ETD tải bếp: $T_{est} = T_{base} + \sum t_i \times \text{queue\_factor}$.
  - Thuật toán Haversine tính khoảng cách địa lý chính xác, lọc POI dưới 1km kèm chỉ đường Google Maps.
  - Deep linking WhatsApp tự động định dạng Markdown chi tiết hóa đơn gửi đến số hotline của quán.
- **Ràng buộc kỹ thuật:**
  - Hệ thống hỗ trợ đa nền tảng Adaptive (Web Responsive Mobile-First & Android App).
  - Tối ưu hóa kích thước ảnh ẩm thực tĩnh cục bộ (~30-90KB) phục vụ trực tiếp từ máy chủ để tải siêu tốc.
  - Hoạt động 24/7 trên môi trường container Docker (Render/Docker Hub).

## Brand Commitments

- **Tên thương hiệu:** Vocalicious (Voice-Assisted Food Ordering & Recommendation System).
- **Phong cách & Ngôn ngữ:** Giao diện tối hiện đại (Dark Theme) làm nổi bật màu sắc ấm cúng của ẩm thực Việt Nam (vàng hổ phách Amber, xanh ngọc Emerald, đen xám Slate sâu lắng).
- **Âm thanh nhận diện:** Âm báo chime thanh lịch bằng Web Audio API (Start chime 520Hz/650Hz, Success chime 880Hz, Error chime 300Hz), không làm phiền không gian quán ăn.
- **Tính chân thực:** Hình ảnh món ăn đại diện đúng văn hóa ẩm thực truyền thống Việt Nam (Phở bò tái lăn, Phở tái nạm, Phở chín, Bánh mì giòn, Bún bò Huế, Trà đào cam sả, Sữa chua nếp cẩm).

## Evidence on Hand

- **Cơ sở học thuật:** Kế thừa và cải tiến từ nghiên cứu quốc tế *VOCALICIOUS - Voice-Assisted Food Ordering Web Application* (IJRASET, 05/2023, DOI: 10.22214/ijraset.2023.52445).
- **Bộ dữ liệu thực đơn:** 35 món ăn và đồ uống chuẩn hóa kèm vector hương vị 8 chiều (`backend/app/infrastructure/db/seed.py`).
- **Hình ảnh cục bộ:** Toàn bộ thư mục `backend/app/static/images/` với hình ảnh chân thực đã được nén tối ưu.
- **Kiểm thử tự động:** 19/19 test cases Pytest tự động bao phủ NLU, ETD, Haversine, Cosine Recommendation và API endpoints.
- **Hạ tầng triển khai thực tế:** Production URL `https://mobile-app-wl4i.onrender.com` và Docker Hub `trongmanhhh/voice-food-app:latest`.

## Product Principles

1. **Voice First, Zero Friction:** Người dùng không bao giờ bị bắt buộc phải gõ phím hay qua nhiều bước lọc phức tạp; mọi thao tác cốt lõi đều thực hiện được bằng khẩu lệnh tự nhiên.
2. **Authentic & Delightful:** Mọi món ăn, hình ảnh, âm thanh và phản hồi đều phản ánh chân thực ẩm thực Việt Nam và mang lại trải nghiệm ấm cúng, tinh tế.
3. **Transparent Waiting Experience:** Biến thời gian chờ đợi thụ động thành trải nghiệm thư giãn chủ động thông qua ước tính thời gian minh bạch và gợi ý dạo chơi lân cận.
4. **Adaptive Excellence:** Đảm bảo trải nghiệm mượt mà, đồng nhất trên màn hình di động web cũng như trên ứng dụng Android gốc theo nguyên tắc Material Design 3.

## Accessibility & Inclusion

- Giao diện cỡ chữ rõ ràng, độ tương phản cao trên nền tối, kích thước vùng chạm (touch target) tối thiểu 48x48dp.
- Phản hồi đa phương thức: kết hợp cả thị giác (badge trạng thái, sóng âm dynamic waveform), thính giác (web audio chimes, text-to-speech) và xúc giác (haptic-ready interaction).
- Hỗ trợ khử dấu tiếng Việt và ngữ âm đa vùng miền trong khẩu lệnh đặt món.


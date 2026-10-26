# Database design

Thiết kế CSDL ở giai đoạn tiếp theo phải lưu vector nội dung **324 chiều** theo
thứ tự `A(16), B(120), C(24), D(84), E(48), F(32)` của
[báo cáo PDF](../00-source-documents/bao-cao-csdldpt.pdf). Trạng thái hợp lệ
và chất lượng phép đo là metadata riêng, không tính vào 324 chiều. Nhãn hành
động, tên file và mã người chỉ phục vụ quản trị/đánh giá, không là đặc trưng
truy hồi. Migration hiện tại mới là khung và chưa tạo bảng vector.

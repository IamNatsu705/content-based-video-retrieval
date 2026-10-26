# Feature extraction implementation

## Hợp đồng triển khai bắt buộc

Tham chiếu [PDF Chương 3](../00-source-documents/bao-cao-csdldpt.pdf) và
[đặc tả đặc trưng](../02-features/feature-specification.md). Pipeline trích
toàn bộ sáu nhóm theo đúng thứ tự `A(16), B(120), C(24), D(84), E(48), F(32)`
thành vector 324 chiều cho từng video. Không dùng phương án 306 chiều của
bản Markdown cũ, cũng không thay bằng embedding CNN/HOG nếu chưa được yêu cầu
thay đổi đặc tả.

**Nguồn đầu vào của đặc trưng:** chỉ nội dung hình ảnh theo thời gian của file
video. Tên file, tên thư mục, nhãn, metadata, mã người, đường dẫn hoặc kết quả
đánh giá không được đọc để quyết định giá trị vector, trạng thái nội dung,
chuẩn hóa theo lớp hay giá trị thay thế. Metadata kỹ thuật trong container
chỉ được decoder sử dụng để giải mã; không đưa metadata đó vào đặc trưng,
không dùng để chọn/điều chỉnh phép đo. Dùng các giả định lấy mẫu cố định theo
báo cáo. Nếu cần nhận dạng video, dùng ID riêng trong manifest/CSDL, không
mã hóa ID vào vector.

Phải lưu riêng các cờ hợp lệ/tỷ lệ quan sát cho A–F, đặc biệt tương quan C,
các hệ số độ trễ và đỉnh D, các ô F; số 0 điền cho phép đo thiếu không được
diễn giải là chuyển động bằng 0. Giữ quy ước 25 FPS hoặc xử lý nhịp lấy mẫu
khi đầu vào khác FPS trước khi so sánh. Chưa có mã trích xuất hoàn chỉnh;
chi tiết thư viện, tham số flow và cách lưu kết quả sẽ được bổ sung lúc triển
khai, trên cơ sở các công thức cố định trong PDF.

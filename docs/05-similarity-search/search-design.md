# Similarity search design

Truy vấn sẽ dùng đúng vector 324 chiều theo
[PDF Chương 3](../00-source-documents/bao-cao-csdldpt.pdf), kèm thông tin
chất lượng của phép đo. Các nhóm có thang số và số chiều khác nhau, nên cần
chuẩn hóa và đánh giá vai trò từng nhóm trước khi chốt hàm xếp hạng Top-5.
PDF chưa quy định trọng số, khoảng cách hoặc ngưỡng cho nội dung ngoài tập;
những quyết định đó thuộc giai đoạn thiết kế và đánh giá tìm kiếm.

Điểm tương đồng và thứ tự Top-5 chỉ được tính từ vector đặc trưng suy ra từ
nội dung video. Nhãn, tên file/thư mục, metadata hoặc ID không được dùng làm
tín hiệu xếp hạng; chúng chỉ phục vụ tra cứu bản ghi, hiển thị hoặc phân tích
kết quả đánh giá.

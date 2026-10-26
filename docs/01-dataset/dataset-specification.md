# Đặc tả bộ dữ liệu (phần 1)

## Nguồn và vị trí

Bản nguồn được người dùng cung cấp từ thư mục dataset KTH; bản đã sao chép
vào dự án nằm tại `data/raw/`. Pipeline đọc dữ liệu từ thư mục này.

## Kiểm kê trực tiếp từ file

| Hành động (thư mục) | Số video MP4 |
| --- | ---: |
| boxing | 100 |
| handclapping | 99 |
| handwaving | 100 |
| jogging | 100 |
| running | 100 |
| walking | 100 |
| **Tổng** | **599** |

Tổng dung lượng file MP4: 90.387.248 byte (khoảng 86,2 MiB). Tên file ví dụ:
`boxing/person01_boxing_d1.mp4`; nhãn hành động hiện được suy ra từ thư mục.
Số lượng ở đây là số file có đuôi `.mp4`, chưa phải kết quả kiểm tra giải mã
từng video.

## Xuất xứ và đơn vị dữ liệu

Theo Chương 2 của [báo cáo PDF](../00-source-documents/bao-cao-csdldpt.pdf),
tập này được sưu tầm từ
[KTH Human Actions](https://www.csc.kth.se/cvap/actions/), dùng cho mục đích
phi thương mại và cần ghi nhận công trình của Schuldt, Laptev và Caputo khi
công bố kết quả. Phạm vi của dự án là 599 clip MP4 đã chọn, không phải toàn bộ
video ở nguồn KTH. Mỗi clip là một đối tượng độc lập; một cảnh là một diễn biến
vận động trong bối cảnh quay tương đối liên tục, có thể chứa nhiều chu kỳ động
tác. Nhãn trong tên file dùng để mô tả/đối chiếu, không phải bằng chứng hai
video cùng nhãn giống nhau hoàn toàn.

Tên file theo mẫu `personNN_<action>_dN.mp4`, ví dụ
`person01_boxing_d1.mp4`. Có 25 người và bốn điều kiện ghi hình: ngoài trời
cơ sở (150 clip), ngoài trời thay đổi tỷ lệ người (150), ngoài trời thay đổi
trang phục (149), trong nhà (150). Tổ hợp thiếu là vỗ tay của người 13 tại
điều kiện thay đổi trang phục. Cần giữ nguyên nhãn hành động từ thư mục và mã
người/điều kiện khi tạo metadata để phục vụ đánh giá; không đưa chúng vào
vector đặc trưng dùng để tìm kiếm.

## Đặc điểm kỹ thuật và thời lượng

Các số liệu kiểm tra giải mã dưới đây là thông tin **bổ sung từ bản chương 2
Markdown của dự án gốc**, không nằm trong Chương 2 của PDF. Phép kiểm kê ở dự
án này đã xác nhận số file, phân bố thư mục và tổng dung lượng; các thông số
giải mã/thời lượng cần được tái kiểm tra trong pipeline triển khai.

| Chỉ số | Giá trị báo cáo |
| --- | ---: |
| File đọc hết số frame khai báo | 599/599 |
| Kích thước, tỷ lệ khung hình | 160 × 120 pixel, 4:3 |
| FPS và codec | 25 FPS, `mpeg4` |
| File có luồng âm thanh | 0 |
| Tổng số frame giải mã | 66.708 |
| Số frame/clip | 31–362 |
| Thời lượng/clip | 1,24–14,48 giây |
| Trung bình; trung vị | khoảng 4,45 giây; 4,56 giây |
| Phân vị 25%; 75% | 2,86 giây; 5,60 giây |
| Tổng thời lượng | 2.668,32 giây |
| Nhóm file trùng SHA-256 | 0 |

Thời lượng danh định tính bằng số frame giải mã chia cho 25 FPS. Có 47 clip
dưới 2 giây, 184 clip từ 2 đến dưới 4 giây, 244 clip từ 4 đến dưới 6 giây,
122 clip từ 6 đến dưới 10 giây và 2 clip dài ít nhất 10 giây. Như vậy
597/599 clip ngắn hơn 10 giây. Trung bình theo lớp: boxing 5,50; handclapping
5,17; handwaving 6,31; jogging 2,93; running 2,13; walking 4,70 giây.

## Nội dung sáu nhóm

| Nhóm | Diễn biến chủ yếu | Thông tin quan sát quan trọng |
| --- | --- | --- |
| boxing | Tay đưa ra rồi thu về | Hướng, biên độ tay và xoay thân |
| handclapping | Hai tay khép lại và mở ra | Quan hệ đồng thời giữa hai phía, nhịp lặp |
| handwaving | Tay nâng, hạ và mở rộng | Độ cao, phạm vi tay và hình chiếu cơ thể |
| walking | Người đi qua ảnh, chân bước luân phiên | Dịch chuyển thân cùng nhịp bước |
| jogging | Người chạy chậm qua ảnh | Chuyển động tay chân và nhịp di chuyển |
| running | Người chạy qua ảnh | Các pha chân tay và thời gian đi qua cảnh |

Điểm chung là vận động của người trong cảnh có nền tương đối đơn giản và
camera cố định. Các clip khác nhau ở dạng động tác, người thực hiện, chiều
di chuyển, nhịp và biên độ, độ lớn người, trang phục, nền, ánh sáng và pha
động tác ở đầu/cuối. Một số clip di chuyển có đoạn đầu hoặc cuối chỉ thấy
nền. Vì thế, ảnh đại diện duy nhất hay thời lượng file không đủ để đánh giá
nội dung vận động của cả video. Đặc biệt, đi bộ/chạy chậm/chạy có thể gần
nhau về dịch chuyển nhưng khác nhịp; boxing/vỗ tay/vẫy tay có thể cùng nền
nhưng khác vị trí, hướng và quan hệ chuyển động của tay.

## Chất lượng, giới hạn và sử dụng về sau

Bản chương 2 Markdown bổ sung đối chiếu số frame với `00sequences.txt`: 598 clip bằng độ dài đoạn
được chú thích dài nhất cùng tên; `boxing/person01_boxing_d4.mp4` có 60 frame
trong khi đoạn dài nhất được chú thích có 125. Chỉ bằng nhau về độ dài không
chứng minh clip được cắt đúng mốc; trường hợp khác biệt này vẫn đọc được và
không tự động là file hỏng. Báo cáo đã kiểm tra giải mã toàn bộ file nhưng
chỉ xem nội dung chi tiết ở các clip đại diện, chưa duyệt thủ công mọi ranh
giới cảnh.

Tập ảnh 160 × 120 khó giữ chi tiết nhỏ, phụ thuộc góc nhìn và không đại diện
cho video tự nhiên có camera di động, nhiều người hay che khuất phức tạp.
Chưa có phép chia cố định thành tập truy vấn/đánh giá trong hai chương gốc;
bước đánh giá cần quy định tách người và điều kiện quay, tránh dùng video
cùng người/cùng lần ghi ở cả hai phía rồi diễn giải quá mức kết quả.

**Nguồn ưu tiên:** Báo cáo CSDLDPT, Chương 2, trang 8–17. PDF gốc được giữ
cục bộ vì có thông tin cá nhân và bị loại khỏi GitHub. Thống kê kỹ thuật chi
tiết và đối chiếu `00sequences.txt` được bổ sung từ bản chương 2 Markdown đã
đối chiếu trên máy.

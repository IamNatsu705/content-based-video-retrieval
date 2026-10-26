# Đặc tả bộ đặc trưng nội dung video (phần 2)

## Mục tiêu và trạng thái

Thiết kế dưới đây tuân thủ **Chương 3, trang 18–30 của bản PDF báo cáo** do
người dùng cung cấp. Đây là chuẩn bắt buộc cho phần trích xuất sau này.
Đối tượng tìm kiếm là **cách người vận động** trong 599 video KTH ảnh xám:
dịch chuyển toàn thân, vị trí/hướng/cường độ cử động, quan hệ hai phía và
diễn biến thời gian. Màu sắc không được dùng vì nguồn không có thông tin màu
đáng tin. Nhãn `boxing`, `walking`…, tên file và mã người **không** là đầu vào
của vector truy hồi. Các dấu hiệu hình dạng và mức xám chỉ đóng vai trò bổ
trợ. Đây là **đặc tả đề xuất**, chưa phải pipeline đã trích rút 599 vector hay
kết quả độ chính xác tìm kiếm.

### Điều kiện tiên quyết về nguồn giá trị

Mọi chiều của vector và mọi giá trị được gọi là đặc trưng/nội dung phải được
tính từ pixel các frame và diễn biến của chính video theo công thức trong
báo cáo. Mặt nạ, hộp bao, flow và cờ hợp lệ cũng phải được tạo từ quá trình
xử lý video. Không dùng metadata, nhãn lớp, tên file, tên thư mục, đường dẫn,
mã người, timestamp ngoài video hoặc thông tin bên ngoài để điền, suy diễn,
hiệu chỉnh theo lớp hay thay đổi bất kỳ giá trị nội dung nào. Metadata có thể
lưu riêng để nhận diện bản ghi và đánh giá kết quả; nó không thuộc vector 324
chiều và không được ảnh hưởng điểm tương đồng/xếp hạng nội dung.

Vector cho một video có thứ tự cố định:

$$
F_{video}=[A_{16},B_{120},C_{24},D_{84},E_{48},F_{32}]\in\mathbb R^{324}.
$$

| Nhóm | Chiều | Biểu diễn | Giá trị thông tin chính |
| --- | ---: | --- | --- |
| A | 16 | Dịch chuyển vùng giữa người, hướng, mức, độ ổn định, tỷ lệ hộp | Phân biệt tịnh tiến toàn thân với vận động tại chỗ |
| B | 120 | 96 phần tử vị trí × hướng flow tương đối và 24 thống kê cường độ | Giữ cử động nằm ở đâu, theo hướng nào, mạnh đến đâu |
| C | 24 | Cân bằng, tương quan và hai chỉ số hướng vào/ra của hai phía | Phân biệt cách hai phía phối hợp cùng thời điểm |
| D | 84 | 48 tương quan theo độ trễ, 12 chỉ số đỉnh, 24 mức hoạt động theo đoạn | Giữ nhịp và diễn biến đầu–cuối ở mức thô |
| E | 48 | Hình chiếu, bố cục xám, histogram xám | Bổ sung tư thế và diện mạo, dễ chịu tác động ngoài hành động |
| F | 32 | Tỷ lệ pixel thay đổi quanh vùng người | Bổ sung cử động ngoài mặt nạ/hộp |

Số chiều không phải trọng số. Không thể so trực tiếp khoảng cách của sáu nhóm
trước khi xác định chuẩn hóa từng thành phần và trọng số qua đánh giá.

## Biểu diễn và quy ước chung

Video có $T\ge2$ ảnh xám $I_t$ (0–255), $N=T-1$ cặp liên tiếp. $M_t$ là mặt
nạ tiền cảnh coi là vùng người; $\Omega_t=(x_t,y_t,w_t,h_t)$ là hộp bao người.
Tọa độ pixel trong hộp được đổi thành $(\xi,\eta)=((x-x_t)/w_t,
(y-y_t)/h_t)$, để ô không gian bám theo người thay vì bám theo nền. Ô hình
học không đồng nghĩa đã nhận diện tay, chân hay khớp.

Optical flow $f_t(p)=(u_t,v_t)$ biểu diễn dịch chuyển biểu kiến từ $I_t$
sang $I_{t+1}$ theo pixel/frame. Ước lượng $g_t$ là trung vị flow vùng giữa
người (khoảng 25–65% chiều cao hộp); $c_t$ là trung vị flow nền. Với
$H_t=\max(h_t,12)$, dùng:

$$
a_t=(g_t-c_t)/H_t,\qquad r_t(p)=(f_t(p)-g_t)/H_t.
$$

$a_t$ giữ tịnh tiến thân so với nền; $r_t$ giữ cử động so với thân. Chia cho
chiều cao người giảm tác động của tỷ lệ đối tượng; sàn 12 pixel tránh khuếch
đại nhiễu với hộp quá nhỏ. Ở 25 FPS, một cặp cách nhau 0,04 giây. Flow là
chuyển động ảnh 2D, không đo vận tốc vật lý hay chuyển động 3D.

Gọi $G$ là các cặp có mặt nạ/hộp và tham chiếu flow đủ dùng cho A–E.
F có điều kiện hợp lệ riêng. Trung bình và độ lệch chuẩn dùng toàn bộ quan
sát hợp lệ của từng chuỗi; phân vị dùng nội suy tuyến tính ở vị trí $(n-1)p$
trên dãy đã sắp. Giá trị thiếu phải có cờ hợp lệ/độ tin cậy riêng: số 0
điền thay không được hiểu là không chuyển động.

## A — Dịch chuyển toàn vùng người (16 chiều)

Từ $a_t$ lấy trung bình, độ lệch chuẩn của hai trục (4); phân vị 25/50/75%
và trung bình của $\|a_t\|$ (4); mức chuyển động trung bình trên toàn $N$
cặp (1); dịch chuyển tâm vùng người **trung bình trên $N$ cặp** theo hai
trục (2); chỉ số nhất
quán hướng $\|\sum a_t\|/\max(\sum\|a_t\|,\epsilon)$ (1); trung bình/độ lệch
chuẩn biến đổi giữa hai vector hợp lệ kế tiếp (2); trung bình/độ lệch chuẩn
tỷ lệ rộng/cao của hộp (2). Tổng 16.

Nhóm này giữ khác biệt giữa người đi/chạy qua ảnh và người vận động quanh
một vị trí, cùng chiều/mức dịch chuyển và độ ổn định hướng. Trung bình
dịch chuyển tâm làm giảm phụ thuộc độ dài video. Độ biến thiên vector chỉ
tính trên hai cặp frame **liền kề** cùng hợp lệ. Tốc độ ảnh không đủ để quyết định đi bộ hay
chạy, và hộp bị nhiễu có thể làm sai tỷ lệ rộng/cao.

## B — Vị trí, hướng và cường độ cử động (120 chiều)

Chia hộp người thành **6 hàng × 2 cột**. Ở 12 ô, tích lũy histogram hướng
của $r_t$ với **8 tâm cách nhau 45°**, đóng góp có trọng số $\|r_t\|$ và
phân bổ mềm vào hai hướng kề. Chuẩn hóa **chung toàn bộ 96 ô hướng**, để
giữ tỷ trọng giữa các vị trí. Thêm trung bình và độ lệch chuẩn mức flow
tương đối trung bình theo pixel tiền cảnh của từng ô: $12\times2=24$.

B có $6\times2\times8+6\times2\times2=120$ chiều. Nó mô tả tay chuyển
động ở phần trên, chân ở phần dưới, hướng ngang/chéo và cường độ. Histogram
gộp cả video nên mất thứ tự xuất hiện của hướng; ô nhỏ, mặt nạ/hộp sai hoặc
ước lượng $g_t$ sai làm đặc trưng nhiễu.

## C — Phối hợp chuyển động hai phía (24 chiều)

Dùng **cùng hộp $\Omega_t$ và flow tương đối $r_t$ của B**, chia thành
**6 hàng × 2 nửa** trái/phải. Mặt nạ hỗ trợ $S_t$ mở rộng $M_t$ tối đa 3
pixel mỗi phía trong hộp (lân cận 7 × 7). Với mỗi hàng $b$, mức hoạt động
$L_b(t)$ và $R_b(t)$ là tổng $\|r_t(p)\|$ ở pixel hỗ trợ chia cho
**diện tích toàn nửa ô**, kể cả pixel ngoài mặt nạ. Lưu trung bình theo
$G$ của $q_b(t)=\min(L_b,R_b)/\max(L_b,R_b,\epsilon)$ (quy ước 0 khi
cả hai phía đứng yên) và $\rho_b=\operatorname{corr}_G(L_b,R_b)$.

Để phân biệt chuyển động hướng vào/ra trục giữa, trên cùng cặp frame tính
bốn mức flow ngang không âm cho từng nửa: $L_p$ là tổng
$\max(r_x,0)$ ở nửa trái; $L_n$ là tổng $\max(-r_x,0)$ ở nửa trái;
$R_p,R_n$ tương tự cho nửa phải. Mỗi tổng chia cho diện tích toàn nửa ô.
Với $Z=L_p+L_n+R_p+R_n$, đặt:

$$
I_b(t)=\frac{2\min(L_p,R_n)}{\max(Z,\epsilon)},\qquad
O_b(t)=\frac{2\min(L_n,R_p)}{\max(Z,\epsilon)}.
$$

$I$ giữ đồng thời hướng vào trục giữa, $O$ giữ đồng thời hướng ra ngoài;
cả hai bằng 0 khi không có chuyển động ngang. Mỗi hàng ghép
$[\mu_G(q_b),\rho_b,\mu_G(I_b),\mu_G(O_b)]$: **$6\times4=24$ chiều**.
Nếu phương sai một chuỗi gần 0, điền tương quan 0 kèm cờ không xác định.
Hai chỉ số chỉ mô tả hướng theo ảnh, không đo khoảng cách hoặc tiếp xúc
thực của hai bàn tay, không xác định từng tay và không giữ thứ tự các pha.

## D — Tính lặp và diễn biến thời gian (84 chiều)

Lấy tín hiệu hoạt động của mỗi hàng bằng trung bình hai ô cường độ trong B.
Trên **đoạn liên tục hợp lệ dài nhất**, loại xu hướng tuyến tính, sau đó
tính tương quan Pearson giữa hai đoạn chồng lấp tại các độ trễ
`3, 5, 8, 12, 16, 24, 32, 48` frame (0,12–1,92 giây ở 25 FPS).
Chỉ dùng độ trễ khi $n\ge\max(25,2\ell)$, độ lệch chuẩn của chuỗi sau
loại xu hướng ít nhất $10^{-4}$ và mẫu số khác 0. Tám hệ số × sáu hàng
tạo **48 chiều**. Khi không đủ điều kiện, điền 0 và đánh dấu thiếu tin cậy;
không xóa toàn bộ tám hệ số chỉ vì thiếu đỉnh vượt ngưỡng 0,35.

Với từng hàng, khảo sát **mọi độ trễ nguyên** từ 3 đến
$L=\min(48,\lfloor n/2\rfloor)$. Trong các vị trí nội bộ
$4\le\ell\le L-1$, chọn đỉnh cực đại cục bộ dương có tương quan lớn nhất.
Lưu $\nu_b=\ell_{peak}/48$ và $\pi_b=r_b(\ell_{peak})$; nếu không có
đỉnh hợp lệ, cả hai bằng 0 và ghi rõ trạng thái. Sáu hàng × hai số tạo
**12 chiều bổ sung**. Đỉnh chỉ thể hiện tín hiệu lặp theo chuỗi mức chuyển
động, không phải tần số bước chân thật.

Chia toàn bộ $N$ vị trí thời gian gốc thành **bốn đoạn gần bằng nhau**,
giữ trung bình mức hoạt động cho sáu hàng trong mỗi đoạn: $4\times6=24$
chiều. Không dồn các cặp hợp lệ trước khi chia, vì như vậy sẽ đổi vị trí
đầu/giữa/cuối. Tổng $48+12+24=84$ chiều. Tương quan yếu nhưng tính được vẫn có giá trị;
thiếu quan sát không có nghĩa không lặp. Các hệ số độ trễ chỉ mô tả nhịp
tín hiệu, không tự chứng minh tần số bước chân; lưu cờ hợp lệ và số cặp
chồng lấp bên cạnh vector.

## E — Hình chiếu và mức xám (48 chiều)

Chuẩn hóa vùng người/mặt nạ thành ảnh **32 × 32**; mặt nạ vẫn là nhị phân.
Trên tám dải ngang cao bốn pixel, đo tỷ lệ cột có ít nhất một pixel người;
trung bình và độ lệch chuẩn theo thời gian: **16 chiều**. Trên lưới **4 × 2**,
đo mức xám đã chia 255 và nhân mặt nạ, rồi chia cho toàn diện tích ô;
trung bình và độ lệch chuẩn: **16 chiều**. Histogram xám của pixel thuộc
mặt nạ với **16 khoảng rộng 16 mức**, lấy trung bình theo thời gian:
**16 chiều**. Tổng 48.

E bổ sung độ mở dáng người và bố cục sáng tối. Mức xám ô trộn độ sáng với
tỷ lệ người chiếm ô, không phải độ sáng riêng của người. Trang phục, bóng,
ánh sáng và lỗi mặt nạ có thể làm E thay đổi dù hành động tương tự; không
để E chi phối kết quả chỉ vì có nhiều giá trị biến thiên.

## F — Thay đổi ảnh quanh vùng người (32 chiều)

Với hộp có chiều cao $h_t$, chiều rộng $w_t$ và tâm ngang $c_{x,t}$,
đặt $W_t^F=\max(1,5h_t,w_t+0,2h_t)$. Miền hình học có chiều ngang
$[c_{x,t}-W_t^F/2,c_{x,t}+W_t^F/2]$, biên trên $y_{0,t}-0,15h_t$,
biên dưới $y_{1,t}+0,10h_t$. Chia miền hình học thành **4 × 4 ô trước
khi cắt theo biên ảnh**; mỗi ô chỉ đo phần giao thực với ảnh, giữ nguyên
vị trí ô khi người ở sát mép. Với mỗi cặp frame, tính tỷ lệ pixel trong
phần giao có $|I_{t+1}(p)-I_t(p)|>12$ tại **cùng tọa độ ảnh**. Lấy
trung bình và độ lệch chuẩn của từng ô trên **các cặp hợp lệ riêng của F**:
$16\times2=32$ chiều.

F hỗ trợ phát hiện chuyển động tay ngoài hộp hoặc mặt nạ. Hộp lỗi, $h_t<16$
hoặc ô không có phần giao với ảnh thì giá trị ô đó điền 0 kèm cờ thiếu;
**không áp dụng điều kiện $h_t\ge1,2w_t$ của bản thiết kế cũ**.
Nền, bóng,
ánh sáng, rung hình và cắt miền ở mép ảnh cũng có thể làm F sai lệch.

## Giá trị khi kết hợp và bước kiểm chứng

A tách tịnh tiến toàn thân; B mô tả vị trí và hướng cử động; C thêm quan hệ
hai phía; D thêm nhịp và thứ tự thô; E bổ sung hình dạng/diện mạo; F thêm
ngoại vi. Nhờ vậy, boxing và vỗ tay có thể giống ở mức ít tịnh tiến nhưng
khác quan hệ tay; vỗ tay và vẫy tay có thể giống ở vùng phần trên nhưng
khác phạm vi/cao độ; đi bộ, chạy chậm và chạy có thể giống ở tịnh tiến nhưng
khác nhịp và cường độ. Đây là giá trị thông tin **dự kiến từ định nghĩa**.

Khi triển khai cần kiểm tra tỷ lệ cặp hợp lệ, chất lượng mặt nạ, phân bố
từng chiều, chuẩn hóa và trọng số nhóm, rồi so sánh truy hồi Top-5 theo
từng nhóm và các tổ hợp (ablation). Các ngưỡng 12 pixel của F, 12 pixel sàn
chiều cao, lưới và độ trễ là lựa chọn thiết kế, chưa được chứng minh tối ưu.
Không dùng nhãn hoặc mã người để cải thiện điểm tương đồng; chỉ dùng chúng
cho kiểm kê và đánh giá độc lập.

**Nguồn ưu tiên:** Báo cáo CSDLDPT, Chương 3, trang 18–30. PDF gốc được giữ
cục bộ vì có thông tin cá nhân và bị loại khỏi GitHub. Bản Markdown cũ mô tả
306 chiều và khác báo cáo; mọi triển khai mới phải theo đặc tả 324 chiều này.

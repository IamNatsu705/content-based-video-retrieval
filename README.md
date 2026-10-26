# Content-Based Video Retrieval (CBVR)

Dự án môn Cơ sở dữ liệu đa phương tiện: quản lý bộ video KTH Human Actions,
trích xuất biểu diễn nội dung và tìm 5 video gần nhất với một video truy vấn.

> **Trạng thái hiện tại:** cấu trúc dự án và đặc tả đã có; API mới cung cấp
> endpoint kiểm tra sức khỏe. Trích xuất đặc trưng, xây chỉ mục, tìm kiếm và
> đánh giá vẫn đang là khung, chưa chạy được end-to-end.

## Tài liệu chuẩn

- [Đề bài](docs/00-source-documents/assignment.md)
- Báo cáo CSDLDPT (PDF) là nguồn chuẩn cho phần dữ liệu và đặc trưng; bản gốc
  có thông tin cá nhân nên được giữ cục bộ và không đưa lên GitHub.
- [Đặc tả dataset](docs/01-dataset/dataset-specification.md)
- [Đặc tả đặc trưng](docs/02-features/feature-specification.md)
- [Kế hoạch trích xuất](docs/03-feature-extraction/implementation.md)
- [Thiết kế CSDL](docs/04-database/database-design.md)
- [Thiết kế tìm kiếm](docs/05-similarity-search/search-design.md)
- [Đánh giá](docs/06-evaluation/evaluation.md) · [Hướng dẫn demo](docs/07-demo/demo-guide.md)

Các triển khai tiếp theo phải theo PDF, gồm vector 324 chiều ghép theo thứ tự
`A(16) + B(120) + C(24) + D(84) + E(48) + F(32)`. Thiết kế chưa được kiểm
chứng thực nghiệm nhưng vẫn là hợp đồng triển khai hiện hành; không tự đổi số
chiều, phép đo, thứ tự ghép hoặc thay bằng một biểu diễn khác.

## Điều kiện về nguồn đặc trưng

Vector và mọi giá trị nội dung dùng để so sánh chỉ được tính từ frame và diễn
biến hình ảnh của chính video, theo công thức trong báo cáo. Không dùng
metadata, nhãn, tên file, tên thư mục, đường dẫn, ID hay thông tin ngoài video
để tạo, suy diễn, điền hoặc điều chỉnh vector và điểm xếp hạng. Metadata chỉ
dùng riêng cho định danh bản ghi, quản trị, hiển thị và đánh giá. Thông tin
kỹ thuật trong container chỉ phục vụ giải mã; không trở thành đặc trưng.

## Dataset

599 video MP4 được đặt trong `data/raw/`, chia theo thư mục hành động:

| Thư mục | Số video |
| --- | ---: |
| `boxing` | 100 |
| `handclapping` | 99 |
| `handwaving` | 100 |
| `jogging` | 100 |
| `running` | 100 |
| `walking` | 100 |

Tổng dung lượng hiện tại khoảng 86,2 MiB. Dataset được lấy từ KTH Human
Actions; xem [đặc tả dataset](docs/01-dataset/dataset-specification.md) để
biết xuất xứ, nội dung, giới hạn và thống kê. Tên thư mục/file có thể được
dùng cho kiểm kê hoặc đánh giá, nhưng tuyệt đối không làm đầu vào đặc trưng.

## Cấu trúc dự án

```text
docs/                 Đề bài, báo cáo nguồn và đặc tả từng phần
data/raw/             599 video nguồn
data/processed/       Dữ liệu trung gian đã xử lý
data/queries/         Video truy vấn
data/metadata/        Metadata quản trị/đánh giá, không phải đặc trưng
src/cbvr/             Package Python: preprocessing, features, database,
                      retrieval, evaluation, api
scripts/              Điểm vào dự kiến cho extract, index và search
database/migrations/  Migration PostgreSQL/pgvector
outputs/              Đặc trưng và kết quả sinh tự động
tests/                Kiểm thử
```

## Thiết lập môi trường (Windows PowerShell)

Yêu cầu Python 3.11 trở lên.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
```

## Chạy API hiện có

```powershell
$env:PYTHONPATH = "src"
uvicorn cbvr.api.main:app --reload
```

Kiểm tra tại `http://127.0.0.1:8000/health`; tài liệu OpenAPI tại
`http://127.0.0.1:8000/docs`. Hiện API chỉ trả trạng thái `ok`, chưa kết nối
CSDL và chưa cung cấp endpoint tìm kiếm.

## Docker Compose

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Compose khởi động PostgreSQL có pgvector và API mẫu. Migration hiện chỉ bật
extension `vector`; schema video/đặc trưng và kết nối CSDL từ API chưa được
triển khai. Dừng bằng `Ctrl+C`, sau đó chạy `docker compose down`.

## Các lệnh pipeline dự kiến

```powershell
python scripts/extract_features.py
python scripts/build_index.py
python scripts/run_search.py
```

Ba script hiện ném `NotImplementedError`; các lệnh trên chỉ là điểm vào dự
kiến, chưa thực hiện trích xuất, lập chỉ mục hay tìm kiếm.

## Trạng thái triển khai

- [x] Bộ dữ liệu 599 video được đặt trong dự án.
- [x] Đề bài, báo cáo chuẩn và đặc tả dataset/đặc trưng.
- [x] API mẫu `/health`, cấu hình Docker và migration bật pgvector.
- [ ] Tiền xử lý/mặt nạ và trích vector 324 chiều theo PDF.
- [ ] Schema quản trị video, đặc trưng và chất lượng phép đo.
- [ ] Tìm kiếm Top-5 chỉ dựa trên vector nội dung.
- [ ] Bộ đánh giá, kết quả trung gian và demo hoàn chỉnh.

## Git và dữ liệu

`.gitignore` bỏ qua video trong `data/raw/`, dữ liệu truy vấn, metadata, dữ
liệu xử lý, kết quả sinh tự động và PDF báo cáo gốc có thông tin cá nhân. Các
file vẫn được giữ trên máy hiện tại. Khi clone dự án, cần tự cung cấp dataset
và báo cáo nguồn; đặc tả đã biên soạn được lưu trong `docs/`. `.env.example`,
tài liệu và file `.gitkeep` vẫn được theo dõi bằng Git.

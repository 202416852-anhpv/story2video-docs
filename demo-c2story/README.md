# Demo C2Story Studio — Bộ tài liệu đặc tả để phát triển lại từ đầu

> **Phiên bản:** 1.1 · **Ngày:** 2026-10-19 · **Vai trò soạn thảo:** Business Analyst
> **Trạng thái:** Bản nháp để review

## 1. Mục đích

Bộ tài liệu đặc tả hệ thống **AI Story Studio theo dự án (Project)**. Người dùng biến một truyện dài thành **video minh họa có thuyết minh nguyên văn**, theo luồng 6 bước:

```
1. Nhập truyện  →  2. Chia chương  →  3. AI dựng thế giới truyện
→  4. AI sinh tư liệu (ảnh + thuyết minh nguyên văn)
→  5. Chỉnh sửa video trên timeline (chuyển cảnh, nhạc nền, SFX, tinh chỉnh)
→  6. Xuất & tải video
```

Nhân vật và bối cảnh được giữ nhất quán xuyên suốt. Người dùng có thể làm thủ công từng bước, hoặc giao cho **AI Director** chạy tự động từ bước 2 đến khi có bản nháp timeline.

> **Nguyên tắc cốt lõi: Thuyết minh nguyên văn (Verbatim narration).** Audio của video đọc **toàn bộ** văn bản truyện, **đúng từng chữ, đúng thứ tự**. Không chỉnh sửa, không tóm tắt, không bỏ đoạn. AI chỉ được *minh họa* câu chuyện, không được *viết lại* nó. Xem BR-19..BR-23 ở [08](tai-lieu/08-quy-tac-nghiep-vu.md).

Chức năng tham chiếu module Projects của c2story.com. Tài liệu dùng để **phát triển lại từ đầu**: backend, API, cơ sở dữ liệu và tích hợp AI đều do nhóm tự thiết kế.

## 2. Phạm vi

**Trọng tâm:** Studio dự án, gồm quản lý dự án và cộng tác, bản thảo và chương, thế giới truyện, **sinh tư liệu** (storyboard tự động, ảnh, thuyết minh nguyên văn), **trình chỉnh sửa video timeline** (nhạc nền, SFX, chuyển cảnh, tinh chỉnh) và xuất video, AI Director.

**Không làm video bằng AI sinh video.** Video được dựng từ ảnh minh họa tĩnh với hiệu ứng chuyển động (Ken Burns), chuyển cảnh, phụ đề, nhạc nền và SFX trên trình chỉnh sửa timeline, rồi render bằng hạ tầng của hệ thống.

**Phụ trợ, chỉ ở mức Studio cần:**

| Phụ trợ | Vì sao cần |
|---|---|
| Tích hợp **SSO có sẵn** (vd. SSO Vbee) | Định danh Owner/Editor, phân quyền dự án. **Không tự phát triển** đăng ký, đăng nhập, đăng xuất, mật khẩu; chỉ tích hợp qua OIDC |
| Thư viện tài sản cá nhân | Tái sử dụng nhân vật giữa các dự án |
| Thư viện âm thanh | Nhạc nền & SFX có license cho trình chỉnh sửa |
| Credit & thanh toán | Chi trả các job AI tốn phí |
| Quản trị tối thiểu | Cấu hình giá credit, mô hình AI; theo dõi job |

**Đã lược bỏ** (không thiết kế ở phiên bản này): Explore/thư viện cộng đồng, Create nhanh (Auto-make), Remix (Continue/Rewrite), Chat nhân vật, Guide cộng đồng, bán sách và chia doanh thu cho tác giả, API công khai, Poster/Trailer cho sách tạo nhanh, Like/Share công khai, **video AI (image-to-video, Video Storyboard, Animated Book, chất lượng Basic/Enhance/Cinema)**, **AI viết lại văn bản truyện**, **sách tranh (Compile book, trình đọc, PDF)**.

## 3. Nguyên tắc "phát triển sạch" (clean-room)

| # | Nguyên tắc |
|---|---|
| CR-01 | **Không dùng bất kỳ API key, token, publishable key, endpoint hay CDN nào của c2story.com**, kể cả key Clerk công khai, `cdn.c2story.com` hay `/api/*` của họ. |
| CR-02 | Mọi dịch vụ ngoài (AI, thanh toán, email, lưu trữ) dùng **tài khoản và key do nhóm tự đăng ký**, cấu hình qua biến môi trường và quản lý bằng secret manager. |
| CR-03 | Không sao chép mã nguồn, hình ảnh, văn bản marketing, logo hay nội dung người dùng của c2story. Chỉ tham chiếu **hành vi chức năng**. |
| CR-04 | API được **thiết kế lại** theo REST và OpenAPI 3.1 (xem `06`). Không phụ thuộc hệ thống cũ. |
| CR-05 | Giá credit ghi lại làm **giá trị tham khảo**, lưu thành cấu hình. |

## 4. Nguồn thông tin

Khảo sát bằng công cụ REA ngày 2026-10-19:

- 14 màn hình Studio (`?v=map|source|workspace|assets|timeline|relationships|visual-rules|storyboard|pages|images|video|animatedBook|videos|archives`) trên một dự án thật của người khảo sát.
- Chuỗi giao diện và cấu trúc tài nguyên trong bundle trang `/project/[id]`.
- Trang `/project/new`, `/dashboard`, `/characters`, `/pricing`.

Mức độ chắc chắn được đánh dấu như sau:

| Ký hiệu | Ý nghĩa |
|---|---|
| **[QS]** | Quan sát trực tiếp trên giao diện |
| **[SL]** | Suy luận từ chuỗi UI hoặc cấu trúc tài nguyên |
| **[ĐX]** | Đề xuất của BA |

## 5. Cấu trúc thư mục

```
demo-c2story/
├── README.md                     # Tài liệu này
├── tai-lieu/                     # 10 tài liệu đặc tả (xem §6)
│   └── 03-dac-ta-use-case/       # Đặc tả 165 use case: mục lục + 10 file M01–M10
├── so-do/                        # Sơ đồ PlantUML của hệ thống mới (xem §7)
│   ├── 01-use-case/
│   │   └── phan-ra/              # Use case phân rã theo phân hệ M01–M10
│   ├── 02-du-lieu/               # Domain model, ERD đầy đủ + ERD theo phân hệ
│   ├── 03-kien-truc/             # C4 (context, container, component API/AI/editor), deployment
│   ├── 04-tuan-tu/               # Sơ đồ tuần tự
│   ├── 05-hoat-dong/             # Sơ đồ hoạt động
│   ├── 06-trang-thai/            # Sơ đồ trạng thái
│   └── tools/split_erd.py        # Sinh ERD theo phân hệ từ erd.puml
└── khao-sat-c2story/             # Kết quả khảo sát c2story.com bằng REA (tham chiếu, không phải thiết kế mới)
    └── uc04-studio/
```

## 6. Danh mục tài liệu (`tai-lieu/`)

| Mã | Tài liệu | Chuẩn tham chiếu |
|---|---|---|
| 01 | [Tài liệu yêu cầu nghiệp vụ (BRD)](tai-lieu/01-tai-lieu-yeu-cau-nghiep-vu-BRD.md) | BABOK v3 |
| 02 | [Đặc tả yêu cầu phần mềm (SRS)](tai-lieu/02-dac-ta-yeu-cau-phan-mem-SRS.md) | ISO/IEC/IEEE 29148:2018 |
| 03 | [Đặc tả Use Case (165 use case, theo phân hệ)](tai-lieu/03-dac-ta-use-case/00-muc-luc.md) | Cockburn fully-dressed |
| 04 | [Mô hình dữ liệu](tai-lieu/04-mo-hinh-du-lieu.md) | ERD, 3NF |
| 05 | [Kiến trúc hệ thống](tai-lieu/05-kien-truc-he-thong.md) | C4 model, ADR |
| 06 | [Đặc tả API](tai-lieu/06-dac-ta-api.md) | REST, OpenAPI 3.1, RFC 9457 |
| 07 | [Yêu cầu phi chức năng](tai-lieu/07-yeu-cau-phi-chuc-nang.md) | ISO/IEC 25010 |
| 08 | [Quy tắc nghiệp vụ & credit](tai-lieu/08-quy-tac-nghiep-vu.md) | — |
| 09 | [Kế hoạch phát triển & ma trận truy vết](tai-lieu/09-ke-hoach-phat-trien.md) | RTM |
| 10 | [Thuật ngữ](tai-lieu/10-thuat-ngu.md) | — |

## 7. Danh mục sơ đồ (`so-do/`)

| Thư mục | File |
|---|---|
| `01-use-case/` | `uc-tong-quan` (tổng quan), `uc-studio-chi-tiet` (Studio) |
| `01-use-case/phan-ra/` | `uc-m01-tich-hop-sso`, `uc-m02-du-an-cong-tac`, `uc-m03-ban-thao-chuong`, `uc-m04-the-gioi-truyen`, `uc-m05a-storyboard`, `uc-m05b-sinh-anh-thuyet-minh`, `uc-m06-trinh-chinh-sua-video`, `uc-m07-ai-director`, `uc-m08-thu-vien-tai-san`, `uc-m09-credit-thanh-toan`, `uc-m10-quan-tri` |
| `02-du-lieu/` | `domain-class`, `erd` (đầy đủ); ERD theo phân hệ `erd-1-tai-khoan-credit`, `erd-2-du-an-ban-thao`, `erd-3-the-gioi-truyen`, `erd-4-sinh-tu-lieu`, `erd-5-trinh-chinh-sua-video`, `erd-6-director-job-ha-tang`. Các ERD con sinh tự động: chỉ sửa `erd.puml` rồi chạy `python3 so-do/tools/split_erd.py` |
| `03-kien-truc/` | `c4-context`, `c4-container`, `c4-component-api`, `c4-component-ai`, `c4-component-editor`, `deployment` |
| `04-tuan-tu/` | `seq-dang-nhap-sso`, `seq-import-chia-chuong`, `seq-storyboard-sinh-anh`, `seq-director`, `seq-sinh-tu-lieu`, `seq-thuyet-minh-nguyen-van`, `seq-chinh-sua-xuat-video`, `seq-cong-tac-xung-dot`, `seq-thanh-toan` |
| `05-hoat-dong/` | `act-quy-trinh-project`, `act-giu-tru-credit`, `act-phu-kin-van-ban` |
| `06-trang-thai/` | `state-job`, `state-chapter-media`, `state-narration-render`, `state-director-plan`, `state-tool-proposal`, `state-subscription` |

Render toàn bộ sơ đồ (cần Java và Graphviz), chạy trong `demo-c2story/`:

```bash
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -tpng "so-do/**.puml"
```

> `erd.puml` rộng khoảng 4900px. Nếu không đặt `PLANTUML_LIMIT_SIZE`, ảnh sẽ bị cắt ở 4096px. Có thể xuất SVG (`-tsvg`) để xem không giới hạn.

## 8. Lịch sử phiên bản

| Phiên bản | Ngày | Nội dung |
|---|---|---|
| 1.0 | 2026-10-19 | Bản đầu, phạm vi toàn sản phẩm |
| 1.1 | 2026-10-19 | Thu hẹp phạm vi về Project Studio và phụ trợ |
| 1.2 | 2026-10-19 | Đổi đầu ra video sang **slideshow ảnh minh họa**; thêm nguyên tắc **thuyết minh nguyên văn**; bỏ video AI và AI viết lại văn bản |
| 1.3 | 2026-10-19 | Xác thực dùng **SSO có sẵn** (tích hợp OIDC, mẫu BFF); bỏ đăng ký, đăng nhập, mật khẩu tự xây |
| 1.4 | 2026-10-19 | Cấu trúc lại thư mục: `tai-lieu/`, `so-do/` theo loại sơ đồ, `khao-sat-c2story/` |
| 1.5 | 2026-10-19 | Luồng Studio 6 bước: bỏ sách tranh; bước "Sinh tư liệu" chỉ ra ảnh + thuyết minh; thêm **trình chỉnh sửa video timeline** (nhạc nền, SFX, chuyển cảnh, tinh chỉnh) |
| 1.6 | 2026-10-19 | Đặc tả đầy đủ **165 use case** (mã `UC-xx.yy`, ghi trên sơ đồ phân rã), tách theo phân hệ trong `tai-lieu/03-dac-ta-use-case/` |
| 1.7 | 2026-10-19 | Mô hình dữ liệu 2.0: 55 bảng, 6 nhóm theo luồng; thêm audit, outbox, idempotency, đề xuất tool Director, gợi ý SFX, gán người nói; cột trạng thái chương `media_status` |
| 1.8 | 2026-10-19 | Kiến trúc 2.0: ánh xạ luồng 6 bước ↔ module/queue/bảng; module theo M01–M10 + lớp platform; Scheduler, Media Processing Worker; điều phối Sinh tư liệu bằng BullMQ Flows; thành phần trình chỉnh sửa; ADR-15..19; thêm `c4-component-api`, `c4-component-editor` |
| 1.9 | 2026-10-20 | Bổ sung từ bản nháp `docs/`: tìm/lọc dự án, trạng thái dự án suy ra (UC-02.01); xem timeline truyện theo mạch/thời gian, thêm `chrono_index` (UC-04.07, UC-04.09); thay ảnh shot bằng ảnh tải lên, `edit_kind = UPLOAD`, endpoint `:upload`, mở rộng BR-14 (UC-05.10); vùng an toàn & lưới (UC-06.06); preset phụ đề (UC-06.08) ; chuẩn hóa tên use case theo quy cách mới (00-muc-luc §2) |
| 1.10 | 2026-10-20 | Đặc tả chi tiết **57 use case con** (include/extend) theo khung đầy đủ: tác nhân, tiền/hậu điều kiện, kích hoạt, truy vết, luồng chính và luồng thay thế / ngoại lệ |
| 1.11 | 2026-10-20 | Cập nhật 10 sơ đồ tuần tự, hoạt động và trạng thái theo đặc tả use case con (đăng nhập SSO, nhập / nhập lại, xung đột khi lưu, thuyết minh nguyên văn, trình chỉnh sửa & xuất, Director, sinh tư liệu, thanh toán, phủ kín văn bản); thêm `state-tool-proposal` |

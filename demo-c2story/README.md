# Demo C2Story Studio — Bộ tài liệu đặc tả để phát triển lại từ đầu

> **Phiên bản:** 1.16 · **Ngày:** 2026-10-20 · **Vai trò soạn thảo:** Business Analyst
> **Trạng thái:** Đã chốt phạm vi MVP và kế hoạch theo 4 vòng câu hỏi ([sổ quyết định](quyet-dinh.md))
> **Bối cảnh:** đồ án tốt nghiệp, nhóm 3 người, 7 tháng phát triển; MVP = hết P3; thử nghiệm bằng closed beta 10–20 người

## 1. Mục đích

Bộ tài liệu đặc tả hệ thống **AI Story Studio theo dự án (Project)**. Người dùng biến một truyện dài thành **video minh họa có thuyết minh nguyên văn**, theo luồng 6 bước:

```
1. Nhập truyện  →  2. Chia chương  →  3. AI dựng thế giới truyện
→  4. AI sinh tư liệu (ảnh + thuyết minh nguyên văn)
→  5. Chỉnh sửa video trên timeline (chuyển cảnh, nhạc nền, SFX, tinh chỉnh)
→  6. Xuất & tải video
```

Nhân vật và bối cảnh được giữ nhất quán xuyên suốt. Trong MVP, người dùng (Owner) làm từng bước với AI hỗ trợ ở mỗi bước. **AI Director** chạy tự động từ bước 2 đến bản nháp timeline là hướng phát triển sau MVP.

> **Nguyên tắc cốt lõi: Thuyết minh nguyên văn (Verbatim narration).** Audio của video đọc **toàn bộ** văn bản truyện, **đúng từng chữ, đúng thứ tự**. Không chỉnh sửa, không tóm tắt, không bỏ đoạn. AI chỉ được *minh họa* câu chuyện, không được *viết lại* nó. Xem BR-19..BR-23 ở [08](tai-lieu/08-quy-tac-nghiep-vu.md).

Chức năng tham chiếu module Projects của c2story.com. Tài liệu dùng để **phát triển lại từ đầu**: backend, API, cơ sở dữ liệu và tích hợp AI đều do nhóm tự thiết kế.

## 2. Phạm vi

**Trọng tâm:** Studio dự án, gồm quản lý dự án và cộng tác, bản thảo và chương, thế giới truyện, **sinh tư liệu** (storyboard tự động, ảnh, thuyết minh nguyên văn), **trình chỉnh sửa video timeline** (nhạc nền, SFX, chuyển cảnh, tinh chỉnh) và xuất video, AI Director.

**Không làm video bằng AI sinh video.** Video được dựng từ ảnh minh họa tĩnh với hiệu ứng chuyển động (Ken Burns), chuyển cảnh, phụ đề, nhạc nền và SFX trên trình chỉnh sửa timeline, rồi render bằng hạ tầng của hệ thống.

**Phụ trợ, chỉ ở mức Studio cần:**

| Phụ trợ | Vì sao cần |
|---|---|
| Tích hợp **SSO** (Keycloak tự dựng; **SSO Vbee** trước khi bảo vệ) | Định danh người dùng, danh sách mời beta, đồng ý xử lý dữ liệu. **Không tự phát triển** đăng ký, đăng nhập, đăng xuất, mật khẩu; chỉ tích hợp qua OIDC (hoặc OAuth 2.0 nếu Vbee chỉ hỗ trợ chuẩn này) |
| Thư viện tài sản cá nhân *(sau MVP)* | Tái sử dụng nhân vật giữa các dự án |
| Âm thanh | MVP: nhạc nền & SFX người dùng tải lên; sau MVP: thư viện CC0/CC-BY |
| Ví & thanh toán | Ví USD; giá = chi phí AI thực × 110%; tiền dùng thử $2; nạp tiền qua cổng ở chế độ sandbox |
| Quản trị tối thiểu | Bảng giá, mô hình AI, giọng (file seed); danh sách mời; trần chi tiêu AI $10/ngày |

**Đã lược bỏ** (không thiết kế ở phiên bản này): Explore/thư viện cộng đồng, Create nhanh (Auto-make), Remix (Continue/Rewrite), Chat nhân vật, Guide cộng đồng, bán sách và chia doanh thu cho tác giả, API công khai, Poster/Trailer cho sách tạo nhanh, Like/Share công khai, **video AI (image-to-video, Video Storyboard, Animated Book, chất lượng Basic/Enhance/Cinema)**, **AI viết lại văn bản truyện**, **sách tranh (Compile book, trình đọc, PDF)**.

## 3. Nguyên tắc "phát triển sạch" (clean-room)

| # | Nguyên tắc |
|---|---|
| CR-01 | **Không dùng bất kỳ API key, token, publishable key, endpoint hay CDN nào của c2story.com**, kể cả key Clerk công khai, `cdn.c2story.com` hay `/api/*` của họ. |
| CR-02 | Mọi dịch vụ ngoài (AI, thanh toán, email, lưu trữ) dùng **tài khoản và key do nhóm tự đăng ký**, cấu hình qua biến môi trường và quản lý bằng secret manager. |
| CR-03 | Không sao chép mã nguồn, hình ảnh, văn bản marketing, logo hay nội dung người dùng của c2story. Chỉ tham chiếu **hành vi chức năng**. |
| CR-04 | API được **thiết kế lại** theo REST và OpenAPI 3.1 (xem `06`). Không phụ thuộc hệ thống cũ. |
| CR-05 | Giá thao tác tính theo chi phí thực của nhà cung cấp AI của nhóm × 110%, lưu thành cấu hình; không sao chép bảng giá của hệ thống tham chiếu. |

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
├── quyet-dinh.md                 # Sổ quyết định (QĐ-xx) từ 4 vòng câu hỏi chốt kế hoạch
├── CLAUDE.md                     # Hướng dẫn cho Claude Code khi làm việc với bộ tài liệu
├── tai-lieu/                     # 13 tài liệu đặc tả (xem §6); schemas/ chứa JSON Schema
│   └── 03-dac-ta-use-case/       # Đặc tả 165 use case: mục lục + 10 file M01–M10
├── so-do/                        # Sơ đồ PlantUML của hệ thống mới (xem §7)
│   ├── 01-use-case/
│   │   └── phan-ra/              # Use case phân rã theo phân hệ M01–M10
│   ├── 02-du-lieu/               # Domain model, ERD đầy đủ + ERD theo phân hệ
│   ├── 03-kien-truc/             # C4 (context, container, component API/AI/editor), deployment, gói, lớp thiết kế
│   ├── 04-tuan-tu/               # Sơ đồ tuần tự
│   ├── 05-hoat-dong/             # Sơ đồ hoạt động
│   ├── 06-trang-thai/            # Sơ đồ trạng thái
│   ├── mvp/                      # Bản MVP của các sơ đồ có phần sau MVP (xem so-do/mvp/README.md)
│   └── tools/                    # split_erd.py (ERD theo phân hệ), gen_mvp.py (sơ đồ MVP + tô xám)
├── tools/gen_backlog.py          # Sinh 11-product-backlog.md từ đặc tả use case
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
| 08 | [Quy tắc nghiệp vụ, phân quyền & tính phí](tai-lieu/08-quy-tac-nghiep-vu.md) | — |
| 09 | [Kế hoạch phát triển & ma trận truy vết](tai-lieu/09-ke-hoach-phat-trien.md) | RTM |
| 10 | [Thuật ngữ](tai-lieu/10-thuat-ngu.md) | — |
| 11 | [Product backlog (nháp, sinh tự động)](tai-lieu/11-product-backlog.md) | User story + Gherkin |
| 12 | [Đặc tả kỹ thuật lõi](tai-lieu/12-dac-ta-ky-thuat-loi.md): tách câu, ánh xạ timestamp, `timeline_snapshot` ([JSON Schema](tai-lieu/schemas/timeline-snapshot.schema.json)) | JSON Schema 2020-12 |
| 13 | [Tích hợp hệ thống AI bên ngoài](tai-lieu/13-tich-hop-he-thong-ai.md): Gemini (LLM, ảnh), TTS tự host, port, hợp đồng dữ liệu, vòng đời lời gọi, lỗi, tiền, bảo mật, mock, eval (tổng hợp từ 05, 08, 09, 12) | — |
| — | [Sổ quyết định](quyet-dinh.md) | — |

## 7. Danh mục sơ đồ (`so-do/`)

| Thư mục | File |
|---|---|
| `01-use-case/` | `uc-tong-quan` (tổng quan), `uc-studio-chi-tiet` (Studio) |
| `01-use-case/phan-ra/` | `uc-m01-tich-hop-sso`, `uc-m02-du-an-cong-tac`, `uc-m03-ban-thao-chuong`, `uc-m04-the-gioi-truyen`, `uc-m05a-storyboard`, `uc-m05b-sinh-anh-thuyet-minh`, `uc-m06-trinh-chinh-sua-video`, `uc-m07-ai-director`, `uc-m08-thu-vien-tai-san`, `uc-m09-vi-thanh-toan`, `uc-m10-quan-tri`. Use case sau MVP tô nền xám |
| `02-du-lieu/` | `domain-class`, `erd` (đầy đủ); ERD theo phân hệ `erd-1-tai-khoan-vi`, `erd-2-du-an-ban-thao`, `erd-3-the-gioi-truyen`, `erd-4-sinh-tu-lieu`, `erd-5-trinh-chinh-sua-video`, `erd-6-director-job-ha-tang`. Các ERD con sinh tự động: chỉ sửa `erd.puml` rồi chạy `python3 so-do/tools/split_erd.py` |
| `03-kien-truc/` | `c4-context`, `c4-container`, `c4-component-api`, `c4-component-ai`, `c4-component-editor`, `deployment`; UML: `package-modules` (sơ đồ gói: module, platform, phụ thuộc), `class-job-vi` và `class-ai-gateway` (sơ đồ lớp mức thiết kế cho phần lõi) |
| `04-tuan-tu/` | Mức thiết kế (thành phần, phương thức, bảng), mỗi sơ đồ gộp nhiều use case: `seq-vong-doi-job` (khung chung cho mọi thao tác AI tốn phí, các sơ đồ khác tham chiếu bằng `ref`), `seq-dang-nhap-sso`, `seq-quan-ly-du-an`, `seq-import-chia-chuong`, `seq-doi-ranh-gioi-shot`, `seq-the-gioi-truyen`, `seq-tai-san-phong-cach`, `seq-storyboard-sinh-anh`, `seq-sinh-tu-lieu`, `seq-thuyet-minh-nguyen-van`, `seq-chinh-sua-xuat-video`, `seq-thanh-toan`, `seq-quan-tri`; sau MVP: `seq-director`, `seq-cong-tac-xung-dot`. Màu và chú giải dùng chung ở `_style-tuan-tu.iuml` (biến `$API`, `$WORKER`…); cột xếp theo tầng: người dùng → giao diện → API → dữ liệu → worker → AI Gateway → dịch vụ ngoài. Mọi UC MVP nằm trong ít nhất một sơ đồ tuần tự; use case nào nằm trong sơ đồ nào: cột Sơ đồ của RTM (09 §4) |
| `05-hoat-dong/` | `act-quy-trinh-project`, `act-giu-tru-tien`, `act-phu-kin-van-ban`; theo nhóm chức năng (mức nghiệp vụ, làn màu Người dùng / Hệ thống / Dịch vụ AI / bên ngoài, kiểu chung `_style-hoat-dong.iuml`): `act-m01-dang-nhap`, `act-m03-ban-thao-chuong`, `act-m04-the-gioi-truyen`, `act-m05-sinh-tu-lieu`, `act-m06-chinh-sua-xuat-video`, `act-m09-vi-thanh-toan`. M02, M10 chủ yếu thêm/sửa/xóa; M07, M08 sau MVP |
| `06-trang-thai/` | `state-job`, `state-chapter-media`, `state-narration-render`, `state-director-plan`, `state-tool-proposal`, `state-subscription` |
| `mvp/` | 43 sơ đồ phạm vi MVP: use case (tổng quan, Studio, 9 phân rã), ERD, mô hình miền, C4 (context, container, API, editor), deployment, sơ đồ gói và 2 sơ đồ lớp thiết kế (sinh tự động), 13 tuần tự (sinh tự động), quy trình và 6 hoạt động theo nhóm chức năng (sinh tự động), 2 trạng thái. Danh mục và cách cập nhật: [`so-do/mvp/README.md`](so-do/mvp/README.md) |

Render toàn bộ sơ đồ (cần Java và Graphviz), chạy trong `demo-c2story/`:

```bash
python3 so-do/tools/gen_mvp.py && python3 so-do/tools/split_erd.py   # sinh lại sơ đồ MVP, tô xám, ERD con
python3 tools/gen_backlog.py                                          # sinh lại product backlog
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
| 1.12 | 2026-10-20 | Áp toàn bộ 4 vòng câu hỏi chốt phạm vi và kế hoạch ([sổ quyết định](quyet-dinh.md)): **MVP = hết P3** cho một người dùng (Owner), cột **Giai đoạn** cho mọi FR và use case, thứ tự cắt giảm ✂1–✂5; **ví USD** thay credit (chi phí thực × 110%, giữ ước tính / trừ thực / hoàn dư, $2 dùng thử, Free / Đã nạp tiền, nạp tiền sandbox); closed beta: **danh sách mời**, **đồng ý xử lý dữ liệu**, **trần $10/ngày**; Keycloak → SSO Vbee (ADR-20); bỏ Fix a spot, AI nhạc/SFX, gợi ý SFX, credit hằng ngày; dời ranh giới shot sang Workspace (UC-03.02a); kiểm chứng thủ công (UC-05.18), WER từng shot sau MVP; đổi tốc độ clip thuyết minh 0,8–1,25×; quy tắc ký hiệu trình bày; kế hoạch 24 tuần + RTM có giai đoạn; product backlog sinh tự động; **26 sơ đồ MVP riêng** (`so-do/mvp/`) và tô xám phần sau MVP trong bộ đầy đủ |
| 1.13 | 2026-10-20 | Áp đánh giá PM vào kế hoạch (QĐ-90..99): mốc khung chạy đầu-cuối T6, đo vận tốc T8, spike editor/render T14; dời 9 UC từ P1 sang P2 (P1 49 · P2 21 story); thứ tự cắt giảm tầng 2 (✂6–✂10) và tầng 3; Tết 2027 và lịch thi; vai trò kèm người dự phòng; bảng rủi ro có ngưỡng kích hoạt và người phụ trách; quy tắc dự phòng P0; benchmark render staging; viết báo cáo dần |
| 1.14 | 2026-10-20 | Theo đánh giá kỹ sư phần mềm: thêm **12 — Đặc tả kỹ thuật lõi** (tách câu tiếng Việt `SentenceSegmenter` với 22 ca kiểm thử; `NormalizationMap` và thuật toán ánh xạ timestamp từ bản đọc về văn bản gốc, dựng phụ đề; hợp đồng `timeline_snapshot` + JSON Schema và ví dụ đã kiểm); **ADR-23** triển khai rút gọn cho MVP (một tiến trình worker, không outbox, bỏ worker Python khi TTS có timestamp, IC-08 chỉ ở service); **ADR-24** đổi tốc độ thuyết minh bằng file audio dẫn xuất để preview = render; **ADR-25** trần chi tiêu ngày bằng bộ đếm nguyên tử `daily_ai_budgets` (sửa race condition); 9 mã test mới |
| 1.15 | 2026-10-20 | Theo đánh giá back-end: **ADR-26** mọi offset văn bản theo UTF-16, bỏ `char_length()` khỏi IC-08, thêm ca kiểm thử có emoji; **ADR-27** Kysely + SQL tay; **ADR-28** semaphore Redis theo người dùng (thay BullMQ Pro groups); **ADR-29** bảng `jobs` là nguồn sự thật, nhận việc an toàn khi giao lại, chi phí lần thử lỗi do hệ thống chịu (WR-09), mở khóa chương trong giao dịch kết thúc job và reconciler; SSE MVP không phát lại sự kiện; OpenAPI viết trước (80/119 endpoint thuộc MVP); dời danh sách mời và đồng ý dữ liệu sang P1; PO tách khỏi back-end; nền tảng kiểm thử (09 §2.3) |
| 1.16 | 2026-10-20 | Theo đánh giá AI Engineering (QĐ-110..118): cách đo cho các ngưỡng AI ở P0 (rubric và 2 người chấm cho ảnh nhất quán; WER theo âm tiết trừ WER nền của ASR, danh sách khó; tỷ lệ ảnh bị từ chối; sai lệch timestamp); 4 mã test mới `EVAL-refusal-rate`, `EVAL-asset-extraction`, `EVAL-alignment`, `EVAL-cost-per-minute`; mật độ ảnh mặc định 3 ảnh/phút và chi phí/phút đo ở M0; làm rõ BR-18 (được sửa brief, không sửa văn bản truyện); rủi ro R-21; **nạp tiền sandbox lên ✂1**, đánh số lại tầng 1 (✂1–✂6); ablation cho báo cáo trong UAT |
| 1.17 | 2026-10-20 | Thêm **13 — Tích hợp hệ thống AI bên ngoài**: tổng hợp port, danh mục tác vụ AI, hợp đồng đầu ra LLM/ảnh/TTS, vòng đời lời gọi tốn phí, ranh giới tin cậy, phân loại lỗi, giám sát, giới hạn đồng thời, mock và eval; 8 đề xuất mở ĐX-AI-01..08 (chưa có QĐ) |
| 1.18 | 2026-10-20 | Chọn lại nhà cung cấp AI và duyệt ĐX-AI-01..08 (QĐ-119..131): **LLM và ảnh dùng Google Gemini**; **TTS tự host trong MVP** (TTS Server trên GPU, **ADR-30**), Vbee AIVoice sau MVP; Alignment Worker WhisperX bắt buộc; chi phí TTS theo giây GPU; fallback chỉ cho LLM; timeout theo loại lời gọi; nghe thử phát âm đồng bộ; `BENCH-tts`; rủi ro R-22, R-23 |
| 1.19 | 2026-10-20 | **Vẽ lại sơ đồ tuần tự ở mức thiết kế** (thành phần, phương thức, bảng; mỗi sơ đồ gộp nhiều use case): thêm `seq-vong-doi-job` (khung chung cho thao tác AI tốn phí, tham chiếu bằng `ref`), `seq-the-gioi-truyen` (M04), `seq-doi-ranh-gioi-shot` (UC-03.02a); vẽ lại 7 sơ đồ còn lại theo ADR-23..30 và QĐ-119..131; bản `-mvp` của sơ đồ tuần tự sinh tự động bằng `gen_mvp.py`; bổ sung tên sơ đồ vào Truy vết của use case và cột Sơ đồ của RTM |
| 1.20 | 2026-10-20 | **Đồng bộ thiết kế giữa tài liệu và sơ đồ tuần tự:** 05 thêm §5.1 danh mục thành phần theo module và handler theo loại job; bảng §3 đủ job (`REWRITE_SHOT`, `EDIT_IMAGE`, `PROCESS_AUDIO_RATE`, `PRONUNCIATION_PREVIEW`); bỏ queue `export` không tồn tại (05, C4, deployment); danh sách sự kiện SSE thống nhất với 06 §3, tách sự kiện nội bộ `storyboard.current-changed`. 06: `/me:consent` không còn tạo ví (ví tạo lúc JIT, UC-01.01b), `media:quote` nhận `only`/`parts`, `GET /jobs` có `result`, payload `job.updated`, `chapter.updated`, `chapter.media-ready`. 08: ánh xạ job miễn phí `PROCESS_AUDIO_*`, `EXPORT_ZIP`. 13: nghe thử vẫn ghi `jobs`. BRD BP-00 và `act-quy-trinh-project` sửa thứ tự JIT → đồng ý. Sơ đồ tuần tự sửa đường dẫn, payload theo 06 |
| 1.21 | 2026-10-20 | **Rà soát lần 2 (02, 04, 07, 10, 12, M07/M08/M10, C4, trạng thái job):** bỏ queue `export` ở NFR-SCAL-02; outbox ghi rõ sau MVP ở 05, 07, 10 và C4 (bản MVP bỏ hẳn); offset storyboard theo code unit UTF-16; từ điển phát âm MVP chỉ `ALIAS`; render engine = Remotion + FFmpeg; 04 thêm ghi chú `jobs.type`, job miễn phí, cache audio dẫn xuất và thời hạn giữ; 08 ánh xạ `REDIRECT_CHAPTER`; UC-10.07a bỏ trạng thái job không tồn tại; UC-10.06 dùng `PROCESS_AUDIO_UPLOAD` và `/admin/audio-assets`; `state-job` thêm hủy render đang chạy; 10 thêm 5 thuật ngữ thiết kế |
| 1.22 | 2026-10-20 | **Rà soát kỹ thuật, bỏ phần làm quá mức cho MVP** (QĐ-132..138): bỏ semaphore theo người dùng, circuit breaker, `ModerationFilter` riêng, `RetryPolicy` trong gateway (thử lại một tầng ở mức job); chỉ job gốc giữ/quyết toán tiền, job cha chờ con không bị coi là treo; nghe thử phát âm miễn phí; render một lượt Remotion; bỏ leader lock Scheduler, hàng đợi offline của `OpsBatcher`, sự kiện `media.progress`; sửa `target_shot_seconds` 20 s, NFR-PERF-01/08; `IT-user-concurrency` thay bằng `IT-flow-settlement` |
| 1.23 | 2026-10-20 | Theo PO (QĐ-139..141): giữ giới hạn Free 10 phút/tháng (một chương thường ~10 phút); **bỏ tốc độ từng clip thuyết minh**, chỉ còn tốc độ đọc của dự án áp ở bước TTS (bỏ ADR-24, IC-17, `PROCESS_AUDIO_RATE`, `playback_rate`, `derived_media_id`); **MVP không có timeline cả dự án**, thêm xuất cả dự án tự động (FR-EDT-28, `POST /projects/{pid}/renders`, `renders.scope`); `timeline_snapshot` lên `schemaVersion` 2 (bỏ `playbackRate`, thêm `sourceTimelines`, SNP-T08); mô hình dữ liệu 2.2; test `IT-project-render` thay `UT-narration-speed`, `IT-narration-rate-variant` |
| 1.24 | 2026-10-20 | Đồng bộ sơ đồ UML với tài liệu sau QĐ-132..141: `target_shot_seconds` 20 s trong seq-sinh-tu-lieu; bước `atempo` khi model TTS không hỗ trợ tốc độ (seq-thuyet-minh-nguyen-van); chu kỳ reconciler 1 phút / 5 phút và job cha chờ con (seq-vong-doi-job, act-giu-tru-tien); OpsBatcher không hàng đợi offline, render một lượt, xuất cả dự án (C4 editor, quy trình project, trạng thái render, Studio use case); `Render.scope` trong domain class; OpenTelemetry ghi sau MVP (deployment); bỏ "tốc độ đọc"/"đổi tốc độ audio" còn sót ở bản MVP. **Đủ sơ đồ tuần tự cho MVP:** thêm `seq-quan-ly-du-an` (UC-01.03..01.05, 02.01, 02.04, 02.05, 02.09, 03.01), `seq-tai-san-phong-cach` (UC-04.02, 04.05, 04.06, 04.10), `seq-quan-tri` (M10 qua seed/CLI); 5 sơ đồ trước đây "dùng chung" nay có đánh dấu MVP và sinh bản `-mvp`; `so-do/mvp/04-tuan-tu/` có 13 sơ đồ, phủ 104/104 UC MVP; cập nhật Truy vết UC, RTM, 05 §4 |
| 1.25 | 2026-10-20 | Đồng bộ tên nhóm chức năng M01–M10 theo tiêu đề đặc tả use case (`03/m*.md`) giữa bản MVP và bản đầy đủ: sơ đồ use case tổng quan, Studio chi tiết, phân rã M05a/M05b, M08; 02 §1.3 và §2.5, 06 §2.2 và §2.5, 09 §4.5 |
| 1.26 | 2026-10-20 | Ngoại hình theo giai đoạn truyện (QĐ-142): ghi rõ sửa facts/mô tả tài sản là ghi đè, ảnh đã sinh không đổi, ảnh sinh lại ở chương trước dùng giá trị mới (UC-04.02e bước 4, 4b; BR-08 thêm mô tả + facts cuối thứ tự); MVP tạo tài sản riêng cho từng giai đoạn; sau MVP thêm FR-WLD-13, bảng `story_asset_variants`, lớp `AssetVariant` (ERD, sơ đồ lớp miền) |
| 1.27 | 2026-10-20 | Quan hệ nhân vật theo giai đoạn (QĐ-143): mỗi dòng `relationships` là một giai đoạn từ `from_chapter_id`, thêm IC-19; `STORY_META` hợp nhất theo thứ tự chương; đồ thị quan hệ có thanh chọn chương (UC-04.08), API `?atChapter`; prompt storyboard chỉ nhận quan hệ hiệu lực (05 §7.4, 13); test `UT-relationship-at-chapter`; cập nhật seq-the-gioi-truyen |
| 1.28 | 2026-10-20 | Sơ đồ tuần tự có màu theo tầng kiến trúc (người dùng, giao diện, API, dữ liệu, worker, AI Gateway, dịch vụ ngoài) và chú giải, dùng chung file `so-do/04-tuan-tu/_style-tuan-tu.iuml`; lifeline nhạt, khung alt/opt chỉ tô nhãn; sắp lại cột theo tầng để giảm số lifeline mũi tên phải băng qua (vd. `seq-vong-doi-job` 158 → 120, `seq-quan-tri` 50 → 26) |
| 1.29 | 2026-10-20 | Thêm **sơ đồ gói** `package-modules` và **sơ đồ lớp mức thiết kế** `class-job-vi` (JobService, BudgetGuard, WalletPort, JobRunner, AbstractJobHandler, Reconciler, WalletService) và `class-ai-gateway` (ProviderRouter, Port/Adapter, ContextBuilder, PromptCompiler, CoverageValidator, SpeechNormalizer…), kèm bản MVP sinh tự động; QĐ-144 đảo phụ thuộc `platform/jobs` → `billing` qua `WalletPort`, chỉ cho phép hai cặp phụ thuộc hai chiều; 05 §5, §5.1, §7 dẫn sơ đồ |
| 1.30 | 2026-10-20 | Thêm **6 sơ đồ hoạt động theo nhóm chức năng** (UML, mức nghiệp vụ): `act-m01-dang-nhap`, `act-m03-ban-thao-chuong`, `act-m04-the-gioi-truyen`, `act-m05-sinh-tu-lieu`, `act-m06-chinh-sua-xuat-video`, `act-m09-vi-thanh-toan`; làn màu theo tầng, hành động tô màu theo loại (lỗi, tiền, gọi AI, thành công) có chú giải; bản MVP sinh tự động; gắn vào Truy vết của 53 UC và cột Sơ đồ của RTM |
| 1.31 | 2026-10-21 | Thêm thư mục **`so-do/07-tich-hop-ai/`** gồm 9 sơ đồ tích hợp AI bên ngoài theo 13 (góc nhìn kỹ sư phần mềm / AI): tuần tự `seq-ai-goi-llm`, `seq-ai-sinh-anh`, `seq-ai-tts-tu-host` (MVP), `seq-ai-tts-vbee` (sau MVP), `seq-ai-danh-gia-provider`; hoạt động `act-ai-goi-provider`, `act-ai-chon-provider`; trạng thái `state-ai-loi-goi`, `state-ai-dau-ra`; 13 §2.3, §4.4, §13 dẫn sơ đồ |
| 1.32 | 2026-10-21 | **QĐ-145** đổi provider TTS chỉ bằng adapter + dữ liệu seed: `TtsPort.speak` nhận `NormalizedSpeech`; thêm `ai_models.unit`, định nghĩa `ai_models.capabilities` (phoneme, speedParam, timestampsTrusted…); hợp đồng đầu ra TTS và test `IT-tts-port-contract`; 13 §4.5 các bước chuyển sang Vbee AIVoice; cập nhật 04, 05, 08, 09, 12, UC-05.12/05.13/05.13b, `class-ai-gateway`, `seq-thuyet-minh-nguyen-van`, `seq-ai-tts-*` |
| 1.33 | 2026-10-21 | **10 Thuật ngữ** chia 11 nhóm, bổ sung khoảng 130 thuật ngữ chuyên ngành đang dùng trong 01–13 nhưng chưa định nghĩa (quy ước tài liệu, OIDC/bảo mật, khóa lạc quan, SSML/STT/aligner, editor/render, AI provider/eval, thanh toán, hạ tầng job, kiểm thử) |

# Sổ quyết định

> Ghi các quyết định đã chốt của nhóm (ngày, nội dung, lý do). Không cần duyệt riêng; khi bất đồng, PO quyết định cuối (QĐ-50).
> Nguồn: 4 vòng câu hỏi chốt phạm vi và kế hoạch ngày 2026-10-20 (file câu hỏi đã được xóa sau khi chốt; nội dung trả lời được ghi đầy đủ ở đây). Mã ở cột Nguồn: **A/B/C/D…** = vòng 1, **V2 / V3 / V4 + số câu** = vòng 2–4.
> Mọi quyết định dưới đây chốt ngày **2026-10-20** và đã được áp vào bộ tài liệu phiên bản 1.12; mục 7 áp ở phiên bản 1.13; mục 8 áp ở phiên bản 1.15; mục 9 áp ở phiên bản 1.16; mục 11 áp ở phiên bản 1.18; mục 12 áp ở phiên bản 1.22.

## 1. Bối cảnh, năng lực, lộ trình

| Mã | Quyết định | Nguồn | Tài liệu |
|---|---|---|---|
| QĐ-01 | Đây là **đồ án tốt nghiệp**: 7 tháng phát triển, sau đó 2 tháng viết báo cáo và bảo vệ. 7 tháng đã gồm 20% dự phòng, nên chỉ lập kế hoạch cho khoảng **24 tuần** làm việc | C1, C4, V2 1.4 | 09 §1 |
| QĐ-02 | Nhóm 3 người, đều full-stack, mỗi người 20 giờ/tuần, có Coding Agent hỗ trợ. Năng lực ≈ 36 tuần-người (54–72 nếu Coding Agent tăng năng suất 1,5–2 lần) | C2, V3 4 | 09 §1 |
| QĐ-03 | **MVP = hết P3.** Lộ trình: P0 4 tuần, P1–P3 20 tuần | B8, V3 4 | 02, 09 §1 |
| QĐ-04 | Thu gọn MVP về luồng 6 bước cho **một người dùng (Owner)**; giữ thêm Timeline truyện, Relationships và Visual Rules ở P1 | V2 1.1, 1.2, A4, B6 | 01 §4, 02, 09 |
| QĐ-05 | **Thứ tự cắt giảm** khi trễ: (1) Map → (2) phụ đề preset và chuyển cảnh nâng cao → (3) Relationships → (4) Timeline truyện → (5) từ điển phát âm. AI Director đã nằm ngoài MVP | V3 4, V4 4 | 09 §1.3 |
| QĐ-06 | **Mốc kiểm tra cuối P1:** tiến độ dưới 80% kế hoạch thì áp thứ tự cắt giảm | V3 4 | 09 §1.4 |
| QĐ-07 | Tiêu chí kết thúc giai đoạn: demo được luồng chính của giai đoạn, test trong RTM của các UC thuộc giai đoạn đều pass, không còn lỗi mức High, PO ký nghiệm thu. Riêng P0: ảnh sai ngoại hình ≤ 10%, TTS vi/en WER ≤ 3% | C3 | 09 §1.5 |

## 2. Cách làm việc

| Mã | Quyết định | Nguồn | Tài liệu |
|---|---|---|---|
| QĐ-10 | Sprint 1 tuần, ước lượng bằng story point, planning poker cả nhóm, quản lý trên GitHub Projects | D1, D3 | 09 §2 |
| QĐ-11 | BA soạn nháp backlog; **story chi tiết (kèm Gherkin) chỉ cho UC thuộc MVP**, mỗi UC con một story. UC sau MVP gom thành epic, mỗi epic một dòng | D2, V3 8 | 11 |
| QĐ-12 | Gherkin **sinh tự động** từ luồng chính và luồng thay thế trong đặc tả UC; nhóm chỉ rà lại | V2 1.3 | 11, `tools/gen_backlog.py` |
| QĐ-13 | Kiểm soát thay đổi nới lỏng: ghi quyết định vào file này; thay đổi đặc tả commit kèm mô tả; BA cập nhật RTM và lịch sử phiên bản **cuối mỗi sprint** | C8, V2 11 | README, 09 |

## 3. Tài khoản, SSO, dữ liệu cá nhân

| Mã | Quyết định | Nguồn | Tài liệu |
|---|---|---|---|
| QĐ-20 | Dùng **Keycloak tự dựng** làm SSO từ P0; thiết kế OIDC giữ nguyên | V2 5.2 | 05, 09 |
| QĐ-21 | **Bắt buộc tích hợp SSO Vbee trước khi bảo vệ**, làm ở cuối MVP (P3). Hạn chót có tài liệu từ Vbee: **hết tháng thứ 2** | V3 6, V2 5.1 | 01 A-03, 02 FR-AUTH-13, 09 |
| QĐ-22 | Quá hạn tài liệu Vbee: **giữ Keycloak cho bản bảo vệ**, báo cáo ghi "đã thiết kế adapter OIDC, chờ đối tác cung cấp thông tin"; không để việc này chặn các phần khác | V4 2 | 09 §1.6 |
| QĐ-23 | Nếu Vbee chỉ có OAuth 2.0 (không OIDC): chấp nhận làm thêm 1–2 tuần-người (userinfo, không back-channel logout), lấy bằng thứ tự cắt giảm QĐ-05 | V4 2 | 05 ADR-20, 09 §1.6 |
| QĐ-24 | Phát hiện tài khoản bị khóa/xóa khi đăng nhập hoặc gia hạn phiên (≤ 15 phút); không có webhook/SCIM | V2 5.3 | FR-AUTH-06, 10 |
| QĐ-25 | **Closed beta tắt tự đăng ký:** ứng dụng có **danh sách email được mời** do Admin quản lý. Email không có trong danh sách: hiện "Bạn chưa được mời tham gia beta", không tạo hồ sơ, không tặng tiền dùng thử. Bỏ danh sách khi mở rộng | V3 2, V4 1 | BR-30, FR-AUTH-11, UC-01.01b, UC-10.11 |
| QĐ-26 | Màn hình **đồng ý xử lý dữ liệu cá nhân** ở lần đăng nhập đầu: dữ liệu thu thập, mục đích (đồ án), thời hạn xóa sau khi bảo vệ; lưu thời điểm đồng ý (Nghị định 13/2023) | V3 7 | BR-31, FR-AUTH-12, UC-01.01d |
| QĐ-27 | Không cần ToS, không có quy trình gỡ nội dung khi khiếu nại; người dùng tự chịu trách nhiệm nội dung tải lên. Admin vẫn xóa được file qua quyền quản trị dữ liệu chung | A7, V2 7, V3 ghi chú | BR-26 |

## 4. Tiền, giá, giới hạn

| Mã | Quyết định | Nguồn | Tài liệu |
|---|---|---|---|
| QĐ-30 | Bỏ khái niệm credit. Đơn vị tính là **USD**, lưu chính xác tới 1/1.000.000 USD (micro-USD); hiển thị USD hoặc quy đổi VND. Nạp tiền qua cổng thanh toán ở **chế độ sandbox** | A1, A2, V2 2.1 | 08 §3–4, 04, 06 |
| QĐ-31 | Giá = **chi phí thực của provider × 110%**, áp cho mọi thao tác gọi AI bên ngoài (LLM, sinh ảnh, TTS) | A1, V2 2.2 | BR-01, 08 §3 |
| QĐ-32 | Báo giá: hiện **giá ước tính tối đa** (theo độ dài đầu vào và giới hạn token đầu ra) → **giữ** đúng số đó → khi xong **trừ** chi phí thực × 110% và **hoàn** phần dư | V2 2.3 | BR-02 |
| QĐ-33 | Không giới hạn tần suất về **tính phí**, nhưng giữ giới hạn **kỹ thuật**: ≤ 30 yêu cầu LLM/phút/người | A1, V2 2.4 | BR-32, 06 §1 |
| QĐ-34 | Render chạy trên hạ tầng của nhóm, **miễn phí** trong giới hạn gói | V2 2.2 | 08 §3 |
| QĐ-35 | MVP chỉ có hai trạng thái tài khoản: **Free** và **Đã nạp tiền**. Gói đăng ký tháng/năm để sau MVP | V2 2.6 | BR-27, 08 §3.3 |
| QĐ-36 | Gói Free: 1 dự án, 3 chương, 3 lần render/tháng, tổng 10 phút video/tháng, 720p, watermark gồm các đường kẻ kèm logo. Tắt watermark khi đã nạp tiền rồi render lại | A2 | BR-27, FR-BIL-12 |
| QĐ-37 | Tặng **$2 dùng thử một lần** khi tạo hồ sơ (đủ khoảng 1 chương). Bỏ daily claim (FR-BIL-07, UC-09.07) | V2 2.5 | BR-28 |
| QĐ-38 | "Đã nạp tiền" chỉ bật khi **tổng nạp tiền thật > 0**. Tiền tặng và tiền nạp là hai loại bút toán khác nhau trong sổ cái | V3 1 | BR-27, BR-28, 04 |
| QĐ-39 | **Trần chi tiêu AI toàn hệ thống: $10/ngày** trong closed beta. Vượt trần thì tạm dừng job mới và báo Admin | V3 2, V4 3 | BR-29, FR-ADM-07 |
| QĐ-40 | Ngân sách AI do PO trả: P0 **$200**; P1–P3 **$50/tháng** (dev và CI dùng mock adapter, chỉ gọi provider thật khi demo và E2E hằng tuần); UAT **$200** | V2 10, V3 5, V2 9.1 | 07 NFR-COST, 09 §1.7 |
| QĐ-41 | Hạ tầng: ưu đãi sinh viên (GitHub Student Developer Pack, Azure for Students); dev chạy docker-compose trên máy cá nhân | V2 10 | 05 §10 |
| QĐ-42 | **Sau MVP** (ghi lại để không mất): Editor tiêu ví Owner không giới hạn; ví Owner không đủ thì Editor trả bằng ví mình; Editor không thấy và không nạp vào ví Owner; Owner được thông báo và có báo cáo chi tiêu theo thành viên; Owner bị khóa thì Editor không làm được; Owner hạ gói thì Editor vẫn làm và tự trả | A3, V2 6 | BR-03 |

## 5. Phạm vi chức năng

| Mã | Quyết định | Nguồn | Tài liệu |
|---|---|---|---|
| QĐ-50 | Quy trình ra quyết định: họp chốt cả nhóm; bất đồng thì PO quyết định cuối | C6, V2 11 | 09 §2 |
| QĐ-51 | Bỏ hẳn "Fix a spot" (inpainting): xóa UC-05.10b, `edit_kind = INPAINT`, `mask_media_id`, tham số `mask`, phần "chỉnh ảnh theo mask" trong A-01 | B3 | 01, 02, 03-M05, 04, 05, 06 |
| QĐ-52 | Dời ranh giới shot làm ở **Workspace (M03)**: hiện vạch ranh giới shot khi chương đã có storyboard, kéo vạch theo câu. Sau khi dời, AI viết lại brief của 2 shot bị ảnh hưởng (có phí, báo giá và chờ xác nhận). Bỏ nút ◀ ▶ trong storyboard; tách, gộp, xóa shot vẫn ở storyboard | B4, V2 8 | FR-BOK-01b, UC-03.02a, BR-33 |
| QĐ-53 | *(Thay bằng QĐ-140)* Cho đổi tốc độ clip thuyết minh trong khoảng **0,8×–1,25×** (giữ cao độ, phụ đề co giãn theo) | B5 | BR-24, FR-EDT-04, UC-06.02 |
| QĐ-54 | Kiểm chứng lời đọc thủ công là M: mỗi shot có "Nghe" và "Đánh dấu cần sinh lại", **không bắt buộc** nghe hết mới được xuất. Kiểm chứng ASR từng shot (WER, `NEEDS_REVIEW`, chấp nhận thủ công) là S, sau MVP. WER ≤ 3% bảo đảm ở **khâu chọn provider** (`EVAL-wer-golden`, P0) | B1, V2 3 | BR-11, BR-23, FR-NAR-07, 08 |
| QĐ-55 | BR-23 nới thành: xuất được khi độ phủ 100%, mọi shot có ảnh `DONE` và thuyết minh `DONE`, không clip nào `OUTDATED` | V2 3 | BR-23, FR-EDT-22 |
| QĐ-56 | Ký hiệu trình bày: **đọc chữ, bỏ ký hiệu** (`*Bố*` đọc "Bố"); phụ đề **hiện nguyên** `*Bố*`. Dòng phân cách `---` không đọc (lặng 0,5 s) và không có phụ đề. Danh sách mặc định toàn hệ thống, mỗi dự án bật/tắt từng mẫu | A5, V2 4.1–4.3, V3 ghi chú | BR-19, BR-22, 08 §6 |
| QĐ-57 | Bỏ AI sinh nhạc/SFX (FR-EDT-16) và gợi ý SFX theo đoạn văn (UC-06.11c) | A7, V2 7 | 02, 03-M06, 04, 05, 06 |
| QĐ-58 | MVP chỉ cho **tải nhạc/SFX lên** (≤ 100 MB, ≤ 15 phút, không cần ô cam kết). Sau MVP nạp sẵn bộ CC0/CC-BY từ Pixabay/Freesound, nhạc CC-BY tự sinh dòng ghi công | A7, B2, V2 7 | FR-EDT-12, FR-EDT-27, BR-26 |
| QĐ-59 | Tách FR-WLD-05: gỡ tài sản khỏi dự án là M (FR-WLD-05); thư viện là S (FR-WLD-12) | B7 | 02 |
| QĐ-60 | Lời thoại một giọng kể trong MVP; đa giọng sau. Ngôn ngữ thuyết minh lúc ra mắt: tiếng Việt và tiếng Anh. Tiêu đề chương không đọc | 09 §6 câu 5–7 | 02 |
| QĐ-61 | Giữ **Map** (UC-02.09) trong MVP nhưng ở **đầu** thứ tự cắt giảm | V4 4 | 02, 09 |
| QĐ-62 | ~~Đưa **Vbee AIVoice** vào danh sách provider TTS so sánh ở P0~~ (thay bằng QĐ-121: Vbee AIVoice sau MVP) | V3 6 | 05 §7.3, 09 |

## 6. Kiểm thử và UAT

| Mã | Quyết định | Nguồn | Tài liệu |
|---|---|---|---|
| QĐ-70 | Golden set do nhóm chuẩn bị: 5–10 chương từ tác phẩm hết thời hạn bảo hộ (Nam Cao, Vũ Trọng Phụng, Ngô Tất Tố…) cho tiếng Việt, Project Gutenberg cho tiếng Anh, cộng 1–2 chương nhóm tự viết có tên riêng, số và từ mượn. Truyện người dùng đưa vào hệ thống do người dùng chịu trách nhiệm | C7, V2 9.2, V3 3 | 07 NFR-MNT-06, 09 |
| QĐ-71 | UAT đợt 1: **closed beta 10–20 người** được mời riêng, có phiếu khảo sát, khoảng 3 tuần. Đợt 2 mở rộng nếu còn thời gian | C7, V2 9.1 | 09 §1.8 |

## 7. Điều chỉnh kế hoạch theo đánh giá PM (2026-10-20)

Nguồn: đánh giá kế hoạch với vai trò Project Manager, nhóm đồng ý áp dụng ngày 2026-10-20. Chi tiết ở [09 §1–§2, §5](tai-lieu/09-ke-hoach-phat-trien.md).

| Mã | Quyết định | Tài liệu |
|---|---|---|
| QĐ-90 | Làm theo nguyên tắc **rủi ro trước**: mốc **M1 khung chạy đầu-cuối** ở T6 (import → storyboard → ảnh → TTS → MP4 có phụ đề, chưa cần editor) | 09 §1.2 |
| QĐ-91 | Thêm **thứ tự cắt giảm tầng 2** (✂6 nạp tiền sandbox → CLI cộng tiền; ✂7 giới hạn Free + watermark; ✂8 dời ranh giới shot ở Workspace; ✂9 preview thời gian thực → render nháp; ✂10 undo/redo đầy đủ, nhiều track, Ken Burns nhiều pha) và **tầng 3 kịch bản tối thiểu** (bỏ editor thủ công, cần PO duyệt) để tổng phần cắt được xấp xỉ khoảng hở xấu nhất 27 tuần-người | 09 §1.3, 02 cột GĐ |
| QĐ-92 | **Spike editor/render** trong P2, mốc **M3** ở T14 (preview và render lệch ≤ 1 khung hình); không đạt thì kích hoạt ✂9 trước P3 | 09 §1.2 |
| QĐ-93 | Cân lại khối lượng: dời 9 use case từ P1 sang P2 (UC-01.03, 01.05, 03.01a, 03.01b, 04.07, 04.08, 04.09, 09.05, 10.12). P1 rút còn T5–T11, P2 thành T12–T16. Thay vị trí P1 của Timeline truyện và Relationships đã chốt ở QĐ-04 | 03, 02, 09 |
| QĐ-94 | Mốc **M2 đo vận tốc ở T8**: ước lượng story point toàn bộ backlog MVP và dự báo ngày xong; kiểm tra 80% vẫn ở cuối P1 và P2 | 09 §1.4 |
| QĐ-95 | Tính **Tết 2027 (T15–T16, 50% năng lực)** và lịch thi của từng thành viên vào kế hoạch; dự phòng thực còn 2 tuần | 09 §1.1, §1.9 |
| QĐ-96 | Gán **vai trò** (PO, backend & AI, frontend & editor, DevOps & chất lượng, BA) kèm người dự phòng; bảng rủi ro có xác suất, tác động, ngưỡng kích hoạt, người phụ trách | 09 §2.1, §5 |
| QĐ-97 | **Quy tắc dự phòng P0** khi không provider nào đạt ngưỡng: ảnh ≤ 15%, TTS ≤ 5% (khi đó từ điển phát âm thoát khỏi thứ tự cắt giảm) | 09 §1.5 |
| QĐ-98 | **Benchmark render trên máy staging ở P0** để chọn cấu hình; ngưỡng MVP 1 phút 720p ≤ 2 phút; NFR-PERF-10 thành mục tiêu sau MVP | 09 §1.5, §1.7; 07 |
| QĐ-99 | **Viết báo cáo đồ án dần** theo từng giai đoạn; nghi thức sprint gọn (≤ 10% thời gian); công viết test nằm trong story point | 09 §1.10, §2 |

## 8. Điều chỉnh theo đánh giá back-end (2026-10-20)

| Mã | Quyết định | Tài liệu |
|---|---|---|
| QĐ-100 | Dời **danh sách mời** (UC-10.11) và **màn hình đồng ý dữ liệu** (UC-01.01d) từ P0 sang P1 để giảm tải back-end ở P0; closed beta bắt đầu T25 nên không ảnh hưởng. P0 chốt ADR-26..29 ở tuần 1 | 09 §1.2, 02, 03, 08 |
| QĐ-101 | PO / BA **không giữ vai trò back-end**; back-end & AI giao cho một thành viên riêng | 09 §2.1 |
| QĐ-102 | Nền tảng kiểm thử: Vitest + fast-check, Testcontainers, fixture ghi từ provider thật, Playwright, OpenAPI viết trước so trong CI | 09 §2.3, 06 §1.2 |

Các quyết định kỹ thuật kèm theo ghi ở 05 §9: ADR-26 (offset UTF-16), ADR-27 (Kysely), ADR-28 (semaphore theo người dùng), ADR-29 (bảng `jobs` là nguồn sự thật, chi phí lần thử lỗi do hệ thống chịu).

## 9. Điều chỉnh theo đánh giá AI Engineering (2026-10-20)

Nguồn: đánh giá kế hoạch với vai trò AI Engineer. Ý chính: các ngưỡng chất lượng AI đã có số nhưng chưa có cách đo; mô hình chi phí dựa vào mật độ ảnh thấp. Chi tiết ở [09 §1.5](tai-lieu/09-ke-hoach-phat-trien.md). Nhóm duyệt ngày 2026-10-20, kể cả việc QĐ-116 thay thứ tự cắt giảm của QĐ-05, QĐ-61. Các ngưỡng số trong QĐ-110..117 là **ngưỡng tạm**, hiệu chỉnh ở M0 theo số liệu PoC (ghi QĐ mới nếu đổi).

| Mã | Quyết định | Tài liệu |
|---|---|---|
| QĐ-110 | **Giao thức chấm `EVAL-consistency`:** ≥ 150 shot có nhân vật trên golden set cho mỗi provider ảnh. Rubric 4 thuộc tính so với ảnh tham chiếu: khuôn mặt, tóc, trang phục, tuổi/vóc dáng. Shot "sai ngoại hình" khi có ít nhất một nhân vật lệch một thuộc tính. 2 người chấm độc lập, ghi Cohen's κ; κ < 0,6 thì sửa rubric và chấm lại; bất đồng do người thứ ba (PO) quyết. Báo cáo tỷ lệ kèm khoảng tin cậy 95% (Wilson), **tách shot 1 nhân vật và shot ≥ 2 nhân vật**. Ngưỡng ≤ 10% / 15% giữ nguyên, áp cho tỷ lệ chung | 09 §1.5, §4.13; 01 BO-02 |
| QĐ-111 | **Cách đo WER:** tính trên âm tiết (token tách bằng khoảng trắng); hai phía chuẩn hóa NFC, chữ thường, bỏ dấu câu, đọc số theo đúng quy tắc của `SpeechNormalizer`, giữ dấu thanh. Đo **WER nền** của ASR trên bản ghi giọng người (tiếng Việt: nhóm tự đọc khoảng 20 phút trên golden set; tiếng Anh: bản LibriVox của chương Gutenberg). Ngưỡng ≤ 3% áp cho **WER hiệu chỉnh = WER(TTS) − WER nền**. Thêm **danh sách khó** (khoảng 100 tên riêng, từ Hán Việt, số, từ mượn) chấm bằng tai: đọc đúng ≥ 95% | 09 §1.5; 05 §7; 07 NFR-INT-03; 01 BO-04 |
| QĐ-112 | **Mật độ ảnh là tham số sản phẩm**, chốt ở P0: mặc định khoảng **3 ảnh/phút** (một ảnh khoảng 20 s, khớp cảnh báo ảnh > 30 s ở R-08), đặt trong prompt template storyboard. M0 phải có **chi phí AI/phút video đo thật** ở mật độ đã chốt. Vượt $0,15/phút (BO-06) thì PO chọn một trong ba: giảm mật độ (không thấp hơn 2 ảnh/phút), đổi provider rẻ hơn, hoặc nâng BO-06; đồng thời kiểm lại $2 dùng thử còn đủ 1 chương không | 09 §1.5; 08 §3.2; 01 BO-06 |
| QĐ-113 | **Moderation:** đo **tỷ lệ ảnh bị provider từ chối** trên golden set ở P0 và dùng làm tiêu chí chọn provider (≤ 5% shot). Làm rõ BR-18: chỉ **văn bản truyện** là không được sửa; brief do AI viết được người dùng sửa (UC-05.06) rồi sinh lại, và prompt storyboard hướng dẫn tả gián tiếp cảnh bạo lực, nhạy cảm. Không tự động thử lại để vượt bộ lọc. Thêm R-21 | 08 BR-18; 09 §1.5, §5; 01 §8 |
| QĐ-114 | Thêm **`EVAL-asset-extraction`**: golden set có nhãn tay danh sách nhân vật (kèm bí danh), địa điểm, vật quan trọng. Ngưỡng: recall nhân vật có tên ≥ 90%, precision ≥ 80%. BA gán nhãn ở P0–P1; chạy khi xong UC-04.01 và mỗi lần đổi prompt hoặc mô hình | 09 §4.5, §4.13; 07 NFR-MNT-06 |
| QĐ-115 | Thêm **`EVAL-alignment`** ở P0, áp cho cả timestamp do TTS trả và aligner tự host: so với nhãn tay biên từ (khoảng 200 từ mỗi ngôn ngữ), sai lệch trung vị ≤ 100 ms, p95 ≤ 250 ms. Aligner tự host phải chạy ≤ 0,5× thời lượng audio trên máy staging (CPU). Không đạt thì ưu tiên provider TTS có timestamp | 09 §1.5, §4.13; 05 §7.3 |
| QĐ-116 | **Đổi thứ tự cắt giảm:** nạp tiền sandbox + webhook (✂6 cũ) lên **✂1**, thay bằng Admin cộng tiền qua CLI. Lý do: tiền sandbox không đo được ý định trả tiền thật, và việc này không phải trọng tâm AI của đồ án. Đánh số lại: Map ✂1→✂2, preset/chuyển cảnh ✂2→✂3, Relationships ✂3→✂4, Timeline truyện ✂4→✂5, từ điển phát âm ✂5→✂6; ✂7–✂10 giữ nguyên. Tầng 1 thành ✂1–✂6, tầng 2 thành ✂7–✂10. Thay phần "Map ở **đầu** thứ tự cắt giảm" của QĐ-61. Nếu cắt ✂1, BO-05 đo bằng câu hỏi khảo sát beta | 09 §1.3; 02; 03; 01 BO-05 |
| QĐ-117 | **Ablation cho báo cáo** trong cửa sổ UAT (T25–T27): chạy `EVAL-consistency` trên 2–3 chương golden với 4 cấu hình: đầy đủ / bỏ ảnh tham chiếu / bỏ Visual Rules / bỏ Timeline truyện + Relationships. `PromptCompiler` có cờ cấu hình bật/tắt từng phần ngữ cảnh, chỉ dùng cho eval. Ngân sách ≤ $30, lấy từ khoản UAT | 09 §1.7, §1.10; 05 §7.1 |
| QĐ-118 | Phần việc chấm và gán nhãn của QĐ-110, 111, 114, 115 (khoảng 1 tuần-người) giao cho **PO/BA và frontend**, không giao cho back-end & AI ở P0 | 09 §2.1 |

## 10. Rủi ro đã chấp nhận

| Mã | Nội dung | Nguồn |
|---|---|---|
| QĐ-80 | Từ điển phát âm nằm trong thứ tự cắt giảm (cuối cùng, vị trí 5). Nếu bị cắt, mục tiêu WER ≤ 3% chỉ còn dựa vào chọn provider ở P0. Ghi vào R-06 | V4 lưu ý |
| QĐ-81 | Kế hoạch chỉ vừa khít nếu Coding Agent giúp được ít nhất 1,5 lần năng suất (R-12); được giảm bớt bằng QĐ-91, QĐ-94 | V3 4 |

## 11. Tích hợp hệ thống AI bên ngoài (2026-10-20)

Nguồn: [13 — Tích hợp hệ thống AI bên ngoài](tai-lieu/13-tich-hop-he-thong-ai.md). PO chọn lại nhà cung cấp và duyệt cả 8 đề xuất ĐX-AI-01..08. QĐ-121 thay QĐ-62.

| Mã | Quyết định | Tài liệu |
|---|---|---|
| QĐ-119 | **LLM: Google Gemini.** Mô hình nhanh (Flash) cho tác vụ thường; mô hình mạnh (Pro) cho storyboard, phân tích dài, Director *(sau MVP)*. Mã mô hình chốt ở P0 theo eval. MVP không seed provider LLM khác; port vẫn giữ để đổi sau (AG-02) | 05 §7.3; 13 §1.1 |
| QĐ-120 | **Ảnh: Google Gemini Image** cho ảnh tham chiếu, ảnh shot, sửa ảnh. P0 đo Gemini Image theo ngưỡng 09 §1.5; không đạt thì áp quy tắc dự phòng (QĐ-97), gồm thử thêm một provider | 05 §7.3; 09 §1.2, §1.5 |
| QĐ-121 | **TTS: MVP dùng model tự host** (mã nguồn mở, tiếng Việt và tiếng Anh, giấy phép cho phép dùng trong đồ án), chạy thành **TTS Server** nội bộ trên GPU (ADR-30). P0 chọn model trong 2–3 ứng viên bằng `EVAL-wer-golden`, `EVAL-alignment`, `BENCH-tts`. **Sau MVP: Vbee AIVoice** qua adapter `TtsPort`. Thay QĐ-62 | 02 IF-05; 05 §4, §7.3, ADR-30; 09 |
| QĐ-122 | **Aligner / STT giữ nguyên:** WhisperX tự host (MFA thay thế). TTS tự host không trả timestamp tin cậy nên **Alignment Worker bắt buộc trong MVP** (bỏ điều kiện "tùy chọn" của ADR-23) | 05 §4.1 |
| QĐ-123 | **Chi phí TTS tự host** tính theo giây GPU: `ai_models.unit_cost_usd` (đơn vị `SECONDS`) = giá thuê GPU một giờ / 3.600, đo ở P0. Giá vẫn × 110% và tính vào trần chi tiêu ngày như provider ngoài. Chi phí máy GPU lúc rảnh thuộc ngân sách hạ tầng | 08 §3.2; 09 §1.7 |
| QĐ-124 | (ĐX-AI-01) **Fallback chỉ áp cho LLM**, giữa các mô hình Gemini. Ảnh và TTS ghim theo dự án / giọng; circuit breaker mở thì job lỗi tạm thời, không đổi provider | 05 §7.1 |
| QĐ-125 | (ĐX-AI-02) Chỉ fallback sang mô hình có `unit_cost_usd` ≤ mô hình đã báo giá | 05 §6.1, §7.1; 08 §3.1 |
| QĐ-126 | (ĐX-AI-03) **Timeout** mỗi lời gọi: LLM 120 s, ảnh 90 s, TTS ≥ 2× thời lượng audio dự kiến (tối thiểu 30 s), nghe thử 15 s; quá hạn là lỗi tạm thời | 07 NFR-REL-04 |
| QĐ-127 | (ĐX-AI-04) `ai_usage_records` ghi thêm `prompt_version` và `seed` (nếu provider hỗ trợ) để tái lập kết quả LLM; không lưu toàn văn prompt LLM | 04 §3 |
| QĐ-128 | (ĐX-AI-05) Dùng Gemini API **gói trả phí** (không dùng gói miễn phí, vì dữ liệu gói miễn phí có thể được dùng để cải thiện sản phẩm; kiểm lại điều khoản ở P0). Thông báo đồng ý (BR-31) nêu tên Google là bên nhận văn bản truyện và ảnh; TTS tự host không gửi văn bản ra ngoài | 08 BR-31 |
| QĐ-129 | (ĐX-AI-06) Báo giá chỉ dùng hệ số ký tự/token cục bộ; tokenizer thật chỉ dùng để hiệu chỉnh hệ số ở P0 | 05 §7.1 |
| QĐ-130 | (ĐX-AI-07) Ghi bảng ánh xạ `jobs.type` ↔ `price_rules.operation` vào 08 §3.2 | 08 §3.2 |
| QĐ-131 | (ĐX-AI-08) **Nghe thử phát âm là ngoại lệ đồng bộ** của AG-01: báo giá → giữ chỗ trần ngày + HOLD → gọi TTS (timeout 15 s, không thử lại) → CAPTURE/RELEASE trong cùng request; vẫn ghi `ai_usage_records` | 05 AG-01, §6.1; 06 |

## 12. Rà soát kỹ thuật: bỏ phần làm quá mức cần cho MVP (2026-10-20)

Áp ở phiên bản 1.22 (QĐ-139..141: phiên bản 1.23). Bối cảnh: closed beta 20 người, 5 người đồng thời, một máy staging, một máy GPU (QĐ-71). Các phần dưới đây giữ trong thiết kế sau MVP; port và ranh giới module không đổi.

| Mã | Quyết định | Tài liệu |
|---|---|---|
| QĐ-132 | **Bỏ semaphore theo người dùng khỏi MVP** (ADR-28 thành sau MVP). MVP giới hạn đồng thời toàn hệ thống bằng `concurrency` của từng queue và rate limiter có sẵn của BullMQ; render 1 đang chạy/người, kiểm bằng DB lúc tạo job. Lý do: với 5 người đồng thời, semaphore chỉ đem lại công bằng nhưng thêm bộ đếm Redis có thể rò khi worker chết | 05 §6.1, §6.2, ADR-28; 08 BR-32; 07 NFR-SCAL-03; 13 §8 |
| QĐ-133 | **Thử lại một tầng ở mức job**: mỗi lần thử của job gọi provider một lần; lỗi tạm thời → `RETRYING` → BullMQ thử lại theo backoff (tối đa 3 lần). Bỏ `RetryPolicy` lặp bên trong AI Gateway (trước đây hai tầng chồng nhau có thể thành 9 lời gọi, và `attempt` mang hai nghĩa). **Bỏ circuit breaker khỏi MVP** | 05 §6.1, §7.1; 13 §2, §7; 07 NFR-REL-04 |
| QĐ-134 | **Chỉ job gốc giữ và quyết toán tiền** (WR-05 mới). Job con của Flow có `held_micro = 0`; job cha CAPTURE chi phí các con thành công × 110% (≤ HOLD), RELEASE phần còn lại, một lần. Bỏ "giữ thêm khi biết số shot" và việc chia HOLD cho từng con. Regenerate all: n job gốc tạo trong một giao dịch. Job cha đang chờ con không bị reconciler coi là treo | 08 WR-05; 05 §6.1, §6.2; 04 IC-05; seq-sinh-tu-lieu, seq-vong-doi-job |
| QĐ-135 | **Bỏ `ModerationFilter` riêng khỏi MVP**; dựa vào bộ lọc an toàn có sẵn của Gemini (LLM, ảnh). Không kiểm duyệt văn bản truyện của chính người dùng hay audio TTS đọc nguyên văn | 05 §7.1; 13 §2, §6.3 |
| QĐ-136 | **Nghe thử phát âm miễn phí** (sửa QĐ-131): vẫn đồng bộ, nhưng không báo giá, không tạo job, không HOLD, không tính vào trần ngày; rate limit 10 lần/phút/người, cache 24 giờ. Lý do: ≤ 200 ký tự trên TTS tự host tốn chưa tới 0,1 cent | 05 §6.1; 06 §2.5; 08 §3.2, BR-32; 13 §3 |
| QĐ-137 | Đơn giản hóa khác: render một lượt `renderMedia` của Remotion (không tự chia đoạn rồi nối); Scheduler dùng BullMQ repeatable job, bỏ leader lock; `OpsBatcher` không có hàng đợi offline lưu bền; bỏ sự kiện SSE `media.progress` (trùng `illustration.ready`, `narration.updated`, `job.updated`); log có `jobId` thay cho OpenTelemetry trong MVP | 05 §4, §6.4, §6.6, §10; 06 §3; 07 NFR-MNT-03 |
| QĐ-138 | Sửa số liệu không khớp: `target_shot_seconds` mặc định 20 s (khớp 3 ảnh/phút, QĐ-112; trước ghi 15 s); NFR-PERF-08 tính 36 ảnh/chương thay vì 10; NFR-PERF-01 đo ở 20 RPS cho closed beta (200 RPS sau MVP) | 02 FR-PRJ-07, FR-BOK-01; 04; 07 |
| QĐ-139 | **Giữ giới hạn Free 10 phút video/tháng**: một chương thông thường dài khoảng 10 phút, nên tài khoản Free xuất được khoảng một chương mỗi tháng, khớp mức "$2 đủ khoảng 1 chương" (QĐ-36, QĐ-37) | 08 BR-27 |
| QĐ-140 | **Bỏ tốc độ từng clip thuyết minh** (thay QĐ-53; bỏ ADR-24, IC-17, job `PROCESS_AUDIO_RATE`). Chỉ còn **một** tốc độ đọc cho cả dự án (`narration_settings.speed`, 0,8–1,3×), áp ở bước TTS: truyền cho model nếu hỗ trợ, nếu không adapter đổi tốc độ audio (giữ cao độ) ngay sau khi tổng hợp, **trước** khi căn timestamp. Đổi tốc độ đọc thì sinh lại thuyết minh. Timeline chỉ cho dời và chỉnh âm lượng clip thuyết minh | 01, 02 FR-NAR-01, FR-EDT-04; 04; 05; 06; 08 BR-24; 12; schema v2; M06 |
| QĐ-141 | **MVP không có timeline cả dự án.** Trình chỉnh sửa chỉ làm theo chương. Thêm **xuất cả dự án tự động** (FR-EDT-28): ghép timeline từng chương (đã chỉnh hoặc bản nháp tự dựng) nối tiếp, cắt thẳng giữa hai chương, render một lần; mọi chương phải đạt điều kiện xuất. Timeline cả dự án để chỉnh trên một trục: sau MVP | 02 FR-EDT-01, FR-EDT-28; 04 `renders.scope`; 05; 06 `POST /projects/{pid}/renders`; 12 §3; schema v2; UC-06.01, UC-06.16 |


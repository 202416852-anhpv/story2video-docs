# Sổ quyết định

> Ghi các quyết định đã chốt của nhóm (ngày, nội dung, lý do). Không cần duyệt riêng; khi bất đồng, PO quyết định cuối (QĐ-50).
> Nguồn: 4 vòng câu hỏi chốt phạm vi và kế hoạch ngày 2026-10-20 (file câu hỏi đã được xóa sau khi chốt; nội dung trả lời được ghi đầy đủ ở đây). Mã ở cột Nguồn: **A/B/C/D…** = vòng 1, **V2 / V3 / V4 + số câu** = vòng 2–4.
> Mọi quyết định dưới đây chốt ngày **2026-10-20** và đã được áp vào bộ tài liệu phiên bản 1.12; mục 7 áp ở phiên bản 1.13.

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
| QĐ-53 | Cho đổi tốc độ clip thuyết minh trong khoảng **0,8×–1,25×** (giữ cao độ, phụ đề co giãn theo) | B5 | BR-24, FR-EDT-04, UC-06.02 |
| QĐ-54 | Kiểm chứng lời đọc thủ công là M: mỗi shot có "Nghe" và "Đánh dấu cần sinh lại", **không bắt buộc** nghe hết mới được xuất. Kiểm chứng ASR từng shot (WER, `NEEDS_REVIEW`, chấp nhận thủ công) là S, sau MVP. WER ≤ 3% bảo đảm ở **khâu chọn provider** (`EVAL-wer-golden`, P0) | B1, V2 3 | BR-11, BR-23, FR-NAR-07, 08 |
| QĐ-55 | BR-23 nới thành: xuất được khi độ phủ 100%, mọi shot có ảnh `DONE` và thuyết minh `DONE`, không clip nào `OUTDATED` | V2 3 | BR-23, FR-EDT-22 |
| QĐ-56 | Ký hiệu trình bày: **đọc chữ, bỏ ký hiệu** (`*Bố*` đọc "Bố"); phụ đề **hiện nguyên** `*Bố*`. Dòng phân cách `---` không đọc (lặng 0,5 s) và không có phụ đề. Danh sách mặc định toàn hệ thống, mỗi dự án bật/tắt từng mẫu | A5, V2 4.1–4.3, V3 ghi chú | BR-19, BR-22, 08 §6 |
| QĐ-57 | Bỏ AI sinh nhạc/SFX (FR-EDT-16) và gợi ý SFX theo đoạn văn (UC-06.11c) | A7, V2 7 | 02, 03-M06, 04, 05, 06 |
| QĐ-58 | MVP chỉ cho **tải nhạc/SFX lên** (≤ 100 MB, ≤ 15 phút, không cần ô cam kết). Sau MVP nạp sẵn bộ CC0/CC-BY từ Pixabay/Freesound, nhạc CC-BY tự sinh dòng ghi công | A7, B2, V2 7 | FR-EDT-12, FR-EDT-27, BR-26 |
| QĐ-59 | Tách FR-WLD-05: gỡ tài sản khỏi dự án là M (FR-WLD-05); thư viện là S (FR-WLD-12) | B7 | 02 |
| QĐ-60 | Lời thoại một giọng kể trong MVP; đa giọng sau. Ngôn ngữ thuyết minh lúc ra mắt: tiếng Việt và tiếng Anh. Tiêu đề chương không đọc | 09 §6 câu 5–7 | 02 |
| QĐ-61 | Giữ **Map** (UC-02.09) trong MVP nhưng ở **đầu** thứ tự cắt giảm | V4 4 | 02, 09 |
| QĐ-62 | Đưa **Vbee AIVoice** vào danh sách provider TTS so sánh ở P0 | V3 6 | 05 §7.3, 09 |

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

## 8. Rủi ro đã chấp nhận

| Mã | Nội dung | Nguồn |
|---|---|---|
| QĐ-80 | Từ điển phát âm nằm trong thứ tự cắt giảm (cuối cùng, vị trí 5). Nếu bị cắt, mục tiêu WER ≤ 3% chỉ còn dựa vào chọn provider ở P0. Ghi vào R-06 | V4 lưu ý |
| QĐ-81 | Kế hoạch chỉ vừa khít nếu Coding Agent giúp được ít nhất 1,5 lần năng suất (R-12); được giảm bớt bằng QĐ-91, QĐ-94 | V3 4 |

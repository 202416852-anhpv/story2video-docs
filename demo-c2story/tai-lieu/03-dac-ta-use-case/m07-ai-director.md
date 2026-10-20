# M07 — AI Director

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m07-ai-director.puml`, `../../so-do/04-tuan-tu/seq-director.puml`, `../../so-do/06-trang-thai/state-director-plan.puml`. Yêu cầu: FR-DIR-01..09. Director dùng **cùng quyền và cùng bảng giá** như thao tác tay; **không có công cụ ghi văn bản truyện** (BR-21).
> **Toàn bộ phân hệ nằm ngoài MVP** (QĐ-04): chỉ làm nếu MVP xong sớm. Khi làm, điểm duyệt thuyết minh (UC-07.06) dùng nghe & đánh dấu (UC-05.18) cho tới khi có kiểm chứng ASR; mọi thao tác tốn phí tính theo chi phí thực × 110% (BR-01).

---

<a id="uc-0701"></a>
## UC-07.01 Ra lệnh bằng chat

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | Yêu cầu Director thực hiện thao tác bằng ngôn ngữ tự nhiên ("làm lại shot 3 chương 2 cho trời tối hơn") |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** thao tác tương ứng được thực hiện như thao tác tay; hội thoại được lưu. **Tối thiểu:** không thực hiện thao tác ngoài quyền hoặc tốn phí khi chưa xác nhận |
| Kích hoạt | Gửi tin nhắn trong panel Director |
| Quan hệ | được mở rộng bởi UC-07.01a..d |
| Truy vết | FR-DIR-01..03, 08; NFR-SEC-08 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor gửi tin nhắn.
2. Hệ thống gửi LLM: lịch sử hội thoại, tóm tắt trạng thái dự án, danh sách tool được phép theo quyền. Văn bản truyện được đánh dấu là **dữ liệu**, không phải chỉ dẫn.
3. LLM trả lời và/hoặc đề xuất tool call (vd. `rewrite_shot(2, 3, "trời tối hơn")`).
4. Hệ thống kiểm tra quyền; thực thi tool (tạo job như thao tác tay).
5. Kết quả được stream về chat; Director note được ghi nếu cần.

**Luồng thay thế / ngoại lệ**
- **3a.** Lệnh thiếu tham số: UC-07.01a.
- **3b.** Tool tốn phí: UC-07.01b.
- **3c.** Yêu cầu sửa hoặc tóm tắt văn bản: UC-07.01c.
- **4a.** Tool nằm ngoài quyền (vd. Editor đòi xóa dự án): từ chối và giải thích.

### UC-07.01a Hỏi lại khi lệnh mơ hồ
<a id="uc-0701a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-07.01 (điểm mở rộng: bước 3) |
| Tác nhân | Editor / Director |
| Mô tả | Khi lệnh thiếu tham số, Director hỏi lại thay vì đoán |
| Tiền điều kiện | Director nhận ra lệnh cần một tool nhưng thiếu tham số bắt buộc (chương nào, shot số mấy…) |
| Hậu điều kiện | **Thành công:** lệnh đủ tham số và quay lại UC-07.01 bước 3. **Tối thiểu:** không tool nào chạy khi còn thiếu tham số |
| Kích hoạt | LLM trả về yêu cầu làm rõ thay vì tool call |
| Truy vết | FR-DIR-01..03; NFR-SEC-08 |
| Giai đoạn | Sau |

**Luồng chính**
1. Director hỏi lại ngắn gọn về tham số còn thiếu và gợi ý lựa chọn lấy từ trạng thái dự án (danh sách chương, shot).
2. Editor trả lời.
3. Hệ thống ghép câu trả lời vào lệnh ban đầu.
4. Quy trình quay lại UC-07.01 bước 3 với lệnh đủ tham số.

**Luồng thay thế / ngoại lệ**
- **2a.** Editor đổi chủ đề hoặc không trả lời: lệnh dở bị bỏ, hội thoại tiếp tục bình thường.
- **2b.** Câu trả lời vẫn mơ hồ: Director hỏi lại; nếu vẫn không rõ, gợi ý Editor thao tác trực tiếp trên giao diện.

### UC-07.01b Xác nhận thao tác tốn phí
<a id="uc-0701b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-07.01 (điểm mở rộng: bước 3) |
| Tác nhân | Editor / Director |
| Mô tả | Mọi thao tác tốn phí phải được Editor xác nhận bằng thẻ đề xuất trước khi tạo job (tool proposal) |
| Tiền điều kiện | LLM đề xuất một tool tốn phí; Editor có quyền Editor trong dự án |
| Hậu điều kiện | **Thành công:** chỉ khi Editor đồng ý mới tạo job; tiền trừ vào ví người xác nhận. **Tối thiểu:** chưa xác nhận thì không giữ tiền và không tạo job |
| Kích hoạt | Director đề xuất tool tốn phí |
| Truy vết | ADR-19; BR-01, BR-03; NFR-SEC-08; 04 §3.6 `director_tool_proposals`; API 2.7 `…/tool-proposals/{tpid}:confirm` |
| Giai đoạn | Sau |

**Luồng chính**
1. Hệ thống tạo `director_tool_proposals` ở trạng thái `PENDING` (tool, tham số, giá theo `price_rules`); chưa giữ tiền, chưa tạo job.
2. Hệ thống gửi `tool_proposal` qua SSE; giao diện hiện thẻ gồm thao tác, phạm vi, giá và số dư.
3. Editor bấm Đồng ý: client gọi `:confirm` kèm `Idempotency-Key`.
4. Hệ thống kiểm tra quyền, giữ tiền của người xác nhận (UC-05.17, BR-03), tạo job, đặt `CONFIRMED` kèm `decided_by`, `decided_at`, `job_id`.
5. Kết quả được stream về chat (`tool_result`).

**Luồng thay thế / ngoại lệ**
- **3a.** Editor bấm Hủy: đặt `REJECTED`, Director ghi nhận và hỏi có muốn thay đổi lệnh.
- **4a.** Không đủ số dư: `402`; thẻ giữ `PENDING` để xác nhận lại sau khi nạp tiền hoặc bị hủy.
- **4b.** Giá đã đổi kể từ lúc đề xuất: hệ thống tính lại và yêu cầu xác nhận với giá mới [ĐX].
- **3b.** Thẻ quá hạn (`EXPIRED`): không xác nhận được; Director đề xuất lại khi Editor yêu cầu.

### UC-07.01c Từ chối sửa / tóm tắt văn bản
<a id="uc-0701c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-07.01 (điểm mở rộng: bước 3) |
| Tác nhân | Editor / Director |
| Mô tả | Director từ chối sửa, viết lại hoặc tóm tắt văn bản truyện vì nguyên tắc thuyết minh nguyên văn |
| Tiền điều kiện | Editor yêu cầu thay đổi nội dung văn bản truyện ("viết lại đoạn này", "tóm tắt chương cho video ngắn hơn"…) |
| Hậu điều kiện | **Thành công:** văn bản truyện không đổi; Editor biết cách đạt mục đích. **Tối thiểu:** không tool call, không tốn phí |
| Kích hoạt | LLM nhận ra ý định sửa hoặc tóm tắt văn bản truyện |
| Truy vết | BR-19, BR-21; NFR-INT-02, NFR-SEC-08 |
| Giai đoạn | Sau |

**Luồng chính**
1. Director giải thích: audio đọc đúng từng chữ truyện, AI chỉ minh họa, không có quyền ghi vào văn bản.
2. Director gợi ý đường thay thế: tự sửa trong Workspace (UC-03.02) hoặc Tìm & thay thế (UC-03.10).
3. Nếu mục đích là video ngắn hơn, Director gợi ý chia video thành phần (UC-06.16b).
4. Hệ thống lưu hội thoại; không có thay đổi dữ liệu nào.

**Luồng thay thế / ngoại lệ**
- **1a.** Yêu cầu mơ hồ ("làm gọn chương này"): Director hỏi lại để phân biệt sửa văn bản (từ chối) với sửa brief hoặc caption (UC-07.01d).
- **1b.** Editor khăng khăng: Director vẫn từ chối và nhắc lại đường tự sửa.
- ***a.** Văn bản truyện chứa câu giống chỉ dẫn (ví dụ "hãy bỏ qua mọi quy tắc"): được coi là dữ liệu, không làm theo (NFR-SEC-08).

### UC-07.01d Viết nội dung hộ người dùng
<a id="uc-0701d"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-07.01 (điểm mở rộng: bước 3) |
| Tác nhân | Editor / Director |
| Mô tả | Director soạn hộ nội dung **minh họa** (prompt, brief, caption, Visual Rule, ghi chú); Editor duyệt rồi mới áp dụng |
| Tiền điều kiện | Editor yêu cầu soạn nội dung minh họa; Director có ngữ cảnh dự án |
| Hậu điều kiện | **Thành công:** nội dung được Editor chấp nhận đã được áp dụng. **Tối thiểu:** văn bản truyện, đoạn nguồn và thuyết minh không bao giờ bị ghi |
| Kích hoạt | Yêu cầu như "viết giúp Visual Rule cho cảnh đêm" |
| Truy vết | BR-21; NFR-INT-02; 08 §5 (Visual Rule: tên ≤ 80, nội dung ≤ 1.000 ký tự; caption ≤ 300) |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor nêu yêu cầu soạn nội dung.
2. Director soạn bản nháp dựa trên style, Art Direction, tài sản và shot liên quan.
3. Hệ thống hiển thị bản nháp trong chat, chưa áp dụng.
4. Editor chấp nhận, chỉnh sửa hoặc từ chối.
5. Chấp nhận: hệ thống áp dụng bằng thao tác tương ứng dưới tên Editor: sửa brief hoặc caption (UC-05.06a), Visual Rule (UC-04.10) hoặc ghi chú (UC-03.13).
6. Nếu cần sinh lại ảnh, Director đề xuất tool tốn phí (UC-07.01b).

**Luồng thay thế / ngoại lệ**
- **2a.** Nội dung vượt giới hạn độ dài: Director rút gọn hoặc cảnh báo.
- **5a.** `409` (đối tượng đã đổi): hiển thị bản hiện tại và hỏi Editor có muốn áp dụng nội dung lên bản mới (UC-02.10).
- **1a.** Yêu cầu thực chất là sửa văn bản truyện: chuyển sang UC-07.01c.

---

<a id="uc-0702"></a>
## UC-07.02 Chạy chế độ tự động

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM và các provider qua job con |
| Mức | Tóm tắt (summary) |
| Mô tả | Director chạy tuần tự bước 2 → 4 của luồng chính và dựng bản nháp timeline |
| Tiền điều kiện | Dự án có văn bản |
| Hậu điều kiện | **Thành công:** mọi chương "Sẵn sàng dựng" và có bản nháp timeline. **Tối thiểu:** kế hoạch lưu bền vững; bước dở tiếp tục được; tiền giữ cho job lỗi được hoàn |
| Kích hoạt | Bật "Tự động" trong panel Director |
| Quan hệ | include UC-07.02a; được mở rộng bởi UC-07.03..06 |
| Truy vết | FR-DIR-04..07; BR-09 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor bật chế độ tự động.
2. Hệ thống tạo DirectorPlan `RUNNING`, thực hiện **UC-07.02a**.
3. **pickStyle:** nếu chưa có style, thực hiện UC-07.03.
4. **split:** nếu dự án chỉ có 1 chương dài hơn ngưỡng, chạy UC-03.03 và áp dụng gợi ý.
5. **cast:** chạy UC-04.01 bước 2–3, thực hiện UC-07.04, rồi sinh ảnh tham chiếu (UC-04.03).
6. **pickVoice:** nếu chưa có giọng đọc, thực hiện UC-07.05.
7. **media:** chạy UC-05.07 cho mọi chương chưa "Sẵn sàng dựng".
8. **verify:** nếu có shot `NEEDS_REVIEW`, thực hiện UC-07.06.
9. **draftTimeline:** bảo đảm mọi chương có bản nháp timeline (UC-06.01a).
10. Plan `COMPLETED`; Director báo "Mọi chương đã sẵn sàng dựng video", gợi ý mở trình chỉnh sửa để thêm nhạc nền, SFX và xuất.

**Luồng thay thế / ngoại lệ**
- **\*a.** Thiếu số dư cho bước kế tiếp: plan `AWAITING_INPUT(INSUFFICIENT_BALANCE)` kèm link nạp tiền.
- **\*b.** Một job lỗi sau retry: ghi note, bỏ qua mục đó, tiếp tục; cuối plan liệt kê mục lỗi.
- **\*c.** Editor tạm dừng hoặc thoát: UC-07.07.
- **10a.** Editor yêu cầu "xuất luôn": Director chạy UC-06.16 với timeline nháp (chưa có nhạc/SFX) sau khi Editor xác nhận.

### UC-07.02a Lập & cập nhật kế hoạch bước
<a id="uc-0702a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-07.02 (bước 2) |
| Tác nhân | Hệ thống (`PlanEngine`) |
| Mô tả | Xác định bước nào của kế hoạch đã xong, bước nào cần làm, ước tính chi phí còn lại và cập nhật khi tiến trình thay đổi |
| Tiền điều kiện | Có DirectorPlan vừa tạo hoặc đang chạy |
| Hậu điều kiện | **Thành công:** `director_plans` phản ánh đúng trạng thái dự án; bước đã xong bị bỏ qua. **Tối thiểu:** kế hoạch bền vững, tiếp tục được sau khi tạm dừng hoặc lỗi |
| Kích hoạt | UC-07.02 bước 2; sau mỗi job xong hoặc lỗi; sau mỗi điểm duyệt |
| Truy vết | FR-DIR-04..07; BR-09; 04 §3.6 `director_plans`; API 2.7 `GET/POST /projects/{pid}/director/plan`, sự kiện `director.plan` |
| Giai đoạn | Sau |

**Luồng chính**
1. Hệ thống đọc trạng thái dự án: có style chưa, số chương, tài sản đã duyệt và có ảnh chưa, giọng đọc, `media_status` từng chương, shot `NEEDS_REVIEW`, timeline.
2. Hệ thống đánh dấu từng bước (`pickStyle`, `split`, `cast`, `pickVoice`, `media`, `verify`, `draftTimeline`) là đã xong, cần làm hoặc bỏ qua.
3. Bước đầu tiên chưa xong là `current_step`.
4. Hệ thống ước tính số tiền còn cần: ảnh tham chiếu còn thiếu cộng báo giá `media:quote` của các chương chưa sẵn sàng.
5. Hệ thống lưu `step_state`, `estimated_remaining_micro` và tăng `version`.
6. Sau mỗi job xong, job lỗi hoặc điểm duyệt, hệ thống tính lại và phát `director.plan {status, currentStep, awaitingReason?}`.

**Luồng thay thế / ngoại lệ**
- **1a.** Editor sửa tay ngoài Director: lần tính lại sau đó phản ánh thay đổi, bước đã được Editor làm xong bị bỏ qua.
- **3a.** Mọi bước đã xong: đặt plan `COMPLETED`.
- **4a.** Không đủ số dư cho bước kế tiếp: plan `AWAITING_INPUT (INSUFFICIENT_BALANCE)` (UC-07.02 nhánh *a).

---

<a id="uc-0703"></a>
## UC-07.03 Chọn style (điểm duyệt)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Director dừng để Editor chọn style trước khi sinh bất kỳ ảnh nào |
| Tiền điều kiện | Plan đang chạy, dự án chưa có style |
| Hậu điều kiện | **Thành công:** dự án có style; plan tiếp tục |
| Kích hoạt | Plan `AWAITING_INPUT(PICK_STYLE)` |
| Quan hệ | extend UC-07.02 |
| Truy vết | FR-DIR-05; BR-09 |
| Giai đoạn | Sau |

**Luồng chính**
1. Director mở Styles Library và thông báo cần chọn style.
2. Editor chọn style (UC-04.05).
3. Editor bấm "Continue"; plan quay về `RUNNING`.

---

<a id="uc-0704"></a>
## UC-07.04 Duyệt cast (điểm duyệt)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Director dừng để Editor duyệt nhân vật, địa điểm, đạo cụ trước khi sinh ảnh tham chiếu |
| Tiền điều kiện | Đã có danh sách tài sản đề xuất |
| Hậu điều kiện | **Thành công:** tài sản được duyệt; ảnh tham chiếu được sinh sau khi xác nhận giá |
| Kích hoạt | Plan `AWAITING_INPUT(REVIEW_CAST)` |
| Quan hệ | extend UC-07.02 |
| Truy vết | FR-DIR-05; BR-09 |
| Giai đoạn | Sau |

**Luồng chính**
1. Director hiện "Review your cast & places" (UC-04.01a) kèm tổng giá ảnh tham chiếu.
2. Editor chỉnh danh sách và xác nhận.
3. Plan tiếp tục; hệ thống sinh ảnh tham chiếu.

---

<a id="uc-0705"></a>
## UC-07.05 Chọn giọng (điểm duyệt)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Director dừng để Editor nghe thử và chọn giọng đọc trước khi sinh thuyết minh |
| Tiền điều kiện | Dự án chưa có giọng đọc |
| Hậu điều kiện | **Thành công:** `narration_settings.voice_id` được đặt |
| Kích hoạt | Plan `AWAITING_INPUT(PICK_VOICE)` |
| Quan hệ | extend UC-07.02 |
| Truy vết | FR-DIR-05 |
| Giai đoạn | Sau |

**Luồng chính**
1. Director mở Cài đặt thuyết minh (UC-05.11) với gợi ý giọng theo ngôn ngữ truyện.
2. Editor nghe thử (UC-05.11a), chọn giọng, bấm "Continue".

---

<a id="uc-0706"></a>
## UC-07.06 Duyệt thuyết minh (điểm duyệt)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Director dừng để Editor xử lý các shot `NEEDS_REVIEW` |
| Tiền điều kiện | Có shot `NEEDS_REVIEW` sau bước media |
| Hậu điều kiện | **Thành công:** mọi shot `VERIFIED`/`ACCEPTED`; plan tiếp tục |
| Kích hoạt | Plan `AWAITING_INPUT(REVIEW_NARRATION)` |
| Quan hệ | extend UC-07.02 |
| Truy vết | FR-DIR-05; BR-23 |
| Giai đoạn | Sau |

**Luồng chính**
1. Director liệt kê shot cần duyệt kèm từ lệch.
2. Editor xử lý từng shot (UC-05.14).
3. Khi hết shot cần duyệt, Editor bấm "Continue".

---

<a id="uc-0707"></a>
## UC-07.07 Tạm dừng / tiếp tục / thoát

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Điều khiển chế độ tự động |
| Tiền điều kiện | Có DirectorPlan đang hoạt động |
| Hậu điều kiện | **Thành công:** plan ở `PAUSED`, `RUNNING` hoặc `CANCELLED`; kết quả đã có được giữ |
| Kích hoạt | Nút Pause / Continue / Exit auto |
| Truy vết | FR-DIR-06 |
| Giai đoạn | Sau |

**Luồng chính**
1. *Pause:* hệ thống không tạo job mới; job đang chạy được để xong; plan `PAUSED`.
2. *Continue:* hệ thống tính lại bước kế tiếp (UC-07.02a), plan `RUNNING`.
3. *Exit:* plan `CANCELLED`; job `QUEUED` bị hủy và hoàn tiền; mọi kết quả đã có được giữ.

**Luồng thay thế / ngoại lệ**
- **\*a.** Tải lại trang hoặc đăng nhập máy khác: trạng thái plan được khôi phục từ DB.

---

<a id="uc-0708"></a>
## UC-07.08 Xem tiến độ & Director note

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Theo dõi bước hiện tại, số việc xong/lỗi, chi phí đã dùng, ghi chú của Director |
| Tiền điều kiện | Có DirectorPlan |
| Hậu điều kiện | **Thành công:** hiển thị tiến độ realtime |
| Kích hoạt | Mở panel Director |
| Truy vết | FR-DIR-06, 08 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor mở panel Director.
2. Hệ thống hiển thị dải bước (pickStyle → … → draftTimeline), bước hiện tại, số chương/shot xong, lỗi, tiền đã dùng và ước tính còn lại, các Director note.
3. Editor bấm một mục lỗi để đi tới màn hình xử lý.

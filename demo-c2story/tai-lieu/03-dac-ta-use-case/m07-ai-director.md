# M07 — AI Director

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m07-ai-director.puml`, `../../so-do/04-tuan-tu/seq-director.puml`, `../../so-do/06-trang-thai/state-director-plan.puml`. Yêu cầu: FR-DIR-01..09. Director dùng **cùng quyền và cùng bảng giá** như thao tác tay; **không có công cụ ghi văn bản truyện** (BR-21).

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
- **Loại:** extend. **Các bước:** Director hỏi lại tham số thiếu ("Chương nào? Shot số mấy?"); Editor trả lời; quay lại bước 3. **Kết quả:** lệnh đủ tham số.

### UC-07.01b Xác nhận thao tác tốn phí
<a id="uc-0701b"></a>
- **Loại:** extend. **Các bước:** hiện thẻ đề xuất (thao tác, phạm vi, giá); Editor bấm Đồng ý hoặc Hủy. **Kết quả:** chỉ thực thi khi Editor đồng ý; credit trừ vào ví Editor (BR-03).

### UC-07.01c Từ chối sửa / tóm tắt văn bản
<a id="uc-0701c"></a>
- **Loại:** extend. **Điều kiện:** Editor yêu cầu "viết lại đoạn này", "tóm tắt chương cho video ngắn hơn"… **Các bước:** Director giải thích nguyên tắc thuyết minh nguyên văn (BR-19, BR-21); gợi ý tự sửa trong Workspace (UC-03.02) hoặc chia video theo chương (UC-06.16b). **Kết quả:** văn bản truyện không đổi.

### UC-07.01d Director viết nội dung hộ
<a id="uc-0701d"></a>
- **Loại:** extend. **Các bước:** Director soạn prompt ảnh, brief, Visual Rule hoặc ghi chú theo yêu cầu; hiển thị bản nháp; Editor chấp nhận để áp dụng. **Kết quả:** nội dung **minh họa** được cập nhật (không phải văn bản truyện).

---

<a id="uc-0702"></a>
## UC-07.02 Chạy chế độ tự động

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM và các provider qua job con |
| Mức | Tóm tắt (summary) |
| Mô tả | Director chạy tuần tự bước 2 → 4 của luồng chính và dựng bản nháp timeline |
| Tiền điều kiện | Dự án có văn bản |
| Hậu điều kiện | **Thành công:** mọi chương "Sẵn sàng dựng" và có bản nháp timeline. **Tối thiểu:** kế hoạch lưu bền vững; bước dở tiếp tục được; credit job lỗi được hoàn |
| Kích hoạt | Bật "Tự động" trong panel Director |
| Quan hệ | include UC-07.02a; được mở rộng bởi UC-07.03..06 |
| Truy vết | FR-DIR-04..07; BR-09 |

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
- **\*a.** Thiếu credit cho bước kế tiếp: plan `AWAITING_INPUT(INSUFFICIENT_CREDITS)` kèm link nạp credit.
- **\*b.** Một job lỗi sau retry: ghi note, bỏ qua mục đó, tiếp tục; cuối plan liệt kê mục lỗi.
- **\*c.** Editor tạm dừng hoặc thoát: UC-07.07.
- **10a.** Editor yêu cầu "xuất luôn": Director chạy UC-06.16 với timeline nháp (chưa có nhạc/SFX) sau khi Editor xác nhận.

### UC-07.02a Lập & cập nhật kế hoạch bước
<a id="uc-0702a"></a>
- **Loại:** include. **Các bước:** đọc trạng thái dự án; xác định bước đầu tiên chưa xong; ước tính tổng chi phí còn lại; lưu `step_state`; cập nhật sau mỗi job xong và phát `director.plan`. **Kết quả:** kế hoạch luôn phản ánh đúng trạng thái; bước đã xong được bỏ qua.

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

**Luồng chính**
1. *Pause:* hệ thống không tạo job mới; job đang chạy được để xong; plan `PAUSED`.
2. *Continue:* hệ thống tính lại bước kế tiếp (UC-07.02a), plan `RUNNING`.
3. *Exit:* plan `CANCELLED`; job `QUEUED` bị hủy và hoàn credit; mọi kết quả đã có được giữ.

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

**Luồng chính**
1. Editor mở panel Director.
2. Hệ thống hiển thị dải bước (pickStyle → … → draftTimeline), bước hiện tại, số chương/shot xong, lỗi, credit đã dùng và ước tính còn lại, các Director note.
3. Editor bấm một mục lỗi để đi tới màn hình xử lý.

# 08 — Quy tắc nghiệp vụ, phân quyền & credit

## 1. Danh mục quy tắc nghiệp vụ

| Mã | Quy tắc | Phân hệ | Nguồn |
|---|---|---|---|
| BR-01 | Mọi thao tác AI tốn phí có giá cấu hình (`price_rules`) và được hiển thị trước khi xác nhận. | M09 | QS |
| BR-02 | Vòng đời credit của job: HOLD khi tạo job → CAPTURE khi thành công / RELEASE khi thất bại hoặc bị hủy. | M09 | ĐX |
| BR-03 | Credit được tính cho người kích hoạt thao tác, kể cả khi do Director thay mặt người đó. | M02/M07 | ĐX |
| BR-04 | Chỉ Owner: mời/xóa thành viên, thu hồi link, đổi Settings, xóa dự án. | M02 | QS |
| BR-05 | Lưu đối tượng có version phải kèm `If-Match`; sai version thì từ chối và đưa ra lựa chọn xử lý xung đột. | M02/M03 | QS |
| BR-06 | Sửa nội dung chương hoặc tái cấu trúc chương: thuyết minh của các shot có đoạn nguồn bị đổi chuyển `OUTDATED`, và clip tương ứng trên timeline được đánh dấu. | M05/M06 | QS + ĐX |
| BR-07 | Mỗi chương có tối đa 1 storyboard hiện hành. | M05 | QS |
| BR-08 | Thứ tự chỉ dẫn hình ảnh: Style → Art Direction → Visual Rules (dự án) → Visual Rules (chương) → Chapter rules → Shot brief. Chỉ dẫn sau có ưu tiên cao hơn khi mâu thuẫn. | M04/M05 | QS |
| BR-09 | Director không tạo job sinh ảnh khi chưa có style và chưa xác nhận cast; không sinh thuyết minh khi chưa chọn giọng. | M07 | QS + ĐX |
| BR-10 | Archive là bất biến. | M03 | QS |
| BR-11 | Chương chỉ "Sẵn sàng dựng" khi mọi shot của storyboard hiện hành có ảnh `DONE` và thuyết minh `VERIFIED`/`ACCEPTED`. | M05 | ĐX |
| BR-12 | Một chương bị khóa khi đang tái cấu trúc hoặc đang có job thuyết minh chạy trên nó; khóa tự hết khi thao tác kết thúc. | M03 | QS |
| BR-14 | Ảnh tham chiếu tải lên với cờ "use exact" không bao giờ bị AI vẽ lại, kể cả khi chạy "Regenerate all". Tương tự, shot có ảnh hiện hành là `UPLOAD` không bị thay bởi sinh ảnh hàng loạt (UC-05.07, UC-05.07c); chỉ thay khi Editor chủ động sinh/sửa ảnh của shot đó. | M04/M05 | QS + ĐX |
| BR-15 | Mỗi lần sinh lại ảnh hoặc clip tạo phiên bản mới; phiên bản cũ giữ 90 ngày. | M05/M06 | ĐX |
| BR-16 | Gỡ tài sản khỏi dự án không xóa ảnh đã sinh của shot; shot giữ `raw_name` và chuyển sang "chưa liên kết". | M04 | SL |
| BR-17 | Xóa thành viên thì job đang chạy của người đó vẫn hoàn tất, nhưng người đó không xem được kết quả. | M02 | ĐX |
| BR-18 | Nội dung bị moderation chặn: job `FAILED` với `CONTENT_POLICY`, hoàn credit, không lưu đầu ra. **Không tự sửa văn bản để vượt bộ lọc.** | M10 | ĐX |
| **BR-19** | **Thuyết minh nguyên văn:** văn bản đưa vào TTS là đúng `chapter.content[sourceStart:sourceEnd]`. Chỉ được biến đổi ở mức phát âm: SSML break/alias/phoneme, bỏ ký hiệu markdown, đọc số. Không thêm, bớt, đổi, sắp xếp lại hay tóm tắt từ. | M06 | ĐX (yêu cầu khách hàng) |
| **BR-20** | **Phủ kín:** các shot của storyboard hiện hành chia văn bản chương thành đoạn liên tục, không chồng lấn, không bỏ sót; mọi thao tác trên shot (tách, gộp, xóa, dời ranh giới) giữ nguyên bất biến này. | M05 | ĐX |
| **BR-21** | **Chỉ tác giả sửa văn bản:** văn bản chương chỉ thay đổi bởi thao tác trực tiếp của Owner/Editor (gõ, Find & replace, Re-import, khôi phục phiên bản). Không AI nào (Director, phân tích, storyboard) có quyền ghi văn bản chương. | M03/M07 | ĐX |
| **BR-22** | Phụ đề hiển thị đúng nguyên văn đoạn đang đọc, ngắt dòng theo timestamp. | M06 | ĐX |
| **BR-23** | Chỉ xuất video khi: độ phủ 100%; mọi shot có ảnh `DONE`; thuyết minh `VERIFIED` hoặc `ACCEPTED`; không clip nào `OUTDATED`; timeline thỏa BR-24. | M06 | ĐX |
| **BR-24** | **Khóa thuyết minh trên timeline:** clip thuyết minh không được cắt, trim, xóa, đổi thứ tự, đổi tốc độ hay chồng lấn; chỉ được dời thời điểm (chèn khoảng lặng) và chỉnh âm lượng. Số lượng và thứ tự clip do storyboard quyết định. | M06 | ĐX |
| BR-25 | Clip ảnh của shot phải hiển thị suốt thời gian đọc đoạn của shot (được dài hơn, không ngắn hơn); chuyển cảnh, nhạc và SFX không được làm mất lời đọc (ducking bắt buộc khi nhạc chồng thuyết minh). | M06 | ĐX |
| BR-26 | Nhạc nền chỉ được dùng khi có license hợp lệ: thư viện hệ thống, cam kết của người tải lên, hoặc AI có quyền thương mại. | M06 | ĐX |

## 2. Ma trận phân quyền

| Hành động | Owner | Editor | User ngoài dự án | Admin |
|---|:-:|:-:|:-:|:-:|
| Xem dự án, chương, tài sản, tư liệu, timeline, video | ✓ | ✓ | ✗ | ✓ (chỉ hỗ trợ, có audit) |
| Sửa bản thảo, chương, notes, archives | ✓ | ✓ | ✗ | ✗ |
| Sửa Story Assets, Visual Rules, Art Direction | ✓ | ✓ | ✗ | ✗ |
| Sinh tư liệu: storyboard, sinh/sửa ảnh | ✓ | ✓ | ✗ | ✗ |
| Thuyết minh: cài giọng, từ điển phát âm, sinh, chấp nhận thủ công | ✓ | ✓ | ✗ | ✗ |
| Trình chỉnh sửa: hiệu ứng, chuyển cảnh, phụ đề, nhạc nền, SFX, overlay, xuất video | ✓ | ✓ | ✗ | ✗ |
| Dùng Director (chat, auto) | ✓ | ✓ | ✗ | ✗ |
| Tải MP4 / SRT / ZIP ảnh | ✓ | ✓ | ✗ | ✗ |
| Settings dự án (style, model, ngôn ngữ, trang/chương, hiển thị) | ✓ | ✗ | ✗ | ✗ |
| Tạo / thu hồi link mời, xóa thành viên | ✓ | ✗ | ✗ | ✗ |
| Xóa dự án | ✓ | ✗ | ✗ | ✓ (vi phạm chính sách) |
| Rời dự án | ✗ (phải xóa dự án) | ✓ | — | — |

> Owner đổi style dự án sau khi đã có ảnh thì không sinh lại tự động. Hệ thống gợi ý "Regenerate all" và hiện giá.

## 3. Bảng giá credit (giá trị tham khảo, cấu hình được)

> Quan sát từ hệ thống tham chiếu ngày 2026-10-19. Đội sản phẩm quyết định giá cuối cùng dựa trên chi phí AI thực tế (`ai_usage_records`).

### 3.1 Quy ước
1 credit ≈ chi phí 1 ảnh minh họa [QS: "1 credit = 1 illustration"].

### 3.2 Ảnh & văn bản

| Mã thao tác (`price_rules.operation`) | Giá | Nguồn |
|---|---|---|
| `ASSET_REFERENCE_IMAGE` | 1 / tài sản | QS |
| `SHOT_IMAGE` | 1 / shot | QS |
| `IMAGE_EDIT` (Describe→Edit, Fix a spot, Retry) | 1 / lần | QS |
| `SUGGEST_SPLITS`, `ANALYZE_ASSETS`, `STORY_META`, `STORYBOARD_DRAFT`, `REDIRECT`, `REWRITE_SHOT` (chỉ viết lại brief minh họa), Director chat | 0 credit; giới hạn tần suất (vd. 60 lần/giờ/dự án) | ĐX — tham chiếu không hiển thị giá cho các thao tác LLM |
| `EXPORT_ZIP` | 0 | ĐX |

### 3.3 Thuyết minh & video trình chiếu [ĐX]

| Mã thao tác | Giá | Ghi chú |
|---|---|---|
| `NARRATION_TTS` | 1 credit / 1.000 ký tự đoạn nguồn (làm tròn lên theo shot) | Bao gồm alignment và kiểm chứng WER. 1 chương 10.000 ký tự ≈ 10 credit |
| `NARRATION_REGENERATE` | Như trên, theo ký tự của shot | Sinh lại sau khi sửa từ điển phát âm hoặc đổi giọng |
| `PRONUNCIATION_PREVIEW` | 0 (≤ 200 ký tự, giới hạn tần suất) | |
| `MUSIC_AI` | 2 credit / bài ≤ 3 phút | Tùy chọn, trong trình chỉnh sửa; nhạc thư viện miễn phí |
| `SFX_AI` | 1 credit / hiệu ứng ≤ 10 s | Tùy chọn, trong trình chỉnh sửa; SFX thư viện miễn phí |
| `SFX_SUGGEST` | 0 (giới hạn tần suất) | AI gợi ý SFX theo đoạn văn; chỉ tốn phí khi sinh SFX mới |
| `RENDER_TIMELINE` | 0 | Chạy trên hạ tầng nội bộ; giới hạn số render đồng thời theo gói |

> **So sánh chi phí:** với hệ thống tham chiếu, 1 phút video AI (6 cảnh 10 s, Basic) tốn khoảng 120 credit. Với video dựng từ ảnh trên timeline, 1 phút đọc (khoảng 900 ký tự) tốn khoảng 1 credit TTS cộng ảnh (khoảng 4–6 slide = 4–6 credit).

### 3.5 Gói (tham khảo)

| Gói | Giá/tháng | Credit/tháng | Quyền lợi chính |
|---|---|---|---|
| Free | 0 | Daily claim (ĐX: 3/ngày, tối đa tích 10) | 1 dự án, 3 chương, render 720p có watermark |
| Starter | $10.99 | 100 | Mọi style, giọng đọc tiêu chuẩn, render 1080p, xuất MP4/SRT, ZIP ảnh, thư viện nhạc & SFX đầy đủ |
| Creator | $24.99 | 300 | + giọng đọc cao cấp, đa giọng nhân vật, ưu tiên hàng đợi |
| Studio | $49.99 | 600 | + cộng tác không giới hạn thành viên, render song song, ưu tiên cao nhất |

- Annual: giảm khoảng 17% (2 tháng miễn phí); credit vẫn cấp hằng tháng.
- Credit pack: mua một lần, không hết hạn.

## 4. Quy tắc ví credit

| Mã | Quy tắc |
|---|---|
| CR-01 | Ví có 3 bucket: `SUBSCRIPTION` (hết hạn cuối kỳ), `PACK` (không hết hạn), `BONUS` (daily claim, admin tặng; có thể hết hạn). |
| CR-02 | Thứ tự trừ khi HOLD: `SUBSCRIPTION` → `BONUS` → `PACK` (bucket sắp hết hạn được dùng trước). |
| CR-03 | HOLD: `available -= x`, `held += x` trong cùng giao dịch với tạo job, dùng `SELECT … FOR UPDATE` trên `credit_balances`. |
| CR-04 | CAPTURE: `held -= x`. RELEASE: `held -= x`, `available += x` (trả về đúng bucket đã giữ). |
| CR-05 | Job hàng loạt (Generate all): HOLD toàn bộ trước; mỗi job con CAPTURE hoặc RELEASE phần của nó. |
| CR-06 | Gia hạn subscription: EXPIRE phần `SUBSCRIPTION` còn lại (trừ phần đang held, phần này hết hạn khi job xong), rồi GRANT credit kỳ mới. |
| CR-07 | Hoàn tiền thanh toán (refund/chargeback): ghi ADJUST âm; nếu số dư âm thì khóa thao tác tốn phí đến khi bù. |
| CR-08 | Admin điều chỉnh: ADJUST kèm `reason` bắt buộc và `actor_id`. |

Sơ đồ: `../so-do/05-hoat-dong/act-giu-tru-credit.puml`.

## 5. Quy tắc kiểm tra dữ liệu

| Trường | Ràng buộc |
|---|---|
| Tiêu đề dự án | 1–120 ký tự |
| Văn bản import | ≤ 500.000 ký tự; file ≤ 2 MB; .txt/.md/.docx |
| Nội dung một chương | ≤ 60.000 ký tự (vượt quá thì gợi ý chia) |
| Số chương / dự án | ≤ 200 |
| Pages per chapter | 4–24 (mặc định 8) |
| Shot / bản nháp | 1–40 |
| Tên tài sản | 1–80 ký tự; bí danh ≤ 10 mục |
| Story Assets / dự án | ≤ 200 |
| Visual Rule | tên ≤ 80, nội dung ≤ 1.000 ký tự |
| Caption | ≤ 300 ký tự |
| Ảnh tải lên | PNG/JPEG/WebP ≤ 10 MB, ≥ 512px cạnh ngắn |
| Đoạn nguồn một shot | ≥ 1 câu; cảnh báo nếu > 30 s đọc (~450 ký tự tiếng Việt) |
| Từ điển phát âm | ≤ 500 mục / dự án; mỗi mục ≤ 100 ký tự |
| Ngưỡng WER | 0,01–0,10 (mặc định 0,03) |
| Nhạc tải lên | MP3/WAV/M4A ≤ 30 MB, ≤ 15 phút |
| Chuyển cảnh | 0–1.500 ms |
| Thành viên / dự án | Starter 3, Creator 10, Studio không giới hạn (ĐX) |

# 08 — Quy tắc nghiệp vụ, phân quyền & tính phí

> Mọi quyết định nguồn ghi ở [sổ quyết định](../quyet-dinh.md) (mã `QĐ-xx`). Cột **GĐ** là giai đoạn áp dụng: P0–P3 thuộc MVP; "Sau" là sau MVP.

## 1. Danh mục quy tắc nghiệp vụ

| Mã | Quy tắc | Phân hệ | GĐ | Nguồn |
|---|---|---|---|---|
| BR-01 | Mọi thao tác gọi AI bên ngoài (LLM, sinh ảnh, TTS) có giá bằng **chi phí thực của provider × 110%** (`price_rules`). Trước khi xác nhận, hệ thống hiện **giá ước tính tối đa**, tính từ độ dài đầu vào và giới hạn đầu ra (token, số ảnh, số ký tự). | M09 | P1 | QĐ-31, QĐ-32 |
| BR-02 | Vòng đời tiền của job: **HOLD** đúng giá ước tính tối đa khi tạo job → khi thành công **CAPTURE** chi phí thực × 110% và **RELEASE** phần dư; khi thất bại hoặc bị hủy RELEASE toàn bộ. Số trừ không bao giờ vượt số đã giữ. | M09 | P1 | QĐ-32 |
| BR-03 | Tiền trừ vào ví người kích hoạt thao tác. **MVP chỉ có Owner** nên luôn là ví Owner. *Sau MVP* (QĐ-42): trong dự án chung, Editor tiêu ví Owner không giới hạn; ví Owner không đủ thì Editor trả bằng ví mình; Editor không thấy và không nạp vào ví Owner; Owner được thông báo và xem báo cáo chi tiêu theo thành viên; Owner bị khóa thì Editor không làm được; Owner hạ gói thì Editor vẫn làm và tự trả. | M02/M09 | P1 / Sau | QĐ-42 |
| BR-04 | Chỉ Owner: mời/xóa thành viên, thu hồi link, đổi Settings, xóa dự án. | M02 | P1 | QS |
| BR-05 | Lưu đối tượng có version phải kèm `If-Match`; sai version thì từ chối. MVP báo "Dữ liệu đã thay đổi ở tab khác, tải lại"; hộp thoại xử lý xung đột giữa nhiều người (UC-02.10) làm sau MVP. | M02/M03 | P1 | QS |
| BR-06 | Sửa nội dung chương, tái cấu trúc chương hoặc dời ranh giới shot: thuyết minh của các shot có đoạn nguồn bị đổi chuyển `OUTDATED`, và clip tương ứng trên timeline được đánh dấu. | M05/M06 | P2 | QS + ĐX |
| BR-07 | Mỗi chương có tối đa 1 storyboard hiện hành. | M05 | P1 | QS |
| BR-08 | Thứ tự chỉ dẫn hình ảnh: Style → Art Direction → Visual Rules (dự án) → Visual Rules (chương) → Chapter rules → Shot brief. Chỉ dẫn sau có ưu tiên cao hơn khi mâu thuẫn. | M04/M05 | P1 | QS |
| BR-09 | Director không tạo job sinh ảnh khi chưa có style và chưa xác nhận cast; không sinh thuyết minh khi chưa chọn giọng. | M07 | Sau | QS + ĐX |
| BR-10 | Archive là bất biến. | M03 | Sau | QS |
| BR-11 | Chương chỉ "Sẵn sàng dựng" khi mọi shot của storyboard hiện hành có ảnh `DONE` và thuyết minh `DONE`. *Sau MVP, khi bật kiểm chứng ASR:* thuyết minh phải `VERIFIED` hoặc `ACCEPTED`. | M05 | P2 | QĐ-54 |
| BR-12 | Một chương bị khóa khi đang tái cấu trúc hoặc đang có job sinh tư liệu chạy trên nó; khóa tự hết khi thao tác kết thúc. | M03 | P2 | QS |
| BR-14 | Ảnh tham chiếu tải lên với cờ "use exact" không bao giờ bị AI vẽ lại, kể cả khi chạy "Regenerate all". Tương tự, shot có ảnh hiện hành là `UPLOAD` không bị thay bởi sinh ảnh hàng loạt (UC-05.07, UC-05.07c); chỉ thay khi Editor chủ động sinh/sửa ảnh của shot đó. | M04/M05 | P1 | QS + ĐX |
| BR-15 | Mỗi lần sinh lại ảnh hoặc clip tạo phiên bản mới; phiên bản cũ giữ 90 ngày. | M05/M06 | P1 | ĐX |
| BR-16 | Gỡ tài sản khỏi dự án không xóa ảnh đã sinh của shot; shot giữ `raw_name` và chuyển sang "chưa liên kết". | M04 | P1 | SL |
| BR-17 | Xóa thành viên thì job đang chạy của người đó vẫn hoàn tất, nhưng người đó không xem được kết quả. | M02 | Sau | ĐX |
| BR-18 | Nội dung bị moderation chặn: job `FAILED` với `CONTENT_POLICY`, RELEASE toàn bộ tiền đã giữ, không lưu đầu ra. **Không tự sửa văn bản để vượt bộ lọc.** | M10 | P1 | ĐX |
| **BR-19** | **Thuyết minh nguyên văn:** văn bản đưa vào TTS là đúng `chapter.content[sourceStart:sourceEnd]`. Chỉ được biến đổi ở mức phát âm: SSML break/alias/phoneme, **bỏ ký hiệu trình bày nhưng giữ chữ bên trong** (§6), đọc số. Không thêm, bớt, đổi, sắp xếp lại hay tóm tắt từ. | M05 | P2 | ĐX (yêu cầu khách hàng), QĐ-56 |
| **BR-20** | **Phủ kín:** các shot của storyboard hiện hành chia văn bản chương thành đoạn liên tục, không chồng lấn, không bỏ sót; mọi thao tác trên shot (tách, gộp, xóa, dời ranh giới) giữ nguyên bất biến này. | M05 | P1 | ĐX |
| **BR-21** | **Chỉ tác giả sửa văn bản:** văn bản chương chỉ thay đổi bởi thao tác trực tiếp của Owner/Editor (gõ, Find & replace, Re-import, khôi phục phiên bản). Không AI nào (Director, phân tích, storyboard) có quyền ghi văn bản chương. | M03/M07 | P1 | ĐX |
| **BR-22** | Phụ đề hiển thị **đúng nguyên văn** đoạn đang đọc, kể cả ký hiệu trình bày (`*Bố*`, `[…]`, `# …` hiện nguyên), ngắt dòng theo timestamp. Dòng phân cách (`---`, `***`) không có thuyết minh nên **không có phụ đề** ở khoảng lặng đó. | M06 | P3 | QĐ-56 |
| **BR-23** | Chỉ xuất video khi: độ phủ 100%; mọi shot có ảnh `DONE`; mọi shot có thuyết minh `DONE` (sau MVP: `VERIFIED` hoặc `ACCEPTED`); không clip nào `OUTDATED`; timeline thỏa BR-24. **Không bắt buộc** người dùng nghe hết thuyết minh; shot "cần sinh lại" (BR-34) chỉ là cảnh báo. | M06 | P3 | QĐ-55 |
| **BR-24** | **Khóa thuyết minh trên timeline:** clip thuyết minh không được cắt, trim, xóa, đổi thứ tự hay chồng lấn. Chỉ được (a) dời thời điểm (chèn khoảng lặng), (b) chỉnh âm lượng, (c) **đổi tốc độ trong khoảng 0,8×–1,25×**, giữ nguyên cao độ; clip ảnh và phụ đề co giãn theo. Số lượng và thứ tự clip do storyboard quyết định. | M06 | P3 | QĐ-53 |
| BR-25 | Clip ảnh của shot phải hiển thị suốt thời gian đọc đoạn của shot (được dài hơn, không ngắn hơn); chuyển cảnh, nhạc và SFX không được làm mất lời đọc (ducking bắt buộc khi nhạc chồng thuyết minh). | M06 | P3 | ĐX |
| BR-26 | Nhạc nền và SFX: **MVP chỉ dùng file người dùng tự tải lên**; người tải lên tự chịu trách nhiệm bản quyền, không có ô cam kết và không có quy trình gỡ nội dung. *Sau MVP:* thư viện hệ thống gồm bộ CC0/CC-BY tuyển chọn (Pixabay, Freesound); nhạc CC-BY tự sinh dòng ghi công vào clip kết hoặc file mô tả. | M06 | P3 / Sau | QĐ-27, QĐ-58 |
| BR-27 | **Trạng thái tài khoản:** *Free* hoặc *Đã nạp tiền*. "Đã nạp tiền" bật khi **tổng nạp tiền thật > 0** (tiền dùng thử không tính). Free bị giới hạn theo §3.3 và render có watermark; Đã nạp tiền bỏ giới hạn và watermark. Video đã render khi còn Free giữ watermark; render lại để có bản không watermark. | M09 | P1, P3 | QĐ-35, QĐ-36, QĐ-38 |
| BR-28 | **Tiền dùng thử:** tặng **$2 một lần** khi tạo hồ sơ (UC-01.01b), ghi bút toán `TRIAL_GRANT`, khác loại với `TOPUP`. Không tặng lại khi xóa và tạo lại hồ sơ cùng `sso_subject` hoặc cùng email. | M09 | P1 | QĐ-37, QĐ-38 |
| BR-29 | **Trần chi tiêu AI toàn hệ thống** mỗi ngày (closed beta: **$10**, cấu hình được). Trần tính trên **chi phí thật của provider** (chưa cộng phí 10%): chi phí đã phát sinh trong ngày cộng chi phí ước tính của các job đang chạy cộng job mới không được vượt trần, nếu vượt thì **từ chối job tốn phí mới** (`503 DAILY_BUDGET_EXCEEDED`); job đang chạy vẫn hoàn tất; gửi cảnh báo cho Admin. Kiểm tra và giữ chỗ phải **nguyên tử** (một câu cập nhật có điều kiện trên bộ đếm của ngày, cùng giao dịch với HOLD; ADR-25), để các yêu cầu đồng thời không thể cùng vượt trần. Ngày tính theo giờ Việt Nam (UTC+7); job tính vào ngày nó được tạo. | M10 | P2 | QĐ-39 |
| BR-30 | **Closed beta:** chỉ email có trong danh sách mời mới tạo được hồ sơ (so khớp không phân biệt hoa thường). Không có trong danh sách thì không tạo hồ sơ, không tạo phiên, không tặng tiền dùng thử. Người đã có hồ sơ vẫn đăng nhập được khi bị gỡ khỏi danh sách. Tắt quy tắc bằng cấu hình khi mở rộng. | M01 | P0 | QĐ-25 |
| BR-31 | **Đồng ý xử lý dữ liệu cá nhân:** lần đăng nhập đầu (hoặc khi nội dung thông báo đổi phiên bản), người dùng phải đồng ý trước khi dùng ứng dụng. Thông báo nêu dữ liệu thu thập (email, tên, truyện, file tải lên), mục đích (đồ án tốt nghiệp), thời hạn xóa (sau ngày bảo vệ). Lưu thời điểm và phiên bản đã đồng ý. Không đồng ý thì đăng xuất. | M01 | P0 | QĐ-26 |
| BR-32 | **Giới hạn kỹ thuật** (không liên quan tính phí): ≤ 30 yêu cầu LLM/phút/người; ≤ 8 job ảnh, 8 job TTS và 1 job render đồng thời/người. Vượt thì `429` kèm `Retry-After`. | M10 | P1 | QĐ-33 |
| BR-33 | **Dời ranh giới shot** chỉ làm ở Workspace, theo câu, giữa hai shot liền kề của storyboard hiện hành. Sau khi dời, AI viết lại brief của 2 shot bị ảnh hưởng: hệ thống hiện giá ước tính, Editor xác nhận thì mới dời và tạo job; hủy thì không dời. Thuyết minh của 2 shot chuyển `OUTDATED`. | M03/M05 | P2 | QĐ-52 |
| BR-34 | **Kiểm chứng thủ công:** mỗi shot có "Nghe" và "Đánh dấu cần sinh lại". Đánh dấu chỉ là ghi nhớ cho người dùng; không chặn xuất (BR-23) nhưng hiện cảnh báo trong báo cáo điều kiện xuất. Sinh lại thuyết minh thì xóa đánh dấu. | M05 | P2 | QĐ-54 |

## 2. Ma trận phân quyền

> **MVP chỉ có Owner** thao tác trên dự án của mình (QĐ-04). Cột Editor áp dụng khi có chức năng cộng tác (sau MVP).

| Hành động | Owner | Editor *(sau MVP)* | User ngoài dự án | Admin |
|---|:-:|:-:|:-:|:-:|
| Xem dự án, chương, tài sản, tư liệu, timeline, video | ✓ | ✓ | ✗ | ✓ (chỉ hỗ trợ, có audit) |
| Sửa bản thảo, chương, notes, archives | ✓ | ✓ | ✗ | ✗ |
| Sửa Story Assets, Visual Rules, Art Direction | ✓ | ✓ | ✗ | ✗ |
| Sinh tư liệu: storyboard, sinh/sửa ảnh | ✓ | ✓ | ✗ | ✗ |
| Thuyết minh: cài giọng, từ điển phát âm, sinh, nghe & đánh dấu | ✓ | ✓ | ✗ | ✗ |
| Trình chỉnh sửa: hiệu ứng, chuyển cảnh, phụ đề, nhạc nền, SFX, xuất video | ✓ | ✓ | ✗ | ✗ |
| Dùng Director (chat, auto) *(sau MVP)* | ✓ | ✓ | ✗ | ✗ |
| Tải MP4 / SRT | ✓ | ✓ | ✗ | ✗ |
| Settings dự án (style, model, ngôn ngữ, tỷ lệ khung hình, quy tắc ký hiệu) | ✓ | ✗ | ✗ | ✗ |
| Tạo / thu hồi link mời, xóa thành viên *(sau MVP)* | ✓ | ✗ | ✗ | ✗ |
| Xóa dự án | ✓ | ✗ | ✗ | ✓ (vi phạm chính sách) |
| Rời dự án *(sau MVP)* | ✗ (phải xóa dự án) | ✓ | — | — |
| Quản lý danh sách mời beta, xem cảnh báo trần chi tiêu | ✗ | ✗ | ✗ | ✓ |

> Owner đổi style dự án sau khi đã có ảnh thì không sinh lại tự động. Hệ thống gợi ý "Regenerate all" và hiện giá ước tính.

## 3. Bảng giá

### 3.1 Quy ước

- Đơn vị: **USD**. Mọi số tiền lưu bằng số nguyên **micro-USD** (1 USD = 1.000.000 µUSD) để không sai số làm tròn. Giao diện hiện USD với 2–4 chữ số thập phân, có thể kèm quy đổi VND theo tỷ giá cấu hình (chỉ để hiển thị).
- `price_rules.formula` của mọi thao tác AI: `ceil(cost_usd × 1,10)` tính bằng µUSD, trong đó `cost_usd` là chi phí thực ghi ở `ai_usage_records` của job (QĐ-31).
- Giá ước tính tối đa (BR-01) dùng đơn giá provider trong `ai_models.unit_cost_usd` và giới hạn đầu ra của từng thao tác ở §3.2.

### 3.2 Thao tác tính phí

| Mã thao tác (`price_rules.operation`) | Cơ sở tính chi phí thực | Giới hạn đầu ra dùng để ước tính | GĐ |
|---|---|---|---|
| `SUGGEST_SPLITS` | Token LLM | 2.000 token ra | P1 |
| `ANALYZE_ASSETS` | Token LLM (map theo chương + reduce) | 4.000 token ra mỗi chương | P1 |
| `STORY_META` (timeline truyện, quan hệ) | Token LLM | 4.000 token ra mỗi chương | P1 |
| `STORYBOARD_DRAFT` | Token LLM | 8.000 token ra mỗi chương | P1 |
| `REWRITE_SHOT` (gồm viết lại brief sau khi dời ranh giới, BR-33) | Token LLM | 1.000 token ra mỗi shot | P1 |
| `ASSET_REFERENCE_IMAGE` | Số ảnh × đơn giá ảnh | 1 ảnh | P1 |
| `SHOT_IMAGE` | Số ảnh × đơn giá ảnh | 1 ảnh | P1 |
| `IMAGE_EDIT` (Describe→Edit, Retry) | Số ảnh × đơn giá sửa ảnh | 1 ảnh | P1 |
| `NARRATION_TTS` | Số ký tự gửi TTS × đơn giá ký tự (+ chi phí aligner nếu dùng dịch vụ ngoài) | Số ký tự đoạn nguồn | P2 |
| `PRONUNCIATION_PREVIEW` | Số ký tự (≤ 200) | 200 ký tự | P2 |
| `REDIRECT`, Director chat | Token LLM | theo thao tác | Sau |
| `RENDER_TIMELINE` | — | **Miễn phí** trong giới hạn gói (QĐ-34) | P3 |
| `EXPORT_ZIP`, tải nhạc lên, thay ảnh bằng ảnh tải lên, nghe mẫu giọng có sẵn | — | Miễn phí | P3 / Sau |

> Đã bỏ: `MUSIC_AI`, `SFX_AI`, `SFX_SUGGEST` (QĐ-57); bảng giá credit cũ và "1 credit ≈ 1 ảnh".
> **Ước lượng tham khảo:** một chương 10.000 ký tự (khoảng 10 ảnh + 12 phút audio) tốn khoảng $0,5–1 tiền AI thực; $2 dùng thử đủ khoảng 1 chương (QĐ-37). Số liệu thật lấy từ PoC ở P0.

### 3.3 Trạng thái tài khoản (thay cho gói trong MVP)

| Trạng thái | Điều kiện | Giới hạn | Render |
|---|---|---|---|
| **Free** | Tổng nạp tiền thật = 0 | 1 dự án; 3 chương/dự án; 3 lần render/tháng; tổng 10 phút video/tháng | 720p, **watermark**: các đường kẻ chéo mờ kèm logo |
| **Đã nạp tiền** | Tổng nạp tiền thật > 0 (BR-27) | Không giới hạn số dự án, chương, lượt render (vẫn theo BR-32) | 720p hoặc 1080p, không watermark |

- Tháng tính theo lịch, giờ Việt Nam. Một lần render tính khi job render `READY`; render lỗi hoặc bị hủy không tính.
- Gói đăng ký tháng/năm (Starter, Creator, Studio) để **sau MVP** (QĐ-35); khi làm thì định nghĩa lại quyền lợi theo mô hình tính phí thực tế.

## 4. Quy tắc ví

| Mã | Quy tắc | GĐ |
|---|---|---|
| WR-01 | Mỗi người dùng có **một ví** USD: `available` (khả dụng), `held` (đang giữ), `topup_total` (tổng đã nạp thật, chỉ tăng). Không chia bucket. | P1 |
| WR-02 | Sổ cái chỉ ghi thêm. Loại bút toán: `TRIAL_GRANT` (tiền dùng thử, BR-28), `TOPUP` (nạp tiền thật qua cổng), `HOLD`, `CAPTURE`, `RELEASE`, `ADJUST` (Admin, sau MVP), `REFUND` (hoàn tiền thanh toán, sau MVP). | P1 |
| WR-03 | HOLD: `available -= x`, `held += x` trong cùng giao dịch với tạo job, dùng `SELECT … FOR UPDATE` trên ví. Không đủ `available` thì `402 INSUFFICIENT_BALANCE`. | P1 |
| WR-04 | Khi job xong: CAPTURE `c = min(chi phí thực × 110%, x)` (`held -= c`), RELEASE phần dư `x − c` (`held -= x − c`, `available += x − c`). Thất bại: RELEASE toàn bộ. | P1 |
| WR-05 | Job hàng loạt (Sinh tư liệu, Regenerate all): HOLD tổng ước tính trước; khi biết số shot thực tế thì giữ thêm hoặc trả lại; mỗi job con CAPTURE/RELEASE phần của nó. | P1 |
| WR-06 | TOPUP: chỉ ghi khi webhook của cổng xác nhận thanh toán (sandbox); `available += x`, `topup_total += x`. Số nạp tối thiểu $1, tối đa $100 mỗi lần [ĐX]. | P3 |
| WR-07 | Hoàn tiền thanh toán (refund/chargeback, sau MVP): ghi `REFUND` âm; số dư âm thì khóa thao tác tốn phí đến khi bù. | Sau |
| WR-08 | Admin điều chỉnh (sau MVP): `ADJUST` kèm `reason` bắt buộc và `actor_id`. | Sau |

Sơ đồ: `../so-do/05-hoat-dong/act-giu-tru-tien.puml`.

## 5. Quy tắc kiểm tra dữ liệu

| Trường | Ràng buộc |
|---|---|
| Tiêu đề dự án | 1–120 ký tự |
| Văn bản import | ≤ 500.000 ký tự; file ≤ 2 MB; .txt/.md/.docx |
| Nội dung một chương | ≤ 60.000 ký tự (vượt quá thì gợi ý chia) |
| Số chương / dự án | ≤ 200 (Free: ≤ 3) |
| Số dự án / người dùng | Free: 1; Đã nạp tiền: không giới hạn |
| Shot / bản nháp | 1–40 |
| Tên tài sản | 1–80 ký tự; bí danh ≤ 10 mục |
| Story Assets / dự án | ≤ 200 |
| Visual Rule | tên ≤ 80, nội dung ≤ 1.000 ký tự |
| Caption | ≤ 300 ký tự |
| Ảnh tải lên | PNG/JPEG/WebP ≤ 10 MB, ≥ 512px cạnh ngắn |
| Đoạn nguồn một shot | ≥ 1 câu; cảnh báo nếu > 30 s đọc (~450 ký tự tiếng Việt) |
| Từ điển phát âm | ≤ 500 mục / dự án; mỗi mục ≤ 100 ký tự |
| Tốc độ đọc của dự án | 0,8–1,3× |
| Tốc độ một clip thuyết minh trên timeline | 0,8–1,25× (BR-24) |
| Ngưỡng WER *(sau MVP)* | 0,01–0,10 (mặc định 0,03) |
| Nhạc / SFX tải lên | MP3/WAV/M4A ≤ 100 MB, ≤ 15 phút |
| Chuyển cảnh | 0–1.500 ms |
| Số tiền nạp một lần | $1–$100 [ĐX] |
| Email trong danh sách mời | Định dạng email hợp lệ, lưu chữ thường, duy nhất |
| Trần chi tiêu AI / ngày | > 0; mặc định $10 |
| Thành viên / dự án *(sau MVP)* | Định nghĩa khi có gói đăng ký |

## 6. Quy tắc đọc ký hiệu trình bày

Áp lên **bản đọc** ở bước chuẩn hóa phát âm (UC-05.13b). Văn bản chương và phụ đề giữ nguyên (BR-19, BR-22). Danh sách mặc định toàn hệ thống; mỗi dự án bật/tắt từng mẫu trong cài đặt thuyết minh (`narration_settings.symbol_rules`). Mẫu tắt thì ký hiệu được gửi nguyên cho TTS.

| Mã | Mẫu | Ví dụ | Đọc thành | Phụ đề |
|---|---|---|---|---|
| SYM-01 | `*…*`, `**…**`, `_…_` | `*Bố*` | Bố | `*Bố*` |
| SYM-02 | `[ … ]` (khung tin nhắn) | `[Về ăn cơm]` | Về ăn cơm | `[Về ăn cơm]` |
| SYM-03 | `~~…~~` | `~~xóa~~` | xóa | `~~xóa~~` |
| SYM-04 | `#` đầu dòng (tiêu đề phụ) | `# Hồi 2` | Hồi 2 | `# Hồi 2` |
| SYM-05 | `---`, `***` (dòng phân cách) | | Không đọc; khoảng lặng 0,5 s | Không có phụ đề |

- Độ phủ (NFR-INT-01) vẫn tính trên **toàn bộ** ký tự chương, gồm cả ký hiệu: ký hiệu thuộc đoạn nguồn của shot.
- Mọi biến đổi được ghi vào `narrations.normalization_log` để truy vết.

# 01 — Tài liệu yêu cầu nghiệp vụ (BRD)

## 1. Bối cảnh

Người viết truyện dài (tác giả web novel, người viết fanfic, kênh "đọc truyện" trên YouTube/TikTok, giáo viên) muốn biến tác phẩm thành **video đọc truyện có hình minh họa**: người xem nghe **toàn văn câu chuyện** do giọng đọc thể hiện, trong khi màn hình trình chiếu ảnh minh họa đúng với đoạn đang được đọc. Gặp bốn vấn đề chính:

1. **Thiếu nhất quán:** công cụ sinh ảnh AI tạo ảnh rời rạc; nhân vật đổi mặt, đổi trang phục giữa các cảnh và chương.
2. **Khối lượng lớn:** một tiểu thuyết có hàng chục chương, mỗi chương cần 8–30 ảnh. Viết prompt và căn ảnh khớp lời đọc bằng tay mất nhiều ngày.
3. **AI hay "sáng tác thêm":** công cụ video AI thường tóm tắt hoặc viết lại truyện, làm sai lệch tác phẩm gốc. **Tác giả cần lời đọc đúng nguyên văn.**
4. **Chi phí video AI cao:** sinh video bằng AI tốn kém và khó kiểm soát; với video đọc truyện, ảnh tĩnh có chuyển động nhẹ, dựng trên một trình chỉnh sửa video, là đủ và rẻ hơn nhiều lần.

Hệ thống cần một **Studio theo dự án** với luồng 6 bước: **nhập truyện → chia chương → AI dựng thế giới truyện → AI sinh tư liệu (ảnh + thuyết minh nguyên văn) → chỉnh sửa video trên timeline (chuyển cảnh, nhạc nền, SFX, tinh chỉnh) → xuất & tải video**. Studio có "bộ nhớ thế giới truyện" (Story Assets, Timeline, Relationships, Visual Rules) để giữ nhất quán, và có AI Director để tự động hóa khi người dùng muốn.

## 2. Mục tiêu kinh doanh

| Mã | Mục tiêu | KPI | Mục tiêu MVP [ĐX] |
|---|---|---|---|
| BO-01 | Rút ngắn thời gian chuyển thể | Thời gian trung vị từ import đến video chương đầu tiên | ≤ 30 phút (chế độ Director) |
| BO-02 | Nhân vật nhất quán | Tỷ lệ shot bị sinh lại vì sai ngoại hình nhân vật | ≤ 15% |
| BO-03 | **Trung thành với nguyên tác** | Tỷ lệ văn bản chương được đọc trong video (độ phủ) | **100%** (bắt buộc) |
| BO-04 | Chất lượng lời đọc | Tỷ lệ lỗi từ (WER) giữa audio và văn bản gốc | ≤ 3% |
| BO-05 | Doanh thu định kỳ | Tỷ lệ người dùng Studio trả phí | ≥ 5% |
| BO-06 | Kiểm soát chi phí | Chi phí AI trung bình trên mỗi phút video | ≤ $0,15 |

## 3. Các bên liên quan

| Bên liên quan | Vai trò | Mối quan tâm |
|---|---|---|
| Owner (chủ dự án) | Tạo và sở hữu dự án, mời cộng tác | Toàn quyền, chi phí credit, **tác phẩm không bị sửa** |
| Editor (cộng tác viên) | Cùng biên tập dự án | Không ghi đè dữ liệu của nhau |
| Người xem video (gián tiếp) | Nghe và xem video trên mạng xã hội | Giọng đọc rõ, hình khớp lời, phụ đề đúng |
| Quản trị viên | Vận hành hệ thống | Cấu hình giá, provider AI, giám sát job |
| Đội sản phẩm / tài chính | Định giá | Chi phí AI theo job, doanh thu |
| Nhà cung cấp AI, cổng thanh toán | Dịch vụ ngoài | Hạn mức, SLA |

## 4. Phạm vi

### 4.1 Trong phạm vi

| Mã | Phân hệ | Loại | Mô tả |
|---|---|---|---|
| M01 | Tích hợp SSO & hồ sơ | Phụ trợ | **Dùng SSO có sẵn (vd. SSO Vbee), không tự phát triển** đăng ký, đăng nhập, đăng xuất, mật khẩu. Ứng dụng chỉ tích hợp (OIDC), tạo hồ sơ cục bộ từ thông tin SSO, Dashboard |
| M02 | Quản lý dự án & cộng tác | **Lõi** | Danh sách dự án, import (giữ nguyên văn), cài đặt, chia sẻ qua link, vai trò Owner/Editor, xử lý xung đột, Map |
| M03 | Bản thảo & chương | **Lõi** | Văn bản gốc, Workspace, chia/gộp/sắp xếp chương, Find & replace, Archives, Notes, phiên bản |
| M04 | Thế giới truyện | **Lõi** | Story Assets, Art Direction, Timeline, Relationships, Visual Rules |
| M05 | **Sinh tư liệu** | **Lõi** | Storyboard tự động **phủ kín văn bản**; sinh và sửa ảnh minh họa; thuyết minh nguyên văn (TTS) + kiểm chứng lời đọc; Tư liệu dự án (media bin). **Đầu ra chỉ gồm ảnh + thuyết minh** |
| M06 | **Trình chỉnh sửa & xuất video** | **Lõi** | Timeline nhiều track: ảnh + Ken Burns, chuyển cảnh, phụ đề nguyên văn, overlay chữ, tinh chỉnh màu, **nhạc nền, SFX**, trộn âm; track thuyết minh khóa; xem trước; xuất MP4 và tải xuống |
| M07 | AI Director | **Lõi** | Trợ lý chat và chế độ tự động có điểm duyệt; **không sửa văn bản truyện** |
| M08 | Thư viện tài sản cá nhân | Phụ trợ | Tái sử dụng nhân vật, địa điểm, đạo cụ giữa các dự án |
| M09 | Credit & thanh toán | Phụ trợ | Ví credit, gói đăng ký, gói credit, sổ cái, hóa đơn |
| M10 | Quản trị | Phụ trợ | Bảng giá credit, provider/mô hình AI, giọng đọc, thư viện nhạc & SFX, giám sát job |

### 4.2 Ngoài phạm vi

Video sinh bằng AI (image-to-video, Animated Book, Video Storyboard có kịch bản cảnh); **sách tranh** (Compile book, trình đọc, PDF); AI viết lại, tóm tắt hoặc chuyển giọng văn bản truyện; Explore và thư viện cộng đồng; Create nhanh; Remix; Chat nhân vật; Guide cộng đồng; bán sách và chia doanh thu; API công khai; ứng dụng di động native; in sách vật lý.

## 5. Quy trình nghiệp vụ chính

Sơ đồ tổng thể: `../so-do/05-hoat-dong/act-quy-trinh-project.puml`.

| Mã | Quy trình | Các bước |
|---|---|---|
| BP-01 | Khởi tạo dự án | Import văn bản (luôn giữ nguyên văn) → chọn style và **tỷ lệ khung hình video** → Project có Chapter 1 |
| BP-02 | Cấu trúc truyện | Gợi ý hoặc chia chương thủ công → sắp xếp/gộp → lưu Archive trước khi tái cấu trúc lớn |
| BP-03 | Dựng thế giới | AI phân tích tài sản → duyệt cast/địa điểm/đạo cụ → sinh ảnh tham chiếu → Art Direction, Visual Rules; AI dựng Timeline và Relationships |
| BP-04 | **Sinh tư liệu** | Chọn giọng đọc → "Sinh tư liệu" cho chương: storyboard **tự động** (các shot chia toàn bộ văn bản chương thành đoạn liên tục) → song song sinh **ảnh** và **thuyết minh nguyên văn** cho từng shot → kiểm chứng lời đọc (WER) → sửa ảnh hoặc phát âm nếu cần → chương "Sẵn sàng dựng" |
| BP-05 | **Chỉnh sửa video** | Mở trình chỉnh sửa (bản nháp timeline dựng sẵn từ tư liệu) → hiệu ứng ảnh, chuyển cảnh → **thêm nhạc nền, SFX** từ thư viện, file tải lên hoặc AI (tùy chọn) → phụ đề, overlay chữ, tinh chỉnh màu, trộn âm → xem trước |
| BP-06 | **Xuất & tải video** | Kiểm tra điều kiện (độ phủ 100%, thuyết minh đã kiểm chứng) → xuất MP4 → tải MP4, SRT/VTT, audio |
| BP-09 | Tự động hóa | AI Director chạy BP-02 → BP-04 và dựng sẵn bản nháp timeline, dừng ở điểm duyệt (style, cast, giọng đọc, thuyết minh); người dùng tự chỉnh sửa và xuất ở BP-05, BP-06 |
| BP-07 | Cộng tác | Owner tạo link → Editor tham gia → cùng sửa; xung đột được phát hiện khi lưu |
| BP-08 | Chi trả | Nạp credit → job AI giữ credit → quyết toán khi xong |

## 6. Quy tắc nghiệp vụ chính

Chi tiết nằm ở [08](08-quy-tac-nghiep-vu.md).

| Mã | Quy tắc |
|---|---|
| BR-01 | Mọi thao tác AI tốn phí có giá cấu hình được, hiển thị **trước** khi xác nhận. |
| BR-02 | Credit bị **giữ** khi job bắt đầu, **trừ** khi thành công và **hoàn** khi thất bại. |
| BR-04 | Chỉ Owner được mời hoặc xóa thành viên, đổi cài đặt và xóa dự án. |
| BR-05 | Lưu chương dùng khóa lạc quan (version); không có ghi đè ngầm. |
| BR-06 | Sửa văn bản chương thì thuyết minh (và clip tương ứng trên timeline) của các shot bị ảnh hưởng chuyển `OUTDATED`. |
| BR-09 | AI Director không sinh ảnh hoặc audio khi chưa có style, chưa duyệt cast và chưa chọn giọng. |
| **BR-19** | **Thuyết minh nguyên văn:** văn bản đưa vào TTS là đúng đoạn văn gốc của chương; không AI nào được chỉnh sửa, tóm tắt hay diễn giải. |
| **BR-20** | **Phủ kín:** các shot của storyboard hiện hành chia văn bản chương thành các đoạn **liên tục, không chồng lấn, không bỏ sót**; nối lại theo thứ tự phải bằng đúng văn bản chương. |
| **BR-21** | **Chỉ tác giả sửa văn bản:** văn bản truyện chỉ thay đổi bởi thao tác trực tiếp của Owner/Editor (gõ, Find & replace, Re-import). |
| **BR-22** | Phụ đề hiển thị **đúng nguyên văn** đoạn đang đọc. |
| **BR-23** | Video chỉ được xuất khi mọi shot có thuyết minh đạt kiểm chứng (WER ≤ ngưỡng) hoặc đã được chấp nhận thủ công, và độ phủ văn bản 100%. |
| **BR-24** | Trong trình chỉnh sửa, track thuyết minh **khóa nội dung**: không cắt, xóa, đảo thứ tự, đổi tốc độ; chỉ dời thời điểm và chỉnh âm lượng. |

## 7. Giả định và ràng buộc

- **A-01:** Có nhà cung cấp AI thương mại cho: LLM có structured output; sinh ảnh có ảnh tham chiếu; chỉnh ảnh theo mask; **TTS chất lượng cao cho tiếng Việt và tiếng Anh, trả timestamp hoặc cho phép forced alignment**; STT để kiểm chứng.
- **A-02:** Người dùng chấp nhận chờ bất đồng bộ (vài giây với ảnh, vài phút với audio và render một chương).
- **A-03:** SSO có sẵn hỗ trợ **OpenID Connect** (Authorization Code + PKCE), có discovery document, JWKS, `end_session_endpoint`; cấp cho ứng dụng một `client_id`/`client_secret` riêng. *Cần xác nhận với đội SSO; xem câu hỏi mở ở 09.*
- **C-01:** Clean-room, xem README §3.
- **C-05:** Không phát triển chức năng đăng ký, đăng nhập, đăng xuất, quên/đổi mật khẩu, xác minh email, đăng nhập mạng xã hội hay MFA. Các chức năng này thuộc SSO có sẵn.
- **C-02:** Tuân thủ Nghị định 13/2023/NĐ-CP. Không lưu thẻ (PCI-DSS SAQ-A).
- **C-03:** Văn bản truyện là tài sản trí tuệ của người dùng; không được dùng để huấn luyện mô hình; **không bị AI biến đổi**.
- **C-04:** Nhạc nền và SFX phải có giấy phép rõ ràng (thư viện có license, nhạc người dùng tải lên kèm cam kết bản quyền, hoặc nhạc AI có quyền thương mại).

## 8. Rủi ro

| Mã | Rủi ro | Mức | Biện pháp |
|---|---|---|---|
| R-01 | Chi phí AI vượt doanh thu credit | Trung bình | Bảng giá cấu hình; ghi chi phí thực từng job. Không có video AI nên chi phí chủ yếu ở ảnh và TTS |
| R-02 | Nội dung vi phạm trong văn bản hoặc ảnh | Cao | Moderation đầu vào và đầu ra. Văn bản không bị sửa, nên khi vi phạm thì chặn và báo tác giả, không tự làm mềm câu chữ |
| R-03 | Phụ thuộc một nhà cung cấp AI | Trung bình | Adapter provider, chuyển đổi qua cấu hình |
| R-04 | Mất dữ liệu khi tái cấu trúc chương | Trung bình | Archive, version chương, giao dịch DB |
| R-05 | Văn bản dài vượt context LLM | Trung bình | Xử lý theo chương; tóm tắt cuốn chiếu **chỉ dùng nội bộ cho ngữ cảnh**, không bao giờ đưa vào audio |
| **R-06** | **TTS đọc sai hoặc bỏ chữ** (số, từ mượn, tên riêng, từ Hán Việt) | Cao | Kiểm chứng WER bằng STT/alignment; từ điển phát âm theo dự án; cho phép sinh lại từng shot |
| **R-07** | **LLM chia shot không phủ kín văn bản** | Cao | Validator phía server + thuật toán sửa ranh giới tất định (`act-phu-kin-van-ban.puml`) |
| R-08 | Một đoạn văn dài khiến một ảnh đứng quá lâu, gây nhàm | Trung bình | Cảnh báo ảnh > 30 s; gợi ý tách shot; Ken Burns nhiều pha |
| R-11 | Trình chỉnh sửa timeline trên web phức tạp, chậm với video dài | Trung bình | Dùng thư viện timeline/preview có sẵn (Remotion); ảo hóa danh sách clip; chỉnh theo chương |
| R-09 | SSO gián đoạn thì người dùng không đăng nhập được | Trung bình | Phiên ứng dụng vẫn hiệu lực đến hết hạn; trang lỗi thân thiện; theo dõi uptime SSO |
| R-10 | SSO không hỗ trợ chuẩn OIDC đầy đủ (vd. thiếu logout hoặc JWKS) | Trung bình | Xác nhận năng lực SSO ở P0; adapter xác thực tách riêng để thích nghi |

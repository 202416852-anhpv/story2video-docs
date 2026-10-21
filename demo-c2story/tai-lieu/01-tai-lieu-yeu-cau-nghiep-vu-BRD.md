# 01 — Tài liệu yêu cầu nghiệp vụ (BRD)

## 1. Bối cảnh

Người viết truyện dài (tác giả web novel, người viết fanfic, kênh "đọc truyện" trên YouTube/TikTok, giáo viên) muốn biến tác phẩm thành **video đọc truyện có hình minh họa**: người xem nghe **toàn văn câu chuyện** do giọng đọc thể hiện, trong khi màn hình trình chiếu ảnh minh họa đúng với đoạn đang được đọc. Gặp bốn vấn đề chính:

1. **Thiếu nhất quán:** công cụ sinh ảnh AI tạo ảnh rời rạc; nhân vật đổi mặt, đổi trang phục giữa các cảnh và chương.
2. **Khối lượng lớn:** một tiểu thuyết có hàng chục chương, mỗi chương cần 8–30 ảnh. Viết prompt và căn ảnh khớp lời đọc bằng tay mất nhiều ngày.
3. **AI hay "sáng tác thêm":** công cụ video AI thường tóm tắt hoặc viết lại truyện, làm sai lệch tác phẩm gốc. **Tác giả cần lời đọc đúng nguyên văn.**
4. **Chi phí video AI cao:** sinh video bằng AI tốn kém và khó kiểm soát; với video đọc truyện, ảnh tĩnh có chuyển động nhẹ, dựng trên một trình chỉnh sửa video, là đủ và rẻ hơn nhiều lần.

Hệ thống cần một **Studio theo dự án** với luồng 6 bước: **nhập truyện → chia chương → AI dựng thế giới truyện → AI sinh tư liệu (ảnh + thuyết minh nguyên văn) → chỉnh sửa video trên timeline (chuyển cảnh, nhạc nền, SFX) → xuất & tải video**. Studio có "bộ nhớ thế giới truyện" (Story Assets, Timeline, Relationships, Visual Rules) để giữ nhất quán.

**Bối cảnh dự án:** đây là **đồ án tốt nghiệp** của nhóm 3 người (full-stack, 20 giờ/tuần/người, có Coding Agent hỗ trợ), thời gian phát triển 7 tháng (đã gồm 20% dự phòng), sau đó 2 tháng viết báo cáo và bảo vệ. Sản phẩm được thử nghiệm bằng **closed beta 10–20 người dùng được mời**. Thanh toán chạy ở chế độ sandbox. Chi tiết quyết định ở [sổ quyết định](../quyet-dinh.md).

## 2. Mục tiêu kinh doanh

| Mã | Mục tiêu | KPI | Mục tiêu MVP [ĐX] | Cách đo trong đồ án |
|---|---|---|---|---|
| BO-01 | Rút ngắn thời gian chuyển thể | Thời gian trung vị từ import đến video chương đầu tiên | ≤ 60 phút (thao tác tay, chương 10.000 ký tự) | Đo trong closed beta |
| BO-02 | Nhân vật nhất quán | Tỷ lệ shot bị sinh lại vì sai ngoại hình nhân vật | ≤ 15% (provider chọn ở P0 phải ≤ 10% trên golden set) | `EVAL-consistency` (rubric, 2 người chấm, QĐ-110), thống kê beta |
| BO-03 | **Trung thành với nguyên tác** | Tỷ lệ văn bản chương được đọc trong video (độ phủ) | **100%** (bắt buộc) | Kiểm tra tự động trước mỗi render |
| BO-04 | Chất lượng lời đọc | Tỷ lệ lỗi từ (WER) giữa audio và văn bản gốc, đã trừ WER nền của ASR | ≤ 3% | Bảo đảm ở **khâu chọn provider** (`EVAL-wer-golden`, P0, QĐ-111); không kiểm tra từng shot lúc chạy trong MVP (QĐ-54) |
| BO-05 | Khả năng thu phí | Tỷ lệ người dùng beta nạp tiền (sandbox) sau khi dùng hết tiền dùng thử | ≥ 20% người dùng beta | Sổ cái ví; câu hỏi khảo sát nếu cắt nạp tiền sandbox (✂1, QĐ-116) |
| BO-06 | Kiểm soát chi phí | Chi phí AI trung bình trên mỗi phút video | ≤ $0,15 | `EVAL-cost-per-minute` ở P0 (QĐ-112), `ai_usage_records` khi beta |

## 3. Các bên liên quan

| Bên liên quan | Vai trò | Mối quan tâm |
|---|---|---|
| Owner (chủ dự án) | Tạo và sở hữu dự án | Toàn quyền, chi phí, **tác phẩm không bị sửa** |
| Editor (cộng tác viên, sau MVP) | Cùng biên tập dự án | Không ghi đè dữ liệu của nhau |
| Người dùng closed beta | Dùng thử và trả lời khảo sát | Dễ dùng, dữ liệu cá nhân được bảo vệ và xóa sau đồ án |
| Người xem video (gián tiếp) | Nghe và xem video trên mạng xã hội | Giọng đọc rõ, hình khớp lời, phụ đề đúng |
| Quản trị viên | Vận hành hệ thống | Cấu hình giá, provider AI, danh sách mời, trần chi tiêu |
| Product Owner | Chốt phạm vi, **trả chi phí AI** và đăng ký tài khoản provider | Ngân sách không vượt, đồ án đúng hạn |
| Nhóm phát triển (3 người) | Thiết kế, phát triển, kiểm thử | Phạm vi vừa năng lực |
| Hội đồng bảo vệ | Đánh giá đồ án | Tính đúng đắn, pháp lý (thanh toán, dữ liệu cá nhân), demo chạy được |
| Vbee (đối tác SSO) | Cung cấp SSO và tài liệu tích hợp | Tích hợp đúng chuẩn của họ |
| Nhà cung cấp AI, cổng thanh toán | Dịch vụ ngoài | Hạn mức, SLA |

## 4. Phạm vi

### 4.1 Trong phạm vi

| Mã | Phân hệ | Loại | Mô tả | MVP (hết P3) |
|---|---|---|---|---|
| M01 | Tích hợp SSO & hồ sơ | Phụ trợ | **Dùng SSO có sẵn, không tự phát triển** đăng ký, đăng nhập, đăng xuất, mật khẩu. Keycloak tự dựng từ P0, **SSO Vbee bắt buộc trước khi bảo vệ**. Tạo hồ sơ cục bộ từ thông tin SSO, danh sách mời beta, đồng ý xử lý dữ liệu, Dashboard | Có (trừ back-channel logout, tự xóa dữ liệu) |
| M02 | Quản lý dự án & cộng tác | **Lõi** | Danh sách dự án, import (giữ nguyên văn), cài đặt, Map; chia sẻ qua link, vai trò Owner/Editor, xử lý xung đột | Có, **chỉ Owner**; cộng tác sau MVP |
| M03 | Bản thảo & chương | **Lõi** | Văn bản gốc, Workspace, chia/gộp/sắp xếp chương, dời ranh giới shot; Find & replace, Archives, Notes, phiên bản | Có (trừ Find & replace, Archives, Notes, phiên bản) |
| M04 | Thế giới truyện | **Lõi** | Story Assets, Art Direction, Timeline, Relationships, Visual Rules | Có |
| M05 | **Sinh tư liệu** | **Lõi** | Storyboard tự động **phủ kín văn bản**; sinh và sửa ảnh minh họa; thuyết minh nguyên văn (TTS); nghe & đánh dấu cần sinh lại; Tư liệu dự án (media bin). **Đầu ra chỉ gồm ảnh + thuyết minh** | Có (trừ nhiều bản nháp, chapter rules, đa giọng, kiểm chứng ASR) |
| M06 | **Trình chỉnh sửa & xuất video** | **Lõi** | Timeline nhiều track: ảnh + Ken Burns, chuyển cảnh, phụ đề nguyên văn, **nhạc nền, SFX tải lên**, ducking; track thuyết minh khóa; xem trước; xuất MP4 và tải xuống | Có (trừ overlay, tinh chỉnh màu, thư viện âm thanh, lịch sử phiên bản) |
| M07 | AI Director | **Lõi** | Trợ lý chat và chế độ tự động có điểm duyệt; **không sửa văn bản truyện** | Sau MVP |
| M08 | Thư viện tài sản cá nhân | Phụ trợ | Tái sử dụng nhân vật, địa điểm, đạo cụ giữa các dự án | Sau MVP |
| M09 | Ví & thanh toán | Phụ trợ | Ví USD, tiền dùng thử, giữ/trừ/hoàn theo chi phí thực × 110%, giới hạn Free, nạp tiền sandbox, sổ cái; gói đăng ký | Có (trừ gói đăng ký, portal) |
| M10 | Quản trị | Phụ trợ | Bảng giá, provider/mô hình AI, giọng đọc, danh sách mời, trần chi tiêu; giám sát job, báo cáo | Có, qua file cấu hình; giao diện sau MVP |

### 4.2 Ngoài phạm vi

Video sinh bằng AI (image-to-video, Animated Book, Video Storyboard có kịch bản cảnh); **sách tranh** (Compile book, trình đọc, PDF); AI viết lại, tóm tắt hoặc chuyển giọng văn bản truyện; **AI sinh nhạc/SFX và gợi ý SFX** (QĐ-57); **sửa vùng tô trên ảnh (inpainting)** (QĐ-51); thanh toán thật (chỉ sandbox); tiền mã hóa; Explore và thư viện cộng đồng; Create nhanh; Remix; Chat nhân vật; Guide cộng đồng; bán sách và chia doanh thu; API công khai; ứng dụng di động native; in sách vật lý.

## 5. Quy trình nghiệp vụ chính

Sơ đồ tổng thể: `../so-do/05-hoat-dong/act-quy-trinh-project.puml`.

| Mã | Quy trình | Các bước |
|---|---|---|
| BP-00 | Tham gia beta | Admin thêm email vào danh sách mời → người dùng đăng nhập qua SSO → hệ thống tạo hồ sơ, ví và tặng $2 dùng thử (JIT) → người dùng đồng ý xử lý dữ liệu rồi mới dùng Studio |
| BP-01 | Khởi tạo dự án | Import văn bản (luôn giữ nguyên văn) → chọn style và **tỷ lệ khung hình video** → Project có Chapter 1 |
| BP-02 | Cấu trúc truyện | Gợi ý hoặc chia chương thủ công → sắp xếp/gộp |
| BP-03 | Dựng thế giới | AI phân tích tài sản → duyệt cast/địa điểm/đạo cụ → sinh ảnh tham chiếu → Art Direction, Visual Rules; AI dựng Timeline và Relationships |
| BP-04 | **Sinh tư liệu** | Chọn giọng đọc → "Sinh tư liệu" cho chương: storyboard **tự động** (các shot chia toàn bộ văn bản chương thành đoạn liên tục) → song song sinh **ảnh** và **thuyết minh nguyên văn** cho từng shot → người dùng nghe, đánh dấu shot cần sinh lại (không bắt buộc) → sửa ảnh hoặc phát âm nếu cần → chương "Sẵn sàng dựng" |
| BP-05 | **Chỉnh sửa video** | Mở trình chỉnh sửa (bản nháp timeline dựng sẵn từ tư liệu) → hiệu ứng ảnh, chuyển cảnh → **thêm nhạc nền, SFX** từ file tải lên → phụ đề → xem trước |
| BP-06 | **Xuất & tải video** | Kiểm tra điều kiện (độ phủ 100%, ảnh và thuyết minh `DONE`) → xuất MP4 (Free: 720p có watermark, trong giới hạn tháng) → tải MP4, SRT/VTT, audio |
| BP-07 | Cộng tác *(sau MVP)* | Owner tạo link → Editor tham gia → cùng sửa; xung đột được phát hiện khi lưu |
| BP-08 | Chi trả | Dùng tiền dùng thử hoặc nạp tiền (sandbox) → mỗi job AI giữ giá ước tính tối đa → trừ chi phí thực × 110%, hoàn phần dư |
| BP-09 | Tự động hóa *(sau MVP)* | AI Director chạy BP-02 → BP-04 và dựng sẵn bản nháp timeline, dừng ở điểm duyệt |

## 6. Quy tắc nghiệp vụ chính

Chi tiết nằm ở [08](08-quy-tac-nghiep-vu.md).

| Mã | Quy tắc |
|---|---|
| BR-01 | Mọi thao tác AI có giá bằng **chi phí thực × 110%**; giá ước tính tối đa hiển thị **trước** khi xác nhận. |
| BR-02 | Tiền bị **giữ** theo giá ước tính khi job bắt đầu, **trừ** chi phí thực × 110% khi thành công, **hoàn** phần dư hoặc toàn bộ khi thất bại. |
| BR-04 | Chỉ Owner được đổi cài đặt và xóa dự án (mời, xóa thành viên: sau MVP). |
| BR-05 | Lưu chương dùng khóa lạc quan (version); không có ghi đè ngầm. |
| BR-06 | Sửa văn bản chương thì thuyết minh (và clip tương ứng trên timeline) của các shot bị ảnh hưởng chuyển `OUTDATED`. |
| **BR-19** | **Thuyết minh nguyên văn:** văn bản đưa vào TTS là đúng đoạn văn gốc của chương; chỉ bỏ ký hiệu trình bày khi đọc, không AI nào được chỉnh sửa, tóm tắt hay diễn giải. |
| **BR-20** | **Phủ kín:** các shot của storyboard hiện hành chia văn bản chương thành các đoạn **liên tục, không chồng lấn, không bỏ sót**; nối lại theo thứ tự phải bằng đúng văn bản chương. |
| **BR-21** | **Chỉ tác giả sửa văn bản:** văn bản truyện chỉ thay đổi bởi thao tác trực tiếp của Owner/Editor (gõ, Find & replace, Re-import). |
| **BR-22** | Phụ đề hiển thị **đúng nguyên văn** đoạn đang đọc, kể cả ký hiệu trình bày. |
| **BR-23** | Video chỉ được xuất khi độ phủ văn bản 100%, mọi shot có ảnh và thuyết minh `DONE`, không clip nào `OUTDATED`. Không bắt buộc người dùng nghe hết. |
| **BR-24** | Trong trình chỉnh sửa, track thuyết minh **khóa nội dung**: không cắt, xóa, đảo thứ tự; chỉ dời thời điểm và chỉnh âm lượng. Tốc độ đọc đặt một lần cho cả dự án ở bước sinh thuyết minh. |
| BR-27 | Tài khoản Free bị giới hạn (1 dự án, 3 chương, 3 lần render và 10 phút video mỗi tháng, watermark) cho tới khi **nạp tiền thật**. |
| BR-29 | Trần chi tiêu AI toàn hệ thống **$10/ngày** trong closed beta. |
| BR-30 | Closed beta chỉ nhận người dùng có email trong **danh sách mời**. |
| BR-31 | Người dùng phải **đồng ý xử lý dữ liệu cá nhân** ở lần đăng nhập đầu. |

## 7. Giả định và ràng buộc

- **A-01:** Có nhà cung cấp AI thương mại cho: LLM có structured output; sinh ảnh có ảnh tham chiếu; sửa ảnh theo mô tả; **TTS chất lượng cao cho tiếng Việt và tiếng Anh, trả timestamp hoặc cho phép forced alignment**; STT để đánh giá WER ở P0.
- **A-02:** Người dùng chấp nhận chờ bất đồng bộ (vài giây với ảnh, vài phút với audio và render một chương).
- **A-03:** SSO Vbee hỗ trợ **OpenID Connect** (Authorization Code + PKCE, discovery, JWKS, `end_session_endpoint`) và cấp cho ứng dụng `client_id`/`client_secret`. **Chưa xác nhận**: các đường dẫn discovery chuẩn của `auth.vbee.vn` trả 404. Hạn có tài liệu: hết tháng thứ 2; quá hạn thì giữ Keycloak cho bản bảo vệ (QĐ-21, QĐ-22). Nếu Vbee chỉ có OAuth 2.0, làm thêm adapter userinfo (QĐ-23).
- **A-04:** Coding Agent giúp nhóm đạt ít nhất 1,5 lần năng suất (QĐ-81); kiểm chứng bằng vận tốc thực ở mốc T8 (QĐ-94).
- **C-01:** Clean-room, xem README §3.
- **C-02:** Tuân thủ Nghị định 13/2023/NĐ-CP: màn hình đồng ý xử lý dữ liệu, lưu thời điểm đồng ý, xóa dữ liệu beta sau ngày bảo vệ. Không lưu thẻ (PCI-DSS SAQ-A).
- **C-03:** Văn bản truyện là tài sản trí tuệ của người dùng; không được dùng để huấn luyện mô hình; **không bị AI biến đổi**. Người dùng tự chịu trách nhiệm bản quyền nội dung họ đưa vào (truyện, ảnh, nhạc).
- **C-04:** MVP chỉ dùng nhạc/SFX người dùng tải lên; thư viện CC0/CC-BY có ghi công làm sau MVP (QĐ-58).
- **C-05:** Không phát triển chức năng đăng ký, đăng nhập, đăng xuất, quên/đổi mật khẩu, xác minh email, đăng nhập mạng xã hội hay MFA. Các chức năng này thuộc SSO.
- **C-06:** Đồ án tốt nghiệp: 7 tháng phát triển (khoảng 24 tuần làm việc sau dự phòng), MVP = hết P3, nhóm 3 người (QĐ-01..03).
- **C-07:** Ngân sách AI do PO trả: P0 $200, P1–P3 $50/tháng, UAT $200; trần $10/ngày trong closed beta (QĐ-39, QĐ-40). Đơn vị tiền là USD; **không dùng tiền mã hóa**; thanh toán chỉ ở chế độ sandbox (QĐ-30).

## 8. Rủi ro

> Rủi ro có trong bảng rủi ro triển khai (09 §5) chỉ ghi mã và tên ở đây; mức và ứng phó xem 09 §5, nơi được rà ở mỗi buổi retro. Các rủi ro còn lại có nguồn tại bảng này (QĐ-146).

| Mã | Rủi ro | Mức | Biện pháp |
|---|---|---|---|
| R-01 | Chi phí AI vượt ngân sách của PO | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-02 | Nội dung vi phạm trong văn bản hoặc ảnh | Cao | MVP dựa vào bộ lọc an toàn có sẵn của Gemini cho prompt và ảnh; không kiểm duyệt văn bản truyện của chính người dùng (QĐ-135). Văn bản truyện không bị sửa, nên khi vi phạm thì chặn và báo tác giả, không tự làm mềm câu chữ; brief ảnh do AI viết thì người dùng sửa được (BR-18) |
| R-03 | Phụ thuộc một nhà cung cấp AI | Trung bình | Adapter provider, chuyển đổi qua cấu hình |
| R-04 | Mất dữ liệu khi tái cấu trúc chương | Trung bình | Giao dịch DB; Archive và version chương sau MVP |
| R-05 | Văn bản dài vượt context LLM | Trung bình | Xử lý theo chương; tóm tắt cuốn chiếu **chỉ dùng nội bộ cho ngữ cảnh**, không bao giờ đưa vào audio |
| **R-06** | **TTS đọc sai hoặc bỏ chữ** (số, từ mượn, tên riêng, từ Hán Việt) | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| **R-07** | **LLM chia shot không phủ kín văn bản** | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-08 | Một đoạn văn dài khiến một ảnh đứng quá lâu, gây nhàm | Trung bình | Cảnh báo ảnh > 30 s; gợi ý tách shot; Ken Burns nhiều pha |
| R-09 | SSO gián đoạn thì người dùng không đăng nhập được | Trung bình | Phiên ứng dụng vẫn hiệu lực đến hết hạn; trang lỗi thân thiện |
| R-10 | SSO Vbee không hỗ trợ chuẩn OIDC đầy đủ (chỉ OAuth 2.0, thiếu logout hoặc JWKS) | Cao | `IdentityProviderPort` tách riêng; adapter OAuth 2.0 + userinfo; làm thêm 1–2 tuần-người lấy từ thứ tự cắt giảm (QĐ-23) |
| R-11 | Trình chỉnh sửa timeline trên web phức tạp, chậm với video dài | Trung bình | Dùng thư viện timeline/preview có sẵn (Remotion); ảo hóa danh sách clip; chỉnh theo chương |
| R-12 | **Năng lực nhóm không đủ** cho phạm vi MVP | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-13 | Tài khoản rác đốt tiền dùng thử | Cao | Danh sách mời beta; trần chi tiêu ngày; giới hạn kỹ thuật (BR-29, BR-30, BR-32) |
| R-14 | Vbee giao tài liệu muộn | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-15 | Render / preview không đạt yêu cầu (chậm, lệch khung, máy staging yếu) | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-16 | Mất năng lực vì Tết, thi, thành viên vắng | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-17 | Báo cáo đồ án dồn cuối | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |
| R-21 | Provider ảnh từ chối nhiều cảnh trong văn học (bạo lực, nghèo đói, tình dục) | → 09 §5 | Xem 09 §5 (xác suất, tác động, ngưỡng kích hoạt, ứng phó) |

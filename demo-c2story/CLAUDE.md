# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Bản chất thư mục

`demo-c2story/` là **bộ tài liệu đặc tả** (BA) cho đồ án tốt nghiệp "AI Story Studio": biến truyện dài thành video minh họa có thuyết minh **nguyên văn**. Không có mã ứng dụng; "mã" ở đây là Markdown (tiếng Việt), sơ đồ PlantUML và vài script Python sinh tài liệu. Viết mới bằng tiếng Việt, câu ngắn, ưu tiên bảng, giống văn phong các file hiện có.

`khao-sat-c2story/` là kết quả khảo sát hệ thống tham chiếu c2story.com, **không phải thiết kế mới**; tuân thủ nguyên tắc clean-room CR-01..05 ở README §3.

## Lệnh

Chạy trong `demo-c2story/`:

```bash
python3 so-do/tools/gen_mvp.py      # sinh sơ đồ MVP + tô xám phần sau MVP trong bản đầy đủ
python3 so-do/tools/split_erd.py    # sinh erd-1..6-*.puml từ erd.puml
python3 tools/gen_backlog.py        # sinh tai-lieu/11-product-backlog.md từ đặc tả use case
java -jar plantuml.jar -checkonly $(find so-do -name '*.puml')   # kiểm tra cú pháp mọi sơ đồ
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -tpng "so-do/**.puml"  # render (erd.puml rộng ~4900px)
```

Thứ tự khi sửa đặc tả: sửa nguồn → `gen_mvp.py` → `split_erd.py` → `gen_backlog.py` → `-checkonly`.

## Nguồn duy nhất và file sinh tự động

Phần lớn sự nhất quán giữa các file dựa trên vài "nguồn" sau. Sửa nguồn, rồi chạy lại script; **không sửa tay file sinh ra**.

| Nguồn | Điều khiển |
|---|---|
| Tiêu đề `## UC-xx.yy Tên` / `### UC-xx.yyz Tên` trong `tai-lieu/03-dac-ta-use-case/m*.md` | Tên UC phải **giống hệt** ở mục lục `00-muc-luc.md` §5 và nhãn `usecase "UC-xx.yy\nTên"` trên sơ đồ `so-do/01-use-case/` (quy cách đặt tên ở `00-muc-luc.md` §2) |
| Dòng `\| Giai đoạn \| … \|` ngay sau dòng `\| Truy vết \|` của mỗi UC | Cột GĐ ở mục lục và RTM (`09` §4), phân loại story/epic trong `11`, sơ đồ use case MVP, tô xám UC sau MVP |
| Đánh dấu `` `bảng` *(sau MVP)* `` trong `tai-lieu/04-mo-hinh-du-lieu.md` §3 | `so-do/mvp/02-du-lieu/erd-mvp.puml`, tô xám trong `erd.puml` |
| `POST_CLASSES` trong `so-do/tools/gen_mvp.py`; dòng chứa `(sau MVP)` trong lớp | `so-do/mvp/02-du-lieu/domain-class-mvp.puml` |
| `so-do/02-du-lieu/erd.puml` | `erd-1..6-*.puml` |

File sinh tự động: `so-do/mvp/01-use-case/phan-ra/*-mvp.puml`, `so-do/mvp/02-du-lieu/*`, `so-do/02-du-lieu/erd-[1-6]-*.puml`, `tai-lieu/11-product-backlog.md`; màu `#DDDDDD` trên sơ đồ đầy đủ cũng do `gen_mvp.py` đặt.

Mục lục `00-muc-luc.md` §5 và RTM `09` §4 **không có script**: khi thêm, đổi tên, bỏ UC hoặc đổi giai đoạn thì cập nhật tay cả hai (kể cả bảng "Tổng hợp" và §4.12 Độ phủ). Mọi mã test dùng trong RTM phải có trong danh mục `09` §4.13 và ngược lại.

Sơ đồ MVP **viết tay** (tổng quan/Studio use case, C4, deployment, 5 tuần tự, quy trình, 2 trạng thái — danh mục ở `so-do/mvp/README.md`) phải sửa cùng lúc với bản đầy đủ cùng tên.

## Cấu trúc tài liệu và truy vết

- `tai-lieu/01` BRD → `02` SRS (FR, cột Ưu tiên MoSCoW + **GĐ**) → `03` use case (Cockburn) → `04` dữ liệu → `05` kiến trúc (ADR; §4.1 cấu hình rút gọn cho MVP theo ADR-23) → `06` API → `07` NFR → `08` quy tắc nghiệp vụ & tính phí → `09` kế hoạch + RTM → `10` thuật ngữ → `11` backlog → `12` đặc tả kỹ thuật lõi (tách câu, ánh xạ timestamp, `timeline_snapshot`).
- `tai-lieu/schemas/timeline-snapshot.schema.json` là hợp đồng giữa API, preview và render; sửa schema thì sửa luôn file ví dụ cạnh nó và kiểm lại (`jsonschema` Draft 2020-12), cùng các ca SNP-T* ở 12 §3.2.
- `quyet-dinh.md` là sổ quyết định (`QĐ-xx`); mọi thay đổi phạm vi/kế hoạch ghi vào đây trước, các tài liệu khác dẫn mã QĐ ở cột Nguồn.
- Mỗi UC có mục **Truy vết** (FR, BR, IC, NFR, API, sơ đồ); RTM gộp Truy vết của UC gốc và UC con.
- Tiền tố mã: `FR-<PHÂN HỆ>-NN`, `BR-NN`, `IC-NN` (ràng buộc dữ liệu), `WR-NN` (quy tắc ví, 08 §4), `SYM-NN` (ký hiệu trình bày, 08 §6), `NFR-*`, `ADR-NN`, `UC-<phân hệ>.<số>[chữ]`. Nguồn thông tin: `[QS]` quan sát, `[SL]` suy luận, `[ĐX]` đề xuất của BA.
- Ký hiệu giai đoạn: `P0`–`P3` thuộc MVP, `Sau` = sau MVP, `✂n` = vị trí trong thứ tự cắt giảm (`09` §1.3: ✂1–6 tầng 1, ✂7–10 tầng 2; QĐ-116).
- Lịch sử phiên bản ở README §8; thêm một dòng khi có thay đổi đáng kể.

## Nguyên tắc nghiệp vụ không được phá

- **Thuyết minh nguyên văn** (BR-19..BR-25): văn bản TTS = đúng đoạn nguồn của shot; các shot phủ kín 100% chương; AI không bao giờ ghi vào văn bản truyện; track thuyết minh khóa (chỉ dời, chỉnh âm lượng, đổi tốc độ 0,8–1,25×).
- **Tốc độ đọc**: clip thuyết minh đổi tốc độ bằng file audio dẫn xuất sinh ở server, preview và render cùng phát ở tốc độ 1,0 (ADR-24); không dùng `playbackRate` của trình duyệt.
- **Trần chi tiêu ngày** phải giữ chỗ nguyên tử trên `daily_ai_budgets` cùng giao dịch với HOLD (ADR-25), không đọc-rồi-so-sánh.
- **Offset văn bản** luôn là code unit UTF-16 trên văn bản NFC (ADR-26); không dùng `char_length()` của Postgres cho phủ kín hay cắt văn bản.
- **Job**: bảng `jobs` là nguồn sự thật, BullMQ chỉ vận chuyển; nhận việc bằng `UPDATE … WHERE status IN (…)`; giới hạn đồng thời theo người dùng bằng semaphore Redis, không dùng BullMQ Pro groups (ADR-28, ADR-29).
- **Tiền**: không còn "credit". Ví USD lưu micro-USD; giá = chi phí thực của provider × 110%; giữ giá ước tính tối đa → trừ chi phí thực → hoàn phần dư; tài khoản Free / Đã nạp tiền; trần chi tiêu AI $10/ngày.
- **MVP chỉ có Owner**; Editor, cộng tác, AI Director (M07), thư viện (M08) là sau MVP nhưng đặc tả vẫn giữ.
- Đã bỏ hẳn (không đưa lại trừ khi có QĐ mới): Fix a spot/inpainting, AI sinh nhạc/SFX, gợi ý SFX, credit hằng ngày, các UC-05.06d, 05.10b, 06.11b, 06.11c, 09.07.

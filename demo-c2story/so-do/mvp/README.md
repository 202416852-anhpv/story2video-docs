# Sơ đồ phạm vi MVP

Bộ sơ đồ chỉ gồm phần thuộc **MVP (P0–P3)**, dùng cho đồ án và buổi bảo vệ. Bộ đầy đủ ở `so-do/01..06-*` vẫn là thiết kế sản phẩm hoàn chỉnh; trong đó phần sau MVP được **tô nền xám** (use case, ERD, mô hình miền) hoặc ghi "(sau MVP)".

## Cách cập nhật

| Loại | Cách làm |
|---|---|
| Use case phân rã, ERD, mô hình miền | **Sinh tự động**, không sửa tay. Sửa sơ đồ đầy đủ (hoặc dòng "Giai đoạn" của use case trong `tai-lieu/03-dac-ta-use-case/`, đánh dấu `*(sau MVP)*` của bảng trong `tai-lieu/04`), rồi chạy trong `demo-c2story/`: `python3 so-do/tools/gen_mvp.py && python3 so-do/tools/split_erd.py` |
| Tuần tự (`04-tuan-tu/*-mvp`) | **Sinh tự động** bởi `gen_mvp.py` từ bản đầy đủ: dòng giữa `'@sau-mvp` và `'@/sau-mvp` chỉ có ở bản đầy đủ; dòng bắt đầu bằng `'@mvp ` chỉ có ở bản MVP |
| Còn lại | Viết tay; sửa cùng lúc với bản đầy đủ tương ứng |

## Danh mục

| Thư mục | Sơ đồ MVP | Khác bản đầy đủ ở chỗ |
|---|---|---|
| `01-use-case/` | `uc-tong-quan-mvp`, `uc-studio-chi-tiet-mvp` | Không có M07, M08; chỉ Owner; ghi chú thứ tự cắt giảm ✂ |
| `01-use-case/phan-ra/` | `uc-m01..m06, m09, m10-*-mvp` (sinh tự động) | Chỉ còn 104/165 use case thuộc MVP; M07, M08 không có bản MVP |
| `02-du-lieu/` | `erd-mvp` (42/55 bảng), `domain-class-mvp` (sinh tự động) | Bỏ gói đăng ký, thư viện, Director, archive, notes, chapter rules, đa giọng, lịch sử timeline |
| `03-kien-truc/` | `c4-context-mvp`, `c4-container-mvp`, `c4-component-api-mvp`, `c4-component-editor-mvp`, `deployment-mvp` | Không có Director, thư viện, gói; quản trị bằng CLI/seed; triển khai một máy ảo staging |
| `04-tuan-tu/` | `seq-dang-nhap-sso-mvp`, `seq-thanh-toan-mvp`, `seq-sinh-tu-lieu-mvp`, `seq-thuyet-minh-nguyen-van-mvp`, `seq-chinh-sua-xuat-video-mvp` | Không back-channel logout; chỉ nạp tiền (không gói); không kiểm chứng WER từng shot (thay bằng nghe & đánh dấu); không lịch sử timeline, chia video, thư viện âm thanh |
| `05-hoat-dong/` | `act-quy-trinh-project-mvp` | Không Director, Archive; bước tham gia beta |
| `06-trang-thai/` | `state-narration-render-mvp`, `state-chapter-media-mvp` | Thuyết minh chỉ có `DONE`, không `VERIFIED` / `NEEDS_REVIEW` / `ACCEPTED` |

## Sơ đồ dùng chung (MVP giống bản đầy đủ)

`04-tuan-tu/seq-vong-doi-job`, `seq-import-chia-chuong`, `seq-doi-ranh-gioi-shot`, `seq-the-gioi-truyen`, `seq-storyboard-sinh-anh`; `05-hoat-dong/act-giu-tru-tien`, `act-phu-kin-van-ban`; `06-trang-thai/state-job`; `03-kien-truc/c4-component-ai`; ERD theo nhóm `02-du-lieu/erd-1..6-*` (bảng sau MVP tô xám).

## Sơ đồ chỉ có ở bản đầy đủ (toàn bộ sau MVP)

`04-tuan-tu/seq-director`, `seq-cong-tac-xung-dot`; `06-trang-thai/state-director-plan`, `state-tool-proposal`, `state-subscription`; `01-use-case/phan-ra/uc-m07-ai-director`, `uc-m08-thu-vien-tai-san`.

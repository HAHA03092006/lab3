# CHANGELOG CHỈNH LÝ TÀI LIỆU LAB 3 — 13/11/2026

## 1. Mục đích

Xây dựng bộ docs có thể dùng để báo cáo quá trình làm việc: yêu cầu → phân tích → lý thuyết → thiết kế module → kiểm thử → kế hoạch/nhật ký → bằng chứng → vấn đáp.

## 2. Điểm sửa quan trọng

- Sửa **trùng mã FR08–FR11** trong `analysts/requirements_traceability.md`. Giữ nghĩa `FR01–FR12` theo `00_lab3_description.md`; bổ sung `FR13–FR15` cho logits/loss, metrics input validation và alignment/export; `NFR01–NFR08` tách khỏi FR.
- Tạo `docs/README.md` để điều hướng toàn bộ docs; thêm chương `theory/00_theoretical_foundations.md` và kiến trúc tổng `define&design/06_architecture_and_interfaces.md`.
- Tạo phân tích yêu cầu, ADR, audit bằng chứng, kịch bản UAT, workflow/log mẫu và guide bảo vệ.
- Mở rộng đặc tả tổng quan, dữ liệu, model, engine, utils, evaluation; bổ sung ví dụ I/O, bất biến, failure modes, kiểm toán số liệu.
- Mở rộng Test Plan và **sáu** test specs module, thêm bảng case/expected/limitations; phân biệt test code hiện có và test đề xuất.
- Mở rộng 8 phase và kế hoạch tổng, kèm deliverables, review gates, risk và mẫu worklog.

## 3. Không thay đổi gì

- **Không chỉnh sửa `going_modular/`, `tests/`, `notebooks/`, `reports/`, `outputs/`, `requirements.txt`.** Chỉ bổ sung/chỉnh thư mục `docs/` và một mục link điều hướng trong README nếu có.
- **Không chạy lại** training hoặc pytest trong lần biên tập docs.
- **Không thêm** model weights/CSV đang thiếu và không tạo output metrics mới.
- Kết quả quick 86,2% và 24 pytest cases là bằng chứng lịch sử từ ZIP đầu vào.

## 4. Cần nhóm hoàn thiện trước khi nộp

- [ ] Điền người phụ trách và ngày làm thật, link branch/commit/PR vào `plans/team_workflow_and_log.md`.
- [ ] Xác nhận yêu cầu nguyên văn với slide/rubric giảng viên; tài liệu hiện dùng diễn giải từ repo.
- [ ] Nếu muốn nói có model sẵn để demo, chuẩn bị checkpoint thực, path và quyền truy cập.
- [ ] Chạy `python -m pytest -q` trên máy nhóm và giữ log mới nếu cần xác nhận sau update.
- [ ] Nếu cô cần full benchmark, chạy full với resource/versions và report riêng, không tái sử dụng quick metrics.

**Khuyến nghị:** Trong GitHub, mở [README docs](README.md) đầu tiên, sau đó [Ma trận FR](analysts/requirements_traceability.md), [Test Plan](define&design/tests/00_test_plan.md), [Kế hoạch](plans/implementation_plan.md) và [Hướng dẫn bảo vệ](presentation/defense_guide.md).

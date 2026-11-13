# P7 — Kiểm thử tổng hợp, nghiệm thu và bàn giao GitHub

> **Mã:** P7 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Kết thúc khi có test evidence, traceability, review diff, hướng dẫn chạy và danh sách giới hạn trung thực.

**File liên quan:** `tests/`, `docs/define&design/tests/`, `docs/analysts/requirements_traceability.md`, `reports/pytest_output.txt`, `reports/VALIDATION.md`, `Readme.md`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

Kiểm thử offline có thể chạy nhanh trên tiny model nhưng không chứng minh model pretrained thật hoạt động khi thiếu mạng; bản ZIP chỉ chứng minh ở mức artifacts lưu sẵn. Tách kiểm chứng cú pháp và integration test khỏi kiểm tra chất lượng quick.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Chạy `python -m pytest -q` trên venv được cài đủ dependencies, lưu output timestamp nếu thực thi.
- [ ] Rà soát từng file test spec ghi đúng tên hàm test trong `tests/*.py`.
- [ ] Đánh dấu các test đề xuất mở rộng là `Chưa triển khai`, không cộng vào số passed.
- [ ] Kiểm tra `test_engine.py` chứng minh train → dừng sau save → resume → reuse local model.
- [ ] Kiểm tra `test_notebook.py` xác nhận schema và AST của code cells notebook nguồn.
- [ ] Đọc `reports/pytest_output.txt`: log gốc ghi 24 tests passed, không thay bằng kết quả chưa chạy.
- [ ] Kiểm tra report/README có nhắc đúng quick 2.000/500/1.000 và accuracy 0.862.
- [ ] Kiểm tra directory chỉ còn một cây `docs/define&design/` chuẩn, không tạo lại `define&designt/`.
- [ ] So sánh Git diff để đảm bảo docs thay đổi, source code không đổi ngoài phạm vi yêu cầu.
- [ ] Tạo pull request mô tả file sửa/tạo, bằng chứng kiểm thử và các hạn chế cần nhóm trưởng biết.


## 4. Tài liệu/bằng chứng cần bàn giao

- Danh mục tài liệu, test plan và traceability có thể review từ PR.
- Báo cáo `reports/VALIDATION.md` (lịch sử) và các log mới nếu người thực hiện chạy thêm.
- Danh sách khoảng trống: chưa có full run, ZIP thiếu best_model weights nếu không bổ sung bản riêng.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Tất cả liên kết và tên đường dẫn nhất quán.
- Code/bằng chứng/test docs không mâu thuẫn; test existing vs proposed có nhãn rõ ràng.
- Nhóm trưởng có thể đọc từng phase độc lập để phân công, theo dõi và nghiệm thu.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Xử lý |
|---|---|
| PR ghi quá chung chung | Liệt kê 8 phase, model spec, test specs, README, traceability |
| Lẫn test passed với thí nghiệm | Dẫn từng artifact và điều kiện đánh giá |
| Xoá/chỉnh nhầm output | Giữ artifacts gốc, không overwrite khi cập nhật docs |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

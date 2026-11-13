# P6 — Hoàn thiện notebook, README và thuyết minh

> **Mã:** P6 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Cung cấp tài liệu thực hành mà người khác có thể chạy lại hoặc review được, liên kết code với kết quả đúng phạm vi.

**File liên quan:** `notebooks/huggingface_sentiment.ipynb`, `notebooks/huggingface_sentiment_executed.ipynb`, `Readme.md`, `reports/LAB3_THUYET_MINH.md`, `reports/VALIDATION.md`, `tests/test_notebook.py`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

Notebook trình bày Exercise 1 và Exercise 2 theo trình tự cụ thể; mã dùng các module tách biệt. `reporting.write_report` sinh báo cáo từ metrics có thật; notebook executed lưu output lịch sử chứ không chứng minh lần chạy mới trên máy người nhận.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Kiểm tra notebook có phần setup/môi trường; chạy các import cần thiết từ package root.
- [ ] Kiểm tra Exercise 1 có bảng token/ID/mask, suy luận tay và pipeline, lưu output.
- [ ] Kiểm tra Exercise 2 có chia dữ liệu, tokenize, preview batch, TrainingArguments/Trainer.
- [ ] Kiểm tra notebook chỉ gọi test sau chốt best validation checkpoint.
- [ ] Kiểm tra phần evaluation minh họa history, metrics, confusion matrix và lỗi.
- [ ] Kiểm tra save/load model/tokenizer và prediction mới trong notebook.
- [ ] Chạy kiểm tra `nbformat.validate` và parse Python code cells bằng pytest.
- [ ] Đối chiếu bảng hyperparameters README với `config.py` (quick=2 epochs, full=3 epochs).
- [ ] Đối chiếu kết quả README với JSON quick thực tế; không chép dự đoán hiệu năng.
- [ ] Ghi rõ weights/best_model có hay không trong bản nộp; hướng dẫn tái lập khi thiếu.
- [ ] Bảo đảm liên kết từ README đến docs/plans và docs/define&design/tests đúng case-sensitive.


## 4. Tài liệu/bằng chứng cần bàn giao

- Notebook nguồn và notebook executed, có log tại `reports/notebook_execution.log` của lần chạy gốc.
- README cập nhật: cấu trúc phase, đường dẫn docs, cấu hình đúng, thực nghiệm quick đúng.
- `reports/LAB3_THUYET_MINH.md` và REPORT.md phản ánh dữ liệu thực khi trích dẫn.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Không có sai biệt README–code về padding, epochs, metric library hoặc accuracy.
- Các file `.md` mở được trên GitHub và link nội bộ đúng.
- Phân biệt nội dung mô tả mục tiêu với kết quả từng run.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Xử lý |
|---|---|
| Notebook executed từ môi trường cũ | Ghi rõ snapshot lịch sử, không giả đang chạy mới |
| Markdown nhầm cây thư mục | Dùng đúng `Lab3/docs/define&design/` nhất quán |
| Thuyết minh chép số không kiểm chứng | Dẫn `test_metrics.json` và `reports/VALIDATION.md` |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

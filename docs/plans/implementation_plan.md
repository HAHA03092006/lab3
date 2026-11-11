# Kế hoạch hiện thực và chạy Lab 3

## Giai đoạn 1 — Xác định đề

Đối chiếu 4 bước Exercise 1 và 7 bước Exercise 2; phân biệt pretrained inference với fine-tuning.
Chọn IMDb/DistilBERT làm ví dụ phù hợp tài liệu HF; giữ entry point notebook theo Lab 2.

## Giai đoạn 2 — Dữ liệu và model

Cài môi trường, thiết lập seeds, split phân tầng, tokenizer/collator, label mapping.
Kiểm tra đầu vào/đầu ra trước train; lưu manifest để biết chính xác dữ liệu.

## Giai đoạn 3 — Training và persistence

TrainingArguments, Trainer, validation F1, checkpoint và best_model/tokenizer.
Contract action-independent; config trước train; train/resume/reuse rõ ràng.

## Giai đoạn 4 — Evaluation và báo cáo

Một lượt test inference, metrics, CM, lỗi confidence cao, reload equivalence.
Sinh REPORT.md từ số thực, bổ sung phân tích lỗi thủ công có dẫn ví dụ.

## Giai đoạn 5 — Kiểm chứng

Chạy unit/integration CPU offline; kiểm tra schema/syntax notebook; chạy model thật nếu môi trường cho phép.
Ghi đầy đủ kết quả và giới hạn trong VALIDATION.md. Không đổi mô hình sang random để giả hoàn thành thí nghiệm.

## Trước khi nộp

- Xác nhận profile quick/full trong báo cáo đúng với số mẫu.
- Nếu dùng full: chạy run_id mới, không reuse model quick dưới tên full.
- Giữ notebook đã chạy, config/history/metrics/ảnh; lưu weights riêng nếu file quá lớn.
- Dùng test cuối, không tinh chỉnh trên test. Với thử LR khác, chọn theo validation rồi mới đánh giá test.

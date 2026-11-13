# NHẬT KÝ QUYẾT ĐỊNH THIẾT KẾ (ADR) — LAB 3

> **LAB3-ADR v3.0 — 13/11/2026.** Mô tả lý do có thể suy ra từ **cấu hình và code hiện tại**. Đây không phải biên bản đã được tất cả thành viên xác nhận trong những ngày trước; nhóm nên thêm người quyết định/commit link nếu có.

## Cách đọc ADR

Mỗi quyết định ghi: **vấn đề → các lựa chọn → lựa chọn hiện có → đánh đổi → cách kiểm chứng**. Điều này quan trọng trong buổi bảo vệ: khi cô hỏi “vì sao không chọn cách khác?”, cần lý giải thay vì chỉ đọc code.

| ADR | Vấn đề | Quyết định trong code | Đánh đổi/cách kiểm chứng |
|---|---|---|---|
| ADR-01 | Chứng minh được cả inference và fine-tuning | SST-2 checkpoint cho E1, base DistilBERT cho E2 | Dễ tách 2 exercise; không so accuracy trên data khác |
| ADR-02 | Giữ bài dễ bảo trì | notebook orchestration + `going_modular/` | Cần quản path/import; các module có pytest |
| ADR-03 | Tạo validation hợp lệ | tách từ IMDb train bằng stratify, giữ test nguyên | Ngăn test leakage rõ hơn; exact duplicates vẫn có thể tồn tại |
| ADR-04 | Quick không bị lệch nhãn | subset dùng stratified sampling | Không đại diện toàn bộ benchmark nếu size nhỏ |
| ADR-05 | Tránh phá polarity | clean tối thiểu, không xóa stopwords/phủ định | Text giữ nhiễu tự nhiên nhưng bảo toàn ngữ nghĩa |
| ADR-06 | Giảm padding vô ích | tokenizer `padding=False`, collator dynamic | Batch length biến thiên; vẫn có truncation |
| ADR-07 | Bám slide về Trainer | `transformers.Trainer` + `TrainingArguments` | Ít boilerplate nhưng phụ thuộc phiên bản API |
| ADR-08 | Chọn checkpoint có mục tiêu | F1 Positive trên validation, best at end | F1 có thể nhạy phân bố lớp, phải nói rõ |
| ADR-09 | Khả năng tái lập | seed + split manifest/hash + tokenizer fingerprint | Reproducibility có giới hạn, `main` không cố định |
| ADR-10 | Không ghi đè artifacts | run_id, `train/resume/reuse` guard | Cần quản nhiều run IDs, không chống được mọi lỗi FS |
| ADR-11 | Kiểm thử offline tiết kiệm | tiny local DistilBERT + synthetic data | Kiểm logic, **không đo accuracy NLP** |
| ADR-12 | Đánh giá có thể kiểm toán | metrics JSON, CSV, cm PNG, REPORT.md | CSV/weights bị gitignore nên ZIP không đủ mọi artifact |

## ADR-01 — Tách checkpoint E1/E2

**Vấn đề:** Nếu dùng model pretrained sentiment đã fine-tune SST-2 cho cả hai bài, sinh viên dễ nhầm E2 chỉ là inference. **Lựa chọn:** E1 dùng `SENTIMENT_MODEL`, E2 dùng `BASE_MODEL` + head. **Hệ quả:** E2 có gradient/optimizer/checkpoint, do đó có bằng chứng training thực. **Chứng cứ:** `config.py`, notebook, `reports/VALIDATION.md`. **Phản biện:** checkpoint base còn pretrained encoder, không phải train từ đầu.

## ADR-03/04 — Ranh giới dữ liệu

**Vấn đề:** IMDb train/test khác vai trò; lấy quick data theo thứ tự đầu có thể lệch lớp. **Lựa chọn:** tạo validation phân tầng từ original train; chia subset phân tầng trong mỗi split; lưu ID và exact text overlap. **Hệ quả:** công bằng hơn cho subset nhưng không bảo đảm không có semantic duplicates. **Chứng cứ:** DATA-01/DATA-08, split manifest. **Phản biện:** nếu muốn loại tất cả duplicate toàn bộ benchmark, phải thiết kế protocol group split trước khi nhìn test.

## ADR-07/08 — Trainer, metric chọn model

**Vấn đề:** Đề muốn hiểu `TrainingArguments` và `Trainer`, không yêu cầu viết thủ công training loop. **Lựa chọn:** dùng `Trainer`, `eval/save_strategy='epoch'`, `load_best_model_at_end=True`, metric F1 Positive trên validation. **Hệ quả:** code gọn, phụ thuộc API v4.57.1; mỗi epoch có checkpoint/validation; không tune bằng test. **Chứng cứ:** `make_training_args`, `history`, ENGINE-01, reference run.

## ADR-09/10 — Run lifecycle và reusability

**Vấn đề:** Train lại một run ID có thể ghi đè weights, resume từ config khác sinh kết quả sai. **Lựa chọn:** immutable RunConfig, manifest/hash, tokenizer fingerprint trong contract; guard cho train/resume/reuse; JSON ghi qua temp rồi replace. **Hệ quả:** đổi tham số dù nhỏ thường phải tạo run mới, nhưng đổi lại truy vết đáng tin cậy hơn. **Chứng cứ:** UTIL-01/02, ENGINE-01. **Giới hạn:** `main` mutable; không có lock process cho multi-user simultaneous runs.

## ADR-11/12 — Test offline và đánh giá thật

**Vấn đề:** Test end-to-end pretrained qua mạng quá chậm/khó chạy CI; nhưng chỉ test mock không chứng minh Trainer. **Lựa chọn:** tiny local model được train thật 2 epoch + synthetic IMDb-shaped dataset cho integration test, còn quick real run tạo metrics riêng. **Hệ quả:** 24 pytest cases có thể test logic nhanh, nhưng không được coi tương đương đánh giá IMDb. **Chứng cứ:** `tests/conftest.py`, `reports/pytest_output.txt`, `outputs/.../test_metrics.json`.

## Decision review checklist

- [ ] Quyết định có mã ADR, lý do, lựa chọn thay thế, đánh đổi và bằng chứng.
- [ ] Những gì docs gọi là “đã thực hiện” phải tìm thấy trong code/outputs.
- [ ] Nếu thay đổi, bổ sung ngày/author và commit thực tế, không xoá lý do cũ.
- [ ] Cập nhật tương ứng ở FR/ma trận và test spec.

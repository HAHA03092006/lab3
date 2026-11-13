# TEST SPEC MODEL — `going_modular/model_builder.py`

> **ID:** LAB3-TMODEL · **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **Test hiện có:** `../../../tests/test_model_builder.py::test_logits_loss_and_all_trainable`  
> **Phase:** `../../plans/phase2.md` · **Đặc tả model:** `../02_model.md`.

## 1. Đối tượng và mục tiêu

Kiểm tra `build_model(model_id,revision)` trả `AutoModelForSequenceClassification` dùng được với nhãn nhị phân, forward tạo logits hình `[B,2]`, nhận labels sinh loss scalar và không freeze tham số theo thiết kế full fine-tuning. Đây là hợp đồng kỹ thuật tối thiểu; một forward pass thành công không khẳng định mô hình đã học sentiment tốt.

## 2. Fixture và dữ liệu đầu vào

`tests/conftest.py` tạo tokenizer `DistilBertTokenizerFast` local từ `vocab.txt`, đồng thời tạo một `DistilBertForSequenceClassification` random với cấu hình `vocab_size=13`, `dim=16`, `hidden_dim=32`, `n_layers=1`, `n_heads=2`, `max_position_embeddings=64`, `num_labels=2`, dropout=0. Model được `save_pretrained` vào `tmp_path`; `RunConfig.model_id` trỏ đến thư mục local. Dữ liệu tổng hợp có text good/bad và label 0/1; collator padding trong batch 2 mẫu.

### MODEL-01 — Build model và kiểm tra forward/loss/params

| Thuộc tính | Mô tả |
|---|---|
| Đường đi | `tests/test_model_builder.py::test_logits_loss_and_all_trainable` |
| Tiền điều kiện | Tiny checkpoint và tokenizer local đã tạo, có tokenized train split |
| Input | `cfg.model_id` (đường dẫn tiny model); hai rows encoded; collator `DataCollatorWithPadding(tok)` |
| Mục tiêu | Validate model load, tensor contract, scalar supervised loss, không freeze |
| Expected | `tuple(result.logits.shape) == (2,2)`, `result.loss.ndim == 0`, `count_params(model)['frozen'] == 0` |
| Trạng thái | ĐÃ CÓ TRONG CODE — 1 pytest case |

**Các bước:** (1) gọi `build_model(cfg.model_id)`; (2) tạo batch từ 2 records tokenized; (3) `model(**batch)`; (4) assert logits shape; (5) assert loss scalar; (6) đếm tham số bị đóng băng. Exception ở bất kỳ bước nào khiến test fail. Không require API mạng, vì model đã nằm trong tmp local.

**Ý nghĩa lỗi:** Nếu logits chỉ có 1 hoặc nhiều hơn 2 cột, classifier không đáp ứng nhãn nhị phân. Nếu không có loss scalar, Trainer có thể không optimize theo labels. Nếu `frozen>0`, setup hiện tại không khớp chủ trương fine-tune toàn bộ tham số (trong tiny fixture).

## 3. Mối liên hệ với hợp đồng model thực

- `load_tokenizer` và `build_model` dùng Auto classes; trong notebook Exercise 1 dùng SST-2 checkpoint đã có head. Exercise 2 gọi base checkpoint, head mới hai lớp, không phải random toàn bộ encoder.
- **Input thực:** `input_ids[B,L]`, `attention_mask[B,L]`, optional `labels[B]` kiểu integer, L được dynamic padding.
- **Output thực:** logits `[B,2]`, optional scalar loss; prob/label được xử lý trong `evaluate.predict_texts`.
- `tokenizer_identity` tạo hash vocab/special tokens và được dùng để bảo vệ artifact contract trong engine, nhưng không có unit test độc lập trong `test_model_builder.py` hiện tại.

## 4. Pass/Fail và giới hạn bao phủ

Chạy `python -m pytest tests/test_model_builder.py -v`. PASS khi cả ba assert đạt. Có **1 test case** trong file này. Kết quả saved-model/reuse equivalence thuộc test integration `tests/test_engine.py`; không ghi lại là test độc lập ở đây. Test này chưa xác nhận checksum/revision Hub, đúng kiến trúc 6 layer/768 hidden của base thật hoặc số tham số tuyệt đối.

## 5. Các kiểm thử bổ sung đề xuất — CHƯA TRIỂN KHAI

| ID | Kịch bản | Kỳ vọng đề xuất |
|---|---|---|
| MODEL-P01 | `load_tokenizer` với local model và vocab cố định | Trả tokenizer fast, special tokens đúng |
| MODEL-P02 | `tokenizer_identity` gọi lặp trên cùng vocab | Hash và mapping ổn định |
| MODEL-P03 | Input batch thiếu `attention_mask`, labels sai miền | Kiểm tra hành vi cụ thể và thông báo lỗi ở lớp gọi thích hợp |
| MODEL-P04 | Input có L > max position embedding | Trả lỗi rõ thay vì âm thầm cho kết quả giả |
| MODEL-P05 | Tải checkpoint base thật và đọc config | Kiểm tra architecture và revision đã resolve khi có mạng |

Mọi đề xuất ở mục 5 chỉ là backlog, không đưa vào thống kê 24 passed của code gốc.

## 6. Đặc tả thủ tục MODEL-01 chi tiết (v3.0)

| Trường | Nội dung |
|---|---|
| Test ID | MODEL-01 |
| Function | `tests/test_model_builder.py::test_logits_loss_and_all_trainable` |
| Fixture | `tiny_bundle` local vocab 13 tokens, DistilBERT 1-layer dim 16/head 2, synthetic data |
| Setup | `build_model(cfg.model_id)` từ thư mục model đã `save_pretrained` local |
| Input | 2 record tokenized, `DataCollatorWithPadding(tok)` tạo tensor batch |
| Step | gọi `result=model(**batch)`, `count_params(model)` |
| Expected 1 | `tuple(result.logits.shape) == (2, 2)` |
| Expected 2 | `result.loss.ndim == 0` (scalar loss do labels hợp lệ) |
| Expected 3 | `count_params(model)['frozen'] == 0` |
| Failure | shape sai, missing labels, backward incompatibility, frozen count khác |
| Bằng chứng | Test code + `reports/pytest_output.txt` của lần chạy trước |

**Giới hạn oracle:** MODEL-01 **không** chứng minh encoder base 6 layers có đúng weights pretrained hoặc phân loại IMDb tốt. Tiny fixture chủ động dùng random weights để test nhanh offline. File model real được kiểm riêng qua notebook/output thực. Không gọi confusion matrix quick là đầu ra test này.

### Đề xuất chưa có Python test

- MODEL-P01: assert `id2label`, `label2id` và `num_labels=2` trên checkpoint.
- MODEL-P02: tokenizer mismatch khác vocabulary phải phát hiện qua fingerprint/contract.
- MODEL-P03: `max_length` quá 512 bị config guard báo lỗi.
- MODEL-P04: kiểm `params.trainable` khi có chính sách freeze/unfreeze mới; không tự giả định freeze hiện có.
- MODEL-P05: load model/tokenizer real trong môi trường sạch, xác minh revision resolved.

Liên quan FR02, FR03, FR13; [model spec](../02_model.md), [lý thuyết](../../theory/00_theoretical_foundations.md).

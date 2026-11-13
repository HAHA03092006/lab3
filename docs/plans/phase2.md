# P2 — Tokenizer, Model Builder và suy luận pretrained (Exercise 1)

> **Mã:** P2 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Xác minh pipeline SST-2 và hợp đồng input/output của DistilBERT dùng trong Exercise 2.

**File liên quan:** `going_modular/model_builder.py`, `going_modular/data_setup.py` (`tokenize_splits`), `going_modular/evaluate.py` (`predict_texts`), notebook §1–3, `tests/test_model_builder.py`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

Exercise 1 dùng `distilbert/distilbert-base-uncased-finetuned-sst-2-english` đã có sentiment head. Exercise 2 dùng `distilbert/distilbert-base-uncased`; `build_model` thêm classifier 2 nhãn để fine-tune trên IMDb. Tokenizer map dùng truncation không padding; DataCollatorWithPadding thực hiện dynamic padding ở batch.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Tải `AutoTokenizer` và pretrained classifier SST-2 cùng revision trong notebook Exercise 1.
- [ ] Hiển thị token, input_ids, attention_mask, logits và softmax của câu ví dụ.
- [ ] Chạy suy luận tay bằng `predict_texts` và qua `pipeline('sentiment-analysis')`.
- [ ] Xuất câu/nhãn/xác suất dự đoán của Exercise 1 thành `predictions.json` có nguồn checkpoint.
- [ ] Đảm bảo model/tokenizer Exercise 1 được giải phóng khi chuẩn bị chuyển sang fine-tuning.
- [ ] Kiểm tra `load_tokenizer(model_id, revision)` dùng `AutoTokenizer` fast.
- [ ] Kiểm tra `tokenize_splits(..., max_length)` tạo `input_ids`, `attention_mask`, `labels`, giữ thứ tự mẫu.
- [ ] Kiểm tra model Exercise 2 có 2 nhãn, `id2label`, `label2id` nhất quán và head mới phù hợp.
- [ ] Dùng collator tạo mini-batch, kiểm tra logits `[B,2]`, loss scalar khi có nhãn.
- [ ] Kiểm tra `count_params` full fine-tuning báo frozen = 0 (model test local); không coi đó là chất lượng thực nghiệm.


## 4. Tài liệu/bằng chứng cần bàn giao

- `outputs/YYYY-MM-DD/exercise1_pretrained/.../predictions.json` từ lần chạy thật.
- Tokenized DatasetDict cho Trainer; batch collator có tensor IDs/mask/labels.
- Test đã có: `test_logits_loss_and_all_trainable` dùng tiny local model; không cần mạng.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Có thể giải thích `softmax` chỉ dùng suy luận, logits thô đưa vào cross-entropy.
- Token length không vượt `cfg.max_length`; padding ở batch khác với `padding='max_length'`.
- Không đồng nhất checkpoint sentiment đã fine-tune SST-2 với encoder nền của bài 2.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Xử lý |
|---|---|
| Thông báo head mới random | Giải thích đây là classifier của Exercise 2, encoder vẫn pretrained |
| Tokenizer lệch model | Dùng cùng model ID/revision, ghi tokenizer identity |
| Softmax trước loss | Tránh: HF model nhận raw logits/labels và tự tính loss |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

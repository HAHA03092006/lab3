# P3 — Huấn luyện DistilBERT với Trainer và chọn checkpoint

> **Mã:** P3 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Thiết lập Trainer đúng siêu tham số, theo dõi validation và chọn best model mà không dùng test trong training.

**File liên quan:** `going_modular/engine.py`, `going_modular/config.py`, `going_modular/evaluate.py`, notebook §4, `tests/test_engine.py`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

`make_training_args` dùng AdamW, linear scheduler với warmup, gradient clipping; logging theo step; validation và save theo epoch; `metric_for_best_model="f1"`. `Trainer` nhận train và validation; `test` chỉ dùng sau cùng.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Đối chiếu quick: epochs=2, batch_size=16, eval_batch_size=32, learning_rate=2e-5, max_length=128.
- [ ] Đối chiếu full: epochs=3, max_length=256; những thông số khác dùng default nếu không override.
- [ ] Kiểm tra optimizer AdamW, scheduler linear, weight_decay=0.01, warmup_ratio=0.1.
- [ ] Kiểm tra training/evaluation dataset được truyền đúng `tokenized['train']`/`['validation']`.
- [ ] Kiểm tra `compute_metrics` dùng nhãn Positive=1 và trả accuracy/precision/recall/f1/macro_f1.
- [ ] Kiểm tra save/eval theo epoch và `load_best_model_at_end=True`.
- [ ] Xác nhận các tham số `seed`, `data_seed`, accumulation và clipping đều lấy từ config.
- [ ] Chạy một lượt nhỏ khi có môi trường; lưu history và checkpoint, không khẳng định full đã chạy.
- [ ] Quan sát train loss/validation loss/F1, không dùng test để chỉnh learning rate/epochs.
- [ ] Ghi rõ lỗi dừng sớm và tác động đến completed marker.


## 4. Tài liệu/bằng chứng cần bàn giao

- `checkpoints/checkpoint-*`, `history.json`, TensorBoard logs và `best_metric` trong completed khi hoàn tất.
- `reports/reference_run/history.json` là chứng cứ lịch sử quick trong ZIP đầu vào.
- Integration test `test_real_trainer_resume_reuse_roundtrip` bao gồm train thực trên tiny synthetic model.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Checkpoint chọn theo F1 trên validation, không dựa trên test set.
- Dừng trước target epoch phải báo InterruptedError, không được tạo completed.json.
- Không quảng bá accuracy IMDb từ tiny-model integration test.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Xử lý |
|---|---|
| CPU train chậm | Chọn quick hoặc GPU, ghi đúng tài nguyên đã dùng |
| GPU OOM | Giảm batch trong run mới, không resume với contract khác |
| Validation tốt nhưng test chưa tốt | Không sửa bằng test, xem lỗi và đề xuất validation protocol mới |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

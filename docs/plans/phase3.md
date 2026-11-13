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

## 8. Work package, tiến trình giải thích và cách bàn giao (bổ sung v3.0)

**Mục tiêu có thể báo cáo:** Cấu hình và thực hiện fine-tuning bằng Trainer.

### 8.1. Trình tự thực hiện ở mức tác vụ

1. Chốt hyperparams từ RunConfig, giải thích AdamW/LR/warmup/clipping/epochs.
2. Định nghĩa TrainingArguments eval/save mỗi epoch và chọn best theo F1 Positive trên validation.
3. Trainer chỉ dùng train và validation; log loss/metric và checkpoint theo epoch.
4. Trước khi xem test, chọn best validation checkpoint và lưu history.

### 8.2. Bằng chứng lấy từ code/ZIP, không phải báo cáo tiến độ của từng cá nhân

`engine.make_training_args`, `run_experiment`, reference history/completed, ENGINE-01.

**Điều kiện review/Definition of Done cụ thể:** Có 1 run record cho train/validation; dừng sớm không ghi completed, best theo validation F1; không lấy kết quả test để select.

**Rủi ro còn lại:** CPU chậm/OOM, giữa epoch chưa có checkpoint, lệch metric key khi update thư viện.

### 8.3. Checklist nghiệm thu cần xác nhận bằng chứng

- [ ] Chốt hyperparams từ RunConfig, giải thích AdamW/LR/warmup/clipping/epochs.
- [ ] Định nghĩa TrainingArguments eval/save mỗi epoch và chọn best theo F1 Positive trên validation.
- [ ] Trainer chỉ dùng train và validation; log loss/metric và checkpoint theo epoch.
- [ ] Trước khi xem test, chọn best validation checkpoint và lưu history.
- [ ] Người kiểm tra mở đúng file code/test/output trong cột bằng chứng.
- [ ] Nếu không chạy lại được, đánh dấu "Chưa tái kiểm chứng" thay vì tự tick.
- [ ] Nếu chức năng đổi, cập nhật ma trận FR và link spec module liên quan.

### 8.4. Nhật ký công việc dùng cho nhóm điền

| Ngày giờ thực tế | Thành viên | Branch/commit/PR | Công việc có bằng chứng | Test hoặc demo đã làm | Phản hồi reviewer | Trạng thái |
|---|---|---|---|---|---|---|
| _Chưa điền_ | _—_ | _—_ | _—_ | _—_ | _—_ | _Not recorded_ |

**Cách báo cáo phase này:** trình bày mục tiêu → một quyết định kỹ thuật và lý do → file/hàm thực tế → test/metric/manifest → hạn chế hoặc việc chưa làm. Xem [quy trình nhóm](team_workflow_and_log.md) và [ma trận yêu cầu](../analysts/requirements_traceability.md).

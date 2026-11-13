# TEST SPEC ENGINE — `going_modular/engine.py`

> **ID:** LAB3-TENGINE · **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **Test hiện có:** `../../../tests/test_engine.py::test_real_trainer_resume_reuse_roundtrip`  
> **Phase:** `../../plans/phase3.md`, `../../plans/phase4.md` · **Thiết kế:** `../03_engine.md`.

## 1. Mục tiêu và phạm vi

Xác minh vòng đời của một run: `train` thật bằng Hugging Face Trainer trên tiny synthetic model → callback dừng sau checkpoint đầu → `resume` từ checkpoint → lưu best model/completed → `reuse` đọc lại weights và giữ xác suất. Có assert về trạng thái, global step, checkpoint optimizer, tính nhất quán history và guard ghi đè; không chỉ mock phương thức. Vì fixture offline tiny model ngẫu nhiên, test không chứng minh độ chính xác IMDb.

## 2. Fixture, input, expected schedule

- Dataset synthetic raw train=16, validation=8, test=8; training batch=4, eval batch=4.
- `RunConfig` dùng `run_id='tiny_integration'`, `epochs=2`, `max_length=32`, `gradient_accumulation_steps=1`, save/eval theo epoch.
- Với 16 train / batch 4: **4 optimizer steps/epoch**, target 2 epochs → **8 steps**.
- `StopAfterFirstCheckpoint` kế thừa `TrainerCallback`, trong `on_save` đặt `control.should_training_stop=True` khi `state.epoch>=1`.
- `tmp_path/'artifacts'` và `tmp_path/'logs'` chỉ để test ghi file, không đụng outputs thật của người dùng.

## 3. ENGINE-01 — Vòng đời train/resume/reuse (1 test function, nhiều assertions)

| Giai đoạn | Các bước / điều kiện kích hoạt | Expected output cụ thể | Lỗi được ngăn |
|---|---|---|---|
| 1. Train lần đầu | `run_experiment(... action='train', callbacks=[StopAfterFirstCheckpoint()])` | `pytest.raises(InterruptedError)` sau khi lưu checkpoint ở epoch 1 | Không báo completed khi mới hoàn thành 1/2 epochs |
| 2. Checkpoint | Kiểm `run/checkpoints/checkpoint-4/optimizer.pt` | File tồn tại, `completed.json` **không tồn tại** | Resume thiếu optimizer, completed giả |
| 3. Resume | `run_experiment(... action='resume')` với contract nguyên | `trainer.state.global_step==8`, `state.epoch==2` | Train lại từ 0/không khôi phục state |
| 4. Marker | Đọc `run/completed.json` | `global_step==8` | Artifact ghi incomplete thành complete |
| 5. Predict trước reuse | `predict_texts` trên `good movie`, `bad movie` | Hai hàng xác suất `p_positive` | Sai giao diện infer |
| 6. Reuse | `run_experiment(... action='reuse')` | Model local nạp thành công, `history == loaded` | Thay đổi history hoặc train ngoài ý muốn |
| 7. So sánh | `np.allclose` xác suất trước/sau | `atol=1e-7` | Lossy save/reload hoặc head sai |
| 8. History | Lọc các bản ghi có `eval_f1` | Đúng 2 bản ghi validation F1 | Thiếu epoch evaluation |
| 9. Guard train | `run_experiment(... action='train')` vào run đã có | `FileExistsError` | Ghi đè artifacts |
| 10. Guard resume | `run_experiment(... action='resume')` sau completed | `ValueError` | Chạy thừa epoch/đổi trạng thái completed |

**Lưu ý:** 10 hàng bước/điều kiện nằm trong **1** hàm test duy nhất, nên chỉ tính 1 case pytest cho `test_engine.py`.

## 4. Quan sát, acceptance và log lỗi

- Checkpoint từ Trainer phải có optimizer state; `get_last_checkpoint` dùng đường dẫn `checkpoints/checkpoint-*`.
- `completed.json` chỉ được tạo sau khi train đủ epoch và save best model/tokenizer xong.
- `reuse` sử dụng `AutoModelForSequenceClassification.from_pretrained(run/'best_model')` và không gọi `trainer.train`.
- `train/resume/reuse` phải dùng cùng contract: config dict, hash data manifest, tokenizer identity. Guard đơn lẻ được test thêm ở `tests/test_utils.py`.
- Bản log đầu vào có một warning `mtime may not be reliable on this filesystem`; warning không khiến case fail trong môi trường gốc. Nếu run mới có fail, cần giữ traceback cụ thể.

## 5. Cách chạy

```bash
python -m pytest tests/test_engine.py -v
```

Yêu cầu có `torch`, `transformers`, `datasets`, `accelerate` và hỗ trợ save/checkpoint. Dù không cần mạng, integration test sẽ làm forward, backward, checkpoint save/load thật; thời gian chạy tùy máy.

## 6. Kịch bản bổ sung đề xuất — CHƯA TRIỂN KHAI

- ENGINE-P01: `resume` khi không có checkpoint-*: kỳ vọng FileNotFoundError.
- ENGINE-P02: `reuse` khi thiếu `best_model/model.safetensors`: kỳ vọng FileNotFoundError.
- ENGINE-P03: thay data hash/tokenizer hash giữa các lần gọi: từ chối contract mismatch.
- ENGINE-P04: giả lập ngắt tại thời điểm checkpoint đủ epochs nhưng chưa export: yêu cầu quy trình phục hồi minh bạch.
- ENGINE-P05: thử `gradient_accumulation_steps > 1` và kiểm global_step đúng.

Không gọi các scenario đề xuất là đã được pytest chạy.

## 7. Timeline chính xác của ENGINE-01 và bằng chứng (v3.0)

| Stage | Setup/action | Expected kỹ thuật | Trạng thái code |
|---|---|---|---|
| I | Fixture train 16/val 8, 2 epochs, batch=4, callback dừng sau save epoch 1 | Trainer chạy huấn luyện thật trên tiny model local | Có |
| II | `run_experiment(action='train',callbacks=[StopAfterFirstCheckpoint()])` | Raise `InterruptedError`, **không** có `completed.json` | Có |
| III | kiểm `checkpoints/checkpoint-4/optimizer.pt` | Có optimizer state sau 4 steps đầu | Có |
| IV | `run_experiment(action='resume')` | `global_step==8`, `epoch==2`, có completed marker | Có |
| V | `predict_texts` trước/sau `reuse` | `p_positive` xấp xỉ nhau, `atol=1e-7` | Có |
| VI | so sánh history | lịch sử load từ disk bằng history trả về | Có |
| VII | đếm evaluation rows | `len([x for x in history if 'eval_f1' in x])==2` | Có |
| VIII | train trùng ID, resume sau completed | FileExistsError và ValueError tương ứng | Có |

**Tổng:** **1** test function, 1 pytest case; nhiều stages/assertions. Nếu cô hỏi “test huấn luyện thực hay mock?”, trả lời: Trainer thực sự tối ưu tiny random DistilBERT trên synthetic text, không mock train, nhưng không phải pretrained IMDb run.

### Rủi ro và test đề xuất

- ENGINE-P01 (chưa có): checkpoint thiếu optimizer/scheduler hoặc corruption → resume từ chối sớm.
- ENGINE-P02 (chưa có): run ID khác contract/dataset SHA bị từ chối khi reuse.
- ENGINE-P03 (chưa có): đánh giá val không dùng test tokenized (instrument trace).
- ENGINE-P04 (chưa có): callback dừng ngay giữa epoch trước checkpoint và recover policy.
- ENGINE-P05 (chưa có): config evaluation save cadence không tương thích → báo lỗi.
- ENGINE-P06 (chưa có): multi-run concurrency/ghi file, GPU OOM, disk full.

**Sự khác biệt cần phát biểu:** tiny ENGINE-01 kiểm vòng đời; `reports/reference_run/history.json` và metrics quick cung cấp chứng cứ mô hình thật đã từng chạy. Hai loại không thể thay thế nhau. Liên quan FR07/08/10/11 và NFR03.

# Đặc tả huấn luyện — engine.py

## 1. Mục đích

Đáp ứng trực tiếp Exercise 2 bước 5–6: tạo TrainingArguments và Trainer.
Đóng gói các thiết lập và giao toàn bộ loop, optimizer, scheduler, checkpoint cho Trainer quản lý
Không có vòng lặp train_step riêng cạnh tranh với Trainer; tránh hai nguồn trạng thái.

## 2. Hợp đồng

`run_experiment(cfg, tokenized, tokenizer, manifest, artifact_root, log_root, action, callbacks=None)`
trả `(trainer, history, run_dir)`. trainer.model chứa best weights theo validation sau train/resume,
hoặc model đã export khi reuse. Test dataset không đưa vào eval_dataset; caller gọi predict sau khi hoàn tất.
`callbacks` phục vụ kiểm thử gián đoạn có kiểm soát, không thay thuật toán học mặc định.

## 3. TrainingArguments

AdamW (`adamw_torch`), LR 2e-5, weight_decay .01; linear LR schedule với 10% bước warmup.
Gradient clipping max norm 1.0. Validation/save mỗi epoch; logging mỗi 10 steps và bước đầu.
Chọn best theo F1 Positive validation, hướng tăng. `load_best_model_at_end=True`, save_total_limit=2.
Trainer quyết định best/tie theo API phiên bản đã pin; không tự viết bộ so sánh riêng.
Mixed precision tắt để chạy CPU/GPU nhất quán; có thể bổ sung ở run riêng sau khi kiểm chứng.
Dataloader worker 0 phù hợp Windows/Colab, seed/data_seed giống RunConfig, không push Hub.

## 4. Lifecycle và artifacts

### Train
Kiểm tra thư mục run rỗng → seed → build pretrained → Trainer → ghi config/manifest trước train →
train → history → xác nhận đủ epoch → export best_model + tokenizer → completed marker cuối cùng.
Nếu callback dừng sớm, ghi history và báo InterruptedError; không viết completed.
Config ghi trước train giúp resume khi Colab mất kết nối trước lúc export.

### Resume
Đọc config, so sánh contract → tìm checkpoint-* gần nhất → kiểm tra chưa đủ epochs →
Trainer.train(resume_from_checkpoint=path). Trainer khôi phục optimizer/scheduler/RNG/state.
Action không nằm trong contract; timestamp, output path cũng không. Không xóa lịch sử cũ.
Không tăng target epochs tại đây: linear scheduler phụ thuộc tổng bước đã định trước.
Checkpoint chỉ lưu cuối epoch nên có thể phải chạy lại phần epoch đang dang dở.

### Reuse
Yêu cầu config/history/completed và best_model/config, safetensors, tokenizer_config.
Nạp model local, tạo Trainer phục vụ predict nhưng **không gọi train**.
Caller vẫn dùng cùng tokenizer identity và dữ liệu manifest; đổi profile/seed/length thì tạo run riêng.

## 5. Ngoại lệ và phục hồi

| Điều kiện | Hành vi |
|---|---|
| train vào thư mục đã có file bất kỳ | FileExistsError, không xóa |
| action sai | ValueError |
| resume không có checkpoint | FileNotFoundError |
| contract khác | ValueError, yêu cầu run mới |
| resume một run completed | ValueError, chọn reuse |
| thiếu file best_model khi reuse | FileNotFoundError |
| callback dừng trước đủ epoch | InterruptedError, checkpoint giữ nguyên |

Trường hợp hiếm: checkpoint cuối đã đủ epoch nhưng runtime ngắt ngay trước export.
Không tiếp tục scheduler vượt mục tiêu. Có thể phục hồi thủ công từ best checkpoint ghi trong
`checkpoints/checkpoint-<cuối>/trainer_state.json`: dùng AutoModelForSequenceClassification.from_pretrained
với `best_model_checkpoint`, lưu vào best_model và lưu tokenizer; lấy log_history, epoch, global_step,
best_metric từ state để phục hồi history/completed. Nếu chuyển máy, đường dẫn best checkpoint tuyệt đối
trong state cần ánh xạ về checkpoint cùng tên trong run hiện tại. Chỉ làm trên bản sao run.
Cách đơn giản an toàn hơn cho bài thực hành: đổi run_id và train lại.

## 6. Kiểm chứng

Integration test tạo model nhỏ local, train 1/2 epochs rồi callback dừng sau save;
resume đến đủ 2 epochs, kiểm tra global_step không reset; reuse cho xác suất khớp.
Tách test phần mềm này khỏi thí nghiệm IMDb. Không tự suy ra model thật có accuracy tốt từ test này.


## 7. Đối chiếu với kế hoạch và test case (bổ sung phiên bản 2.0)

**Vị trí trong quy trình:** [Phase 3](../plans/phase3.md) xây dựng/kiểm tra Trainer và chiến lược validation; [Phase 4](../plans/phase4.md) kiểm tra lifecycle train/resume/reuse và artifacts. Nếu sửa config để tối ưu một run mới, tạo `run_id` mới thay vì tái sử dụng checkpoint cũ.

**Test hiện có:** [`tests/03_test_engine.md`](tests/03_test_engine.md) mô tả ENGINE-01 trong code `tests/test_engine.py`. Test này tạo tiny DistilBERT local, train 16 mẫu với batch 4 (4 steps/epoch), dừng sau checkpoint-4 tại epoch 1, resume đạt step 8 ở epoch 2, rồi kiểm tra xác suất reuse với atol=1e-7. Mười điều kiện kiểm tra trong đặc tả vẫn chỉ tạo thành **một pytest case** hiện hữu. Các guard atomic và mismatch độc lập xem [`tests/04_test_utils.md`](tests/04_test_utils.md).

**Tiêu chí hoàn tất:** history có validation metrics, completed chỉ xuất hiện sau khi đủ epoch và save model; dữ liệu test không có trong eval_dataset của Trainer; việc reuse phải có `best_model/model.safetensors`, không thể thực hiện chỉ với `reports/reference_run/` trong ZIP hiện tại. Kết quả quick lịch sử nằm ở `reports/VALIDATION.md`, không phải số liệu từ tiny integration test.

## 8. Luồng thao tác từng bước của engine (v3.0)

```text
run_experiment(cfg, tokenized, tokenizer, manifest, artifact_root, log_root, action)
  1. run_dir = artifact_root / cfg.run_id
  2. contract = { run_config, data_sha256=digest(manifest), tokenizer_identity }
  3. utils.check_action(run_dir, action, contract)
  4. nếu resume: get_last_checkpoint + check trainer_state.epoch < cfg.epochs
  5. seed_everything(cfg.seed)
  6. nếu reuse: nạp best_model local; ngược lại build pretrained base + classifier
  7. make_training_args; tạo Trainer(train, validation, collator, compute_metrics)
  8. nếu reuse: return Trainer + stored history ngay (KHÔNG train)
  9. nếu train: lưu config.json + split_manifest.json
 10. trainer.train(resume_from_checkpoint=checkpoint)
 11. ghi history.json; nếu chưa đủ epochs -> InterruptedError (không completed)
 12. save_model(best_model), tokenizer.save_pretrained, save_state, completed.json
 13. return Trainer đã load best weights, history, run_dir
```

Đây là mô tả rút gọn của code hiện hữu; các thư viện có thể có các callback/checkpoint nội bộ. Không được nhầm `train` mới với `resume` từ optimizer checkpoint; nạp `best_model` dùng inference/reuse không đồng nghĩa phục hồi optimizer state để train tiếp.

## 9. Bảng tham số TrainingArguments và lý do

| Tên tham số | Giá trị ở code | Vai trò / rủi ro |
|---|---|---|
| `num_train_epochs` | cfg.epochs (quick=2, full=3) | Number epochs, không phải số update cứng |
| `per_device_train_batch_size` | 16 mặc định | Batch mỗi thiết bị, chi phí RAM |
| `per_device_eval_batch_size` | 32 mặc định | Batch đánh giá, không cập nhật gradient |
| `learning_rate` | 2e-5 | Fine-tune pretrained weights |
| `optim` | `adamw_torch` | Optimizer AdamW |
| `lr_scheduler_type` | `linear` | Warmup + linear decay |
| `warmup_ratio` | 0.1 | Phần thời lượng warmup |
| `gradient_accumulation_steps` | 1 | Effective batch thay đổi nếu >1 |
| `max_grad_norm` | 1.0 | Gradient clipping |
| `eval_strategy`, `save_strategy` | `epoch` | Có cùng cadence để chọn best |
| `load_best_model_at_end` | True | Best weights theo validation metric |
| `metric_for_best_model` | `f1` | Positive F1 trong `compute_metrics` |
| `greater_is_better` | True | F1 càng cao càng tốt |
| `save_total_limit` | 2 | Giới hạn checkpoints, cần đủ để resume |
| `report_to` | `['tensorboard']` | Train/val logs |
| `seed`, `data_seed` | cfg.seed | Reproducibility có giới hạn |
| `fp16`, `bf16` | False | Dùng precision mặc định; giảm rủi ro máy không tương thích |
| `push_to_hub` | False | Không tự upload model |

## 10. Invariant và điều kiện phục hồi

- Train chỉ hợp lệ nếu run dir chưa có dữ liệu; nếu có → báo `FileExistsError`.
- Không được tạo `completed.json` trước khi đủ epochs. Test tích hợp cố ý stop ở epoch 1 và mong đợi `InterruptedError`.
- Resume chỉ khi contract trùng và có checkpoint có optimizer/trainer state; nếu run đã completed phải chuyển reuse.
- Reuse đòi đủ file best_model và metadata. Trong ZIP nộp hiện tại chỉ có một số metadata để đối chiếu run, **không đủ** để chạy reuse thực.
- Nếu đổi model revision/dataset/seed/max_length/batch/epoch, nên đặt run_id mới để tránh trộn thử nghiệm.
- `run_experiment` không đọc tokenized test; notebook gọi `trainer.predict` sau khi chọn model, do đó test không làm điều kiện chọn epoch trong engine.

## 11. Test ENGINE-01 giải thích theo logic kiểm thử

Trên fixture tiny (train=16, val=8, batch=4), epoch có 4 optimizer steps. Callback dừng sau epoch 1, test chờ thấy `checkpoint-4/optimizer.pt`, không có completed. Khi `resume`, global step lên 8 và epoch=2; viết completed, rồi `reuse` phải suy luận gần như cùng `p_positive` (`atol=1e-7`) và cùng history. Cuối cùng `train` lên run cũ và `resume` sau completed phải bị từ chối. Đây là **1 test case tích hợp** với nhiều assert; không phải kết quả từ IMDb.

## 12. Phân tích rủi ro thiết kế

| Rủi ro | Hậu quả | Kiểm soát hiện có | Cần cải tiến nếu triển khai thật |
|---|---|---|---|
| Resume khác data/config | Sai đối chứng | run contract | pin model/dataset SHA, store schema version |
| OOM hoặc hết disk | Dừng train/checkpoint hỏng | quick profile, exception | checkpoint integrity checks, resource monitor |
| Chỉ có best weights mà thiếu optimizer | Không resume train tiếp | `get_last_checkpoint` kiểm | Backup raw optimizer checkpoints |
| `completed` xuất hiện nhưng artifacts hỏng | Reuse fail | `check_action` required files | Validate checksum tất cả safetensors |
| Train F1 cao nhưng test thấp | Overfit/distribution shift | chọn best val, report test | đa seed + phân tích lỗi trên validation |

Tương ứng: FR07/FR08/FR10/FR11, [ENGINE test](tests/03_test_engine.md), [kiến trúc](06_architecture_and_interfaces.md).

# Đặc tả huấn luyện — engine.py

## 1. Mục đích

Đáp ứng trực tiếp Exercise 2 bước 5–6: tạo TrainingArguments và Trainer.
Kế thừa cách phân module của Lab 2 nhưng giao loop, optimizer, scheduler, checkpoint cho Trainer.
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

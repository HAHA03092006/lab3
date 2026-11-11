# Kiểm thử engine

## Ca tích hợp chính

16 mẫu train, 8 validation, batch 4, target 2 epochs. Tổng optimizer steps=8.
Callback on_save dừng sau checkpoint đầu ở epoch 1.

| Bước | Kỳ vọng |
|---|---|
| train với callback | InterruptedError vì mới 1/2 epoch |
| Kiểm tra checkpoint-4 | Có optimizer.pt, chưa có completed.json |
| resume cùng contract | global_step=8, epoch=2; không bắt đầu lại từ 0 |
| Export | completed.json, history, best_model và tokenizer |
| reuse | Không train, xác suất hai câu khớp atol=1e-7 |
| History | Có đủ 2 lần eval_f1 |
| train lại cùng folder | FileExistsError |
| resume khi completed | ValueError |

Số bước và trạng thái được assert, không chỉ kiểm tra import/hàm trả về.
Tests chạy CPU offline. Trainer vẫn thực hiện forward/backward/optimizer/scheduler/save/load thật.

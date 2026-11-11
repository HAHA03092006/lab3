# Kiểm chứng bản bàn giao Lab 3

## Thí nghiệm thật đã hoàn thành
- Exercise 1: tải pretrained SST-2 thật; tokenization, logits, softmax và pipeline đã chạy.
- Exercise 2: DistilBERT base được fine-tune toàn bộ tham số trên IMDb thật.
- Profile quick: 2.000 train, 500 validation, 1.000 test; seed 42; max_length 128; 2 epochs.
- Hoàn thành 250 optimizer steps; chọn best checkpoint bằng validation F1 = 0.862823.
- Test chỉ đánh giá sau khi chọn checkpoint. Accuracy = **86.2000%**;
  precision Positive = 0.867886; recall Positive = 0.854000;
  F1 Positive = **0.860887**; macro F1 = 0.861991; ROC-AUC = 0.931748.
- Confusion matrix (hàng nhãn thật, cột dự đoán, thứ tự Negative/Positive): [[435, 65], [73, 427]].
- Nạp lại model/tokenizer đã lưu và đối chiếu xác suất: assertion np.allclose(atol=1e-6) đạt.

## Bằng chứng và cách xem
- `notebooks/huggingface_sentiment_executed.ipynb`: 11 code cells đã thực thi, không có error output.
- `outputs/2026-11-11/distilbert_imdb_quick/183159-290735`: báo cáo, metrics JSON, predictions CSV, errors CSV, hình loss và confusion matrix.
- `reports/reference_run/`: cấu hình, lịch sử huấn luyện, split manifest và completed marker của run thật.
- `reports/notebook_execution.log`: log chạy từng cell.
- `reports/pytest_output.txt`: **24 tests passed**, kiểm tra split, metrics, lifecycle, save/load và Trainer resume thật trên tiny model offline.
- Một warning kiểm thử liên quan mtime filesystem: Trainer chuyển sang sắp xếp checkpoint theo số bước; không có test fail.

## Môi trường và giới hạn
Môi trường CPU, phiên bản cụ thể trong reference_run/config.json.
Do môi trường không cho kernel Jupyter mở socket ZeroMQ, notebook được chạy tuần tự bằng IPython InteractiveShell;
stdout, stderr và display outputs được lưu trở lại notebook, không tự điền kết quả.
Quick đã chạy đầy đủ. **Profile full chưa chạy**; code cấu hình 20.000 train / 5.000 validation / 25.000 test đã có sẵn.
Không dùng kết quả quick để khẳng định chất lượng trên toàn bộ benchmark hoặc tiếng Việt.
Checkpoint optimizer không nằm trong ZIP model bàn giao; ZIP model dùng cho inference/reuse của run đã hoàn tất.

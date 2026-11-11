# Kế hoạch kiểm thử Lab 3

## Phạm vi

Unit tests và một integration test Trainer thật chạy offline trên CPU, không tải weights/dataset.
Các test dùng dữ liệu tổng hợp hoặc DistilBERT nhỏ random, không dùng thay kết quả IMDb.
Chạy ở project root: `python -m pytest -q`. Kết quả thực tế: `reports/pytest_output.txt`.

| Nhóm | File | Bất biến được kiểm tra |
|---|---|---|
| Dữ liệu | test_data_setup.py | Split phân tầng/rời nhau/tái lập; clean phủ định; schema tokenization |
| Model | test_model_builder.py | Logits [B,2], loss scalar, toàn bộ tham số trainable |
| Engine | test_engine.py | Dừng sau checkpoint → resume đủ epoch → reuse cùng dự đoán |
| Utils/config | test_utils.py | JSON atomic, nonempty guard, contract mismatch, validate config |
| Evaluation | test_evaluate.py | Metrics tính tay, no-NaN, schema và alignment CSV |
| Notebook | test_notebook.py | Schema notebook hợp lệ, mọi code cell parse được |

## Tiêu chí đạt

Không failed tests. Không skip network tests rồi gọi đó là thí nghiệm pretrained thành công.
Khi chạy notebook chính: phải hoàn thành Exercise 1, train/resume/reuse, evaluate và reload.
Đọc log/metrics thực để phân biệt kiểm chứng kỹ thuật và kết quả bài toán.

## Test không bao phủ

GPU OOM, tốc độ Colab, drift main revision trên Hub, độ chính xác sentiment của full dataset,
khác biệt phần cứng/seed, gián đoạn đúng lúc ghi model file lớn trên Google Drive.

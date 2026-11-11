# Báo cáo kết quả Lab 3 — distilbert_imdb_quick

## 1. Mục tiêu và phương pháp
Fine-tune distilbert/distilbert-base-uncased cho phân loại cảm xúc IMDb. Nhãn 0 = NEGATIVE, 1 = POSITIVE.
Đầu vào là văn bản; tokenizer tạo input_ids và attention_mask; model tạo hai logits.
Trainer tối ưu cross-entropy bằng AdamW và linear scheduler có warmup.
Chọn checkpoint theo F1 lớp Positive trên validation; test chỉ chạy sau khi chốt model.

## 2. Cấu hình thực nghiệm
- Profile: **quick**. Kết quả chỉ đại diện tập test thực sự đã dùng.
- Seed: 42; max_length: 128; epochs yêu cầu: 2.
- Learning rate: 2e-05; batch: 16; weight decay: 0.01.
- Số bước optimizer hoàn thành: 250.
- F1 validation tốt nhất: 0.8628.
- Exact-text overlap giữa các split: {'train__validation': 0, 'train__test': 0, 'validation__test': 0}. Đây là chẩn đoán, không sửa benchmark dựa vào test.

## 3. Kết quả đo trên test
| Chỉ tiêu | Giá trị |
|---|---:|
| Số mẫu | 1000 |
| Accuracy | 0.8620 |
| Precision (Positive) | 0.8679 |
| Recall (Positive) | 0.8540 |
| F1 (Positive) | 0.8609 |
| Macro F1 | 0.8620 |

## 4. Nhận xét và giới hạn
Validation loss đầu/cuối: 0.3594 / 0.3227.
Confusion matrix, predictions.csv và errors.csv là bằng chứng để xem loại lỗi và ví dụ cụ thể.
Không suy ra mô hình mới chắc chắn tốt hơn bản SST-2 nếu chưa đánh giá cả hai trên cùng tập test.
Một seed và một lần chia không đủ để kết luận ưu thế thống kê. Văn bản dài bị cắt ở max_length;
phủ định, mỉa mai và cảm xúc pha trộn cần phân tích thủ công. Mô hình tiếng Anh không được đánh giá
cho tiếng Việt. Confidence softmax không phải bảo đảm xác suất đúng đã được hiệu chuẩn.

## 5. Tái lập
Xem config.json, split_manifest.json, history.json, completed.json và best_model/ trong artifacts.
Dùng action='reuse' để tải lại model/tokenizer; giữ profile, seed, cấu hình dữ liệu như lần train.

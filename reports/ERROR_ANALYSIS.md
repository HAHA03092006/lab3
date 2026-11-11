# Phân tích lỗi của lượt quick đã chạy

Có 138/1.000 mẫu bị phân loại sai: 65 Negative bị dự đoán Positive và 73 Positive bị dự đoán Negative.
Bảng dưới dùng hai dòng đầu errors.csv (sắp confidence giảm dần), không phải mẫu được chọn ngẫu nhiên.
Nhãn 0 = Negative, 1 = Positive; độ dài được đếm bằng chính tokenizer đã lưu, trước truncation.

| Dòng errors.csv | Nhãn thật | Dự đoán | Confidence | Số token |
|---|---:|---:|---:|---:|
| 1 | 0 | 1 | 0.9613 | 118 |
| 2 | 0 | 1 | 0.9583 | 256 |

- Mẫu 1 khen cảnh đẹp, gợi lại kỷ niệm tuổi thơ nhưng chê phim lỗi thời và dễ làm trẻ lớn chán.
  Đây là văn bản khen/chê pha trộn; nhãn dataset là Negative nhưng model chọn Positive với confidence cao.
- Mẫu 2 mở đầu bằng việc bất ngờ xem hết phim rồi chuyển sang phê bình tính nhất quán của nhân vật;
  kết luận cuối không còn thích bộ phim. Review vượt max_length=128 nên phần cuối không được đưa đầy đủ vào model.
  Truncation là một giả thuyết hợp lý cho lỗi này, chưa phải quan hệ nhân quả đã kiểm chứng.
- Hai lỗi confidence cao cho thấy không nên xem softmax score là xác suất đúng đã hiệu chuẩn.

Cải tiến cần kiểm tra trên validation: tăng max_length, chia đoạn review, hoặc so sánh cách lấy phần đầu/cuối.
Chỉ đánh giá test sau khi chốt lựa chọn; không dùng 1.000 mẫu test này làm tập điều chỉnh hyperparameters.
Nội dung đầy đủ và sample IDs nằm trong errors.csv/predictions.csv, không cần sao chép dài vào báo cáo.

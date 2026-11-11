# Kiểm thử evaluate

## Tính tay

True=[0,1,1,1], predicted=[0,1,0,1]: TN=1, FP=0, FN=1, TP=2.
Kỳ vọng accuracy=.75, precision=1, recall=2/3, F1=.8. Adapter compute_metrics trả cùng dict.

## Biên và file

- Không dự đoán Positive: precision và F1 bằng 0, không NaN.
- Rỗng, logits không phải hai cột, logits NaN hoặc nhãn ngoài 0/1: ValueError.
- Perfect predictions synthetic: accuracy=1, xuất PNG/JSON/CSV.
- labels dự đoán không khớp raw_test: ValueError trước xuất kết quả.

Kết quả perfect trên synthetic chỉ xác minh phép tính; không được dùng như accuracy IMDb.

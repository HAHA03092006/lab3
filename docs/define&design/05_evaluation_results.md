# Đặc tả đánh giá và kết quả — evaluate.py, reporting.py

## 1. Nguyên tắc

Chốt model bằng validation. Test chỉ đánh giá cuối; không chọn LR/epochs/threshold từ test.
Dùng đúng raw_test và tokenized_test cùng thứ tự, xác nhận labels trước xuất CSV.
Không ghi kết quả kỳ vọng, không lấy số model card thay số thực nghiệm.

## 2. Độ đo

| Metric | Công thức/ý nghĩa |
|---|---|
| Accuracy | (TP+TN)/N |
| Precision Positive | TP/(TP+FP) |
| Recall Positive | TP/(TP+FN) |
| F1 Positive | 2PR/(P+R) |
| Macro F1 | Trung bình F1 hai lớp |
| ROC-AUC | Tính từ p_positive, không từ nhãn argmax |

Mẫu số zero: zero_division=0; nếu test chỉ có một lớp thì AUC=None.
Confusion matrix thứ tự [NEGATIVE, POSITIVE], hàng true, cột predicted: [[TN,FP],[FN,TP]].
Softmax tính sau trừ max logits để ổn định số học.

## 3. API

`metrics_from_logits(logits, labels)`: validates [N,2]/[N], N>0, nhãn 0/1, logits hữu hạn.
`compute_metrics(EvalPrediction)`: adapter cho Trainer, xử lý predictions là array hoặc tuple.
`predict_texts`: inference_mode, eval, batch tokenizer padding/truncation, trả nhãn/confidence/p_positive.
`export_evaluation`: lấy PredictionOutput, raw_test, output_dir, metadata; xuất dict metrics và files.
`plot_history`: train loss theo logging steps, validation loss/F1/accuracy theo epochs; không bịa train accuracy.
`write_report`: tạo Markdown từ metrics/history/completed có thật; nhận xét xu hướng có điều kiện.

## 4. Output schema

- test_metrics.json: accuracy, precision, recall, f1, macro_f1, roc_auc, N, cm, trainer_metrics, metadata.
- predictions.csv: sample_id, text, y_true, y_pred, p_positive, confidence.
- errors.csv: tối đa 20 dự đoán sai có confidence cao nhất. Rỗng có header nếu không có lỗi.
- confusion_matrix.png, history.png: ảnh minh họa từ số liệu chạy.
- REPORT.md: mục tiêu, cấu hình, kết quả, nhận xét và giới hạn tự sinh.
- new_review_predictions.json: kiểm tra inference sau reload.

Metadata ghi profile/seed/config/hash dữ liệu. Quick không được trình bày như kết quả full IMDb.

## 5. Phân tích lỗi và báo cáo

Đọc review bị sai để kiểm tra phủ định, mỉa mai, khen/chê pha trộn, text dài bị cắt.
Confidence lớn không đồng nghĩa đúng; confidence chưa được calibration.
Không quy nguyên nhân chắc chắn chỉ từ một câu lỗi. Ghi giả thuyết, ví dụ và hướng kiểm chứng trên validation.
Không so sánh accuracy giữa hai tập khác nhau. Slide không bắt buộc nhiều model nên một run fine-tune đủ phạm vi.

## 6. Tests

Ma trận nhầm lẫn tính tay; trường hợp không dự đoán Positive không NaN;
logits shape/labels sai phải lỗi; export đúng files; labels đảo phải từ chối.
Reload inference khớp trong test_engine. Chỉ artifact IMDb thật mới dùng báo cáo chất lượng sentiment.

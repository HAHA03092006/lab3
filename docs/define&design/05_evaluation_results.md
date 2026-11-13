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

## 7. Công thức và định nghĩa nhãn cần thống nhất (v3.0)

Với `y_true` và `y_pred` thuộc {0=Negative, 1=Positive}, confusion matrix luôn theo thứ tự rows=true, columns=predicted, nhãn `[0,1]`:

```text
                  Pred Negative   Pred Positive
True Negative          TN             FP
True Positive          FN             TP
```

Accuracy = `(TP+TN)/N`, Precision Positive = `TP/(TP+FP)`, Recall Positive=`TP/(TP+FN)`, F1 Positive=`2PR/(P+R)`, macro F1 là trung bình F1 của hai lớp. Khi mẫu số = 0, code sklearn dùng `zero_division=0`. `roc_auc` dùng `p_positive` liên tục nếu test có đủ cả hai lớp; không tính AUC từ nhãn hard. `metrics_from_logits` kiểm `logits[N,2]`, nhãn `[N]`, hữu hạn và thuộc {0,1} trước khi đo.

## 8. Truy xuất metrics quick đã lưu (không phải kết quả mới chạy)

| Chỉ số | Giá trị | Tính/kiểm tra |
|---|---:|---|
| Test N | 1.000 | JSON `num_samples` |
| TN | 435 | cm[0][0] |
| FP | 65 | cm[0][1] |
| FN | 73 | cm[1][0] |
| TP | 427 | cm[1][1] |
| Accuracy | 0.8620 | (435+427)/1000 |
| Precision Positive | 0.867886 | 427/(427+65) |
| Recall Positive | 0.8540 | 427/(427+73) |
| F1 Positive | 0.860887 | 2PR/(P+R) |
| Macro F1 | 0.861991 | JSON |
| ROC-AUC | 0.931748 | JSON, cần score liên tục để tái tính |

Nguồn: `../../outputs/2026-11-11/distilbert_imdb_quick/183159-290735/test_metrics.json`; báo cáo lịch sử `../../reports/VALIDATION.md`. Best validation F1 theo completed/report là khoảng 0.862823 — **không** thay bằng test F1.

## 9. API và schema xuất file

| File | Ai ghi | Thông tin | Có trong ZIP? |
|---|---|---|---|
| `test_metrics.json` | `export_evaluation` | score, confusion_matrix, trainer_metrics, metadata | **Có** |
| `predictions.csv` | `export_evaluation` | sample_id,text,y_true,y_pred,p_positive,confidence | **Không** (gitignored) |
| `errors.csv` | `export_evaluation` | top 20 lỗi confidence cao | **Không** (gitignored) |
| `confusion_matrix.png` | `export_evaluation` | heatmap confusion | **Có** |
| `history.png` | `plot_history` | training & validation trends | **Có** |
| `REPORT.md` | `write_report` | tổng hợp từ metrics/history/completed | **Có** |

Chính sách file bị bỏ qua giúp repo gọn nhưng giới hạn khả năng audit từng review. Không nhận định đã xác minh file CSV nếu file đó không nằm trong ZIP; khi báo cáo cần đánh dấu bằng chứng nào đã có.

## 10. Bất biến evaluation và giới hạn alignment

- Raw test và tokenized test phải xuất phát từ **cùng split và cùng thứ tự**; không shuffle riêng ở bước predict.
- `Trainer.predict(...metric_key_prefix='test')` chạy trên tokenized test; `prediction.label_ids` phải bằng `raw_test['label']`.
- Kiểm bằng labels chưa đủ phát hiện hoán vị hai review cùng nhãn, do đó nâng cấp bằng sample_id/hashes là cần thiết nếu yêu cầu audit cao.
- Không chọn threshold bằng test; argmax logits là quyết định hiện tại.
- Error CSV là **top 20 lỗi**, không phải tất cả 138 lỗi; nếu mất CSV cần tái xuất từ predictions, không bịa ví dụ.
- `reporting.write_report` hiện không có unit test riêng, dù đã có REPORT.md từ run quick. Đây là một coverage gap cần nói rõ.

## 11. Cách lập luận kết quả trong buổi bảo vệ

1. Đọc profile/seed/split để xác định phạm vi đánh giá.
2. Dùng confusion matrix xác minh accuracy, precision, recall và F1 bằng tay.
3. Phân biệt chọn model bằng validation F1 với đo tổng kết trên test.
4. Chỉ ra 65 FP, 73 FN; mô tả giả thuyết phủ định/độ dài/pha trộn, không khẳng định nhân quả.
5. Kết luận: quick run cho bằng chứng pipeline thực; **không** có full run, không claim generalization sang tiếng Việt hoặc benchmark khác.

Tương ứng FR09, FR12, FR14, FR15. Xem [test evaluation](tests/05_test_evaluate.md) và [đối chiếu bằng chứng](../analysts/implementation_evidence_audit.md).

# P5 — Đánh giá cuối, xuất artifacts và phân tích dự đoán sai

> **Mã:** P5 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Tính metrics chính xác, bảo toàn alignment raw/text/nhãn, xuất bằng chứng và nêu giới hạn có cơ sở.

**File liên quan:** `going_modular/evaluate.py`, `going_modular/reporting.py`, `tests/test_evaluate.py`, notebook §5–6, `docs/define&design/05_evaluation_results.md`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

Sau khi chọn checkpoint bằng validation, gọi Trainer.predict một lượt trên test. Dự đoán nhị phân từ argmax; xác suất Positive từ softmax logits; confusion matrix theo thứ tự label [0,1]. `export_evaluation` kiểm tra labels alignment trước khi ghi output.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Xác nhận test set không có trong `Trainer(eval_dataset=...)` ở phase train.
- [ ] Kiểm tra metrics accuracy/precision/recall/F1 Positive và macro F1 được tính từ logits/labels hợp lệ.
- [ ] Kiểm tra trường hợp không dự đoán Positive dùng `zero_division=0`, tránh NaN.
- [ ] Kiểm tra ROC-AUC tính từ p_positive và chỉ khả dụng khi có hai lớp thật.
- [ ] Kiểm tra confusion matrix `[[TN,FP],[FN,TP]]` với hàng nhãn thật, cột nhãn dự đoán.
- [ ] Xác nhận `prediction.label_ids` bằng raw_test['label'] theo đúng thứ tự trước khi export.
- [ ] Xuất `test_metrics.json`, `predictions.csv`, `errors.csv`, `confusion_matrix.png` và `history.png`.
- [ ] Kiểm tra `errors.csv` chứa tối đa 20 lỗi confidence cao nhất, không phải toàn bộ lỗi.
- [ ] Chạy reload suy luận với review mới và lưu `new_review_predictions.json` khi môi trường phù hợp.
- [ ] Viết nhận xét dựa trên ví dụ lỗi và metrics thực, không khẳng định nguyên nhân chắc chắn nếu chưa kiểm chứng.


## 4. Tài liệu/bằng chứng cần bàn giao

- Kết quả quick gốc ở `outputs/2026-11-11/distilbert_imdb_quick/183159-290735/`.
- `REPORT.md` sinh từ metrics/history/completed, khác với test plan / acceptance.
- Test hiện có: `test_hand_calculated_metrics`, `test_missing_predicted_class_no_nan`, `test_bad_metrics_inputs`, `test_export_and_alignment`.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Có thể tự kiểm confusion matrix quick `[[435,65],[73,427]]`, accuracy 0.862 trên 1.000 mẫu.
- Không khẳng định full dataset đã được đánh giá; dữ liệu quick có giới hạn.
- README/báo cáo chỉ sử dụng số liệu đối chiếu được với `test_metrics.json`.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Xử lý |
|---|---|
| Sai thứ tự raw/test sau map | Kiểm tra label alignment, giữ `sample_id` |
| Thổi phồng confidence | Ghi rõ softmax chưa calibration |
| Diễn giải lỗi một chiều | Tách quan sát, giả thuyết nguyên nhân và kiểm chứng |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

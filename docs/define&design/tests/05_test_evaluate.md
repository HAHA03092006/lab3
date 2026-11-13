# TEST SPEC EVALUATE — `going_modular/evaluate.py`

> **ID:** LAB3-TEVAL · **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **Test hiện có:** `../../../tests/test_evaluate.py` · **Phase:** `../../plans/phase5.md`.

## 1. Mục tiêu, nguyên tắc và thuật ngữ

Đảm bảo metrics phân loại nhị phân từ logits đúng phép tính, không sinh NaN ở trường hợp biên; validate cấu trúc input và nhãn; export kết quả vào file thật, từ chối ghi nếu thứ tự nhãn test mismatch. Nhãn **Positive = 1** là lớp dương. Confusion matrix sắp thứ tự `[0,1]` cho true/pred, tức `[[TN,FP],[FN,TP]]`.

## 2. Case đã triển khai trong Python

### EVAL-01 — Đo metrics bằng kết quả tính tay (`test_hand_calculated_metrics`)

- **Input:** `logits=[[2,0],[0,2],[2,0],[0,2]]`, `labels=[0,1,1,1]`.
- **Thực hiện:** `metrics_from_logits(logits, labels)`, sau đó chuyển kết quả cùng dữ liệu qua `compute_metrics(SimpleNamespace(predictions=..., label_ids=...))`.
- **Mô hình dự đoán:** `y_pred=[0,1,0,1]`; TN=1, FP=0, FN=1, TP=2.
- **Expected:** accuracy `3/4=0.75`, precision Positive `2/2=1.0`, recall Positive `2/3`, F1 Positive `0.8`; `compute_metrics` cho cùng dict với `metrics_from_logits`.
- **Failure mode:** nhầm trục true/pred, nhầm Positive label, tính metrics từ probability sai cách.
- **Trạng thái:** ĐÃ CÓ — 1 case.

### EVAL-02 — Không đoán lớp Positive (`test_missing_predicted_class_no_nan`)

- **Input:** logits `[[2,0],[2,0]]`; labels `[0,1]`; predicted `[0,0]`.
- **Expected:** precision Positive `0`, F1 Positive `0`; không NaN/exception. Sử dụng `zero_division=0` trong sklearn.
- **Trạng thái:** ĐÃ CÓ — 1 case.

### EVAL-03 đến EVAL-06 — Bắt input lỗi (`test_bad_metrics_inputs`, 4 tham số)

| Test ID | `logits`, `labels` | Lý do | Expected |
|---|---|---|---|
| EVAL-03 | `([], [])` | Batch rỗng | `ValueError` |
| EVAL-04 | `([[1,2,3]], [0])` | Logits có 3 cột, không phải 2 | `ValueError` |
| EVAL-05 | `([[NaN,1]], [1])` | Có logits không hữu hạn | `ValueError` |
| EVAL-06 | `([[1,2]], [2])` | Label ngoài {0,1} | `ValueError` |

- **Steps:** gọi `metrics_from_logits` với từng input lỗi trong `pytest.raises(ValueError)`.
- **Trạng thái:** ĐÃ CÓ — 4 cases từ `pytest.mark.parametrize`.

### EVAL-07 — Export kết quả và bảo vệ alignment (`test_export_and_alignment`)

- **Fixture:** `tiny_bundle` có raw test synthetic 8 mẫu; `labels=np.asarray(raw['test']['label'])`.
- **Input:** logits `np.eye(2)[labels]*2`, PredictionOutput dạng `SimpleNamespace(predictions=logits, label_ids=labels, metrics={'test_loss':0.1})`.
- **Steps:** (1) `export_evaluation(p, raw['test'], tmp_path/'eval', {'kind':'synthetic'})`; (2) kiểm tra accuracy; (3) kiểm tra `confusion_matrix.png`; (4) đảo `p.label_ids=1-labels`, gọi export sang `tmp_path/'bad'`.
- **Expected:** lần đầu accuracy `1.0` từ synthetic predictions; PNG tồn tại; lần sau `ValueError` trước khi xuất vì labels đảo không bằng raw_test. Hàm export hiện còn ghi `test_metrics.json`, `predictions.csv`, `errors.csv` nhưng test này **không assert trực tiếp sự tồn tại của mọi file đó**.
- **Trạng thái:** ĐÃ CÓ — 1 case.

## 3. File schema và yêu cầu quan sát

| Artifact | Nội dung đúng theo code | Rủi ro cần kiểm tra |
|---|---|---|
| `test_metrics.json` | accuracy, precision, recall, f1, macro_f1, roc_auc, num_samples, confusion_matrix, trainer_metrics, metadata | Không giả giá trị và phải ghi số mẫu |
| `predictions.csv` | sample_id, text, y_true, y_pred, p_positive, confidence | Alignment với raw test |
| `errors.csv` | Tối đa 20 hàng dự đoán sai, sắp confidence giảm | Không hiểu nhầm là toàn bộ lỗi |
| `confusion_matrix.png` | Ma trận theo thứ tự Negative/Positive | Đúng axes true/pred |
| `history.png` | Train/validation curves từ log_history | Không tự thêm train accuracy nếu không có |

**Lưu ý:** `history.png` thuộc `plot_history` được notebook gọi ở bước khác; không nằm trong assertions của `test_export_and_alignment`.

## 4. Tổng kết pass/fail

**7 pytest cases** trong `test_evaluate.py` (1+1+4+1). Lệnh: `python -m pytest tests/test_evaluate.py -v`. Kết quả synthetic accuracy=1.0 chỉ kiểm tra đường tính toán, tuyệt đối không được đưa vào báo cáo hiệu năng IMDb. So sánh kết quả test thật dựa trên `outputs/.../test_metrics.json`, không lấy từ pytest.

## 5. Mở rộng đề xuất — CHƯA TRIỂN KHAI

- EVAL-P01: Assert mọi output file export có schema đúng, cùng số hàng và metadata.
- EVAL-P02: Kiểm tra `roc_auc=None` khi raw test chỉ có một lớp (nếu export path cho phép).
- EVAL-P03: Kiểm `predict_texts` trả đúng label/confidence/p_positive, đúng batch count.
- EVAL-P04: Stress test logits cực lớn và cực âm để kiểm softmax ổn định.
- EVAL-P05: `plot_history` với history rỗng hoặc thiếu một metric, kiểm output PNG hợp lệ.
- EVAL-P06: Error CSV được sort theo confidence và giới hạn 20 records.

Các đề xuất trên không phải test đã được chạy.

## 6. Quy trình EVAL-01..07 và expected cụ thể (v3.0)

| Case | Input | Action | Expected |
|---|---|---|---|
| EVAL-01 | logits `[[2,0],[0,2],[2,0],[0,2]]`, labels `[0,1,1,1]` | `metrics_from_logits`, `compute_metrics` | accuracy=.75, precision=1, recall≈2/3, F1≈.8; hai API khớp |
| EVAL-02 | logits dự đoán toàn Negative, nhãn [0,1] | metrics | precision=0, F1=0 thay vì NaN |
| EVAL-03 | logits=[], labels=[] | metrics | ValueError N=0 |
| EVAL-04 | logits shape `[1,3]`, labels `[0]` | metrics | ValueError shape không phải `[N,2]` |
| EVAL-05 | logits có `NaN`, labels `[1]` | metrics | ValueError finite guard |
| EVAL-06 | logits `[1,2]`, labels `[2]` | metrics | ValueError nhãn ngoài {0,1} |
| EVAL-07 | synthetic raw test, logits dự đoán nhãn đúng | `export_evaluation` | accuracy=1, có confusion PNG; đảo toàn bộ label_ids → ValueError alignment |

**Failure log:** traceback, logits/labels dạng ẩn danh (nếu chứa dữ liệu riêng tư thì không dump text review), version sklearn/numpy, expected computed by hand. **Bằng chứng:** `tests/test_evaluate.py`, log lịch sử. Tổng **7 test cases**.

### Kiểm toán kết quả quick (bằng chứng khác với test synthetic)

`test_metrics.json` lưu confusion `[[435,65],[73,427]]` → 862/1000 đúng, 138 sai. `predictions.csv` và `errors.csv` được code xuất nhưng **không có trong ZIP**, không ghi là đã audit từng dòng. Trong 138 lỗi, error CSV bình thường chỉ xuất tối đa 20 lỗi confidence cao. F1 Positive chọn để báo theo lớp Positive, macro F1 giúp xem cân bằng lớp.

### Đề xuất chưa implement

- EVAL-P01: logits là tuple từ Trainer với shape hợp lệ và bất hợp lệ.
- EVAL-P02: đảo chỗ hai review **cùng nhãn**; cần sample ID fingerprint để nhận biết, vì label-only guard hiện chưa đủ.
- EVAL-P03: all Positive, NaN/Inf extremes, nhãn 0/1 cân bằng/lệch, ROC-AUC khi chỉ có một lớp.
- EVAL-P04: so JSON accuracy/CM với REPORT.md và PNG bằng script audit.
- EVAL-P05: plot history thiếu key/mỗi epoch lệch, tránh chart gây hiểu nhầm.
- REPORT-P01: unit test `write_report` đọc metrics đúng, không hardcode score.

Liên quan FR09/FR12/FR14/FR15, [module evaluate](../05_evaluation_results.md), [evidence audit](../../analysts/implementation_evidence_audit.md).

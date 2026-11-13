# REQUIREMENTS TRACEABILITY MATRIX — LAB 3

> **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **Mục đích:** Truy vết yêu cầu bài thực hành → module/notebook → phase → test hiện hữu hoặc bằng chứng run thực tế.  
> **Nguồn:** `../define&design/00_lab3_description.md`, `../plans/implementation_plan.md`, `going_modular/`, `tests/`.

## 1. Truy vết theo yêu cầu bài tập

| ID | Yêu cầu | Hiện thực code/notebook | Phase | Kiểm tra / bằng chứng | Ranh giới kết luận |
|---|---|---|---|---|---|
| E1.1 | Cài transformers và môi trường | `requirements.txt`, notebook §0 | P0 | `requirements.txt`, lịch sử môi trường trong reference config | Không suy từ pytest ra việc cài được trên máy khác |
| E1.2 | Nạp model sentiment pretrained | Notebook §1 với `SENTIMENT_MODEL` | P2 | `outputs/.../exercise1_pretrained/.../predictions.json` | Chỉ kiểm chứng pretrained inference |
| E1.3 | Tokenize một câu | `AutoTokenizer`, notebook bảng token/ID/mask | P2 | Bảng notebook đã chạy | Không phải dataset train |
| E1.4 | Sentiment prediction | `evaluate.predict_texts`, HF `pipeline` | P2 | predictions.json | Không có accuracy suy ra từ câu mẫu |
| E2.1 | Cài libraries cho fine-tuning | `requirements.txt`, notebook §0 | P0 | Package metadata | `evaluate` được cài; metrics dùng sklearn trong code |
| E2.2 | Tải binary dataset | `data_setup.load_imdb`, `prepare_raw_splits` | P1 | DATA-01..DATA-08, manifest reference | Test dữ liệu local khác chạy IMDb thật |
| E2.3 | Load model/tokenizer | `model_builder.load_tokenizer`, `build_model` | P2 | MODEL-01 và notebook §3 | MODEL-01 dùng tiny model random để test shape |
| E2.4 | Preprocess dataset | `clean_text`, `tokenize_splits`, collator | P1–P2 | DATA-07, DATA-08, notebook token batch | Dynamic padding trong batch |
| E2.5 | TrainingArguments | `engine.make_training_args` | P3 | Notebook §4 preview, engine spec | No fake train metrics |
| E2.6 | Trainer fine-tune | `engine.run_experiment` | P3–P4 | ENGINE-01, history/finished marker | Tiny integration không phải IMDb accuracy |
| E2.7 | Evaluate trained model | `Trainer.predict`, `export_evaluation` | P5 | EVAL-01..EVAL-07, quick test_metrics.json | Chỉ test sau chốt validation checkpoint |

## 2. Truy vết các yêu cầu mở rộng

| ID | Mục tiêu mở rộng | File thực hiện | Test hoặc bằng chứng | Ghi chú |
|---|---|---|---|---|
| FR08 | Save/reuse/resume không ghi đè | `utils.check_action`, `engine.run_experiment` | UTIL-02, ENGINE-01 | Action không nằm trong contract |
| FR09 | Kiểm model logits/loss hai lớp | `model_builder.build_model` | MODEL-01 | Logits `[B,2]`, scalar loss |
| FR10 | Metrics có kiểm tra input | `evaluate.metrics_from_logits` | EVAL-01..EVAL-06 | Error on empty/NaN/bad shape/label |
| FR11 | Giữ alignment raw/test trước export | `evaluate.export_evaluation` | EVAL-07 | Không xuất số sai mẫu |
| FR12 | Tạo report từ số liệu thật | `reporting.write_report` | Quick REPORT.md + JSON | Chưa có unit test riêng cho reporting |
| NF01 | Bảo vệ thư mục run và JSON atomic | `utils.save_json`, `check_action` | UTIL-01, UTIL-02 | Không tự xóa run cũ |
| NF02 | Reproducible config/splits | `config.RunConfig`, `stratified_indices`, manifest | DATA-01, DATA-08, UTIL-03..06 | Khác môi trường vẫn có thể sai biệt số học |
| NF03 | Notebook có schema/cú pháp đúng | `notebooks/huggingface_sentiment.ipynb` | NOTEBOOK-01 | Chưa phải kiểm thử e2e notebook |

## 3. Ma trận mã test / test function

| ID case | Test function | Số case pytest | Đặc tả |
|---|---|---:|---|
| DATA-01 | `test_split_balanced_disjoint_reproducible` | 1 | `../define&design/tests/01_test_data_setup.md` |
| DATA-02..06 | `test_invalid_split` (5 parametrizations) | 5 | Như trên |
| DATA-07 | `test_clean_keeps_negation` | 1 | Như trên |
| DATA-08 | `test_tokenization_and_identity` | 1 | Như trên |
| MODEL-01 | `test_logits_loss_and_all_trainable` | 1 | `../define&design/tests/02_test_model_builder.md` |
| ENGINE-01 | `test_real_trainer_resume_reuse_roundtrip` | 1 | `../define&design/tests/03_test_engine.md` |
| UTIL-01..06 | `test_atomic_json_preserves_original`, `test_guard_nonempty_and_config_mismatch`, `test_config_validation` (4) | 6 | `../define&design/tests/04_test_utils.md` |
| EVAL-01..07 | `test_hand_calculated_metrics`, `test_missing_predicted_class_no_nan`, `test_bad_metrics_inputs` (4), `test_export_and_alignment` | 7 | `../define&design/tests/05_test_evaluate.md` |
| NOTEBOOK-01 | `test_notebook_schema_and_python_cells` | 1 | `../define&design/tests/06_test_notebook.md` |
| **Tổng** | | **24** | Chỉ tính test code hiện có |

## 4. Bằng chứng và phạm vi đo được

- Bộ pytest trong `reports/pytest_output.txt` ghi lịch sử **24 passed, 1 warning**; thay đổi docs không sinh ra thêm pytest tests.
- `reports/VALIDATION.md` và `outputs/2026-11-11/distilbert_imdb_quick/183159-290735/test_metrics.json` ghi quick với test 1.000, accuracy 0.8620, F1 Positive 0.860887.
- Profile full **chưa chạy** trong artifact đầu vào. Không dùng output quick làm số liệu full.
- `reports/reference_run/` chứa config/history/manifest/marker nhưng không chứa weights safetensors; reuse chỉ chạy được khi đủ `best_model/`.
- Đề xuất test mới trong docs có tiền tố `*-Pxx` và trạng thái **CHƯA TRIỂN KHAI**. Nếu triển khai sau, cần tạo Python test và cập nhật ma trận ở đây.

## 5. Tiêu chí review cuối

- [ ] Mỗi yêu cầu E1.1..E2.7 có code/phase và bằng chứng phù hợp.
- [ ] Model spec ghi rõ ID/revision, input/output và kiến trúc/giới hạn.
- [ ] Test docs không cộng checklist/đề xuất thành test passed.
- [ ] README và validation thống nhất số liệu quick, không đưa ra accuracy dự kiến không có số liệu.
- [ ] `Lab3/docs/define&design/` là cây duy nhất của phần đặc tả.

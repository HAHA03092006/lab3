# MA TRẬN TRUY VẾT YÊU CẦU LAB 3 — MÃ FR CHUẨN HÓA

> **Version:** 3.0 — 13/11/2026. **Quy ước:** `define&design/00_lab3_description.md` là nguồn chuẩn của FR01–FR12. Mã FR08–FR11 cũ trong bảng mở rộng đã bị dùng sai; bản này **không còn dùng trùng mã**. Kết quả thực nghiệm được dẫn chứng từ ZIP, không phải test mới chạy trong lần chỉnh docs.

## 1. Vấn đề phiên bản cũ và cách sửa

| Mã bị trùng | Đặc tả tổng quan (giữ) | Ma trận cũ (loại mã trùng, chuyển sang) |
|---|---|---|
| FR08 | Tạo Trainer và fine-tune | Save/reuse/resume → **FR11** |
| FR09 | Đánh giá best model trên test | Logits/loss nhị phân → **FR13** |
| FR10 | Save/load model + tokenizer | Validation metrics input → **FR14** |
| FR11 | Resume/reuse, không ghi đè | Alignment khi export → **FR15** |
| FR12 | Report từ metrics thật | Giữ nguyên FR12; không trùng |

Mã `FR13`–`FR15` là **mở rộng của nhóm**, không khẳng định slide bắt buộc. `NFR` dành cho chất lượng phi chức năng, để người chấm biết rõ điều nào là yêu cầu và điều nào là phương án gia cố.

## 2. Ma trận E — truy vết từng bước đề bài

| Bước | Diễn giải có thể nghiệm thu | FR chính | Hiện thực/code | Giai đoạn | Kiểm tra và bằng chứng | Phạm vi chứng minh |
|---|---|---|---|---|---|---|
| E1.1 | Cài môi trường hỗ trợ Hugging Face | FR01 | `requirements.txt`, notebook phần 0 | P0 | Danh sách phiên bản, output notebook | Không bảo đảm cài thành công trên mọi máy |
| E1.2 | Nạp mô hình sentiment pretrained | FR02 | Notebook phần 1, `config.SENTIMENT_MODEL` | P2 | `outputs/2026-11-11/exercise1_pretrained/181811-576123/predictions.json` | Pretrained inference, không train |
| E1.3 | Biến câu mẫu thành tokens/IDs/mask và xem logits | FR03 | Notebook phần 1, `AutoTokenizer`/model | P2 | Notebook executed | Chứng minh tensor của câu mẫu |
| E1.4 | Dự đoán sentiment thủ công và pipeline | FR04 | `evaluate.predict_texts`, `pipeline` trong notebook | P2 | Predictions JSON & outputs | Không suy ra accuracy tổng thể từ 4 câu |
| E2.1 | Cài dependencies fine-tuning | FR01 | `requirements.txt` | P0 | Versions trong `reference_run/config.json` | Code dùng sklearn để tính metric, `evaluate` được cài |
| E2.2 | Tải IMDb nhị phân | FR05 | `data_setup.load_imdb` | P1 | `split_manifest.json`, notebook | Dataset tải khi có mạng/cache |
| E2.3 | Nạp tokenizer & classifier | FR02, FR06, FR13 | `model_builder.load_tokenizer`, `build_model` | P2 | MODEL-01, executed notebook | MODEL-01 dùng tiny model offline |
| E2.4 | Làm sạch, split và tokenize | FR06 | `prepare_raw_splits`, `clean_text`, `tokenize_splits` | P1–P2 | DATA-01..08, manifest | Test synthetic, IMDb có manifest thật |
| E2.5 | Cấu hình `TrainingArguments` | FR07 | `engine.make_training_args` | P3 | Notebook preview, source `engine.py` | Kiểm được tham số cấu hình, không tự suy đủ training |
| E2.6 | Fine-tune bằng `Trainer` | FR08, FR11 | `engine.run_experiment` | P3–P4 | ENGINE-01, history & completed | Test nhỏ + run quick được ghi nhận |
| E2.7 | Đánh giá model đã fine-tune | FR09, FR12, FR14, FR15 | `trainer.predict`, `export_evaluation`, `write_report` | P5–P6 | EVAL-01..07, metrics JSON, REPORT.md | Quick 1.000 test; full chưa chạy |

## 3. Ma trận FR chính thức — mỗi mã có đúng một nghĩa

| FR | Mô tả/điều kiện chấp nhận | Module hoặc notebook chính | Test/evidence | Phase | Mức xác minh trong ZIP |
|---|---|---|---|---|---|
| FR01 | Xác định/cài thư viện cần thiết; version tương thích API | `requirements.txt`, notebook §0 | file requirements, config môi trường | P0 | Có code và môi trường lịch sử |
| FR02 | Load checkpoint sentiment Exercise 1 và base Exercise 2 đúng vai trò | `config.py`, `model_builder.py`, notebook §1/§3 | JSON E1, notebook executed; MODEL-01 dùng tiny | P2 | Có bằng chứng notebook/run |
| FR03 | Trình bày tokens, input IDs, mask, logits/softmax câu mẫu | notebook §1 | notebook executed | P2 | Có output đã lưu |
| FR04 | Predict sentiment câu bằng API thấp và `pipeline` | `evaluate.predict_texts`, notebook §1 | E1 predictions.json | P2 | Có output đã lưu |
| FR05 | Load binary IMDb, giữ split benchmark | `data_setup.load_imdb` | manifest tham chiếu | P1 | Có manifest run quick |
| FR06 | Chia validation phân tầng, subset quick, clean & tokenize đúng | `data_setup.py` | DATA-01..08, manifest | P1–P2 | Test offline + manifest thật |
| FR07 | Định nghĩa TrainingArguments tương thích Trainer, best F1 | `engine.make_training_args` | inspect code, notebook preview | P3 | Có config, bằng chứng run quick |
| FR08 | Huấn luyện classifier DistilBERT bằng Trainer trên train/validation | `engine.run_experiment` | ENGINE-01, completed/history | P3 | Tiny integration + quick run lịch sử |
| FR09 | Predict trên test sau khi chọn best checkpoint, xuất metrics | `evaluate.export_evaluation`, notebook §5 | EVAL-01..07, `test_metrics.json` | P5 | Quick metrics đã có |
| FR10 | Lưu và nạp lại model/tokenizer, so sánh inference round trip | `engine.py`, notebook §6 | ENGINE-01, VALIDATION.md | P4–P6 | Test offline + xác nhận trong báo cáo lịch sử; weights không trong ZIP |
| FR11 | Phân biệt train/resume/reuse, từ chối ghi đè/sai contract | `utils.check_action`, `engine.run_experiment` | UTIL-02, ENGINE-01 | P4 | Test offline đã ghi |
| FR12 | Sinh báo cáo từ thông số đo được, không bịa kết quả | `reporting.write_report` | quick REPORT.md, metrics JSON | P5–P6 | Có output; chưa có unit test report độc lập |
| FR13 | Kiểm `logits[N,2]`, `loss` vô hướng & trainable params | `model_builder.build_model`, `count_params` | MODEL-01 | P2 | Offline tiny; model thực có parameter summary |
| FR14 | Validate đầu vào của metrics, bắt NaN/shape/nhãn lỗi | `evaluate.metrics_from_logits` | EVAL-01..06 | P5 | Test offline |
| FR15 | Bảo toàn thứ tự `raw_test`/`prediction`, xuất CSV/PNG/JSON | `evaluate.export_evaluation` | EVAL-07, quick JSON/PNG | P5 | Offline + một phần output thực |

**Ghi chú:** FR02 chứa cả hai checkpoint, nhưng tiêu chí của mỗi exercise khác nhau. FR10 không có nghĩa "model weights đang ở GitHub"; test load/reload là evidence trong lần chạy, còn ZIP thiếu weights nên không thể lặp lại chỉ bằng ZIP.

## 4. Ma trận phi chức năng (không dùng mã FR)

| NFR | Tiêu chí kiểm tra | Nguồn thiết kế | Bằng chứng hiện có / giới hạn |
|---|---|---|---|
| NFR01 | Không dùng test để huấn luyện/chọn checkpoint | `data_setup.py`, `engine.py`, notebook | Split/Trainer code, cần audit quy trình nếu chạy thêm |
| NFR02 | Seed, config, IDs và hash giúp tái lập split | `config.py`, `split_manifest` | DATA-01/DATA-08, reference manifest; không cam kết bitwise GPU |
| NFR03 | Không âm thầm ghi đè run, JSON an toàn | `check_action`, `save_json` | UTIL-01/02; atomicity phụ thuộc filesystem |
| NFR04 | Model/tokenizer/dataset revision được ghi nhận | `config.py`, `engine.py`, `model_builder.py` | `resolved_model_revision` có; dataset revision là `main` chưa pin SHA |
| NFR05 | Báo cáo phân biệt quick/full & test offline/real training | `reporting.py`, `reports/` | artifacts quick, full chưa chạy |
| NFR06 | Module phân lớp rõ, dễ chạy test offline | `going_modular/`, `tests/` | 6 test files; chưa đo coverage dòng |
| NFR07 | Dùng trên VS Code/Colab với phiên bản phụ thuộc rõ | requirements, notebook | Notebook có nhánh Colab; không chứng minh mọi OS/CUDA |
| NFR08 | Công bố giới hạn dữ liệu, sai số, truncation và bảo vệ thông tin đầu vào | `reports/ERROR_ANALYSIS.md`, `.gitignore` | Có phân tích; CSV raw review không trong ZIP |

## 5. Ma trận ID test: số lượng KHÔNG được đổi tùy tiện

| Nhóm và mã | Hàm thật trong `tests/` | Số case pytest | Test spec |
|---|---|---:|---|
| DATA-01 | `test_split_balanced_disjoint_reproducible` | 1 | [01_data](../define&design/tests/01_test_data_setup.md) |
| DATA-02..06 | `test_invalid_split` (5 tham số) | 5 | [01_data](../define&design/tests/01_test_data_setup.md) |
| DATA-07 | `test_clean_keeps_negation` | 1 | [01_data](../define&design/tests/01_test_data_setup.md) |
| DATA-08 | `test_tokenization_and_identity` | 1 | [01_data](../define&design/tests/01_test_data_setup.md) |
| MODEL-01 | `test_logits_loss_and_all_trainable` | 1 | [02_model](../define&design/tests/02_test_model_builder.md) |
| ENGINE-01 | `test_real_trainer_resume_reuse_roundtrip` | 1 | [03_engine](../define&design/tests/03_test_engine.md) |
| UTIL-01..06 | `test_atomic_json_preserves_original`, `test_guard_nonempty_and_config_mismatch`, `test_config_validation` (4 param) | 6 | [04_utils](../define&design/tests/04_test_utils.md) |
| EVAL-01..07 | `test_hand_calculated_metrics`, `test_missing_predicted_class_no_nan`, `test_bad_metrics_inputs` (4 param), `test_export_and_alignment` | 7 | [05_evaluate](../define&design/tests/05_test_evaluate.md) |
| NOTEBOOK-01 | `test_notebook_schema_and_python_cells` | 1 | [06_notebook](../define&design/tests/06_test_notebook.md) |
| **TỔNG** | | **24** | Số test trong mã nguồn hiện có và log lịch sử |

**Không thêm** kiểm thử đề xuất `DATA-Pxx`, `ENGINE-Pxx`, ... vào tổng 24. Số 24 là từ code/test log trong ZIP, không phải lần chạy mới khi sửa docs.

## 6. Bảng kiểm truy vết khi bảo vệ

| Câu hỏi cô có thể hỏi | Cách trả lời và chỉ ra bằng chứng |
|---|---|
| Làm sao biết đã hoàn thành Exercise 2? | Đi theo E2.2→E2.7: split manifest, `run_experiment`, `completed.json`, `test_metrics.json`. |
| Vì sao FR08 trong tài liệu này không còn là save/reuse? | Bản cũ trùng mã, đã giữ ý nghĩa FR08 trong đặc tả gốc và chuyển save/reuse sang FR11. |
| Unit test chứng minh accuracy 86,2%? | **Không.** Số đó từ run IMDb quick và `test_metrics.json`, test offline dùng tiny synthetic model. |
| Có thể chạy full và dùng lại weights luôn không? | Config full có; chưa có run full. ZIP thiếu weights để reuse ngay. |
| Xem đường đi từ câu chữ yêu cầu đến mã nguồn? | Hàng E/FR → file module → test ID → artifacts → giải thích hạn chế. |

## 7. Quy trình cập nhật ma trận khi có commit mới

1. Tạo yêu cầu mới chỉ khi có nhu cầu thật; giữ ID cũ không thay nghĩa.
2. Ghi tên hàm/file hiện thực, đường dẫn test tương ứng và trạng thái `đề xuất/đã có code/đã kiểm chứng`.
3. Nếu test được thêm, cập nhật số case từ `pytest --collect-only -q`, không ước lượng theo số assertions.
4. Nếu chạy lại thí nghiệm, lưu output mới, môi trường, seed, split, profile, model revision; không ghi đè kết quả lịch sử.
5. Người review xác nhận cột evidence hợp lý, rồi mới dùng để báo cáo.

Xem thêm: [phân tích yêu cầu](requirements_analysis.md), [kiểm toán bằng chứng](implementation_evidence_audit.md), [đặc tả tổng quan](../define&design/00_lab3_description.md).

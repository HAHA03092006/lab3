# KẾ HOẠCH TRIỂN KHAI LAB 3 — HUGGING FACE SENTIMENT ANALYSIS

> **Mã kế hoạch:** LAB3-PLAN · **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **Phạm vi:** Exercise 1 (pretrained inference), Exercise 2 (fine-tuning DistilBERT trên IMDb).  
> **Tài liệu nguồn:** `../define&design/00_lab3_description.md`; đặc tả model `../define&design/02_model.md`; ma trận truy vết `../analysts/requirements_traceability.md`.  
> **Nguồn sự thật:** code hiện tại trong `going_modular/`, notebook trong `notebooks/`, kết quả chạy trong `reports/` và `outputs/`.

## 1. Mục tiêu, sản phẩm bàn giao và nguyên tắc

Kế hoạch chia quá trình thành 8 phase nhỏ, có **công việc/đầu ra/checklist/điều kiện chuyển phase** để trưởng nhóm dễ giao việc, tự đánh dấu tiến độ và kiểm tra bằng chứng. Phân rã theo phụ thuộc kỹ thuật chứ không đặt thời lượng hoặc ngày hoàn thành giả định. Mỗi phase có thể gán người phụ trách và ngày hoàn thành khi nhóm thống nhất. Các checkbox mặc định chưa tích để người thực hiện xác nhận thực tế.

**Sản phẩm cần có:** notebook chạy được; gói `going_modular/`; bộ `tests/` offline; đặc tả dữ liệu, mô hình, engine, utils và đánh giá; `reports/VALIDATION.md`; bằng chứng kết quả quick; hướng dẫn tái lập. Kết quả bài toán không đồng nhất với kết quả kiểm thử phần mềm: mô hình tiny ngẫu nhiên trong pytest chỉ kiểm tra giao diện/tính đúng của quy trình.

**Nguyên tắc:** hai checkpoint có vai trò khác nhau; không trộn test vào train hoặc chọn siêu tham số bằng test; không ghi đè run cũ; checkpoint `main` không cố định; không tự đánh dấu hoàn thành nếu chưa đối chiếu file/log. Bản cập nhật này ưu tiên tài liệu, **không sửa module Python**.

## 2. Bảng điều phối 8 phase

| Phase | Tên giai đoạn | Tiền đề | Đầu ra bắt buộc | Điều kiện chuyển tiếp |
|---|---|---|---|---|
| P0 | Đọc đề và chuẩn bị môi trường | Bắt đầu | Phạm vi, dependencies, cấu hình quick/full | Setup và quy ước được xác nhận |
| P1 | Chuẩn bị, kiểm tra IMDb | P0 | Raw splits, manifest, schema nhãn | Không lẫn split, giữ sample ID |
| P2 | Tokenizer, model & Exercise 1 | P0; dữ liệu mẫu | Inference SST-2, model 2 lớp, tokenized splits | Kiểm tra IDs/mask/logits/loss |
| P3 | Fine-tuning với Trainer | P1–P2 | TrainingArguments, history, validation F1 | Có best checkpoint, không dùng test |
| P4 | Quản lý run và phục hồi | P3 | train/resume/reuse, contract, best_model | Bảo vệ ghi đè, round-trip hợp lệ |
| P5 | Đánh giá cuối và phân tích lỗi | P4 | Metrics, predictions, confusion matrix | Khớp nhãn/thứ tự; đúng số mẫu |
| P6 | Notebook và thuyết minh | P2–P5 | Notebook đầy đủ bước, báo cáo số liệu thật | Không có số liệu tưởng tượng |
| P7 | Kiểm thử, kiểm tra và bàn giao | P0–P6 | Test log, biên bản, cấu trúc repo | Tiêu chí nghiệm thu đáp ứng |

> **Chú ý:** Bảng trên mô tả thứ tự xây dựng/kiểm tra; các file Python, notebook và kết quả quick đã có trong ZIP đầu vào. Không suy ra rằng tất cả checklist đã được chạy lại trong phiên sửa tài liệu này.

## 3. Danh sách kế hoạch chi tiết

| Kế hoạch | Trọng tâm | Đầu mối code/test |
|---|---|---|
| [`phase0.md`](phase0.md) | Đề bài, môi trường, phạm vi và rủi ro | `config.py`, `requirements.txt`, notebook §0 |
| [`phase1.md`](phase1.md) | IMDb, stratified split, subset, manifest | `data_setup.py`, `test_data_setup.py` |
| [`phase2.md`](phase2.md) | SST-2 inference, tokenizer, DistilBERT head | `model_builder.py`, notebook §1–3, `test_model_builder.py` |
| [`phase3.md`](phase3.md) | Trainer, schedule, validation và checkpoint | `engine.py`, `test_engine.py` |
| [`phase4.md`](phase4.md) | Lưu run an toàn, resume/reuse | `engine.py`, `utils.py`, `test_engine.py`, `test_utils.py` |
| [`phase5.md`](phase5.md) | Metrics, test once, phân tích sai số | `evaluate.py`, `reporting.py`, `test_evaluate.py` |
| [`phase6.md`](phase6.md) | Notebook, artifacts, báo cáo | `notebooks/`, `reports/`, `test_notebook.py` |
| [`phase7.md`](phase7.md) | Test và điều kiện nghiệm thu | `tests/`, `reports/VALIDATION.md` |

## 4. Phân công, thời gian và theo dõi tiến độ (mẫu để điền)

Không tự chỉ định người hoặc hẹn ngày cho nhóm. Sau khi nhóm trưởng phân công, điền bảng và tích checklist trong từng phase:

| Phase | Người phụ trách | Ngày bắt đầu | Ngày hoàn thành | Trạng thái | Link PR/commit |
|---|---|---|---|---|---|
| P0 | Chưa phân công | — | — | Cần đối chiếu | — |
| P1 | Chưa phân công | — | — | Cần đối chiếu | — |
| P2 | Chưa phân công | — | — | Cần đối chiếu | — |
| P3 | Chưa phân công | — | — | Cần đối chiếu | — |
| P4 | Chưa phân công | — | — | Cần đối chiếu | — |
| P5 | Chưa phân công | — | — | Cần đối chiếu | — |
| P6 | Chưa phân công | — | — | Cần đối chiếu | — |
| P7 | Chưa phân công | — | — | Cần đối chiếu | — |

**Quy ước cập nhật:** `TODO` = chưa kiểm chứng; `IN_PROGRESS` = đang triển khai; `DONE` = đã có bằng chứng; `BLOCKED` = thiếu điều kiện; `REVIEW` = chờ nhóm trưởng duyệt. Checklist được tích sau khi chạy lệnh hoặc đối chiếu artifact, không dựa vào cảm tính.

## 5. Checklist nghiệm thu tổng

- [ ] Kiểm tra đề bài có đủ E1.1–E1.4 và E2.1–E2.7 trong notebook/traceability.
- [ ] Xác nhận checkpoint của Exercise 1 khác checkpoint của Exercise 2; tokenizer đồng bộ.
- [ ] Xác minh `RunConfig.for_profile('quick'|'full')` và đường đi `train/resume/reuse`.
- [ ] Xác minh split validation chỉ đến từ train IMDb, test gốc giữ riêng.
- [ ] Đối chiếu đầu vào/đầu ra từng module với tài liệu thiết kế và test specs.
- [ ] Chạy `python -m pytest -q` trên môi trường được cài đúng `requirements.txt`.
- [ ] Kiểm tra notebook nguồn có thể parse và (khi có mạng/tài nguyên) chạy thực tế.
- [ ] Đọc `reports/VALIDATION.md` và `outputs/.../test_metrics.json`, không ghi kết quả full nếu mới chạy quick.
- [ ] Kiểm tra các file code không bị sửa chỉ vì thay đổi tài liệu; review Git diff.
- [ ] Chỉ chốt bản nộp khi các đầu ra P0–P7 có bằng chứng thực tế.

## 6. Quy trình làm việc với Git/GitHub

1. Tạo nhánh riêng cho tài liệu (ví dụ `docs/lab3-spec-and-phases`); không chỉnh trực tiếp `main`.
2. Sửa một nhóm file theo phase, xem diff, commit với thông điệp có ý nghĩa.
3. Chạy kiểm tra khả dụng. Tài liệu không thay thế được test Python.
4. Mở Pull Request, mô tả file tạo mới và file sửa; ghi rõ có/không sửa `going_modular/`.
5. Đối chiếu nhận xét của nhóm trưởng với checklist/acceptance từng phase trước merge.

## 7. Các rủi ro và cách kiểm soát

| Rủi ro | Dấu hiệu | Kiểm soát |
|---|---|---|
| Hiểu nhầm thử nghiệm và unit test | Tiny model đạt test bị gọi là accuracy IMDb | Tách `tests/` khỏi `outputs/` và nêu scope |
| Dữ liệu bị lệch/lẫn | Test vào validation hoặc quick lấy các dòng đầu | Split phân tầng, sample_id và manifest |
| Checkpoint thay đổi | `revision='main'` cập nhật | Lưu resolved commit khi có, cân nhắc pin SHA |
| Resume sai run | Đổi dữ liệu nhưng reuse checkpoint | Contract config + manifest + tokenizer hash |
| Ghi đè dữ liệu | Dùng lại run_id train | `check_action` từ chối thư mục không rỗng |
| Kết quả báo cáo sai | README ghi số không khớp JSON | Lấy từ `test_metrics.json`, ghi rõ quick/full |
| Tài liệu hứa test chưa có | Viết đặc tả như đã implement | Đánh dấu `Đã có` / `Đề xuất thêm` rõ ràng |

## 8. Lệnh đối chiếu nhanh (chạy ở thư mục `Lab3/`)

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m pytest tests/test_engine.py -v
```

Không tự động chạy huấn luyện chỉ để kiểm thử docs. Khi nhóm muốn tái lập mô hình thật, mở `notebooks/huggingface_sentiment.ipynb`, chọn cấu hình/action tương ứng và chuẩn bị mạng/bộ nhớ. Lần chạy quick hiện lưu trong `reports/VALIDATION.md`; đó là bằng chứng lịch sử của bản gốc, không phải kết quả phát sinh khi sửa tài liệu.

## 9. Work Breakdown Structure (WBS) và quản lý phụ thuộc (bản v3.0)

| Mã công việc | Phụ thuộc | Deliverable | Review gate | Phạm vi kiểm chứng hiện có |
|---|---|---|---|---|
| WBS-00 | Bắt đầu | Requirements & environment | E1/E2 rõ, RunConfig nhập hợp lệ | Có specs, requirements, config |
| WBS-01 | WBS-00 | Raw splits, sample IDs, manifest | Disjoint IDs, stratify labels | DATA tests + quick manifest |
| WBS-02 | WBS-00/01 | E1 sentiment & tokenized data E2 | Token IDs/masks, 2 logits, labels correct | E1 output + MODEL/DATA tests |
| WBS-03 | WBS-01/02 | TrainingArguments và Trainer | Best validation F1, no test in train | `engine.py`, quick history |
| WBS-04 | WBS-03 | Artifact lifecycle | No overwrites, resume/reuse contract | ENGINE/UTIL tests |
| WBS-05 | WBS-04 | Test prediction & reports | Metrics from real logits, alignment | Quick metrics/PNG/REPORT |
| WBS-06 | WBS-02..05 | Notebook + thuyết minh | Code/doc/outputs khớp | Executed notebook + report |
| WBS-07 | WBS-00..06 | Test/UAT/handover | 24 existing tests + limitations documented | Old log/validation, not new run |

WBS biểu diễn **thứ tự kỹ thuật**, không phải lịch sử chứng minh từng cá nhân đã làm gì. Các nội dung còn thiếu, như test report độc lập và pin dataset revision SHA, là công việc cải tiến nên không tự điền ngày hoàn thành.

## 10. Phân loại rủi ro và phương án xử lý khi trình bày

| ID | Rủi ro | Xác suất / tác động (định tính) | Chỉ báo sớm | Biện pháp | Bằng chứng cần lưu |
|---|---|---|---|---|---|
| R01 | Dùng test để tune model | TB / Cao | Eval nhiều lần trên test khi đổi LR | Chỉ select bằng validation | Trainer args, notebook order |
| R02 | Quick subset lệch nhãn | TB / Cao | Một lớp chiếm đa số | Stratified sampling | split manifest labels |
| R03 | Tokenizer/model mismatch | Thấp–TB / Cao | IDs lạ, logits bất thường | Shared model ID/revision, tokenizer identity | config.json/sha |
| R04 | OOM/disk full | TB / Cao | Torch OOM, checkpoint hỏng | quick profile, giới hạn seq/batch, output dirs | error trace, resource notes |
| R05 | Resume nhầm run | TB / Cao | Contract mismatch | `check_action`, new run_id | config, ENGINE tests |
| R06 | Docs không khớp code | TB / Cao | FR trùng nghĩa, link lỗi, nói full đã chạy | ma trận FR chuẩn, code review | diff docs, audit links |
| R07 | Không có weights khi demo | Cao nếu dùng ZIP đơn thuần / Cao | Missing best_model.safetensors | tải checkpoint hợp lệ hoặc demo outputs lịch sử minh bạch | link/model checksum thực |
| R08 | Metrics không đúng confusion | TB / Cao | TP/TN/FP/FN bị đọc ngược | tính toán tay 4 ô và cross-check JSON | calculation memo |
| R09 | Model revision drift | TB / TB | Hub main đổi | pin SHA trong run tái lập | resolved SHA, versions |

Các mức định tính là **đánh giá lập kế hoạch**, không phải xác suất thống kê đã đo.

## 11. Mẫu chất lượng ở mỗi checkpoint (gates)

- **G0 – Spec ready:** mục tiêu, input, output, acceptance, test idea và owner dự kiến rõ; không có FR trùng nghĩa.
- **G1 – Module ready:** API contract, exception, unit test tối thiểu; docs lý giải lựa chọn.
- **G2 – Integration ready:** dữ liệu, model và Trainer đi cùng nhau; không dùng test để chọn hyperparameters.
- **G3 – Experiment ready:** log config+versions, split manifest, history, completed marker, test metrics.
- **G4 – Report ready:** số liệu trong slides/REPORT và JSON khớp; thống nhất quick/full, nêu giới hạn.
- **G5 – Handover ready:** link GitHub, README, docs index, notebook, test records; nếu thiếu weights ghi hướng truy xuất.

## 12. Quy trình PR, review và xử lý thay đổi yêu cầu

1. Mở issue hoặc ghi yêu cầu thay đổi với `E/FR/NFR` chịu ảnh hưởng, tác động lên dữ liệu/model/tests.
2. Tạo branch (`docs/traceability-fix`, `feature/...`, `fix/...`) từ `main` mới nhất; commit atomic cho từng mục tiêu.
3. Owner cập nhật spec và code; reviewer kiểm ma trận FR↔API↔tests, những số liệu có thật, đường dẫn nội bộ.
4. Chạy `pytest` nếu có thay code; sửa docs thuần thì audit link/schema/citation, không khẳng định chạy model.
5. Merge sau review; chụp link PR/commit và ghi vào worklog mẫu [quy trình nhóm](team_workflow_and_log.md).
6. Nếu regression, rollback commit liên quan thay vì xóa lịch sử; giữ artifacts run với ID khác để có thể đối chiếu.

## 13. Kế hoạch bàn giao tài liệu phục vụ cô chấm

| Mục cô xem | Mở gì đầu tiên | Dẫn tiếp tới |
|---|---|---|
| “Làm việc như thế nào?” | `../README.md` → kế hoạch này | `team_workflow_and_log.md` và P0–P7 |
| “Yêu cầu nào được làm?” | `../analysts/requirements_analysis.md` | `requirements_traceability.md` |
| “Tại sao thiết kế vậy?” | `../analysts/design_decisions.md` | `../theory/00_theoretical_foundations.md`, spec module |
| “Test những gì?” | `../define&design/tests/00_test_plan.md` | test cases DATA/MODEL/ENGINE/UTIL/EVAL/NOTEBOOK |
| “Kết quả thật ở đâu?” | `../analysts/implementation_evidence_audit.md` | `../../reports/VALIDATION.md`, `../../outputs/` |

**Không tự ký tên, không tự tích completed** nếu nhóm chưa đối chiếu evidence/commit. Đây là tài liệu để điền tiến độ thật, không phải cách trang trí hồ sơ.

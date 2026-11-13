# TEST PLAN — KẾ HOẠCH KIỂM THỬ LAB 3

| Trường | Thông tin |
|---|---|
| ID | LAB3-TEST-00 |
| Phiên bản đặc tả | 2.0 |
| Ngày cập nhật | 11/11/2026 |
| Đối tượng | Các module `going_modular/`, cấu hình và notebook nguồn |
| Framework | `pytest`; tiny offline model + synthetic dataset |
| Tài liệu nguồn | `../00_lab3_description.md`, `../02_model.md`, `../../plans/implementation_plan.md` |
| Bằng chứng lịch sử | `../../../reports/pytest_output.txt`: 24 tests passed, 1 warning trong lần chạy gốc |

## 1. Mục tiêu kiểm thử

Kiểm tra chất lượng phần mềm theo hợp đồng từng module: dữ liệu có split hợp lệ; model nhận tensor và trả logits/loss; Trainer quản lý checkpoint và phục hồi đúng; hàm metrics tính chính xác; utils bảo toàn file và từ chối thao tác nguy hiểm; notebook hợp lệ về cấu trúc/cú pháp. **Không đánh đồng unit test với đánh giá chất lượng mô hình pretrained trên IMDb.** Kết quả inference pretrained thật phải xem `outputs/` và `reports/VALIDATION.md`.

## 2. Chiến lược kiểm thử / môi trường

- **Unit:** gọi trực tiếp hàm Python với đầu vào kiểm soát được; assert invariant và exception.
- **Integration offline:** tạo tiny DistilBERT local (encoder 1 layer, hidden size 16) và dataset synthetic, train thật với `Trainer` qua 2 epoch, kiểm tra checkpoint/resume/reuse. Test này **không tải IMDb/model từ Hub**.
- **Static notebook:** `nbformat` validate và `ast.parse` các code cells của notebook gốc; không thể kết luận notebook đã chạy chỉ từ test này.
- **End-to-end pretrained:** chạy notebook trên Hub/IMDb khi có mạng/tài nguyên, đối chiếu outputs; thuộc phạm vi kiểm chứng thực nghiệm, không nằm trong 24 pytest cases của bản đầu vào.

Bộ requirements khai báo Python 3.10–3.12, `transformers==4.57.1`, `datasets==4.3.0`, `accelerate==1.11.0` và các thư viện hỗ trợ. Khi đổi phiên bản phải kiểm tra tương thích `Trainer(processing_class=...)`, `TrainingArguments(eval_strategy=...)`.

## 3. Ma trận kiểm thử và truy vết

| Nhóm | Đặc tả test | Code kiểm thử hiện có | Số case pytest thu được từ code | Đầu ra chính |
|---|---|---|---:|---|
| DATA | [`01_test_data_setup.md`](01_test_data_setup.md) | `tests/test_data_setup.py` | 8 | indices/labels, tokenized schema, manifest |
| MODEL | [`02_test_model_builder.md`](02_test_model_builder.md) | `tests/test_model_builder.py` | 1 | logits `[2,2]`, loss scalar, frozen=0 |
| ENGINE | [`03_test_engine.md`](03_test_engine.md) | `tests/test_engine.py` | 1 | checkpoint-4 → resume step 8 → reuse |
| UTILS | [`04_test_utils.md`](04_test_utils.md) | `tests/test_utils.py` | 6 | atomic JSON, contract guard, RunConfig validation |
| EVAL | [`05_test_evaluate.md`](05_test_evaluate.md) | `tests/test_evaluate.py` | 7 | metrics số học, lỗi input, CSV/PNG output |
| NOTEBOOK | [`06_test_notebook.md`](06_test_notebook.md) | `tests/test_notebook.py` | 1 | notebook schema và Python AST |
| **Tổng** | | | **24** | Theo số case được pytest parametrization tạo ra |

**Lưu ý:** Một hàm `test_real_trainer_resume_reuse_roundtrip` có nhiều bước assert nhưng vẫn chỉ là **1** test pytest. Đừng cộng số dòng checklist thành số test đã pass. Các test được đề xuất mở rộng trong mỗi tài liệu đều ghi `CHƯA TRIỂN KHAI`, không được tính trong bảng tổng.

## 4. Tiền điều kiện, cách chạy và thu thập bằng chứng

1. Đứng ở root `Lab3/`, kích hoạt venv đã cài thư viện trong `requirements.txt`.
2. Có quyền tạo thư mục trong `tmp_path`; pytest fixtures có thể khởi tạo tiny local weights/cache.
3. Chạy các lệnh:

```bash
python -m pytest -q
python -m pytest tests/test_data_setup.py -v
python -m pytest tests/test_model_builder.py -v
python -m pytest tests/test_engine.py -v
python -m pytest tests/test_utils.py -v
python -m pytest tests/test_evaluate.py -v
python -m pytest tests/test_notebook.py -v
```

4. Ghi ngày/phiên bản môi trường vào biên bản nếu có chạy mới. Chỉ thay `reports/pytest_output.txt` khi chính bạn đã chạy và lưu log mới; không chỉnh kết quả cũ bằng tay.
5. Đối chiếu chức năng test đã implement với test case/acceptance. Nếu bị fail, giữ traceback và phân tích: lỗi môi trường, dependency, regression hay sai kỳ vọng test.

## 5. Mẫu đặc tả test case thống nhất

Mỗi test case nên có: **Test ID**, đường dẫn/hàm thật, mục tiêu và yêu cầu liên quan, setup/tiền điều kiện, input, thao tác, **expected output định lượng**, exception hoặc failure mode, bằng chứng và trạng thái (ĐÃ CÓ TRONG CODE/CHƯA TRIỂN KHAI). Khi nhiều assert nằm trong một test function, mô tả từng assert nhưng không tính thành các pytest test độc lập.

## 6. Tiêu chí Pass/Fail & quy trình xử lý lỗi

- **PASS:** pytest hoàn tất exit code 0, không có failed cases; từng assertion trong case đạt. Warning phải được ghi nhận và đánh giá tác động, không tự coi warning là lỗi nghiêm trọng nếu không ảnh hưởng kết quả.
- **FAIL:** exception/assertion fail; lưu stacktrace, nêu môi trường và dữ liệu tái hiện, xác định module chịu trách nhiệm, sửa rồi chạy lại case liên quan và toàn suite.
- **SKIP:** nếu thêm skip phải ghi rõ lý do; không dùng skip để tuyên bố hoàn thành thử nghiệm pretrained.
- **NOT RUN:** chưa chạy ở môi trường hiện tại; trạng thái trung thực cho phiên sửa tài liệu.

## 7. Các giới hạn của suite hiện hữu

Chưa có coverage bắt buộc cho GPU OOM, inference model thật khi mất Internet, drift của model revision `main`, lỗi hỏng safetensors nửa chừng, đánh giá full IMDb, performance trên tiếng Việt, notebook thực thi từ đầu trong kernel VS Code mới. Đây là khoảng trống minh bạch, không coi là test đã đạt.

## 8. Bằng chứng và nghiệm thu

`reports/pytest_output.txt` ghi **24 passed, 1 warning** từ lần chạy trước khi cập nhật tài liệu. `reports/VALIDATION.md` ghi nhận một run quick pretrained thật. Để nghiệm thu trên máy mới, phải chạy lại lệnh ở mục 4. Các file tài liệu dưới `docs/define&design/tests/` chỉ mô tả phương án/expected results, không phải script tự chạy.

## 9. Chiến lược kiểm thử theo tầng và mức độ rủi ro (v3.0)

| Tầng | Mục đích | Ví dụ | Test gốc | Vị trí bằng chứng |
|---|---|---|---|---|
| Unit / pure function | Toán số và validation inputs | `metrics_from_logits`, `stratified_indices`, `save_json` | DATA/EVAL/UTIL | pytest output cũ |
| Contract / component | Tensor, schema, labels | `build_model`, tokenization | MODEL-01, DATA-08 | pytest output cũ |
| Integration offline | Trainer cùng optimizer/checkpoint, `resume/reuse` | stop epoch 1 → resume epoch 2 | ENGINE-01 | pytest output cũ |
| Static notebook | Notebook parse schema/Python | `nbformat.validate` + AST parse | NOTEBOOK-01 | pytest output cũ |
| Manual/e2e real | Kết quả pretrained E1 + IMDb quick | executed notebook + outputs | **Không nằm trong 24 pytest cases** | `reports/VALIDATION.md`, `outputs/` |
| Khả năng mở rộng | GPU, full, calibration, drift, robustness | chưa triển khai | `*-Pxx` | Không có evidence |

## 10. Entry, exit, artifacts và trách nhiệm kiểm thử

**Entry:** code import được, dependencies tương thích, test fixture chạy offline, tmp_path writable, cấu hình nhãn 0/1. **Exit kỹ thuật:** pytest exit code 0 trên môi trường test, mọi case bắt buộc PASS; nếu warning thì ghi tác động. **Exit thực nghiệm:** quick output từ pretrained thật có config/manifest/history/metrics; **không** tự thay thế exit bởi notebook chỉ parse thành công. **Exit tài liệu:** spec ↔ test code ↔ matrix khớp và bằng chứng dẫn được.

Vai trò đề xuất (cần điền tên thực tế): module owner xây test; reviewer xác nhận oracle/case còn thiếu; integrator chạy toàn suite; nhóm trưởng tổng hợp report. Nếu một người làm cả hai vai, ghi rõ cách review chéo. Không tự điền tên thành viên khi chưa biết.

## 11. Một test case mẫu hoàn chỉnh

**ID:** EVAL-01. **Mục tiêu:** metric tính đúng bằng tay. **Precondition:** nhập module `going_modular.evaluate`, có NumPy/scikit-learn. **Input:** logits `[[2,0],[0,2],[2,0],[0,2]]`, labels `[0,1,1,1]`. **Bước:** gọi `metrics_from_logits`, so các fields với oracle; gọi `compute_metrics` với cùng predictions và labels. **Expected:** accuracy `0.75`, precision `1`, recall `2/3`, F1 `0.8`; hai API cho kết quả tương đương. **Pass:** mọi assert đạt. **Fail:** khác số/NaN/exception; lưu traceback và version thư viện. **Bằng chứng:** `tests/test_evaluate.py::test_hand_calculated_metrics`, code gốc và log lịch sử.

## 12. Hướng dẫn lưu chứng cứ khi cô yêu cầu demo

1. Ghi `git rev-parse HEAD`, `python --version`, pip versions và `pytest` output.
2. Chạy từng case hoặc toàn suite; không chỉnh file log cũ cho khớp môi trường.
3. Với real experiment, ghi profile/action/seed/splits/model+dataset revisions, số epochs và checkpoint được chọn.
4. Đối chiếu test metrics JSON với confusion matrix hình và phép tính tay.
5. Nếu có fail, nêu loại lỗi (input test, environment, regression, version drift) và trace, không chỉ nói “đã fix”.

## 13. Rủi ro còn lại theo ưu tiên

| Mức | Khoảng trống | Đề xuất test (chưa implement) |
|---|---|---|
| Cao | Label-only alignment không bắt hoán đổi sample cùng nhãn | EVAL-P02: đảm bảo sample IDs theo prediction |
| Cao | Weights & CSV không có trong ZIP | END2END-P01: tái xuất model and artifacts từ run thật |
| Trung bình | `reporting.write_report` chưa có unit test | REPORT-P01: số metric trong Markdown khớp JSON |
| Trung bình | Model/dataset `revision='main'` mutable | CONFIG-P01: snapshot pinned revisions & compatibility |
| Trung bình | `load_imdb` thiếu dữ liệu/mất mạng | DATA-P01: explicit error/path |
| Thấp–TB | full/multi-GPU/performance chưa chạy | E2E-P02: benchmark theo tài nguyên và seed |

Đây là **đề xuất**, không phải thêm số test đã passed. Xem [kịch bản nghiệm thu](07_acceptance_scenarios.md) và [evidence audit](../../analysts/implementation_evidence_audit.md).

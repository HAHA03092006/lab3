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

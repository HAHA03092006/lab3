# HỒ SƠ ĐẶC TẢ – THIẾT KẾ – KIỂM THỬ – TRIỂN KHAI LAB 3

> **Lab:** Get Started with Hugging Face – phân loại cảm xúc tiếng Anh.  
> **Bản chỉnh lý docs:** 3.0, ngày 13/11/2026.  
> **Nguyên tắc kiểm chứng:** Những dòng mô tả triển khai dựa trên `going_modular/`, `notebooks/`, `tests/` và artifacts đang có trong ZIP đầu vào. Tài liệu này **không phải nhật ký nhóm đã thực hiện từng ngày** và không xác nhận đã chạy lại các lệnh sau khi chỉnh docs.

## 0. Cách đọc trong buổi báo cáo

1. **Hiểu đề và phân rã yêu cầu:** [Phân tích yêu cầu chi tiết](analysts/requirements_analysis.md) → [đặc tả tổng quan](define&design/00_lab3_description.md).
2. **Chứng minh yêu cầu đã đi vào code:** [Ma trận truy vết FR/E/NFR](analysts/requirements_traceability.md), có đường dẫn file/hàm, test, chứng cứ, hạn chế.
3. **Giải thích tại sao dùng DistilBERT / Trainer / metric:** [Cơ sở lý thuyết](theory/00_theoretical_foundations.md) và [quyết định thiết kế](analysts/design_decisions.md).
4. **Diễn giải từng module:** [Sơ đồ kiến trúc & hợp đồng](define&design/06_architecture_and_interfaces.md) rồi `01_data` → `02_model` → `03_engine` → `04_utils` → `05_evaluation_results`.
5. **Giải thích cách test:** [Kế hoạch kiểm thử](define&design/tests/00_test_plan.md), 7 file test spec tương ứng và [kịch bản nghiệm thu](define&design/tests/07_acceptance_scenarios.md).
6. **Trình bày công việc theo giai đoạn:** [Kế hoạch tổng](plans/implementation_plan.md), [P0–P7](plans/phase0.md) và [quy trình nhóm / nhật ký mẫu](plans/team_workflow_and_log.md).
7. **Trình bày kết quả trung thực:** [Đối chiếu bằng chứng](analysts/implementation_evidence_audit.md), `../reports/VALIDATION.md`, `../reports/pytest_output.txt` và `../outputs/2026-11-11/...`.
8. **Luyện phần vấn đáp:** [Hướng dẫn báo cáo – câu hỏi phản biện](presentation/defense_guide.md).

## 1. Danh mục chính và công dụng

| Nhóm | Tài liệu quan trọng | Câu hỏi mà tài liệu trả lời |
|---|---|---|
| Đặc tả tổng quan | `define&design/00_lab3_description.md` | Bài toán gì, đầu vào/đầu ra nào, phải làm gì, thế nào là đạt? |
| Phân tích yêu cầu | `analysts/requirements_analysis.md`, `requirements_traceability.md` | Vì sao tách các FR, mỗi FR được hiện thực/kiểm chứng ở đâu? |
| Lý thuyết | `theory/00_theoretical_foundations.md` | Pretrained, tokenization, attention, fine-tuning, F1 là gì? |
| Thiết kế module | `define&design/01_...` đến `06_...` | Module nào có trách nhiệm gì, cách gọi API, bất biến, ngoại lệ? |
| Kiểm thử | `define&design/tests/` | Tiền điều kiện, dữ liệu test, thao tác, expected, đối chứng ra sao? |
| Kế hoạch | `plans/` | Làm theo thứ tự nào, đầu ra và DoD cho từng phase? |
| Bằng chứng | `analysts/implementation_evidence_audit.md` | Cái gì đã chạy thật, chỉ là test offline, hoặc còn thiếu? |

## 2. Quy tắc đặt mã và quản trị thay đổi

- **E1.1–E1.4 / E2.1–E2.7:** từng bước của hai exercise, giữ nguyên ổn định.
- **FR01–FR12:** các yêu cầu chức năng trong đặc tả tổng quan làm **nguồn chuẩn duy nhất**.
- **FR13–FR15:** các yêu cầu chức năng mở rộng của nhóm, tách riêng khỏi yêu cầu tối thiểu của slide.
- **NFR01–NFR08:** yêu cầu phi chức năng; không tái sử dụng FR để chỉ tiêu chất lượng.
- **DATA/MODEL/ENGINE/UTIL/EVAL/NOTEBOOK-xx:** mã test case đã có trong mã nguồn.
- **`*-Pxx`:** kiểm thử *đề xuất*, chưa có test Python, không cộng vào số test passed.
- **P0–P7:** giai đoạn xây dựng; thứ tự logic không phải nhật ký thời gian.
- **Trạng thái bằng chứng:** `Đã có code`, `Đã chạy theo artifacts`, `Chỉ test offline`, `Chưa có chứng cứ`, `Đề xuất`.

Khi thay đổi chức năng: sửa `00_lab3_description.md` → chỉnh ma trận truy vết → chỉnh spec module → chỉnh đặc tả test & test Python nếu cần → cập nhật phase / bằng chứng / README. Khi chỉ sửa docs, không được ghi thêm một lần chạy thực nghiệm tưởng tượng.

## 3. Phạm vi những gì đã được đối chiếu

- Module: `config.py`, `data_setup.py`, `model_builder.py`, `engine.py`, `evaluate.py`, `utils.py`, `reporting.py`.
- Tests: 6 tệp `tests/test_*.py`, fixture trong `tests/conftest.py`.
- Notebook: `huggingface_sentiment.ipynb`, bản `huggingface_sentiment_executed.ipynb`.
- Artifacts: `reports/reference_run/`, `reports/VALIDATION.md`, `reports/pytest_output.txt`, `outputs/2026-11-11/`.
- Trong ZIP **không có weights `best_model/` và không có `predictions.csv`, `errors.csv`**; không tuyên bố có thể chạy action `reuse` trực tiếp từ ZIP chỉ với các file còn lại.

## 4. Mốc kiểm chứng từ bản ZIP đầu vào

| Mục | Giá trị | Loại bằng chứng |
|---|---|---|
| Profile quick | Train 2.000 / validation 500 / test 1.000, seed 42 | `reports/VALIDATION.md`, split manifest |
| Kết quả test quick | Accuracy **0.8620**, F1 Positive **0.860887**, ROC-AUC **0.931748** | `outputs/.../test_metrics.json` |
| Confusion matrix | `[[435,65],[73,427]]` (hàng thật, cột đoán) | `test_metrics.json`, hình confusion matrix |
| Pytest lịch sử | 24 passed, 1 warning | `reports/pytest_output.txt` |
| Full profile | Có cấu hình, **chưa có kết quả full** | `RunConfig.for_profile('full')`, `VALIDATION.md` |

Không sửa bảng này khi không có lần chạy mới và file output đối chứng; tỷ lệ thành công của tests không chứng minh accuracy của mô hình.

## 5. Tái lập kiểm thử và giới hạn máy chấm

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

Việc chạy Exercise 1/2 thật cần Internet khi cache trống và đủ RAM/dung lượng. Môi trường/phiên bản có thể ảnh hưởng hành vi tính toán. Không gửi quyền truy cập tài khoản hoặc khóa bí mật vào docs. Không dùng kết quả từ full khi chỉ có quick.

## 6. Nội dung cần xác nhận thêm từ chính nhóm

- Điền tên người làm thực tế, ngày họ làm, link commit/PR và người review trong `plans/team_workflow_and_log.md`.
- Nếu cô cung cấp đề gốc, đính kèm trích dẫn/slide được phép chia sẻ và đối chiếu với E1/E2; không nhận bản diễn giải trong docs là nguyên văn đề.
- Nếu có checkpoint/CSV trên Drive, bổ sung link và chính sách truy cập; không giả định dữ liệu đó đã tồn tại công khai.
- Nếu từng bước chỉ mới có code chứ chưa demo lại được trên máy hiện tại, trình bày là "đã implement, đang chờ tái kiểm chứng".

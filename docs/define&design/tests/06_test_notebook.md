# TEST SPEC NOTEBOOK — Kiểm tra tính toàn vẹn notebook nguồn

> **ID:** LAB3-TNOTEBOOK · **Phiên bản:** 1.0 · **Ngày tạo:** 11/11/2026  
> **Test hiện có:** `../../../tests/test_notebook.py::test_notebook_schema_and_python_cells`  
> **Phase:** `../../plans/phase6.md`, `../../plans/phase7.md`.

## 1. Mục tiêu

Kiểm chứng notebook được lưu đúng định dạng Jupyter và mọi code cell chứa Python có thể được parser đọc. Đây là **static test**: không chạy model, không gọi Trainer, không xác nhận model/data tải thành công hoặc accuracy. Đặc tả mới này bổ sung tài liệu cho một test Python **đã tồn tại**, không phải thêm test mới vào suite.

## 2. NOTEBOOK-01 — Kiểm schema và Python syntax

| Thuộc tính | Mô tả |
|---|---|
| Input | File `notebooks/huggingface_sentiment.ipynb` theo đường dẫn relative từ test root |
| Tiền điều kiện | File notebook có mặt, định dạng JSON .ipynb hợp lệ; đã cài `nbformat` |
| Bước 1 | `nbformat.read(path, as_version=4)` |
| Bước 2 | `nbformat.validate(nb)` với notebook vừa đọc |
| Bước 3 | Lặp qua `nb.cells`; nếu `cell_type=='code'`, `ast.parse(c.source)` |
| Expected | Không có schema error hoặc `SyntaxError` ở bất cứ code cell Python nào |
| Failure mode | Notebook hỏng JSON/schema; cell Python không parse được |
| Trạng thái | ĐÃ CÓ TRONG CODE — 1 pytest case |

## 3. Những gì test không bảo đảm

- Không thực thi cell theo thứ tự; import có thể fail vì thiếu dependencies/môi trường.
- Không truy cập Hugging Face Hub hoặc tải pretrained weights/dataset.
- Không chứng minh checkpoint/Trainer chạy đúng, không kiểm output của các cell.
- Không kiểm notebook đã chạy (`huggingface_sentiment_executed.ipynb`) có còn khớp với source hay không.
- Không đo accuracy, F1, ROC-AUC; các chỉ số này chỉ đến từ evaluation artifacts.

## 4. Cách chạy và chẩn đoán lỗi

```bash
python -m pytest tests/test_notebook.py -v
```

Nếu `nbformat` báo schema error, xem metadata/cell type/id. Nếu `ast.parse` báo syntax error, xem code cell tương ứng. Nếu notebook chứa Jupyter magics (`%...`, `!...`) trực tiếp trong Python cell, AST có thể báo lỗi dù kernel chạy được; phiên bản notebook hiện tại được thiết kế để các code cell parse được, còn lệnh magic được hướng dẫn qua comment/text.

## 5. Các test đề xuất thêm — CHƯA TRIỂN KHAI

- NOTEBOOK-P01: Kiểm sự hiện diện của các đề mục Exercise 1 và Exercise 2 theo yêu cầu.
- NOTEBOOK-P02: Test notebook chạy end-to-end với môi trường và cache được kiểm soát khi có model/dataset.
- NOTEBOOK-P03: Đảm bảo báo cáo, metrics, hình ảnh được tạo đúng đường dẫn sau một run thực tế.
- NOTEBOOK-P04: Đối chiếu notebook nguồn/đã chạy, flag nếu code source bị đổi mà output cũ chưa cập nhật.

## 6. Tiêu chí nghiệm thu

PASS cho NOTEBOOK-01 khi không xuất hiện exception. Đối với nghiệm thu toàn Lab 3, phải bổ sung bằng chứng notebook đã chạy thực tế trong `reports/VALIDATION.md` và các artifacts `outputs/` nếu muốn khẳng định workflow pretrained hoạt động.

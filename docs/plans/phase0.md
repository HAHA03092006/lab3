# P0 — Phân tích đề, kiến trúc dự án và môi trường

> **Mã:** P0 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Tạo nền tảng rõ ràng để các phase còn lại có cấu hình, dependencies và tiêu chí hoàn thành nhất quán.

**File liên quan:** `requirements.txt`, `going_modular/config.py`, `notebooks/huggingface_sentiment.ipynb` (§0), `docs/define&design/00_lab3_description.md`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

Đề Chương 4 yêu cầu 4 bước Exercise 1 và 7 bước Exercise 2. Repo phân tách notebook làm entry point, modules chứa xử lý, tests làm bằng chứng kỹ thuật, outputs/reports ghi kết quả. Python 3.10–3.12 theo dependencies. Dùng `RunConfig` không lặp hyperparameters rải rác.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Đối chiếu 4 mục Exercise 1: cài thư viện, tải pretrained sentiment checkpoint, tokenize, dự đoán bằng pipeline/model.
- [ ] Đối chiếu 7 mục Exercise 2: setup thư viện, dataset, model/tokenizer, preprocessing, training arguments, Trainer fine-tune, evaluation.
- [ ] Xác nhận `SENTIMENT_MODEL` và `BASE_MODEL` là hai model ID độc lập trong `going_modular/config.py`.
- [ ] Xác nhận nhãn 0 = NEGATIVE, 1 = POSITIVE và đây là bài toán hai lớp.
- [ ] Kiểm tra phụ thuộc Torch, Transformers, Datasets, Accelerate, sklearn, pytest và notebook theo requirements.
- [ ] Tạo venv, cài requirements và ghi nhận Python/package version thực tế (không điền số đo chưa chạy).
- [ ] Xác nhận `RunConfig.for_profile('quick')` và `'full'` trả config hợp lệ, seed mặc định 42.
- [ ] Xác nhận notebook tìm được root dự án khi chạy trên VS Code/Jupyter.
- [ ] Kiểm tra `.gitignore` không vô tình commit cache, checkpoint/weights hoặc venv.


## 4. Tài liệu/bằng chứng cần bàn giao

- Bảng yêu cầu FR01–FR12 và E1/E2 trong `00_lab3_description.md`/traceability.
- Danh sách package và cấu hình tham số trong `requirements.txt`, `config.py`.
- Bằng chứng kiểm thử config trong `tests/test_utils.py` và log chạy lệnh nếu thực thi.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Phân biệt rõ nhiệm vụ hai bài; không gọi inference SST-2 là fine-tuning IMDb.
- Có thể giải thích quick chỉ giảm số mẫu để kiểm tra flow, full dùng train 20k + val 5k + test 25k.
- Không khai báo môi trường thành công nếu chưa cài/chạy được trên máy thực tế.


## 6. Rủi ro và hướng khắc phục

| Khó khăn | Xử lý |
|---|---|
| Thiếu mạng tải pretrained | Chỉ kiểm tra code offline, ghi rõ giới hạn |
| Thiếu GPU | Dùng quick / CPU khi phù hợp; không kỳ vọng cùng tốc độ |
| Sai Python/packages | Tạo môi trường riêng và kiểm tra `pip list` |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

## 8. Work package, tiến trình giải thích và cách bàn giao (bổ sung v3.0)

**Mục tiêu có thể báo cáo:** Khóa phạm vi bài, môi trường và hệ thống mã yêu cầu.

### 8.1. Trình tự thực hiện ở mức tác vụ

1. Đối chiếu E1.1–E2.7 với slide gốc (nếu có) và ghi câu hỏi mơ hồ.
2. Tạo venv phù hợp, xác nhận Python/torch/transformers/datasets/accelerate API.
3. Chốt `RunConfig.for_profile` và nhãn 0/1, đặt quy ước branch và run_id.
4. Gắn FR01–FR15/NFR01–NFR08 vào spec; tạo docs index và ma trận.

### 8.2. Bằng chứng lấy từ code/ZIP, không phải báo cáo tiến độ của từng cá nhân

`requirements.txt`, `going_modular/config.py`, notebook §0, docs/README.md, ma trận FR.

**Điều kiện review/Definition of Done cụ thể:** Một người mới đọc README hiểu đâu là pretrained E1, đâu là fine-tuning E2; không trùng FR; môi trường có chỉ dẫn cài và test.

**Rủi ro còn lại:** Version API thay đổi; chưa có slide gốc; không có thông tin người được phân công.

### 8.3. Checklist nghiệm thu cần xác nhận bằng chứng

- [ ] Đối chiếu E1.1–E2.7 với slide gốc (nếu có) và ghi câu hỏi mơ hồ.
- [ ] Tạo venv phù hợp, xác nhận Python/torch/transformers/datasets/accelerate API.
- [ ] Chốt `RunConfig.for_profile` và nhãn 0/1, đặt quy ước branch và run_id.
- [ ] Gắn FR01–FR15/NFR01–NFR08 vào spec; tạo docs index và ma trận.
- [ ] Người kiểm tra mở đúng file code/test/output trong cột bằng chứng.
- [ ] Nếu không chạy lại được, đánh dấu "Chưa tái kiểm chứng" thay vì tự tick.
- [ ] Nếu chức năng đổi, cập nhật ma trận FR và link spec module liên quan.

### 8.4. Nhật ký công việc dùng cho nhóm điền

| Ngày giờ thực tế | Thành viên | Branch/commit/PR | Công việc có bằng chứng | Test hoặc demo đã làm | Phản hồi reviewer | Trạng thái |
|---|---|---|---|---|---|---|
| _Chưa điền_ | _—_ | _—_ | _—_ | _—_ | _—_ | _Not recorded_ |

**Cách báo cáo phase này:** trình bày mục tiêu → một quyết định kỹ thuật và lý do → file/hàm thực tế → test/metric/manifest → hạn chế hoặc việc chưa làm. Xem [quy trình nhóm](team_workflow_and_log.md) và [ma trận yêu cầu](../analysts/requirements_traceability.md).

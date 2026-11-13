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

# P1 — Chuẩn bị và kiểm soát dữ liệu IMDb

> **Mã:** P1 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Sinh ba split ổn định, truy vết được mẫu, không dùng test để ra quyết định học máy.

**File liên quan:** `going_modular/data_setup.py`, `going_modular/config.py`, `tests/test_data_setup.py`, `docs/define&design/01_data.md`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

IMDb `stanfordnlp/imdb` có train/test gốc (mỗi tập 25.000 review có nhãn). Từ train gốc chia ra validation bằng stratification trước khi lấy subset quick. Thêm sample_id trước khi chia. Clean tối thiểu không xóa phủ định, sau đó tokenize riêng ở phase P2.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Kiểm tra `load_imdb(cfg)` tải đúng dataset ID/revision và xử lý ngoại lệ tải dữ liệu.
- [ ] Kiểm tra schema nguồn gồm `text`, `label`, bỏ split unsupervised khỏi quy trình supervised.
- [ ] Thêm `sample_id` có tiền tố `train:` hoặc `test:` trước khi cắt subset.
- [ ] Kiểm tra `stratified_indices` đòi labels 0/1, đủ hai lớp, val_size hợp lệ.
- [ ] Kiểm tra train và validation rời nhau theo chỉ mục, giữ tái lập khi seed không đổi.
- [ ] Kiểm tra quick chọn subset phân tầng riêng sau split, không lấy `select(range(N))`.
- [ ] Kiểm tra `clean_text` xử lý `<br/>`, HTML entities, spaces nhưng giữ `not` và dấu câu.
- [ ] Xuất manifest gồm size, label counts, sample IDs, hash nội dung và exact-text overlap.
- [ ] Ghi nhận exact duplicates giữa split nếu có; không xóa dữ liệu train dựa trên test.
- [ ] Chạy kiểm thử dữ liệu tương ứng, phân biệt dữ liệu synthetic với IMDb thật.


## 4. Tài liệu/bằng chứng cần bàn giao

- Raw `DatasetDict` gồm train/validation/test, mỗi mẫu có `text`, `label`, `sample_id`.
- `split_manifest` gồm `content_sha256`, `duplicate_text_overlap` và nhãn theo split.
- Unit tests: `test_split_balanced_disjoint_reproducible`, `test_invalid_split`, `test_clean_keeps_negation`, `test_tokenization_and_identity`.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Quick được cấu hình 2.000 train, 500 validation, 1.000 test; full 20.000/5.000/25.000 (theo cấu hình khi chạy đúng nguồn).
- Không có trùng sample_id giữa train/val; test lấy từ split gốc, không đưa vào Trainer eval_dataset.
- Nội dung và hash nhận dạng dữ liệu được lưu trước khi train phục vụ truy vết.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Cách xử lý |
|---|---|
| Tập IMDb sắp theo nhãn | Chọn subset phân tầng, không cắt N dòng đầu |
| Trùng text nhưng không trùng ID | Log exact overlap; không chỉnh benchmark theo test |
| Clean quá mạnh đổi sắc thái | Giữ phủ định, thứ tự từ và punctuation |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

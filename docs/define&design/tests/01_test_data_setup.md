# TEST SPEC DATA — `going_modular/data_setup.py`

> **ID:** LAB3-TDATA · **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **Mã nguồn test:** `../../../tests/test_data_setup.py`; fixtures: `../../../tests/conftest.py`  
> **Phase:** `../../plans/phase1.md` · **Phạm vi:** offline synthetic, không tải IMDb từ mạng.

## 1. Mục tiêu và điều kiện chung

Xác minh chia train/validation phân tầng, disjoint và tái lập; làm sạch văn bản giữ ý nghĩa; tokenization tạo đúng dữ liệu cho model; manifest ổn định khi input không đổi. Nhãn chỉ 0/1, `sample_id` giữ khả năng truy vết. `tiny_bundle` tạo train synthetic gốc 24 mẫu và test 8 mẫu, val_size=8 nên raw train=16, val=8; tokenizer local dùng vocab nhỏ. Những con số này là data fixture, **không phải dữ liệu IMDb thực**.

## 2. Các test case đang có trong code

### DATA-01 — Phân tầng, rời nhau, tái lập (`test_split_balanced_disjoint_reproducible`)

- **Mục tiêu:** Chứng minh hàm `stratified_indices` tạo một phân hoạch đúng lớp, cùng seed cho cùng chỉ mục.
- **Tiền điều kiện:** `numpy`, `sklearn` hoạt động; gọi trực tiếp hàm, không cần Hugging Face Hub.
- **Input:** `labels=[0]*50+[1]*50`, `val_size=20`, `seed=42`; gọi thêm seed=43 để so sánh.
- **Bước chạy:** (1) Tạo train/val indices; (2) tính giao và hợp; (3) đếm Positive validation; (4) gọi lại seed=42; (5) so seed=43.
- **Kỳ vọng:** Giao train/val rỗng, hợp chỉ mục là 0..99, validation 20 mẫu gồm 10 Positive/10 Negative, hai lần seed 42 giống nhau, seed 43 đổi validation indices.
- **Lỗi phát hiện:** Trộn split, mất mẫu, không tái lập hoặc validation mất cân bằng.
- **Trạng thái:** ĐÃ CÓ TRONG CODE, một pytest case.

### DATA-02 đến DATA-06 — Input không hợp lệ (`test_invalid_split`, 5 tham số)

- **Mục tiêu:** Từ chối split vi phạm nhãn/size thay vì trả chỉ mục không đáng tin cậy.
- **Test matrix:**

| Test ID | labels | val_size | Expected |
|---|---|---:|---|
| DATA-02 | `[]` | 2 | `ValueError` |
| DATA-03 | `[0,0,0,0]` | 2 | `ValueError` vì thiếu nhãn 1 |
| DATA-04 | `[0,1,0,1]` | 1 | `ValueError` vì val quá nhỏ |
| DATA-05 | `[0,1,0,1]` | 4 | `ValueError` vì không còn train |
| DATA-06 | `[0,2,0,2]` | 2 | `ValueError` vì nhãn không phải 0/1 |

- **Bước chạy chung:** gọi `stratified_indices(labels, size)` trong `pytest.raises(ValueError)`.
- **Trạng thái:** ĐÃ CÓ TRONG CODE, pytest tạo 5 cases từ một hàm parametrize.

### DATA-07 — Làm sạch văn bản không mất phủ định (`test_clean_keeps_negation`)

- **Input:** `' Not<br /> bad &amp; good!  '`.
- **Bước chạy:** `clean_text(input)`; kiểm tra equality thay vì chỉ kiểm tra độ dài chuỗi.
- **Kỳ vọng:** `'Not bad & good!'`; giữ từ `Not`, dấu `!`, giải mã entity `&amp;`, thay `<br />` bằng khoảng trắng và trim.
- **Rủi ro phát hiện:** Loại stopword làm mất phủ định, bỏ dấu câu, HTML artifact còn sót.
- **Trạng thái:** ĐÃ CÓ TRONG CODE, một pytest case.

### DATA-08 — Tokenization, ranh giới split và manifest (`test_tokenization_and_identity`)

- **Input:** Fixture `tiny_bundle` gồm tokenizer local, `DatasetDict` train/validation/test và `cfg.max_length=32`.
- **Bước chạy:** Lấy raw/encoded/manifest từ fixture; kiểm tra kích thước split, ID disjoint, cột tokenized, length và tính lại manifest.
- **Kỳ vọng định lượng:** `len(raw['train']) == 16`, `len(raw['validation']) == 8`; `sample_id` train/val rời nhau; columns của tokenized train đúng `{'input_ids','attention_mask','labels'}`; mọi input_ids length `<=32`; manifest lần 1 bằng manifest lần tính lại.
- **Giải thích:** `tokenize_splits` xoá `text`/`sample_id` ở tokenized dataset nhưng raw dataset vẫn giữ để export dự đoán sai. Tên hàm test có chữ identity, **không có assert trực tiếp `tokenizer_identity()`** trong trường hợp này.
- **Trạng thái:** ĐÃ CÓ TRONG CODE, một pytest case.

## 3. Điều kiện pass và bằng chứng

Tổng **8 pytest cases** thuộc file này (1+5+1+1). Thực hiện `python -m pytest tests/test_data_setup.py -v`; mỗi assertion phải đúng, không có fail. Bản ZIP đầu vào lưu log chung trong `reports/pytest_output.txt`, nhưng log không thay thế cho kiểm chứng lại ở máy khác.

## 4. Các trường hợp đề xuất thêm (CHƯA TRIỂN KHAI)

- DATA-P01: Kiểm tra labels quá mất cân bằng khiến stratify không đủ số mẫu/lớp, ghi nhận exception cụ thể.
- DATA-P02: Kiểm tra `select_subset` với `limit=None`, `limit=len(dataset)` và limit ngoài miền.
- DATA-P03: Kiểm tra duplicate-text overlap trên dataset cố tình trùng text nhưng ID khác.
- DATA-P04: Kiểm tra `load_imdb` xử lý offline/cache, revision không tồn tại khi có harness phù hợp.

**Không cộng các ý trên vào số test passed.**

## 5. Quy trình test dữ liệu và expected cụ thể (bổ sung v3.0)

| Case | Setup/Input | Action | Expected/Oracle | Test source |
|---|---|---|---|---|
| DATA-01 | 50 nhãn 0, 50 nhãn 1; val_size=20, seed=42 | `stratified_indices` gọi hai lần | 20 val: 10 mỗi lớp; train/val disjoint; cùng seed cùng indices; seed 43 khác | `test_split_balanced_disjoint_reproducible` |
| DATA-02 | labels=[], size=2 | split | ValueError | `test_invalid_split` tham số #1 |
| DATA-03 | labels=[0,0,0,0], size=2 | split | ValueError vì thiếu lớp | `test_invalid_split` #2 |
| DATA-04 | labels=[0,1,0,1], size=1 | split | ValueError vì val_size quá nhỏ | `test_invalid_split` #3 |
| DATA-05 | labels=[0,1,0,1], size=4 | split | ValueError vì không chừa train | `test_invalid_split` #4 |
| DATA-06 | labels=[0,2,0,2], size=2 | split | ValueError vì labels không phải {0,1} | `test_invalid_split` #5 |
| DATA-07 | `' Not<br /> bad &amp; good!  '` | `clean_text` | `'Not bad & good!'` | `test_clean_keeps_negation` |
| DATA-08 | tiny raw train 24/test 8 | `prepare_raw_splits` & tokenize & manifest | train 16, val 8, disjoint; columns IDs/mask/labels; len<=32; manifest stable | `test_tokenization_and_identity` |

### Bản ghi cần lưu nếu test fail

- `pytest -q tests/test_data_setup.py -vv` cùng Python/datasets/scikit-learn versions.
- Nếu lệch class balance: kiểm nhãn gốc, seed, stratify; không sửa nhãn test để đạt.
- Nếu sai text clean: so HTML `<br>`, entities, khoảng trắng; bảo toàn từ phủ định.
- Nếu token shape sai: kiểm tokenizer version, max_length, dynamic padding tại collator.

### Kiểm thử đề xuất chưa hiện thực

- DATA-P01: trường `text` rỗng, None hoặc không phải string.
- DATA-P02: multiple duplicated texts với labels khác và exact hash overlap report.
- DATA-P03: data revision/row index đổi, manifest digest phải đổi.
- DATA-P04: random seed reproducibility theo nhiều splits/data sizes cân bằng và rất lệch.
- DATA-P05: load offline khi cache trống và thông báo lỗi rõ ràng.

Các test `DATA-Pxx` không thuộc 24 cases. **FR/NFR liên quan:** FR05/FR06, NFR01/NFR02. Bằng chứng real của data chỉ ở manifest run quick, không phải kết luận về full IMDb.

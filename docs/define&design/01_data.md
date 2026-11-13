# Đặc tả dữ liệu — data_setup.py

## 1. Trách nhiệm

Load IMDb; chia validation từ train; chọn subset phân tầng nếu quick; làm sạch tối thiểu;
tokenize và trả DatasetDict. Không huấn luyện, không chọn hyperparameter, không tính test accuracy.

## 2. Nguồn và schema

`load_dataset('stanfordnlp/imdb')`: train/test có `text` (str), `label` (ClassLabel 0/1).
Tập unsupervised không được sử dụng. Chèn `sample_id` theo split gốc và row index trước khi chia.
ID train: `train:<index>`; ID test: `test:<index>`. Giữ raw text để truy ngược dự đoán sai.

## 3. Luồng và bất biến

1. Validate nhãn có cả 0 và 1.
2. `train_test_split(... stratify=labels, random_state=seed)` tạo chỉ mục train/val.
3. Sort chỉ mục để sample ID ổn định; DataLoader của Trainer tự shuffle lúc train.
4. Quick lấy mẫu phân tầng riêng trong từng split đã chia, không lấy N dòng đầu.
5. Đổi `<br/>`/HTML entity, chuẩn hóa khoảng trắng. Không xóa phủ định, dấu câu, từ hiếm.
6. Tokenizer truncation theo max_length, `padding=False` lúc map.
7. Collator đệm từng batch; cột `label` đổi thành `labels` mà HF model nhận.

Bất biến: train/validation rời nhau theo ID; hợp trước subset phủ train gốc. Test không được trộn vào train.
Chỉ mục rời nhau không đảm bảo văn bản khác nhau: `duplicate_text_overlap` công khai exact duplicates
sau clean. Không xóa train dựa vào nội dung test; nếu cần đánh giá có group splitting, thiết kế một protocol khác từ đầu.

## 4. Đầu vào/đầu ra

| API | Đầu vào | Đầu ra | Lỗi |
|---|---|---|---|
| clean_text | str | str | Kiểu không hợp lệ gây lỗi Python |
| stratified_indices | labels, val_size, seed | Hai list[int] | ValueError nếu split/nhãn sai |
| select_subset | Dataset, limit/None, seed | Dataset | ValueError nếu size ngoài miền |
| prepare_raw_splits | raw DatasetDict, RunConfig | train/validation/test có ID | Lỗi schema hoặc split |
| tokenize_splits | raw, tokenizer, max_length | DatasetDict IDs/mask/labels | Lỗi tokenizer được truyền lên |
| split_manifest | raw splits | dict JSON-compatible | Lỗi schema |
| load_imdb | cfg, cache_dir | raw splits | Lỗi mạng/cache không bị che giấu |

## 5. Tensor và ý nghĩa

`input_ids`: token trong vocabulary, kiểu integer; không normalize IDs như pixel ảnh Lab 2.
`attention_mask`: 1 cho token thật, 0 cho padding. `labels`: integer 0/1 cho cross-entropy.
Kích thước L thay đổi giữa batch, không vượt max_length. `[CLS]/[SEP]` nằm trong giới hạn token.
Review dài bị cắt; đây là trade-off tài nguyên, cần ghi trong báo cáo.

## 6. Manifest và kiểm thử

Ghi số mẫu/lớp, toàn bộ sample_ids, content_sha256 trên (text,label), và duplicate counts.
Engine hash manifest vào contract; thay text/label với cùng ID vẫn bị phát hiện.
Tests: cân bằng lớp, ID disjoint, seed ổn định, seed khác đổi split, lỗi đầu vào,
giữ phủ định và dấu câu, token shape/mask/labels. Xem tests/test_data_setup.py.

## 7. Thiết kế tuần tự chi tiết từ IMDb đến tokenized batch (v3.0)

| Bước | Hàm | Đầu vào | Điều kiện kiểm tra | Đầu ra |
|---|---|---|---|---|
| D1 | `load_imdb(cfg)` | dataset ID/revision, cache_dir | có split train/test và nhãn 0/1 | DatasetDict đã preprocess |
| D2 | `prepare_raw_splits` | raw dataset | `sample_id=train:i`/`test:i` trước split | raw có ID nguồn |
| D3 | `stratified_indices` | label array, val_size, seed | cả hai lớp; val_size đủ chừa train/val | indices sorted disjoint |
| D4 | `select_subset` | mỗi split, limit, seed | không lấy N mẫu đầu; giới hạn hợp lệ | subset phân tầng |
| D5 | `clean_text` | raw HTML-ish review | `br` thành space, HTML unescape, whitespace collapse | text giữ phủ định/dấu câu |
| D6 | `split_manifest` | raw splits | đếm nhãn, ID, hash text/label, exact overlap | dict JSON-compatible |
| D7 | `tokenize_splits` | raw splits, tokenizer, max_length | truncation, padding=False, label→labels | DatasetDict tokenized |
| D8 | collator ở engine | list record tokenized | tokenizer/mask đồng nhất | tensor batch padded |

**Tại sao sort indices?** Sau chia phân tầng, giữ thứ tự chỉ mục tăng dần giúp so chiếu với ID nguồn, trong khi Trainer shuffle train batch riêng. Sort không đảo ngược tính ngẫu nhiên của tập được chọn. **Tại sao giữ original test?** Nếu re-split từ toàn bộ IMDb hoặc chọn LR dựa trên test, không còn đánh giá độc lập.

## 8. Ví dụ biên và validation input

| Đầu vào | Kỳ vọng | Bằng chứng |
|---|---|---|
| `labels=[0]*50+[1]*50`, `val_size=20`, seed 42 | validation gồm 10 mỗi lớp; rời train; cùng seed cùng split | DATA-01 |
| `labels=[]` hoặc chỉ toàn 0 | `ValueError` | DATA-02/03 |
| val_size=1 hoặc dùng gần hết train | `ValueError` | DATA-04/05 |
| nhãn có 2 thay vì chỉ 0/1 | `ValueError` | DATA-06 |
| `Not<br /> bad &amp; good!` | `Not bad & good!` | DATA-07 |
| tiny data train/test | tokenized đúng 3 cột, <= max_length, manifest ổn định | DATA-08 |

**Chưa được test riêng:** đầu vào `text=None`/non-str, dataset có schema lạ, lỗi mạng, numeric labels không phải int, cực nhiều review duplicates, độ dài có thể vượt memory. Không nói các test đó đã được pass; kế hoạch bổ sung trong test spec `01_test_data_setup.md`.

## 9. Bảo vệ dữ liệu và bằng chứng thực nghiệm

Run reference trong ZIP ghi train=2.000, validation=500, test=1.000; mỗi split có nhãn cân bằng và exact overlap = 0 theo manifest. Điều này **không** có nghĩa tất cả dữ liệu IMDb gốc không có duplication. Hash `content_sha256` được tạo từ nội dung+label đã clean; nếu người dùng chạy với version dữ liệu khác, hash có thể đổi và `check_action` từ chối reuse.

`split_manifest.json` có cả danh sách sample IDs nên có thể lớn; không gửi nguyên danh sách vào slide. Khi báo cáo chỉ trích tóm tắt size, nhãn, hash và một ví dụ sample ID; nếu kiểm tra cần xem file gốc.

## 10. Cách giải thích bằng lời khi bảo vệ

“Bọn em không chọn 2.000 review đầu tiên, vì thứ tự dataset có thể khiến lệch nhãn. Em dùng stratified split từ train để tạo validation, rồi lấy quick subset phân tầng trong từng split; test gốc vẫn độc lập. Em giữ sample_id trước khi split, tokenize chỉ sau clean, không bỏ từ phủ định. Manifest cho phép kiểm tra số lượng, tỷ lệ lớp, exact overlap và nội dung dữ liệu dùng trong run.”

Liên quan: FR05/FR06/NFR01/NFR02 trong [ma trận](../analysts/requirements_traceability.md); [DATA test specs](tests/01_test_data_setup.md), [cơ sở lý thuyết](../theory/00_theoretical_foundations.md).

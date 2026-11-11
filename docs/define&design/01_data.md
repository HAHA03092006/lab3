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

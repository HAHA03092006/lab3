# Đặc tả tiện ích và lưu trữ — utils.py

## 1. Trách nhiệm

Seed, JSON an toàn, dấu vết môi trường, hash contract và thư mục output.
Không tải model hay tính độ đo. seed_everything dùng transformers.set_seed cho Python/NumPy/PyTorch.
Tái lập split được đảm bảo bằng random_state; tái lập số học GPU phụ thuộc môi trường.

## 2. Lưu nguyên tử

save_json(path, value) ghi vào file .tmp cạnh đích rồi replace. allow_nan=False từ chối NaN/Inf;
finally xóa file tạm nếu có lỗi, file cũ còn nguyên. Không ghi placeholder metrics trước khi evaluate.
read_json đọc UTF-8; lỗi parse/missing file được báo lên caller thay vì trả dict rỗng.

## 3. Danh tính thí nghiệm

`digest(value)` SHA-256 của JSON sort_keys, Unicode giữ nguyên.
Contract gồm RunConfig.to_dict, digest manifest và tokenizer_identity. Không chứa action/runtime paths.
check_action kiểm tra contract nguyên dict khi resume/reuse. Bảo vệ thư mục train ngay khi có bất kỳ file nào.
Không có FORCE_RETRAIN xóa tự động; đổi run_id giúp giữ kết quả đối chiếu.

## 4. Đường dẫn và metadata

new_output_dir(root,run_id): ngày giờ Asia/Ho_Chi_Minh, đến microsecond, tạo thư mục mới.
`outputs/YYYY-MM-DD/run_id/HHMMSS-microseconds` tách các lần đánh giá, không dùng cache metrics cũ.
Model/checkpoint lưu trong artifacts; logs trong logs; cache Hub/dataset không commit.
Time zone dùng tzdata trên Windows. environment_info ghi Python, torch, transformers, datasets,
evaluate, accelerate, NumPy, sklearn, có CUDA và tên thiết bị.

## 5. Kiểm thử

JSON round-trip; lỗi NaN không hỏng file gốc; config mismatch bị từ chối;
train không đè thư mục nonempty. Thử nghiệm marker completed được kiểm trong test_engine.
Thư viện báo lỗi mạng/GPU không bị utils che thành thành công.

## 6. Danh sách hàm, side effects và hợp đồng lỗi (v3.0)

| Hàm | Input | Output / side effect | Điều kiện/ngoại lệ |
|---|---|---|---|
| `save_json(path, value)` | path, object JSON serializable | ghi temp `.json.tmp` rồi replace đích | `allow_nan=False`; nếu lỗi giữ nguyên file cũ |
| `read_json(path)` | file JSON | object Python | FileNotFound/JSONDecodeError từ stdlib |
| `digest(value)` | object JSON-compatible | SHA256 của JSON `sort_keys=True` | Không dùng như hash bí mật password |
| `seed_everything(seed)` | int | gọi HF `set_seed` | không bảo đảm bitwise GPU |
| `environment_info()` | không | versions/runtime device | thiếu package ghi `not installed` |
| `new_output_dir(root,run_id)` | root/ID | tạo output path theo timezone Asia/Ho_Chi_Minh | `exist_ok=False` chống trùng tên |
| `check_action(run_dir,action,contract)` | action train/resume/reuse | return hoặc raise | bảo vệ run folder/config/artifact |

## 7. Vì sao dùng digest và contract?

Hash SHA-256 trên manifest giúp phát hiện khi nội dung, nhãn hoặc sample IDs của dữ liệu thay đổi. Contract gồm `run_config` + `digest(manifest)` + `tokenizer_identity`. Do đó model cùng ID nhưng thay tokenizer vocabulary/seed/split vẫn phải tạo run mới. SHA không phải chữ ký bảo mật có key: người có quyền sửa cả JSON/weights vẫn có thể thay nội dung; mục tiêu là **phát hiện thay đổi vô tình**, không chống đối tượng tấn công chủ động.

## 8. JSON atomic, không ghi đè, timezone

Ghi file đích qua `.tmp` giúp giữ file cũ nếu serialize lỗi, như UTIL-01 cho NaN. `Path.replace` là thao tác atomic ở mức rename thông thường trên cùng filesystem, nhưng không bảo đảm an toàn khi mất điện đột ngột hoặc trên mọi remote FS. `new_output_dir` dùng ngày/giờ HCM cho tên output để đọc lịch sử tiện hơn, nhưng tuyệt đối không dùng timestamp này làm chứng cứ metadata kiểu “người X đã chạy”. Trạng thái thời điểm thực phải lấy từ logs đã tồn tại.

## 9. Gợi ý test bổ sung chưa triển khai

- UTIL-P01: hỏng JSON đầu vào → thông báo lỗi cụ thể, không tự bỏ qua.
- UTIL-P02: digest thay đổi khi đổi label/text nhưng giữ ID.
- UTIL-P03: thiếu `best_model/model.safetensors` → `reuse` báo rõ file thiếu.
- UTIL-P04: chạy song song cùng run ID → khóa file/atomic creation và hướng xử lý tranh chấp.
- UTIL-P05: lỗi quyền ghi/hết disk → không nhận nhầm completed.

Các test đề xuất không cộng vào **24 passed** của bản ZIP. Tham chiếu [utils test](tests/04_test_utils.md) và [FR11/NFR03](../analysts/requirements_traceability.md).

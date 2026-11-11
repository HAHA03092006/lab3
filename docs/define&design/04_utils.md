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

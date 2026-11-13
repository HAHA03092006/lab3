# TEST SPEC UTILS & CONFIG — `utils.py`, `config.py`

> **ID:** LAB3-TUTILS · **Phiên bản:** 2.0 · **Ngày cập nhật:** 11/11/2026  
> **File:** `../../../tests/test_utils.py` · **Phase:** `../../plans/phase0.md`, `../../plans/phase4.md`.

## 1. Mục tiêu

Kiểm tra tính an toàn khi lưu JSON (không phá file cũ nếu dữ liệu không hợp lệ), guard không ghi đè run hiện hữu, contract mismatch từ chối reuse/resume sai cấu hình và `RunConfig` kiểm các giá trị nguy hiểm. Không có network/model weights trong test nhóm này.

## 2. Tiền điều kiện, fixture và cấu hình

`tmp_path` là thư mục tạm do pytest tạo. `save_json` ghi vào `filename.json.tmp` rồi `replace` file đích, dùng `allow_nan=False`. `check_action` dựa trên thư mục run và JSON chứa contract; với `action='resume'`, nếu config hợp đồng khớp thì guard qua nhưng chưa xác nhận checkpoint thực tồn tại (việc đó là trách nhiệm `run_experiment`).

## 3. Case hiện có

### UTIL-01 — JSON atomic và bảo vệ file cũ (`test_atomic_json_preserves_original`)

- **Input:** `tmp_path/value.json`, dữ liệu hợp lệ `{'ok': 1}`, sau đó dữ liệu lỗi `{'bad': float('nan')}`.
- **Steps:** gọi `save_json` lần đầu, lần hai trong `pytest.raises(ValueError)`; đọc lại bằng `read_json`; kiểm tra file tạm.
- **Expected:** lần ghi thứ hai `ValueError`, file đích vẫn là `{'ok':1}`, `.json.tmp` không còn.
- **Rủi ro:** JSON lỗi làm mất report cũ, file tạm tồn tại hoặc NaN lọt vào artifact.
- **Trạng thái:** ĐÃ CÓ — 1 pytest case.

### UTIL-02 — Guard thư mục không rỗng và contract mismatch (`test_guard_nonempty_and_config_mismatch`)

- **Input:** Tạo `run/config.json` chứa `{'contract': {'seed':42}}`; gọi `check_action(run, ...)`.
- **Steps:** (1) `action='train', contract={}`; (2) `action='resume', contract={'seed':43}`; (3) `action='resume', contract={'seed':42}`.
- **Expected:** (1) `FileExistsError`; (2) `ValueError`; (3) pass guard không raise (không có checkpoint check trong `check_action`).
- **Rủi ro:** ghi đè thí nghiệm trước hoặc lén tiếp tục với seed khác.
- **Trạng thái:** ĐÃ CÓ — 1 pytest case.

### UTIL-03 đến UTIL-06 — Validation của RunConfig (`test_config_validation`, 4 tham số)

| ID | Keyword argument tạo `RunConfig(**kw)` | Kỳ vọng | Ý nghĩa |
|---|---|---|---|
| UTIL-03 | `{'run_id':'../x'}` | `ValueError` | Ngăn path traversal qua run_id |
| UTIL-04 | `{'epochs':0}` | `ValueError` | Epoch phải dương |
| UTIL-05 | `{'max_length':513}` | `ValueError` | Chiều dài vượt miền [8,512] |
| UTIL-06 | `{'warmup_ratio':1}` | `ValueError` | Warmup phải < 1 |

- **Steps chung:** khởi tạo config trong `pytest.raises(ValueError)`.
- **Trạng thái:** ĐÃ CÓ — 4 pytest cases từ parametrize.

## 4. Tổng hợp và lệnh chạy

File có **6 pytest cases** (1+1+4), nhưng các hàm util khác như `new_output_dir`, `environment_info`, `digest` và `seed_everything` không có unit test trực tiếp trong file này. Chạy `python -m pytest tests/test_utils.py -v`; PASS khi tất cả exception và file assertions phù hợp.

## 5. Test đề xuất thêm — CHƯA TRIỂN KHAI

- UTIL-P01: `check_action` từ chối action ngoài 3 giá trị cho phép.
- UTIL-P02: `reuse` thiếu `completed.json` hoặc safetensors tokenizer: `FileNotFoundError` liệt kê tệp thiếu.
- UTIL-P03: `digest` không phụ thuộc thứ tự key JSON nhưng phụ thuộc nội dung.
- UTIL-P04: `new_output_dir` tạo đường dẫn timezone Asia/Ho_Chi_Minh và không ghi đè.
- UTIL-P05: `environment_info` trả metadata gắn với runtime, không bịa package chưa cài.

Các hạng mục đề xuất không được tính vào log 24 passed gốc.

## 6. Test steps – expected – failure modes của utils (v3.0)

| Case | Input/Action | Expected | Ghi chú |
|---|---|---|---|
| UTIL-01 | save `{'ok':1}` rồi thử ghi NaN `{'bad':nan}` lên cùng file | lần hai raise ValueError; file cũ vẫn `{'ok':1}`; không tồn tại `value.json.tmp` | test atomic serialization, không phải transaction cả filesystem |
| UTIL-02 | run dir có config contract `{'seed':42}`; thử train; resume seed 43; resume seed 42 | train → FileExistsError; mismatch → ValueError; match → không raise | test guard/contract, chưa test tất cả lifecycle |
| UTIL-03 | `RunConfig(run_id='../x')` | ValueError | path traversal guard |
| UTIL-04 | `RunConfig(epochs=0)` | ValueError | epochs dương |
| UTIL-05 | `RunConfig(max_length=513)` | ValueError | giới hạn DistilBERT 512 |
| UTIL-06 | `RunConfig(warmup_ratio=1)` | ValueError | ratio `<1` |

**Bằng chứng:** `tests/test_utils.py`; tổng 6 parametrized pytest cases như ma trận. **Tiền điều kiện:** filesystem `tmp_path` ghi được; Python dependencies import được. **Nếu fail:** giữ traceback, file temp/target nếu an toàn, snapshot config; không xóa run thực để sửa test.

### Những gì chưa test

- `read_json` malformed, `new_output_dir` timezone/collision, `environment_info` thiếu package.
- Contract hash thay đổi do content nhưng ID vẫn giữ, đồng bộ concurrent actions, quyền ghi hệ thống.
- Trường hợp `reuse` thiếu model.safetensors (code có guard nhưng chưa có unit case độc lập cho từng required file).

Đề xuất UTIL-P01..P05 ở [utils spec](../04_utils.md), **chưa thực hiện**. Liên quan FR11/NFR02/NFR03.

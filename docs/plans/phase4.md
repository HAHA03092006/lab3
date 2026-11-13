# P4 — Quản lý artifact, checkpoint, resume và reuse

> **Mã:** P4 · **Phiên bản kế hoạch:** 1.0 · **Ngày cập nhật:** 11/11/2026  
> **Người phụ trách:** Chưa phân công · **Ngày thực hiện:** Điền khi bắt đầu  
> **Trạng thái ban đầu của checklist:** Chưa xác nhận; việc dự án đã có code không đồng nghĩa đã kiểm chứng trên máy hiện tại.

## 1. Mục tiêu và phạm vi

Làm rõ ba hành động vòng đời thí nghiệm, dữ liệu bất biến và khả năng phục hồi an toàn.

**File liên quan:** `going_modular/engine.py`, `going_modular/utils.py`, `tests/test_engine.py`, `tests/test_utils.py`, `docs/define&design/03_engine.md`.

## 2. Bối cảnh kỹ thuật / điều kiện đầu vào

Artifact contract chứa `RunConfig.to_dict()`, hash manifest và danh tính tokenizer. `train` không ghi đè; `resume` chỉ dành cho run chưa completed, có checkpoint; `reuse` chỉ khi đủ `best_model` và markers. `action` không nằm trong contract.

**Điều kiện trước phase:** Đã có dữ liệu hoặc các thành phần từ phase phụ thuộc theo `implementation_plan.md`; nếu thiếu mạng, GPU hoặc weights, ghi `BLOCKED` thay vì giả định pass.

## 3. Công việc thực hiện và checklist

- [ ] Kiểm tra `check_action` từ chối action ngoài train/resume/reuse.
- [ ] Kiểm tra `train` từ chối run directory đã chứa file, yêu cầu đổi run_id.
- [ ] Kiểm tra `config.json` lưu contract trước khi bắt đầu train, có environment và số tham số.
- [ ] Kiểm tra `split_manifest.json` lưu trước train và cùng hash với contract.
- [ ] Dừng sau epoch đầu bằng callback (test synthetic), bảo đảm checkpoint có optimizer/scheduler và chưa completed.
- [ ] Thử `resume` với contract đúng, kiểm tra global_step/epoch không reset.
- [ ] Thử contract mismatch, resume completed, thiếu checkpoint: ứng xử lỗi phải rõ ràng.
- [ ] Sau hoàn tất, kiểm tra `best_model/` chứa config/model/tokenizer, `history.json`, `completed.json`.
- [ ] Thử `reuse`: không train lại, tái nạp model local, dự đoán tương đương trong dung sai.
- [ ] Ghi chú trường hợp hiếm checkpoint đủ epoch nhưng export bị ngắt, không tự gọi completed.


## 4. Tài liệu/bằng chứng cần bàn giao

- Artifacts cấu trúc: `artifacts/<run_id>/config.json`, `split_manifest.json`, `checkpoints/`, `history.json`, `best_model/`, `completed.json`.
- Các đường đi là mô tả runtime; ZIP hiện tại chỉ lưu một phần bằng chứng trong `reports/reference_run/`, không kèm weights/checkpoint tối ưu.
- Test hiện có: `test_real_trainer_resume_reuse_roundtrip`, `test_guard_nonempty_and_config_mismatch`, `test_atomic_json_preserves_original`.


## 5. Tiêu chí nghiệm thu (Definition of Done)

- Resume phải kiểm tra hợp đồng và checkpoint; reuse chỉ khi đủ tệp.
- Probability trước/sau reuse khớp atol=1e-7 trong integration test local.
- Không tự nhận `reuse` chạy được từ ZIP hiện tại nếu thiếu weights `best_model/model.safetensors`.


## 6. Rủi ro và hướng khắc phục

| Rủi ro | Xử lý |
|---|---|
| Resume sai config | Chặn bằng hash/contract, tạo run_id mới |
| Ngắt lúc save model | Không sửa marker thủ công trên run gốc, đọc hướng dẫn phục hồi |
| Thiếu weights do ZIP loại bỏ | Ghi rõ thiếu và không tuyên bố package inference-ready |


## 7. Nhật ký triển khai (điền sau khi làm)

| Ngày/giờ | Người làm | Việc đã làm / lệnh chạy | Bằng chứng (file, log, PR) | Trạng thái |
|---|---|---|---|---|
| — | — | Chưa cập nhật | — | TODO |

**Báo cáo khi chuyển phase:** Nêu 1) việc đã có bằng chứng, 2) việc còn thiếu, 3) lỗi/rào cản, 4) commit/PR và 5) người xác nhận. Không sửa kết quả trong `reports/` nếu không chạy lại thật.

## 8. Work package, tiến trình giải thích và cách bàn giao (bổ sung v3.0)

**Mục tiêu có thể báo cáo:** Bảo vệ artifacts, quản lý train/resume/reuse.

### 8.1. Trình tự thực hiện ở mức tác vụ

1. Thiết kế run contract gồm config, manifest SHA, tokenizer fingerprint.
2. Ghi metadata môi trường và resolved model revision khi train.
3. Test guard khi run dir có nội dung, contract mismatch hoặc thiếu checkpoint.
4. Dừng chủ động tiny integration, resume đến completed, reuse so xác suất.

### 8.2. Bằng chứng lấy từ code/ZIP, không phải báo cáo tiến độ của từng cá nhân

`utils.py`, `engine.py`, UTIL-01/02, ENGINE-01, reference config/history/completed.

**Điều kiện review/Definition of Done cụ thể:** Không train đè; resume chỉ với optimizer checkpoint hợp lệ; reuse đúng model/data; ghi rõ ZIP hiện thiếu weights.

**Rủi ro còn lại:** Artifact hỏng/dở, missing best_model, multiple processes cùng run ID, mutable model revision.

### 8.3. Checklist nghiệm thu cần xác nhận bằng chứng

- [ ] Thiết kế run contract gồm config, manifest SHA, tokenizer fingerprint.
- [ ] Ghi metadata môi trường và resolved model revision khi train.
- [ ] Test guard khi run dir có nội dung, contract mismatch hoặc thiếu checkpoint.
- [ ] Dừng chủ động tiny integration, resume đến completed, reuse so xác suất.
- [ ] Người kiểm tra mở đúng file code/test/output trong cột bằng chứng.
- [ ] Nếu không chạy lại được, đánh dấu "Chưa tái kiểm chứng" thay vì tự tick.
- [ ] Nếu chức năng đổi, cập nhật ma trận FR và link spec module liên quan.

### 8.4. Nhật ký công việc dùng cho nhóm điền

| Ngày giờ thực tế | Thành viên | Branch/commit/PR | Công việc có bằng chứng | Test hoặc demo đã làm | Phản hồi reviewer | Trạng thái |
|---|---|---|---|---|---|---|
| _Chưa điền_ | _—_ | _—_ | _—_ | _—_ | _—_ | _Not recorded_ |

**Cách báo cáo phase này:** trình bày mục tiêu → một quyết định kỹ thuật và lý do → file/hàm thực tế → test/metric/manifest → hạn chế hoặc việc chưa làm. Xem [quy trình nhóm](team_workflow_and_log.md) và [ma trận yêu cầu](../analysts/requirements_traceability.md).

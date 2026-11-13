# KIỂM TOÁN BẰNG CHỨNG — CODE / PYTEST / NOTEBOOK / REAL EXPERIMENT

> **LAB3-AUDIT v3.0, 13/11/2026.** Audit nội dung ZIP được cung cấp trong phiên chỉnh sửa. **Không chạy lại training**, không xác nhận người thực hiện, không khẳng định evidence ngoài ZIP tồn tại.

## 1. Quy tắc phân loại bằng chứng

| Mức | Ý nghĩa | Có thể kết luận | Không thể kết luận |
|---|---|---|---|
| A — Thiết kế | docs/plan mô tả bước làm | Nhóm đã xây dựng đặc tả | Code hoặc train đã chạy |
| B — Source code | Có hàm/cấu hình/test | Chức năng đã được implement ở code | Không có bug/runtime failure |
| C — Tests offline | Pytest logs, tiny fixture | Một số invariant/API/lifecycle hoạt động tại môi trường ghi log | Accuracy IMDb, GPU/full correctness |
| D — Notebook execution | Notebook đã lưu outputs | Các cells đã chạy ở môi trường lịch sử theo logs | Chạy được ở mọi máy/phiên bản |
| E — Real experiment | JSON metrics, run config/history | Có kết quả IMDb quick trong ZIP | Full/đa seed/future reproducibility |
| F — Reuse artifact | `best_model` và optimizer nếu cần | Có thể load/reproduce từ chính artifact | **Không có** trong ZIP hiện tại |

## 2. Kiểm kê những file minh chứng hiện có

| Nguồn | Có gì thực tế | Đọc để xác minh |
|---|---|---|
| `requirements.txt` | Bộ dependency pin/giới hạn version | API `Trainer`, `datasets`, Torch |
| `going_modular/` | 7 modules core | hàm `load_imdb`, `build_model`, `run_experiment`, `export_evaluation` |
| `tests/` | 6 Python test files + fixture | 24 pytest parametrized cases |
| `reports/pytest_output.txt` | **24 passed, 1 warning** của lần chạy cũ | không tự coi là log test ngày chỉnh docs |
| `notebooks/huggingface_sentiment_executed.ipynb` | Notebook có outputs | E1 pretrained, E2 quick theo báo cáo |
| `reports/notebook_execution.log` | Log diễn biến notebook | đối chiếu với executed notebook |
| `reports/reference_run/config.json` | Config, versions, param summary, model resolved SHA | run quick environment |
| `reports/reference_run/split_manifest.json` | Sample IDs/hashes/duplicate_text_overlap | split integrity |
| `reports/reference_run/history.json` | Log train/validation | theo dõi loss/F1 theo epochs |
| `reports/reference_run/completed.json` | Train hoàn tất, step/epoch/best checkpoint | hoàn tất run lịch sử |
| `outputs/2026-11-11/distilbert_imdb_quick/183159-290735/test_metrics.json` | Test metrics và confusion matrix | kết quả test quick |
| `outputs/.../confusion_matrix.png` | Hình confusion matrix | minh họa lỗi loại FP/FN |
| `outputs/.../history.png` | Biểu đồ loss/validation | chất lượng quá trình training |
| `outputs/.../REPORT.md` | Báo cáo được tạo tự động | so với metrics JSON |
| `outputs/.../new_review_predictions.json` | Dự đoán câu mới | sanity demonstration, không có ground truth |
| `outputs/.../exercise1_pretrained/.../predictions.json` | E1 sentiment sample outputs | không có accuracy dataset từ câu mẫu |

## 3. Xác minh kết quả quick bằng tay

Confusion matrix JSON `[[435,65],[73,427]]`, tổng 1.000. Đoán đúng `(435+427)=862` mẫu, accuracy `862/1000=0.862`. FP=65, FN=73, tổng sai `65+73=138`. Positive precision `427/(427+65)=0.867886`, recall `427/(427+73)=0.854`, F1 `2PR/(P+R)=0.860887`. Giá trị test này **đã nằm trong ZIP**, không phải do tăng/giảm số khi chỉnh tài liệu. Validation best F1 từ run khoảng 0.862823; không nhầm với test F1.

## 4. Ghi chú về các thiếu vắng quan trọng

- **Không có** `best_model/` với `model.safetensors` trong ZIP → không thể chỉ giải nén và action `reuse` để infer lại weights từ quick.
- **Không có** optimizer checkpoints → không có đủ artifacts cho `resume` cùng run quick trên máy mới.
- **Không có** `predictions.csv`/`errors.csv` trong ZIP → không tự khẳng định đã audit từng sample hoặc kèm top-20 review raw trong bản ZIP này.
- **Không có** output full profile → không điền bảng kết quả full dự đoán.
- **Không có** log mới của buổi chỉnh docs này → 24 passed là **kết quả lịch sử**, phải chạy lại trong môi trường hiện tại nếu muốn xác nhận cập nhật.
- **Không có** tên thành viên, commit/PR timeline đầy đủ trong nguồn → không tự gán trách nhiệm hoặc ngày hoàn thành cho người nào.

## 5. Audit trạng thái theo yêu cầu quan trọng

| Requirement | Code | Test offline | Real evidence | Đánh giá thận trọng |
|---|---|---|---|---|
| FR02/FR04 (pretrained E1) | Có | Không có integration với Hub trong pytest | Predictions JSON E1 / executed notebook | Có output lịch sử E1 |
| FR05/FR06 (IMDb/preprocess) | Có | DATA cases | Manifest quick | Có chứng cứ dạng manifest |
| FR07/FR08 (Trainer) | Có | ENGINE-01 tiny | Quick history/completed | Có quick run lịch sử |
| FR09 (test metrics) | Có | EVAL cases | test_metrics.json | Có số liệu quick 1.000 |
| FR10 (save/load) | Có | ENGINE-01 tiny | VALIDATION mô tả allclose | Weights thật không nằm trong ZIP |
| FR11 (reuse/resume) | Có | ENGINE-01 | metadata quick, không đủ weights | Chức năng có test tiny, không thể reuse zip |
| FR12 (reporting) | Có | Chưa có test riêng | REPORT.md quick | Có report output lịch sử |
| NFR01 (data isolation) | Có | DATA cases | Manifest overlap 0 | Chưa loại được semantic duplicates |
| NFR07 (portability) | Có setup/readme | pytest môi trường cũ | CPU trong config | Chưa chứng minh GPU/VS Code mọi máy |

## 6. Biên bản tái kiểm chứng — mẫu cho nhóm điền

| Thời điểm chạy thật | Người chạy | Env/branch/commit | Lệnh/kịch bản | Kết quả | Link log/artifact | Người review |
|---|---|---|---|---|---|---|
| _Điền khi chạy_ | _—_ | _—_ | `python -m pytest -q` | _—_ | _—_ | _—_ |
| _Điền khi chạy_ | _—_ | _—_ | notebook quick từ đầu | _—_ | _—_ | _—_ |
| _Điền khi chạy_ | _—_ | _—_ | load best_model thực | _—_ | _—_ | _—_ |

**Lệnh tham khảo:**

```powershell
python -m pytest -q
python -m pytest --collect-only -q
```

Nếu có bằng chứng mới, thêm dòng theo ngày chạy thật và giữ kết quả gốc để so sánh; đừng sửa log để nó trông như đã chạy. Khi group bảo vệ, dùng tài liệu này để trả lời “bằng chứng gì cho khẳng định này?”.

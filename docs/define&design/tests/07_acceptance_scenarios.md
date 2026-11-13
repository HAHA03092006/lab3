# KỊCH BẢN NGHIỆM THU THỦ CÔNG — TỪ YÊU CẦU ĐẾN DEMO

> **LAB3-UAT-07 v3.0, 13/11/2026.** Đây là **kịch bản để nhóm chạy và điền biên bản**, không phải test automation đã có. Không cộng các kịch bản này vào 24 pytest cases.

## 1. Mục đích và nguyên tắc

UAT khác unit tests: giảng viên có thể hỏi một yêu cầu trong slide, sinh viên cần mở notebook/source/run output và chứng minh đầu-cuối; phải kiểm khả năng lặp lại, nhưng không cần train lại full khi chỉ báo cáo docs. Mỗi kịch bản ghi **setup → thao tác → expected → evidence → người xác nhận/trạng thái**.

## 2. Kịch bản nghiệm thu đề xuất

| UAT | Yêu cầu | Setup / thao tác demo | Expected evidence | Trạng thái theo ZIP |
|---|---|---|---|---|
| UAT-01 | E1.2–E1.4 | Mở notebook executed phần 1, xem manual + pipeline | Token IDs/mask/logits/predictions JSON | Có output lịch sử; chưa chạy lại |
| UAT-02 | E2.2/E2.4 | Mở `split_manifest.json`, xem sizes/label distribution/IDs/hashes | Quick train 2k, val 500, test 1k; exact overlap=0 | Có manifest trong ZIP |
| UAT-03 | E2.3 | Mở `02_model.md`, `model_builder.py`, `count_params` run config | ID2LABEL 0/1, 66,955,010 trainable ở run quick | Có config lịch sử |
| UAT-04 | E2.5–E2.6 | Mở `engine.make_training_args`, `history.json`, `completed.json` | 2 epochs, validation best model, 250 steps | Có metadata/history lịch sử |
| UAT-05 | FR11 | Chạy ENGINE-01 trên máy demo nếu dependencies đủ | stop → resume → reuse; guard ghi đè | Có test code/log cũ; cần tái chạy để xác nhận môi trường |
| UAT-06 | E2.7/FR09 | Mở `test_metrics.json` + confusion matrix | accuracy=.862, F1=.860887 trên N=1000 | Có output thực |
| UAT-07 | FR12 | So `REPORT.md` và `test_metrics.json` | Số mẫu/metrics nhất quán | Có report output |
| UAT-08 | FR10 | Nạp `best_model` trên máy demo | xác suất trước/sau gần nhau | Test tiny có; ZIP thiếu real weights |
| UAT-09 | NFR07 | Cài clean venv và `pytest -q` trên máy giảng viên | pass/ghi versions/trace nếu fail | Chưa làm trong lần chỉnh docs |
| UAT-10 | Giới hạn | Chỉ ra full chưa chạy, missing artifacts | Không thổi phồng evidence | Có audit tài liệu |

## 3. Biên bản nghiệm thu mẫu

| UAT ID | Người thực hiện | Ngày thật | Machine/env/commit | Thao tác | Expected | Actual | Pass/Fail/Not run | Evidence path | Reviewer |
|---|---|---|---|---|---|---|---|---|---|
| _Điền_ | _—_ | _—_ | _—_ | _—_ | _—_ | _—_ | _Not run_ | _—_ | _—_ |

## 4. Kịch bản hỏi xoáy

- “Điều gì xảy ra nếu train lại cùng run_id?” → `check_action` raise FileExistsError; không tự ghi đè.
- “Tại sao test không ở eval_dataset của Trainer?” → eval_dataset dùng validation để chọn best model; test chỉ chạy sau.
- “Có bằng chứng resume trên IMDb thật?” → code/ENGINE-01 test tiny; chưa có checkpoint thực trong ZIP để tái hiện.
- “Có thật đã chạy full?” → chưa, chỉ có config full và outputs quick.
- “Có chắc predictions/labels cùng sample?” → label alignment được kiểm; vẫn còn lỗ hổng đổi chỗ sample cùng lớp; đề xuất gắn ID.

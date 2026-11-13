# QUY TRÌNH LÀM VIỆC NHÓM, PHÂN CÔNG VÀ NHẬT KÝ MINH CHỨNG

> **LAB3-WORKLOG v3.0, 13/11/2026.** **Mẫu quản lý được tạo để nhóm hoàn thiện bằng dữ liệu thật**, không phải lịch sử đã thực hiện của các thành viên. Có thể sử dụng ngay trong báo cáo nhưng nên bổ sung tên/commit/ngày từ GitHub trước khi nói "nhóm đã làm".

## 1. Tại sao cần một quy trình riêng?

Docs được cô đánh giá không chỉ theo “viết dài” mà theo **khả năng truy vết quy trình**: đề xuất → thiết kế → code → test → review → bằng chứng → tổng kết. Có nhiều file Markdown mà không có người làm, ngày review và link commit thực sẽ khó trả lời câu “nhóm phối hợp như thế nào?”. File này đưa ra cấu trúc để lấp đúng khoảng trống đó mà không bịa lịch sử.

## 2. Vai trò có thể phân công (RACI minh họa, chưa gán người)

| Hoạt động | Requirements owner | Data/Model owner | Integration owner | Tester/reviewer | Người tổng hợp docs |
|---|---|---|---|---|---|
| Đọc slide, mapping E/FR | R | C | C | A | C |
| Data split / tokenizer/model | C | R | C | A | I |
| Trainer/checkpoint/evaluation | C | C | R | A | I |
| Viết unit/integration tests | C | R | R | A | I |
| Review matrix & docs | R | C | C | A | R |
| Run thực và lưu logs | I | R | R | A | C |
| Demo/bảo vệ | A | R | R | R | R |

`R` = responsible thực thi, `A` = accountable phê duyệt, `C` = consulted, `I` = informed. Có thể thay đổi vai trò khi nhóm ít người; **không** gán họ tên khi chưa xác nhận.

## 3. Quy trình một tác vụ từ đầu đến hoàn tất

1. **Đăng ký issue:** tên tác vụ, requirement ID, expected output, dependencies, người nhận.
2. **Định nghĩa acceptance:** mô tả input/output/lỗi cần xử lý; nêu test nào có thể chứng minh.
3. **Tạo branch:** `docs/...`, `feat/...`, `fix/...` từ `main` đã cập nhật; không sửa ngay `main` nếu có người review.
4. **Implement:** commit nhỏ, message mô tả mục tiêu; cập nhật docs module trước hoặc cùng thay đổi code.
5. **Self-test:** chạy test liên quan; với code ảnh hưởng training/data, chạy toàn suite nếu tài nguyên cho phép.
6. **Review chéo:** người khác kiểm semantics, tương thích, test oracle, leakage, artifacts; ghi comment/PR.
7. **Merge:** sau review, lưu URL commit/PR và artifacts; đảm bảo không commit weights/credentials/CSV thô ngoài chính sách.
8. **Báo cáo:** cập nhật phase checkbox có bằng chứng, matrix FR status, worklog và decision record nếu thay đổi thiết kế.

## 4. Mẫu task board dùng để làm rõ cách nhóm làm việc

| Task ID | Requirement | Phase | Task | Owner thực tế | Status | Branch/PR | Evidence | Reviewer |
|---|---|---|---|---|---|---|---|---|
| TASK-EXAMPLE-01 | FR06 | P1 | Kiểm stratified split & manifest | _Nhóm điền_ | _Not recorded_ | _—_ | `test_data_setup.py` | _—_ |
| TASK-EXAMPLE-02 | FR08 | P3 | Kiểm Trainer & validation F1 | _Nhóm điền_ | _Not recorded_ | _—_ | `test_engine.py` | _—_ |
| TASK-EXAMPLE-03 | FR09 | P5 | Audit confusion matrix/metrics | _Nhóm điền_ | _Not recorded_ | _—_ | `test_metrics.json` | _—_ |

**Quan trọng:** Các dòng `TASK-EXAMPLE-*` là **mẫu liên kết công việc**, không phải chứng cứ rằng task được giao cho ai hoặc hoàn thành vào ngày cụ thể.

## 5. Nhật ký review tiêu chuẩn

| Ngày (thực) | PR/commit | Reviewer | File thay đổi | Kiểm tra gì | Đã xem log/evidence? | Kết luận | Follow-up |
|---|---|---|---|---|---|---|---|
| _Chưa điền_ | _—_ | _—_ | _—_ | _—_ | _—_ | _Not reviewed_ | _—_ |

Checklist cho reviewer: `[ ]` FR unique; `[ ]` không sai nhãn; `[ ]` không dùng test chọn model; `[ ]` code/test/spec tương ứng; `[ ]` số metrics đúng JSON; `[ ]` không fake test pass; `[ ]` liên kết docs hoạt động; `[ ]` artifacts có/thiếu được ghi đúng.

## 6. Nhật ký lỗi và cách nhóm xử lý

| Bug ID | Triệu chứng | Reproduce steps | Root cause đã xác minh hay giả thuyết | Fix/commit | Regression test | Reviewer |
|---|---|---|---|---|---|---|
| _Điền khi có bug_ | _—_ | _—_ | _—_ | _—_ | _—_ | _—_ |

Không tự điền lỗi làm như nhóm đã gặp nếu không có issue/commit/log. Có thể dùng **sự bất nhất FR08–FR11 trong docs cũ** làm ví dụ vấn đề tài liệu được sửa ở bản v3.0, vì thật sự có diff ma trận để đối chứng.

## 7. Template biên bản họp quyết định kỹ thuật

```text
Mã quyết định: ADR-...
Ngày/những người tham dự: (điền theo thực tế)
Vấn đề/phạm vi ảnh hưởng: E..., FR..., NFR...
Phương án A/B/C:
Phương án chốt và lý do:
Đánh đổi/rủi ro chấp nhận:
File code/docs cần cập nhật:
Test/artefact cần làm mới:
Người xác nhận/link issue/commit:
```

Nếu muốn giải thích quyết định thiết kế hiện có, dùng [design decisions](../analysts/design_decisions.md); **không** khẳng định những ADR đó đã được ký duyệt lịch sử.

## 8. Dòng thời gian thực nghiệm vs dòng thời gian docs

- `reports/reference_run/` và `outputs/2026-11-11/` là **lịch sử output của quick run**; đây là nơi có metadata/số liệu.
- Bộ docs v3.0 được chỉnh ngày **13/11/2026** để đồng bộ FR và tăng chiều sâu giải thích; việc chỉnh docs **không tạo ra epoch, test pass hay commit lịch sử**.
- Khi chạy lại và có số liệu mới, tạo thư mục output theo timestamp mới, giữ lịch sử cũ; ghi commit SHA và env; báo cáo so sánh có kiểm soát.

## 9. Definition of Done cho tài liệu khi nộp

- [ ] `docs/README.md` dẫn tới mọi nhóm tài liệu và link không hỏng.
- [ ] E1.1–E2.7 và FR01–FR15 chỉ có một nghĩa và có code/test/evidence đúng scope.
- [ ] Từng module có I/O, invariant, lỗi, lý do thiết kế và giới hạn.
- [ ] 24 pytest cases đếm chính xác và không cộng case chưa implement.
- [ ] Có RACI thật, người owner/reviewer, commit/PR nếu muốn khẳng định tiến trình nhóm.
- [ ] Demo quick có evidence history/config/metrics; full chưa chạy được nói rõ.
- [ ] Biên bản UAT (nếu chạy) có ngày máy/env/kết quả thực, không điền khống.
- [ ] Nếu ZIP/GitHub thiếu weights, có chú thích và cách truy xuất nếu thực sự đã lưu ở nguồn khác.

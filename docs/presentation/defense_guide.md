# HƯỚNG DẪN BÁO CÁO VÀ 40 CÂU HỎI PHẢN BIỆN LAB 3

> **LAB3-DEFENSE v3.0, 13/11/2026.** Mục đích: giúp nhóm **dẫn cô từ yêu cầu → tài liệu → code → test → bằng chứng**. Không học thuộc con số ngoài outputs, không giả vờ đã thực hiện các kế hoạch chưa có lịch sử.

## 1. Đề xuất cấu trúc trình bày 12–15 phút (có thể tùy chỉnh)

| Phần | Nội dung cần nói | Mở file | Bằng chứng |
|---|---|---|---|
| 1 | Bài toán và hai Exercises, khác nhau ở inference/fine-tuning | `docs/define&design/00_lab3_description.md` | E1/E2 scope |
| 2 | Quy trình phân tích đề thành E/FR/NFR | `docs/analysts/requirements_analysis.md` | Ma trận FR chuẩn hóa |
| 3 | Cơ sở lý thuyết DistilBERT, tokenizer, self-attention, Trainer | `docs/theory/00_theoretical_foundations.md` | Model ID, input/output |
| 4 | Kiến trúc module và data flow | `docs/define&design/06_architecture_and_interfaces.md` | code trong `going_modular/` |
| 5 | Test plan và một case tiêu biểu | `docs/define&design/tests/00_test_plan.md` | DATA-01, ENGINE-01, EVAL-01 |
| 6 | Kế hoạch P0–P7 và cách review nhóm | `docs/plans/implementation_plan.md` | worklog/PR nếu nhóm bổ sung |
| 7 | Quick run và thảo luận giới hạn | `test_metrics.json`, `reports/VALIDATION.md` | cm/metrics/quick/full status |
| 8 | Kết luận và hỏi đáp | `docs/analysts/implementation_evidence_audit.md` | khoảng trống thật |

Nếu cô ưu tiên docs, phân bổ nhiều thời gian cho phân tích yêu cầu, module contracts, test oracle và workflow; phần chạy mô hình chỉ cần mở evidence đã có, không cần chờ train lại khi đang bảo vệ.

## 2. Demo live an toàn

1. Mở `docs/README.md` làm mục lục thay vì tìm các file rời rạc.
2. Chọn một yêu cầu bất kỳ, ví dụ `FR08`, mở ma trận FR và liên kết `engine.run_experiment` + test ENGINE-01 + run `history.json`.
3. Cho cô xem một phép tính có thể kiểm toán từ confusion matrix: 862/1000 = 86,2%; giải thích FP=65/FN=73.
4. Nếu chạy demo `pytest`, phải nói đó là **lần chạy mới** và ghi log; nếu không chạy, chỉ mở `reports/pytest_output.txt` như log lịch sử.
5. Khi trình bày save/reuse, nêu ZIP thiếu weights; muốn demo load model thật phải chuẩn bị checkpoint có checksum/nguồn truy xuất.
6. Có câu hỏi “ai làm file nào?” → mở bảng worklog đã điền bằng link commit thật. Nếu chưa điền, thừa nhận chưa tổng hợp lịch sử, không đoán.

## 3. Câu hỏi và hướng trả lời dựa trên code thật

### A. Phân tích yêu cầu — 1 đến 8

1. **Lab 3 giải quyết bài toán gì?** Phân loại cảm xúc nhị phân review tiếng Anh; E1 suy luận SST-2, E2 fine-tune DistilBERT base trên IMDb.
2. **Vì sao tách hai exercises?** Một bài thực hành API pretrained inference, một bài chứng minh cập nhật trọng số bằng dữ liệu có nhãn.
3. **Mã E và FR khác nhau gì?** E là bước bài tập, FR là yêu cầu chức năng do nhóm đặc tả cho hệ thống; một bước E có thể gắn nhiều FR.
4. **Lỗi ma trận FR trước đó là gì?** FR08..11 bị dùng hai nghĩa; bản v3.0 lấy 00_lab3_description làm chuẩn và chuyển yêu cầu mở rộng sang FR13..15.
5. **Vì sao cần NFR riêng?** Để tiêu chí tính tái lập/không ghi đè/dễ bảo trì không lẫn tính năng nghiệp vụ.
6. **Ai là stakeholder?** Sinh viên thực hiện/test/review, giảng viên đánh giá, người tái lập; không phải người dùng app thương mại.
7. **Định nghĩa hoàn thành bài theo yêu cầu là gì?** Có code và bằng chứng E1/E2, các hợp đồng dữ liệu/model/engine/evaluate được kiểm, số liệu trình bày đúng phạm vi.
8. **Đề yêu cầu full không?** Cần kiểm lại slide/rubric; tài liệu hiện không tự khẳng định full đã chạy.

### B. Lý thuyết — 9 đến 18

9. **Pretrained khác fine-tuning thế nào?** Pretraining học ngôn ngữ trước; fine-tuning tiếp tục tối ưu theo nhãn IMDb.
10. **DistilBERT là gì?** Encoder Transformer distilled từ BERT, base 6 layers, 768 hidden, 12 attention heads.
11. **SST-2 model khác base model?** SST-2 đã có sentiment head học sẵn; base encoder E2 cần head và fine-tune trên IMDb.
12. **WordPiece tokenization?** Chia thành subword rồi ánh xạ ID; token không nhất thiết bằng word.
13. **`attention_mask` để làm gì?** Ngăn model coi padding là nội dung; 1 thật/0 padding.
14. **Vì sao không xóa 'not'?** Negation có thể đảo cực tính sentiment, xóa làm mất ngữ nghĩa.
15. **Self-attention giúp gì?** Biểu diễn token theo quan hệ với các vị trí khác thông qua Q/K/V, multi-head, normalized attention.
16. **Logits khác softmax thế nào?** Logits là điểm chưa chuẩn hóa; softmax cho phân phối score hai lớp; argmax logits và softmax cùng quyết định lớp.
17. **Loss gì và tại sao?** Cross-entropy với nhãn 0/1; Trainer tối ưu gradients bằng AdamW.
18. **Confidence 0.96 có chắc 96% đúng?** Không, nếu chưa hiệu chuẩn; mô hình có thể tự tin và sai.

### C. Thiết kế và tiến trình — 19 đến 26

19. **Vì sao tách notebook/module?** Dễ test offline, giảm cell logic trùng lặp và cho phép reuse.
20. **`data_setup` có được train model không?** Không, chỉ load/split/clean/tokenize/manifest.
21. **`engine` có dùng test làm eval_dataset?** Không, dùng validation để chọn model; test predict sau.
22. **Tại sao split phân tầng?** Giữ tỷ lệ nhãn, tránh subset quick bị lệch lớp nếu lấy N dòng đầu.
23. **Vì sao giữ raw test?** Để gắn prediction với text/sample_id phục vụ errors CSV.
24. **Tại sao không ghi đè run ID?** Tránh mất kết quả và lẫn config/dữ liệu khi resume/reuse.
25. **`run_config` trong contract bao gồm action không?** Không; action train/resume/reuse là thao tác, không phải danh tính dữ liệu/model của run.
26. **Nếu checkpoint đầy đủ epochs nhưng chưa export thì sao?** Code có guard và báo tình trạng; phải kiểm artifacts để phục hồi đúng, không tạo completed giả.

### D. Kiểm thử — 27 đến 34

27. **Có bao nhiêu pytest test?** 24 cases trong logs lịch sử; test parametrized được tính theo từng bộ input.
28. **ENGINE-01 là 8 test?** Không, một function với các assertions liên tục; là 1 pytest case.
29. **Tiny model có phải pretrained thật không?** Không, tiny local synthetic model chỉ test giao diện/trainer lifecycle.
30. **Làm sao biết metric đúng?** EVAL-01 tính accuracy .75, F1 .8 bằng tay; quick confusion cũng đối chiếu số học.
31. **Các exception đã test?** Invalid split, invalid RunConfig, NaN/wrong-shape logits, run guard, alignment lệch nhãn.
32. **Notebook đã test end-to-end trong pytest?** Không, NOTEBOOK-01 chỉ validate schema và Python AST; executed notebook là evidence thực khác.
33. **Những test còn thiếu?** Report unit test, sample-id-level alignment, corrupt checkpoint, GPU/full, revision drift.
34. **24 passed có nghĩa model đúng 24/24 reviews?** Không, đó là 24 software test cases, không phải dữ liệu đánh giá NLP.

### E. Kết quả thực nghiệm — 35 đến 40

35. **Đã chạy dataset nào?** IMDb quick 2.000 train, 500 validation, 1.000 test; seed 42.
36. **Accuracy test bao nhiêu?** 0.8620 (862/1000), theo `test_metrics.json`.
37. **Confusion matrix có ý nghĩa?** TN=435, FP=65, FN=73, TP=427; 138 dự đoán sai.
38. **Best validation F1 và test F1 giống nhau?** Không: validation best ≈0.862823; test F1 ≈0.860887.
39. **Có chạy full chưa?** Chưa thấy kết quả full trong ZIP; code có profile `full`, không được coi đã hoàn thành thực nghiệm full.
40. **Có thể tái lập nguyên run chỉ bằng ZIP?** Chưa đủ: ZIP thiếu weights/optimizer checkpoints và CSV. Có thể dùng code để train run mới, nhưng không hứa kết quả trùng tuyệt đối.

## 4. Những điều KHÔNG nên nói trước giảng viên

- “Bọn em đã hoàn thành full dataset” khi chỉ có quick.
- “24 test pass nghĩa là mô hình chính xác 100%” (sai mục đích test).
- “Cứ có config.json là load được checkpoint” khi weights không có.
- “Em chọn F1 tốt nhất trên test” (data leakage); phải là validation.
- “Nhóm A làm phase 1 ngày ...” nếu chưa có log/commit xác nhận.
- “Review dài chắc chắn sai vì truncation” khi chưa làm thí nghiệm nhân quả.

## 5. Check cuối cho slide và README

- [ ] Slide yêu cầu có E1/E2, ma trận FR không lặp nghĩa.
- [ ] Sơ đồ data–model–Trainer–evaluate khớp code.
- [ ] Có 1 ví dụ testcase với input/expected thực.
- [ ] Có confusion matrix, tính tay TP/TN/FP/FN và hạn chế quick.
- [ ] Có trang “Công việc nhóm / review / PR” với link thực (nếu có).
- [ ] Có trang “Giới hạn và cải tiến”, không gắn nhãn `đã triển khai` cho đề xuất.
- [ ] Các artifacts dùng trong demo có thật ở laptop/Drive được chuẩn bị trước.

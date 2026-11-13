# PHÂN TÍCH YÊU CẦU LAB 3 TỪ ĐỀ BÀI ĐẾN TIÊU CHÍ NGHIỆM THU

> **LAB3-REQ-ANALYSIS v3.0 — 13/11/2026.** Đây là bản diễn giải các bước Exercise 1/2 đang được dự án mô tả là lấy từ slide Chương 4 trang 25. Vì ZIP không kèm slide gốc, tài liệu **không trích nguyên văn đề** và cần đối chiếu lại với file slide do cô cung cấp khi có.

## 1. Phương pháp phân tích yêu cầu

Thay vì coi từng dòng đề là một dòng code, quy trình phân tích theo 6 bước: (1) xác định mục đích học tập; (2) xác định input/output quan sát được; (3) phân rã thành thao tác tuần tự và bất biến dữ liệu; (4) xác định module chịu trách nhiệm; (5) chọn test có khả năng chứng minh đúng yêu cầu; (6) xác định giới hạn của bằng chứng. Đầu ra của phân tích là `FR`, `NFR`, các kịch bản `UC` và ma trận `E → FR → code → tests → evidence`.

### 1.1. Vấn đề cốt lõi

Một mô hình NLP pretrained có thể đưa ra dự đoán ngay, nhưng **dự đoán được** không đồng nghĩa **đã fine-tune**. Nếu chỉ gọi `pipeline('sentiment-analysis')`, bài 1 có thể hoàn thành nhưng bài 2 chưa chứng minh cập nhật weights. Ngược lại, train head ngẫu nhiên trên review mà không nạp pretrained encoder sẽ không thể hiện mục tiêu transfer learning. Vì vậy đặc tả bắt buộc **hai checkpoint, hai vòng đời, hai loại bằng chứng**.

### 1.2. Các tác nhân và mục tiêu

| Tác nhân | Điều họ cần quan sát | Đối tượng trao đổi |
|---|---|---|
| Sinh viên implement | Biết rõ cần code ở module nào, thứ tự làm | FR, phase, API contract |
| Sinh viên test | Biết input, expected, ngoại lệ và mức bao phủ | Test specs, pytest |
| Người review nhóm | Biết thay đổi có đúng yêu cầu và không phá dữ liệu hay artifacts | Matrix, code diff, logs |
| Giảng viên | Đi từ yêu cầu tới code và kết quả, hỏi được “vì sao” | Bảng E, FR, sơ đồ, báo cáo |
| Người tái lập | Setup môi trường và chạy lại mà không ghi đè run | README, RunConfig, run lifecycle |

## 2. Phân tích Exercise 1 — pretrained inference

| Mã bước | Ý nghĩa nghiệp vụ | Input | Cách triển khai | Expected quan sát | Failure / điều không thể kết luận |
|---|---|---|---|---|---|
| E1.1 | Có môi trường sử dụng HF | Python, requirements | cài `transformers`, thư viện liên quan | import thành công, versions hợp lệ | Không bảo đảm CUDA hoặc Internet |
| E1.2 | Dùng checkpoint đã học phân loại sentiment | checkpoint SST-2 | `AutoTokenizer`, `AutoModelForSequenceClassification` | nhãn 2 lớp phù hợp | Không phải base chưa fine-tune |
| E1.3 | Hiểu phép biến đổi text→tensor | câu ví dụ | tokenize, hiển thị tokens/IDs/mask, model logits | tensor/shape có ý nghĩa, softmax tổng≈1 | Token không tương ứng 1-1 với từ tiếng Việt |
| E1.4 | Biết dùng API suy luận | danh sách câu mẫu | thủ công + `pipeline` | label/confidence/p_positive trong JSON | Không được tính accuracy từ câu tùy chọn |

### 2.1. Các trường hợp biên cần thảo luận

- “not bad” thể hiện phủ định đảo chiều; không xóa từ “not” khi clean.
- Câu có cả khen và chê; binary classifier buộc chọn một trong hai lớp.
- Score softmax cao chưa chứng minh mô hình đúng; không dùng điểm confidence như độ chắc chắn đã hiệu chuẩn.
- Mô hình SST-2 được huấn luyện cho kiểu câu/phân phối khác IMDb; không tuyên bố so sánh công bằng bằng vài ví dụ.

## 3. Phân tích Exercise 2 — supervised fine-tuning

| Mã | Vấn đề cần xử lý | Giải pháp đang dùng | Ràng buộc bắt buộc | Bằng chứng kỳ vọng |
|---|---|---|---|---|
| E2.1 | Thư viện cần đủ để Trainer hoạt động | `requirements.txt` | Pin API tương thích | versions & log môi trường |
| E2.2 | Dataset phải có nhãn và phân chia độc lập | `load_imdb` | Không trộn test benchmark vào train | ID/manifest, phân bố lớp |
| E2.3 | Base encoder phải pretrained, head phù hợp | `build_model` | `num_labels=2`, id2label/label2id đúng | model config, logits/loss |
| E2.4 | Review dài/ngắn thành batch tensor | clean, stratified split, tokenize, collator | Giữ từ phủ định, truncate, dynamic padding | schema tokenized, masks |
| E2.5 | Trainer cần training args rõ ràng | `make_training_args` | epochs/LR/batch, eval/save epoch | config, output dirs |
| E2.6 | Tối ưu thực sự bằng backprop và validation | `Trainer.train` qua engine | train dataset ≠ test, model trainable, lưu checkpoint | log loss/step, completed marker |
| E2.7 | Đánh giá mô hình đã chốt | `Trainer.predict`, export | test chỉ sau best model theo validation | test_metrics, confusion matrix, errors |

### 3.1. Vì sao chọn validation từ train, giữ IMDb test độc lập?

IMDb thường cung cấp train/test; nếu dùng test để chọn epochs/LR, ước lượng cuối bị thiên lệch. Dự án chia **validation phân tầng từ train**, dùng validation F1 Positive để chọn best checkpoint. Sau khi cấu hình được chốt, test được đánh giá để báo cáo. Cách chia bằng ID ngăn trộn hàng trực tiếp, hash exact-text overlap cho thấy khả năng trùng sau clean; không chứng minh không có duplicate gần giống.

### 3.2. Vì sao quick không phải full?

Quick kiểm tra đầu-cuối pipeline ở chi phí thấp (2.000/500/1.000, max_length=128, epochs=2), trong khi full dùng toàn bộ train sau chia và test nguyên bộ, max_length=256, epochs=3. Khác kích thước tập, số token và thời gian huấn luyện → metric quick không được gắn nhãn full hoặc so trực tiếp nếu không kiểm soát protocol.

### 3.3. Điều kiện thành công và thất bại

- **Thành công kỹ thuật:** tokenizer/model nhận input đúng schema; Trainer tạo checkpoint từ train/validation; chọn best validation F1; test metrics tính từ prediction thật; round-trip model hợp lệ.
- **Thành công tài liệu:** E2.1–E2.7 truy vết được code → test/evidence; không có FR dùng hai nghĩa; có kết quả thực tế và giới hạn.
- **Không nhất thiết thành công:** mọi review dự đoán đúng, full đạt accuracy dự kiến, mô hình dùng tốt cho tiếng Việt, số liệu lặp y hệt giữa mọi phần cứng.
- **Thất bại dữ liệu:** split giao nhau, raw/test mismatch, nhãn không thuộc {0,1}, dùng test để chọn checkpoint.
- **Thất bại run:** `train` ghi đè dữ liệu, `resume` từ run khác, completed marker ghi khi train chưa xong.

## 4. Chuyển yêu cầu thành FR/NFR và test

**Ví dụ 1: E2.4 → FR06 → DATA-01/07/08.** Câu “tiền xử lý dữ liệu” mơ hồ; phải chỉ rõ các ràng buộc: giữ nhãn, split rời nhau, giữ phủ định, tokenized columns gồm `input_ids`, `attention_mask`, `labels`, độ dài không vượt max_length. Dùng DATA-07 chứng minh `Not bad` không bị mất ý phủ định, DATA-08 chứng minh schema và manifest.

**Ví dụ 2: E2.6 → FR08 + FR11 → ENGINE-01.** “Train bằng Trainer” là mục tiêu chức năng; “không ghi đè, resume và reuse” là tính năng mở rộng để an toàn. Test tiny offline mô phỏng dừng sau epoch 1 → xác nhận chưa có completed marker → resume đạt step 8 → reuse dự đoán tương đương. Đây là 1 pytest case tích hợp, **không** phải 8 test độc lập.

**Ví dụ 3: E2.7 → FR09 + FR14/15.** “Đánh giá” không chỉ là in accuracy; còn kiểm logits `[N,2]`, nhãn hợp lệ, phân biệt FP/FN, giữ thứ tự mẫu và ghi metrics thực vào JSON. Quick run còn có confusion matrix và ROC-AUC.

## 5. Ràng buộc, giả định và rủi ro khi thực thi

| Loại | Mô tả | Kiểm soát / residual risk |
|---|---|---|
| Chức năng | Nhãn binary: 0 NEGATIVE/1 POSITIVE | `ID2LABEL` và test; review trung tính vẫn ép hai lớp |
| Hạ tầng | Tải pretrained/dataset lần đầu cần mạng/cache | version pin requirements, báo lỗi nguyên nhân; tránh hứa offline thật |
| Tài nguyên | Transformer với optimizer/checkpoint chiếm RAM/disk | profile quick, batches, fp16/bf16 false trong code; full tốn hơn |
| Nguồn model | revision mặc định `main` biến động | lưu resolved model revision, nên pin SHA nếu tái lập nghiêm ngặt |
| Kiểm thử | tiny fixture là random small model | chỉ chứng minh logic I/O và lifecycle, không chất lượng NLP |
| Báo cáo | Chưa có weights/CSV trong ZIP | chỉ dẫn metadata và outputs còn có; lưu liên kết artifacts thật nếu bổ sung |
| Mô hình | Câu dài cắt phần cuối | phân tích lỗi, thử chính sách cắt trên validation trước khi test |

## 6. Requirement ambiguity log — những điểm cần hỏi/giải thích

| Câu hỏi | Quyết định hiện tại | Cần xác nhận gì nếu giảng viên yêu cầu? |
|---|---|---|
| Đề có bắt chạy full dataset? | Bản docs hiện coi quick là bằng chứng thực nghiệm đã chạy, full còn thiếu | Slide gốc/rubric có yêu cầu full hay không |
| Đề có yêu cầu dùng package `evaluate` để tính metrics? | Cài `evaluate`, nhưng code dùng sklearn trực tiếp | Nếu bắt API evaluate, cần chỉnh code và test |
| Đề có yêu cầu chứng minh accuracy tối thiểu? | Không áp ngưỡng tự đặt | Rubric/tiêu chí đo thực tế |
| Đề có bắt sử dụng `pipeline`? | Notebook làm manual và pipeline ở E1 | Xác nhận đúng E1.4 trên slide |
| Có phải lưu weights lên GitHub? | Không; ZIP thiếu weights và có `.gitignore` | Cô có yêu cầu link Google Drive/Hub để tải không |
| “Đúng mọi trường hợp” có phải điều kiện? | Không; hạn chế 1 seed và English NLP | Không claim khả năng ngoài test set |

## 7. Definition of Ready và Definition of Done cho tài liệu

**Ready:** yêu cầu có ID duy nhất, phạm vi, đầu vào/đầu ra, acceptance, người review, nguồn đề; nếu mơ hồ phải ghi vấn đề cần xác nhận. **Done:** có code thực sự, test/evidence phù hợp, ma trận được cập nhật, link không lỗi, reviewer ghi lại mức xác minh, không lấy warning hay result cũ để chứng minh một lần chạy mới. Kế hoạch làm việc chi tiết nằm trong [worklog mẫu](../plans/team_workflow_and_log.md).

## 8. Danh sách các FR chuẩn hóa

`FR01` dependencies · `FR02` pretrained models · `FR03` token/logit inspection · `FR04` inference · `FR05` IMDb · `FR06` split/preprocess · `FR07` args · `FR08` train Trainer · `FR09` test evaluation · `FR10` save/load · `FR11` resume/reuse · `FR12` measured report · **mở rộng** `FR13` logits/loss contract · `FR14` metric validation · `FR15` alignment/export.

Danh sách chi tiết và status: [ma trận truy vết](requirements_traceability.md). Tài liệu gốc để xác nhận nghĩa FR01–FR12: [đặc tả tổng quan](../define&design/00_lab3_description.md).

# Đặc tả tổng quan Lab 3 — Hugging Face

**Phiên bản:** 2.0 · **Ngày tạo:** 11/11/2026 · **Cập nhật đặc tả:** 11/11/2026 · **Nguồn đề:** slide Chương 4, trang 25.
Tài liệu mô tả thiết kế hiện thực; trạng thái thực nghiệm nằm tại `reports/VALIDATION.md`.
Cấu hình có hiệu lực nằm trong `going_modular/config.py`; notebook chỉ chọn profile và action.

## 1. Bối cảnh và vấn đề

Lab 2 tái sử dụng mô hình pretrained xử lý ảnh. Lab 3 chuyển cùng tư duy sang NLP:
biến review thành tensor mà Transformer hiểu, sử dụng checkpoint pretrained, rồi thích nghi với nhãn nhị phân.
Cần phân biệt **inference từ model đã học sentiment** và **fine-tune từ encoder nền**.
Nếu chỉ gọi pipeline thì chưa hoàn thành Exercise 2; nếu train model random thì chưa đáp ứng pretrained.

## 2. Mục tiêu đo được

| Mã | Mục tiêu | Bằng chứng |
|---|---|---|
| O1 | Nạp tokenizer + pretrained sentiment model | Model ID/revision, bảng tokens |
| O2 | Suy luận câu tiếng Anh bằng model và pipeline | Predictions JSON |
| O3 | Chuẩn bị tập train/validation/test không dùng test để chọn tham số | Manifest và Trainer eval_dataset |
| O4 | Fine-tune DistilBERT nền bằng Trainer | Log loss/LR, checkpoint, history |
| O5 | Đánh giá và nạp lại mô hình đã học | Metrics, confusion matrix, round-trip inference |
| O6 | Code dễ đọc, kiểm thử và tái sử dụng theo Lab 2 | Module specs và tests |

## 3. Phạm vi

Bắt buộc: đủ 4 bước Exercise 1 và 7 bước Exercise 2. Dataset chọn IMDb tiếng Anh;
không tự thêm yêu cầu phải thử nhiều kiến trúc. Hai profiles là mức tài nguyên, không phải hai mô hình cạnh tranh.
Ngoài phạm vi: tìm hyperparameter tối ưu, dịch tiếng Việt, deployment website, LoRA/PEFT, multi-GPU.
Full fine-tuning cập nhật toàn bộ encoder và head; không yêu cầu đóng băng vì slide không bắt buộc.

## 4. Yêu cầu chức năng

| Mã | Yêu cầu | Hiện thực |
|---|---|---|
| FR01 | Cài transformers, datasets, evaluate và accelerate | requirements/setup |
| FR02 | Nạp checkpoint sentiment có thật | Notebook §1 |
| FR03 | Hiển thị token, ID, mask, logits, softmax | Notebook §1 |
| FR04 | Chạy sentiment trên câu mẫu | predict_texts + pipeline |
| FR05 | Load dataset nhị phân | load_imdb |
| FR06 | Split và tokenize đúng checkpoint | prepare_raw_splits, tokenize_splits |
| FR07 | Định nghĩa TrainingArguments | make_training_args |
| FR08 | Tạo Trainer và fine-tune | run_experiment |
| FR09 | Đánh giá best model trên test | export_evaluation |
| FR10 | Save/load model + tokenizer | save_pretrained / from_pretrained |
| FR11 | Resume/reuse không ghi đè thầm lặng | check_action + checkpoint |
| FR12 | Báo cáo lấy số liệu thực | write_report |

## 5. Phi chức năng và ràng buộc

Cùng seed tái lập split; không hứa bitwise reproducibility giữa GPU/CPU và phiên bản khác nhau.
Không dùng test để chọn LR, epochs, threshold. Nhãn dự đoán argmax, không tối ưu threshold trên test.
Có Internet lần đầu; GPU khuyến nghị. RAM/disk đủ cho dataset, weights và ít nhất hai checkpoint kèm optimizer.
Pin phiên bản HF trong requirements; model/dataset revision mặc định main có thể thay bằng commit SHA.
Metadata ghi content hash và resolved model revision để truy vết; không coi main bất biến.

## 6. Kiến trúc và giao diện

Notebook gọi data_setup để tạo raw/tokenized DatasetDict; model_builder tạo model/tokenizer;
engine dùng Trainer nhận train + validation; evaluate nhận PredictionOutput và raw test theo cùng thứ tự;
reporting đọc metrics thực để sinh Markdown. utils không import engine.
Input model: input_ids[B,L], attention_mask[B,L], labels[B]. Output logits[B,2], loss scalar khi có labels.

## 7. Cấu hình và run lifecycle

Xem bảng profile ở README; RunConfig.for_profile là nguồn cấu hình.
`run_id` chỉ gồm chữ/số/_/-. Artifact contract gồm config, digest manifest và danh tính tokenizer.
Action không nằm trong contract: chuyển train → resume không tự làm contract khác nhau như lỗi Lab 2.
Không tự ép action; khi có artifacts người dùng chọn resume/reuse hoặc tên run mới.

## 8. Tiêu chí nghiệm thu

1. Notebook thực hiện đủ 11 bước của slide.
2. Tokenizer và model cùng checkpoint, lớp NEGATIVE/POSITIVE đúng.
3. Train/validation không trùng ID, test gốc độc lập, có thống kê exact-text overlap.
4. Trainer train được, có best checkpoint theo validation F1.
5. Test metrics được tính từ logits thật, có số mẫu và profile.
6. Save/load cho cùng dự đoán trong dung sai số học.
7. Kiểm thử offline đạt; báo cáo phân biệt test phần mềm với thí nghiệm pretrained thật.

Không đặt ngưỡng accuracy tùy ý để coi đạt đề. Chất lượng phải diễn giải theo cấu hình và tập đánh giá.


## 9. Kế hoạch theo phase và trách nhiệm kiểm chứng (bổ sung phiên bản 2.0)

Tài liệu tổng này liên kết với [kế hoạch tổng](../plans/implementation_plan.md) và 8 file chi tiết: [P0 môi trường](../plans/phase0.md), [P1 dữ liệu](../plans/phase1.md), [P2 tokenizer/model](../plans/phase2.md), [P3 Trainer](../plans/phase3.md), [P4 checkpoint/lifecycle](../plans/phase4.md), [P5 đánh giá](../plans/phase5.md), [P6 notebook/báo cáo](../plans/phase6.md), [P7 kiểm thử/bàn giao](../plans/phase7.md). Mỗi file có checklist chưa mặc định đánh dấu, đầu ra, tiêu chí nghiệm thu và nhật ký để ghi tên/ngày làm sau khi nhóm phân công.

Hợp đồng model chi tiết gồm kiến trúc DistilBERT, input/output tensor, cấu hình quick/full, checkpoint IDs và điều kiện kiểm thử trong [`02_model.md`](02_model.md). Bộ test specs theo case IDs DATA/MODEL/ENGINE/UTIL/EVAL/NOTEBOOK ở [`tests/00_test_plan.md`](tests/00_test_plan.md), truy vết tổng tại [`../analysts/requirements_traceability.md`](../analysts/requirements_traceability.md).

### Phân biệt ba mức bằng chứng

1. **Test phần mềm:** pytest trong ZIP đầu vào ghi 24 passed; kiểm các bất biến trên tiny model/data synthetic, không đo accuracy mô hình pretrained thật.
2. **Validation training:** đánh giá trên validation để chọn checkpoint tốt nhất theo F1 Positive; không phải kết quả test cuối.
3. **Test IMDb cuối:** run quick trong bản gốc có 1.000 mẫu test, accuracy **0.8620**; full profile chưa chạy. Đọc `reports/VALIDATION.md` và JSON metrics trước khi ghi số liệu.

Phần sửa tài liệu không tự động thay đổi `going_modular/`, không tạo weights model còn thiếu và không tạo log kiểm thử mới.

## 10. Phân tích stakeholder, use case và ranh giới hệ thống (mở rộng 3.0)

**Stakeholder:** (a) sinh viên thực hiện và bảo vệ: muốn chứng minh đủ E1/E2, (b) giảng viên: muốn truy vết code/test/artifact, (c) người tái lập: muốn setup chạy lại, (d) người review: muốn phát hiện vi phạm split/lifecycle. Người dùng là người **chạy notebook** chứ không phải khách hàng sử dụng dịch vụ production. Vì vậy hệ thống ưu tiên khả năng học tập, giải thích, kiểm chứng hơn SLA triển khai.

| Use case | Tác nhân | Tiền điều kiện | Luồng chính | Kết quả đo được | Ngoại lệ |
|---|---|---|---|---|---|
| UC01 Khám phá pretrained sentiment | Sinh viên | Đã cài dependencies / có cache | Load SST-2 → tokenize → infer thủ công/pipeline | IDs/mask/logits/JSON câu mẫu | Lỗi mạng, checkpoint không tồn tại |
| UC02 Chuẩn bị dữ liệu | Sinh viên | Có IMDb train/test | Tạo sample_id → stratified validation → subset → clean → tokenize | DatasetDict + manifest | Thiếu nhãn, kích thước chia bất hợp lệ |
| UC03 Fine-tune | Sinh viên | Có tokenized train/validation, run mới | Tạo TrainingArguments/Trainer → train → validation F1 → save | history, checkpoint và best_model | Thiếu tài nguyên, dừng giữa epoch, lỗi quyền ghi |
| UC04 Phục hồi/Reuse | Sinh viên | Có contract của run, checkpoint/weights phù hợp | Validate contract → resume hoặc load best model | Không train đè, cùng dự đoán (dung sai) | Thiếu checkpoint, mismatch cấu hình |
| UC05 Báo cáo | Sinh viên/giảng viên | Đã chọn model trên validation | Predict test → metrics/CSV/PNG → REPORT | Bảng metrics, số mẫu, confusion matrix | Alignment lệch, logits sai |

### 10.1. In-scope / out-of-scope

Trong phạm vi: 2 exercise, binary sentiment tiếng Anh, fine-tuning DistilBERT bằng Trainer, tái sử dụng module, báo cáo quick theo artifacts. Ngoài phạm vi: mô hình tiếng Việt, service API, bảo đảm fairness giữa các ngôn ngữ, đánh giá đa seed, hyperparameter optimization quy mô lớn, đánh giá full nếu chưa chạy. Không suy ra kết quả mới chỉ từ việc viết thêm docs.

## 11. Đặc tả I/O cấp hệ thống

| Đầu vào | Schema / điều kiện | Đầu ra | Nguồn kiểm chứng |
|---|---|---|---|
| Câu tiếng Anh | `str`, mã hóa văn bản hợp lệ; inference expects list không rỗng | Nhãn và `p_positive`, confidence | `predict_texts`, E1 predictions |
| IMDb | `DatasetDict` gồm `train`, `test`; columns `text` và nhãn 0/1 | `train`,`validation`,`test` sau split và tokenized DatasetDict | `data_setup.py`, manifest |
| RunConfig | Python dataclass; `run_id` chỉ `[A-Za-z0-9_-]`, LR > 0, `8≤max_length≤512` | `config.json` + run directory | UTIL test và config code |
| Logits | `float[N,2]`, finite; nhãn `int[N]` thuộc {0,1} | Accuracy/precision/recall/F1/macro F1 | EVAL tests |
| Run artifact | `config/manifest/history/completed/best_model` tuỳ action | Trainer, predictions, report | ENGINE-01 + output quick |

**Khối nguồn dữ liệu** không được quyết định checkpoint tốt nhất. **Khối huấn luyện** không nhìn test. **Khối đánh giá** không cập nhật model. **Khối báo cáo** không tự chế metrics. Những nguyên tắc này làm cơ sở tách module và giảm rủi ro tự đánh giá sai.

## 12. Các bất biến và giả định có thể phản biện

- Train và validation không giao nhau theo **ID**; `test` giữ từ split benchmark gốc. Nếu có review trùng text giữa splits phải khai báo `duplicate_text_overlap` theo exact hash; giá trị 0 trong run quick không chứng minh không có trùng ngữ nghĩa hoặc đạo văn.
- `model_id` SST-2 ở Exercise 1 dùng cho inference, `model_id` base ở Exercise 2 dùng fine-tune. Hai bài khác nhau về nguồn head và cách tạo weights; không so accuracy trực tiếp trên tập khác nhau.
- `metric_for_best_model='f1'` là validation F1 Positive; không chọn checkpoint bằng test F1.
- Một lần run có `run_id` duy nhất. Khi action `reuse/resume`, contract gồm config, manifest digest, tokenizer identity phải khớp; **action** không nằm trong contract để không gây mismatch giả tạo.
- Lần chạy quick trong ZIP: 2.000 train/500 validation/1.000 test và test accuracy 0.8620; **không phải** benchmark full.
- `trainer.predict` trả kết quả theo thứ tự dataset tokenized; export kiểm tra `label_ids` với `raw_test['label']`. Kiểm chỉ theo nhãn không chứng minh được đảo vị trí giữa hai mẫu **cùng nhãn**; coi đây là điểm còn có thể gia cố.
- Không có ngưỡng accuracy bắt buộc trong đặc tả. Tiêu chí kỹ thuật là tính hợp lệ của quy trình và bằng chứng thực nghiệm trung thực.

## 13. Yêu cầu chất lượng NFR và kiểm chứng

| NFR | Yêu cầu | Cách kiểm chứng / giới hạn |
|---|---|---|
| NFR01 | Tách test khỏi train/validation | `Trainer(...train_dataset,eval_dataset...)` + manifest; không có oracle phát hiện mọi kiểu leakage |
| NFR02 | Tái lập thiết lập | seed, IDs, digest, logs; không cam kết bitwise giữa CPU/GPU |
| NFR03 | An toàn artifact | từ chối train khi thư mục không trống, atomic JSON; không bảo đảm transactional writes toàn pipeline |
| NFR04 | Truy nguyên model/dataset | model revision log có thể là SHA, dataset revision `main` là động |
| NFR05 | Báo cáo không đánh tráo kết quả | tách quick/full/offline tests rõ ràng; review bằng metrics JSON |
| NFR06 | Dễ kiểm thử và bảo trì | module hóa & pytest; chưa đo coverage dòng/nhánh |
| NFR07 | Tương thích môi trường đã chỉ định | requirements Python 3.10–3.12, Colab/VS Code; tuỳ thiết bị/driver |
| NFR08 | Minh bạch giới hạn và thông tin nhạy cảm | không đưa token/HF credentials vào docs; CSV review thô không nằm trong ZIP |

## 14. Thứ tự trình bày đề xuất trong báo cáo

1. Chỉ slide yêu cầu E1.1..E2.7 và sơ đồ 2 bài.
2. Thuyết minh sơ đồ data → model → Trainer → evaluate và các ranh giới split.
3. Nêu 4 quyết định thiết kế quan trọng: 2 checkpoints, stratified subset, best validation F1, run contract.
4. Lật ma trận FR đã chuẩn hóa và chứng minh 2 yêu cầu bất kỳ bằng file code/test/output.
5. Đưa `test_metrics.json` (quick 86,2%) cùng confusion matrix và giới hạn.
6. Kết luận cái gì đã chạy, cái gì chưa chạy, sửa cái gì để đủ chất lượng hơn.

**Tài liệu bổ sung:** [phân tích yêu cầu](../analysts/requirements_analysis.md), [ma trận FR](../analysts/requirements_traceability.md), [kiến trúc](06_architecture_and_interfaces.md), [lý thuyết](../theory/00_theoretical_foundations.md), [hướng dẫn vấn đáp](../presentation/defense_guide.md).

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

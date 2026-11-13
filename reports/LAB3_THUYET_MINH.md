# Thuyết minh Lab 3 — Phân tích cảm xúc và fine-tuning với Hugging Face

## 1. Mục tiêu

Bài thực hành giúp hiểu cách sử dụng mô hình đã huấn luyện và cách thích nghi mô hình với dữ liệu mới.
Hai bài dùng cùng kiểu nhiệm vụ phân loại cảm xúc, nhưng khác giai đoạn: bài 1 suy luận trên câu mẫu;
bài 2 cập nhật tham số bằng dữ liệu có nhãn. 

## 2. Cơ sở lý thuyết

### 2.1. Pretraining và fine-tuning

Một encoder ngôn ngữ học biểu diễn từ ngữ/câu từ dữ liệu lớn trước khi được áp dụng vào bài cụ thể.
Fine-tuning tối ưu thêm encoder và head phân loại bằng nhãn mục tiêu. Điều này khác train random từ đầu.
Trong bài 1, checkpoint đã fine-tune SST-2 nên có thể dự đoán ngay. Trong bài 2, DistilBERT nền được gắn
head hai lớp mới và học trên IMDb. LR nhỏ giúp cập nhật biểu diễn đã học từng bước.

### 2.2. Tokenization và tensor

Mô hình không nhận trực tiếp chuỗi Python. Tokenizer tách thành subword, ánh xạ thành ID trong vocabulary,
thêm token đặc biệt. Attention mask phân biệt token thật và padding. Khi batch gồm chuỗi dài ngắn khác nhau,
collator đệm đến chuỗi dài nhất; truncation kiểm soát giới hạn độ dài.

### 2.3. Phân loại hai lớp

Model tạo logits z0,z1. Softmax cho p0,p1 với tổng bằng 1; argmax chọn Negative hoặc Positive.
Cross-entropy của mẫu nhãn y là -log(p_y). Trainer tính gradient và optimizer AdamW cập nhật tham số.
Scheduler điều chỉnh LR qua warmup rồi giảm tuyến tính; clipping giới hạn norm gradient.
Không đồng nhất AdamW decoupled weight decay với mọi cách cộng L2 vào loss.

### 2.4. Đánh giá đúng vai trò dữ liệu

Train cập nhật weights; validation chọn checkpoint; test chỉ đánh giá model đã chốt.
Accuracy đo tỷ lệ đúng; precision/recall giúp tách lỗi FP/FN; F1 cân bằng hai yếu tố đó.
Macro F1 cân bằng trọng số hai lớp; ROC-AUC dùng score liên tục. Không chọn threshold dựa trên test.

## 3. Thiết kế và quy trình thực hiện

### Exercise 1

Cài thư viện, nạp model/tokenizer sentiment SST-2, tokenize câu mẫu và in bảng IDs/mask.
Thực hiện inference thủ công để hiểu logits/softmax; gọi pipeline để đối chiếu cách dùng API cấp cao.
Dùng câu tích cực, tiêu cực, phủ định và cảm xúc pha trộn; lưu dự đoán thực tế vào JSON.
Ví dụ minh họa chỉ chứng minh thao tác API, không thay tập đánh giá có nhãn.

### Exercise 2

Load IMDb, tách validation phân tầng từ train, chọn profile quick hoặc full, làm sạch và tokenize.
Tạo Trainer với DataCollatorWithPadding, compute_metrics và TrainingArguments.
Fine-tune toàn bộ model, chọn validation F1 tốt nhất, export model/tokenizer.
Dự đoán test một lần, xuất bảng độ đo, confusion matrix và review sai.
Nạp lại model/tokenizer từ disk, so xác suất trước/sau để kiểm tra khả năng tái sử dụng.

## 4. Tổ chức phần mềm

Notebook hiển thị và điều phối; data_setup quản dữ liệu; model_builder quản pretrained;
engine quản Trainer/lifecycle; evaluate tính độ đo; utils quản metadata; reporting tạo báo cáo.
Cấu trúc cho phép thay checkpoint/dataset có kiểm soát thay vì sửa nhiều cell rời rạc.
Module specs 00–05 mô tả I/O, quyết định thiết kế, ngoại lệ và tiêu chí chấp nhận.

## 5. Kết quả và cách đọc bằng chứng

Kết quả phần mềm đã chạy được ghi tại `VALIDATION.md`. Thí nghiệm quick trên dữ liệu IMDb thật đã hoàn tất;
kết quả nằm trong notebook executed và outputs. Không điền accuracy khi chưa có dự đoán model thật.
Khi bạn chạy notebook, `REPORT.md` tự ghi số mẫu, profile, tham số, F1 validation tốt nhất và metrics test.
Đối chiếu `test_metrics.json` với `predictions.csv`; review trong `errors.csv` dùng phân tích lỗi.

### Kết quả quick đã đo

| Độ đo test | Giá trị |
|---|---:|
| Số mẫu test | 1000 |
| Accuracy | 86.2000% |
| Precision Positive | 0.8679 |
| Recall Positive | 0.8540 |
| F1 Positive | 0.8609 |
| Macro F1 | 0.8620 |
| ROC-AUC | 0.9317 |

Best validation F1 = 0.8628; đây là kết quả quick, không phải full IMDb.

## 6. Thảo luận và giới hạn

Quick chỉ dùng subset, không tương đương full benchmark. Chạy một seed không cho biết độ biến thiên thống kê.
Text dài bị cắt có thể bỏ mất câu quyết định cảm xúc. Mỉa mai, phủ định và khen/chê pha trộn có thể gây lỗi.
IMDb và SST-2 khác phân phối: không so trực tiếp hai độ chính xác trên hai test set khác nhau.
Mô hình tiếng Anh không được chứng minh phù hợp tiếng Việt. Confidence chưa hiệu chuẩn nên không phải bảo đảm đúng.

## 7. Kết luận

Bộ bài hiện thực đủ thao tác mà đề yêu cầu, từ pretrained inference đến fine-tuning bằng Trainer,
lưu/nạp và đánh giá. Mức hoàn thành thực nghiệm phải đi cùng log thực tế; không suy từ test phần mềm ra chất lượng sentiment.
Mở rộng hợp lý sau khi hoàn thành: kiểm tra LR trên validation, đánh giá ảnh hưởng max_length,
hoặc so head-only và full fine-tuning trên cùng split, cùng protocol và nhiều seed.

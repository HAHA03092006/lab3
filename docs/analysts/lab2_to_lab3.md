# Đối chiếu Lab 2 → Lab 3

Repo tham chiếu: toan58936/lab2, main tại commit 93d255b.
Đã đọc code package, notebook chính và mô tả tổng quan/data/engine để giữ mức chi tiết tương ứng.

| Nội dung | Lab 2 | Lab 3 |
|---|---|---|
| Điều phối | pretrained_models.ipynb | huggingface_sentiment.ipynb |
| Dữ liệu | CIFAR-10 ảnh 32×32 | IMDb review tiếng Anh |
| Tiền xử lý | ImageNet transforms | Tokenizer, truncation, dynamic padding |
| Model | torchvision VGG/ResNet | HF AutoModelForSequenceClassification |
| Đầu vào | Float tensor [B,3,224,224] | Integer IDs + mask [B,L] |
| Nhãn | 10 lớp | 2 lớp |
| Huấn luyện | Loop PyTorch thủ công | Trainer theo đúng đề bài |
| Tối ưu | Adam | AdamW + warmup/linear schedule |
| Best checkpoint | validation accuracy | validation F1 Positive |
| Save | state_dict .pth | save_pretrained, safetensors, tokenizer |
| Resume | Checkpoint tự quản lý | Trainer model/optimizer/scheduler/RNG |
| Evaluation | Accuracy, CM, per-class | Accuracy, P/R/F1, macro F1, AUC, CM |
| Báo cáo lỗi | Ảnh dự đoán sai | Review dự đoán sai + sample_id |
| Thiết kế | 00–05 + tests/plans/analysts | Giữ hệ thống đặc tả tương ứng |

## Những điều được chỉnh khi kế thừa

- Lab 2 có chỗ tài liệu ghi sáu thí nghiệm trong khi code chỉ ba run. Lab 3 ghi rõ hai bài, một fine-tune chính, hai profiles.
- Action/resume flag không đưa vào config contract để tránh train → resume bị mismatch giả.
- Ghi config trước train thay vì chờ train xong; thư mục nonempty được bảo vệ dù artifacts chưa đủ.
- Không tự dùng metrics cache cũ khi model đổi: mỗi lần đánh giá sinh thư mục mới.
- Không sao chép CNN input/transform hay loop sang text task. Giữ cấu trúc phần mềm, thay đúng nội dung NLP.
- Test độc lập không dùng chọn checkpoint, làm theo nguyên tắc trong slide và sách.

## Nguồn lý thuyết liên quan

Chương 3: training loop, validation, TensorBoard, pretrained và fine-tuning.
Chương 4: optimizer, scheduler, regularization, clipping, Exercise 1/2 với Hugging Face.
Chương 6: sequence, encoding, padding/truncation; DistilBERT dùng Transformer, không phải RNN.
Sách Chollet §3.4/§4.2/§5.3/§6.1 củng cố phân loại nhị phân, đánh giá và biểu diễn văn bản.

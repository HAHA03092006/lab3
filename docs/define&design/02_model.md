# Đặc tả mô hình — model_builder.py

## 1. Hai checkpoint, hai mục đích

| Bài | Checkpoint | Có sẵn head sentiment? | Học trong bài? |
|---|---|---|---|
| Exercise 1 | distilbert-base-uncased-finetuned-sst-2-english | Có, SST-2 | Không |
| Exercise 2 | distilbert-base-uncased | Không có head IMDb đã học | Có, toàn bộ model |

DistilBERT nền đã pretrain ngôn ngữ; AutoModelForSequenceClassification thêm head hai lớp.
Cảnh báo weights classifier/pre_classifier mới khởi tạo là đúng trong Exercise 2, không đồng nghĩa encoder random.
Không dùng câu dự đoán mẫu làm dữ liệu huấn luyện hay bằng chứng chất lượng.

## 2. Luồng toán học

Text → tokenizer → token IDs + mask → Transformer encoder → biểu diễn đầu chuỗi → classification head → z∈R².
P(y=c|x)=exp(z_c)/Σ_j exp(z_j). Quyết định argmax(z), Positive=1.
Loss trên batch là cross-entropy giữa logits và nhãn; HF model tự tính khi nhận labels.
Không softmax logits trước khi đưa vào loss, tránh tính softmax hai lần.

## 3. API

- `load_tokenizer(model_id, revision)`: AutoTokenizer fast, cùng checkpoint/revision với model.
- `build_model(model_id, revision)`: AutoModelForSequenceClassification(num_labels=2), mapping hai chiều.
- `count_params(model)`: total/trainable/frozen; full fine-tuning yêu cầu frozen=0.
- `tokenizer_identity(tokenizer)`: tên, vocabulary hash, special tokens, padding/truncation side.

Input IDs/mask [B,L], labels [B]; output logits [B,2], loss scalar khi có labels.
Bài 1 dùng mapping có sẵn từ model.config; không suy ra tên nhãn từ vị trí tùy ý.

## 4. Save/load

Trainer.save_model + tokenizer.save_pretrained tạo best_model/.
Nạp bằng Auto classes từ đường dẫn local để tái lập tokenizer, casing, vocab và head.
Lưu weights dạng safetensors. Dùng eval() và inference_mode() khi suy luận.
Inference theo batch để tránh giữ toàn bộ tensor của dataset trên GPU; logits cuối đưa về CPU.

## 5. Giả định và giới hạn

Chọn tiếng Anh vì checkpoint và IMDb phù hợp. Không mặc định dùng với tiếng Việt.
Bài không xử lý neutral/multilabel. Không kết luận SST-2 vs IMDb là so sánh fair nếu dữ liệu test khác nhau.
main có thể đổi trên Hub; dùng commit SHA khi cần tái lập dài hạn.
Tests dùng model cực nhỏ khởi tạo random chỉ để kiểm tra API/loss/shape, tuyệt đối không thay thế pretrained experiment.

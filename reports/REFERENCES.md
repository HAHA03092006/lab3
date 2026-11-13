# Tài liệu tham khảo và nguồn thiết kế

1. TS. Nguyễn Thị Khánh Tiên, *Chapter 4 — Fine-tune Models and Training Algorithms*, trang 25: đề Practice 3. Trang 2–4: fine-tuning; 7–14: optimizer/scheduler; 20–23: regularization/clipping.
2. Cùng giảng viên, *Chapter 3 — Training Deep Neural Networks*: trang 3–14 training/validation/TensorBoard; trang 20–24 transfer learning và Practice 2.
3. Cùng giảng viên, *Chapter 6 — RNNs*: dữ liệu chuỗi, encoding, padding/truncation. DistilBERT trong Lab 3 là Transformer, không phải mô hình RNN trong chương này.
4. François Chollet (2018), *Deep Learning with Python*, §3.4 phân loại IMDb, §4.2 đánh giá, §5.3 pretrained/fine-tuning, §6.1 text embeddings. Dùng ý tưởng lý thuyết, không chép API Keras cũ vào PyTorch.
5. Nguyễn Thanh Tuấn (2020), *Deep Learning cơ bản*, bản 2, chương 11 transfer learning, 16–19 sequence/embedding/attention.
6. [Hugging Face — Text classification](https://huggingface.co/docs/transformers/tasks/sequence_classification): DistilBERT, IMDb, tokenizer, collator, Trainer.
7. [Hugging Face — Trainer](https://huggingface.co/docs/transformers/main_classes/trainer): TrainingArguments, checkpoint, best model, predict.
8. [IMDb dataset card](https://huggingface.co/datasets/stanfordnlp/imdb): nguồn dữ liệu và schema.
9. [DistilBERT SST-2 model card](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english): pretrained sentiment model Exercise 1.
10. [DistilBERT base](https://huggingface.co/distilbert/distilbert-base-uncased): encoder nền Exercise 2.

Ngày đối chiếu: 11/11/2026. API triển khai pin transformers 4.57.1, datasets 4.3.0, evaluate 0.4.6, accelerate 1.11.0;
không giả định tài liệu nhánh main luôn trùng API các phiên bản này. Integration tests kiểm tra API cài thực tế.
Tài liệu slide/sách do người học cung cấp để tham khảo; ZIP không phân phối lại các PDF gốc.

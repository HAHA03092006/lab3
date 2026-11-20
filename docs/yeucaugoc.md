# Thực hành 3 – Làm quen với Hugging Face

## Bài tập 1: Phân tích cảm xúc với Hugging Face

1. Cài đặt thư viện `transformers` của Hugging Face.
2. Sử dụng một mô hình phân tích cảm xúc đã được huấn luyện sẵn từ Hugging Face Hub.
3. Tokenize một câu mẫu.
4. Thực hiện phân tích cảm xúc trên câu đó.

### Tài liệu tham khảo

- https://huggingface.co/docs/transformers/en/training#fine-tune-a-pretrained-model
- https://huggingface.co/blog/sentiment-analysis-python
- https://www.kaggle.com/code/gauravduttakiit/sentiment-analysis-using-hugging-face
- https://www.kaggle.com/code/neerajmohan/fine-tuning-bert-for-text-classification

---

## Bài tập 2: Fine-tune mô hình pretrained cho bài toán phân loại văn bản nhị phân

Trong bài tập này, bạn sẽ:

1. Cài đặt các thư viện Hugging Face cần thiết (`transformers`, `datasets`, `evaluate`).
2. Tải một bộ dữ liệu đơn giản cho bài toán phân loại văn bản nhị phân.
3. Tải một mô hình pretrained và tokenizer của nó.
4. Tiền xử lý bộ dữ liệu cho phù hợp với mô hình.
5. Định nghĩa các tham số huấn luyện (training arguments).
6. Tạo đối tượng `Trainer` và fine-tune mô hình.
7. Đánh giá mô hình sau khi fine-tune.

---

*Ghi chú: các thuật ngữ kỹ thuật như tokenize, fine-tune, pretrained, `Trainer` được giữ nguyên để khớp với kịch bản thuyết trình và tài liệu của dự án.*

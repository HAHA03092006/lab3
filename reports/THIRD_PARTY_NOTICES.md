# Nguồn và giấy phép thành phần bên thứ ba

Model quick được fine-tune từ `distilbert/distilbert-base-uncased` (DistilBERT, Hugging Face, Apache-2.0).
Bản model đã thay đổi weights bằng huấn luyện IMDb; không phải checkpoint gốc và không phải sản phẩm được Hugging Face chứng nhận.
Bản Apache-2.0 kèm tại licenses/Apache-2.0.txt. Model card gốc: https://huggingface.co/distilbert/distilbert-base-uncased.

Exercise 1 tải checkpoint `distilbert/distilbert-base-uncased-finetuned-sst-2-english`, Apache-2.0,
không đóng gói lại weights Exercise 1. Model card: https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english.

IMDb do Stanford NLP cung cấp, dùng trong bối cảnh bài tập học thuật. Nguồn và điều kiện dữ liệu:
https://huggingface.co/datasets/stanfordnlp/imdb và https://ai.stanford.edu/~amaas/data/sentiment/.
Gói source không chứa toàn bộ dataset; outputs có các review dự đoán phục vụ phân tích thực nghiệm.

Các thư viện được cài từ requirements; giấy phép thư viện nằm trong distributions tương ứng.

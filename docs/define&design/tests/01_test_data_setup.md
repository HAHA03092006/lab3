# Kiểm thử data_setup

| Trường hợp | Dữ liệu vào | Kỳ vọng |
|---|---|---|
| Chia chuẩn | 100 nhãn, 50 mỗi lớp, val=20 | Train=80, val=20, mỗi lớp val=10 |
| Rời nhau | Chỉ mục train/val | Giao rỗng, hợp phủ đủ 100 |
| Tái lập | Cùng seed=42 | Cùng hai list chỉ mục |
| Đổi seed | Seed 43 | Chỉ mục đổi, số lượng lớp giữ |
| Đầu vào sai | Rỗng, thiếu lớp, nhãn 2, val quá nhỏ/lớn | ValueError |
| Clean | Not + br tag + entity | Giữ Not, dấu câu; bỏ tag/extra spaces |
| Tokenize | DatasetDict + tokenizer local | labels, input_ids, attention_mask; không text/sample_id |
| Giới hạn độ dài | max_length=32 | Mọi IDs length <= 32 |
| Manifest | Hai lần cùng dữ liệu | Cùng JSON nội dung |

Test dùng Dataset local, không gọi load_dataset trên mạng. Mẫu thật được kiểm tra bởi notebook.

# Ma trận truy vết đề bài → code → kiểm chứng

| Bước slide | Nội dung | Hiện thực | Bằng chứng khi chạy |
|---|---|---|---|
| E1.1 | Install transformers | requirements, notebook §0 | Phiên bản in trong environment |
| E1.2 | Pretrained sentiment model | notebook §1 | Checkpoint ID và revision |
| E1.3 | Tokenize sentence | AutoTokenizer | Bảng token/ID/mask |
| E1.4 | Sentiment analysis | predict_texts, pipeline | predictions.json |
| E2.1 | Install transformers/datasets/evaluate | requirements | environment_info |
| E2.2 | Load binary dataset | load_imdb | Split sizes và labels |
| E2.3 | Load model/tokenizer | build_model, load_tokenizer | Model params/config |
| E2.4 | Preprocess dataset | clean/tokenize + collator | Batch shapes, manifest |
| E2.5 | Training arguments | make_training_args | Preview args, config.json |
| E2.6 | Trainer fine-tune | run_experiment | Loss history/checkpoints |
| E2.7 | Evaluate finetuned model | Trainer.predict + export_evaluation | Metrics/CM/report |

Phần bổ sung phục vụ tái sử dụng: resume/reuse, TensorBoard, test module, save/load, error analysis.
`evaluate` được cài theo đề; sklearn tính metrics để tests không cần tải metric scripts.
Không có yêu cầu bắt buộc phải dùng BERT đầy đủ hoặc dataset tiếng Việt trong slide này.

# ĐẶC TẢ MÔ HÌNH — DISTILBERT SENTIMENT ANALYSIS

| Thuộc tính | Thông tin |
|---|---|
| Mã tài liệu | LAB3-MODEL-02 |
| Tên | Đặc tả kiến trúc, input/output, khởi tạo, huấn luyện và lưu/nạp mô hình |
| Phiên bản tài liệu | 2.0 (bổ sung đặc tả, không thay đổi thuật toán) |
| Ngày tạo tài liệu trong bản gốc | 11/11/2026 theo metadata dự án |
| Ngày cập nhật đặc tả | 11/11/2026 |
| Người phụ trách | Nhóm thực hiện Lab 3 — chưa phân công cá nhân |
| Mã nguồn tham chiếu | `../../going_modular/model_builder.py`, `config.py`, `engine.py`, `evaluate.py` |
| Test tham chiếu | `../../tests/test_model_builder.py`, `test_engine.py`, `test_evaluate.py` |
| Trạng thái | Đặc tả dựa trên code/outputs hiện có; không xác nhận đã chạy thử lại |

> **Phân biệt ngày:** Ngày cập nhật tài liệu ở trên không phải ngày xuất bản hoặc cập nhật checkpoint trên Hugging Face Hub. Các model ID đang dùng `revision='main'`; muốn ghi ngày/phiên bản weights chính xác cần tra commit SHA đã được giải quyết trong artifact của một run cụ thể.

## 1. Mục tiêu mô hình và hai bài thực hành

**Bài toán:** Phân loại nhị phân cảm xúc của một review tiếng Anh, `0 = NEGATIVE`, `1 = POSITIVE`. Dự đoán là nhãn theo argmax từ 2 logits. Không có nhãn Neutral. Cấu trúc dự án có hai luồng riêng, tránh hiểu nhầm đã huấn luyện ở Exercise 1.

| Thuộc tính | Exercise 1 — suy luận pretrained | Exercise 2 — fine-tuning IMDb |
|---|---|---|
| Model ID trong code | `distilbert/distilbert-base-uncased-finetuned-sst-2-english` | `distilbert/distilbert-base-uncased` |
| Vai trò | Mô hình sentiment đã fine-tune trên SST-2 | Encoder ngôn ngữ pretrained, **classifier hai lớp mới** |
| Dữ liệu học ở Lab 3 | Không huấn luyện | IMDb train/validation sau chia |
| Nguồn logits | Classification head pretrained từ SST-2 | Classification head được cập nhật trên IMDb |
| Entry point | Notebook §1, `AutoModelForSequenceClassification`, `pipeline` | `model_builder.build_model`, `engine.run_experiment` |
| Đầu ra | Câu mẫu + sentiment/probability tại `predictions.json` | Best model, history, test metrics, predicted labels |
| Mục tiêu kiểm tra | Cách dùng AutoTokenizer/AutoModel và pipeline | Chạy được transfer learning trên downstream dataset |

*Không dùng checkpoint SST-2 thay cho base ở Exercise 2; không dùng ví dụ dự đoán ở bài 1 làm bằng chứng accuracy của IMDb.*

## 2. Danh tính và cấu hình phiên bản

- `SENTIMENT_MODEL`, `BASE_MODEL`, `ID2LABEL` được định nghĩa tại `going_modular/config.py`.
- `RunConfig.model_id` mặc định là `BASE_MODEL`; `model_revision='main'` và `dataset_revision='main'`. `main` là tham chiếu động, không phải số phiên bản bất biến.
- `model_builder.load_tokenizer(model_id, revision)` và `build_model(model_id, revision)` phải sử dụng cùng ID/revision theo mục đích bài thực hành.
- Khi khởi tạo run thật, `engine.py` ghi `resolved_model_revision = getattr(model.config, '_commit_hash', None)` vào `config.json` (có thể `None` tùy nguồn weights), cùng metadata môi trường.
- Phục vụ reproducibility dài hạn: ghi/checkpoint commit SHA của model và dataset khi có thể; đừng tự đặt ngày update Hub hay revision không xuất hiện trong artifacts.

## 3. Kiến trúc DistilBERT và classifier

DistilBERT-base là kiến trúc Transformer encoder dạng distilled, chỉ dùng **phần encoder**, không có decoder sinh văn bản. Mô hình mặc định DistilBERT-base có 6 Transformer layers, hidden size 768, 12 attention heads, feed-forward intermediate size 3072, vocab size 30522 và giới hạn 512 positional embeddings. Các đặc tính này mô tả kiến trúc chuẩn của checkpoint base; **không áp dụng cho tiny model trong pytest**.

**Pipeline khối:**

```text
Văn bản review tiếng Anh
  → clean_text() tối thiểu (Exercise 2)
  → AutoTokenizer (WordPiece, uncased)
  → input_ids[B,L] + attention_mask[B,L]
  → token embedding + positional embedding
  → 6 DistilBERT Transformer encoder blocks
  → vector biểu diễn vị trí đầu chuỗi (hidden state đầu tiên)
  → pre_classifier → ReLU → dropout → classifier (2 logits)
  → softmax (khi suy luận) / cross-entropy (khi train có labels)
  → predicted label 0 hoặc 1
```

**Các lớp/head:** `AutoModelForSequenceClassification` chọn `DistilBertForSequenceClassification` phù hợp từ config. Phần encoder tải trọng số pretrained. Với model base của Exercise 2, classifier head khởi tạo mới; cảnh báo về weights classifier mới là hành vi dự kiến, không có nghĩa toàn bộ DistilBERT khởi tạo random. Trong cấu hình hiện tại không freeze backbone, vì vậy tham số trainable được kiểm tra bằng `count_params(model)`; không gán số lượng tham số cứng nếu chưa đọc từ model thực tế sau khởi tạo.

**Khác biệt với synthetic test:** `tests/conftest.py` tạo DistilBERT nhỏ (`n_layers=1, dim=16, hidden_dim=32, n_heads=2, max_position_embeddings=64`, vocab local 13 token), lưu để Auto classes đọc offline. Mục đích: assert API/shape/optimizer/checkpoint; nó không có năng lực hiểu ngữ nghĩa như base pretrained.

## 4. Đặc tả dữ liệu đầu vào

### 4.1 Input từ người dùng / dataset

| Trường | Kiểu và miền | Nguồn | Quy tắc |
|---|---|---|---|
| `text` | Chuỗi UTF-8 tiếng Anh, không rỗng trong usage bình thường | Review IMDb hoặc câu thử | Giữ thứ tự và phủ định; `clean_text()` chuẩn hóa `<br>`/HTML entities/spaces cho Exercise 2 |
| `label` / `labels` | Integer thuộc {0,1} | IMDb / DatasetDict tokenized | 0 Negative, 1 Positive; raw dùng `label`, sau tokenize đổi thành `labels` |
| `sample_id` | Chuỗi `train:<row>` hoặc `test:<row>` | `prepare_raw_splits` | Chỉ để đối chiếu và export; bỏ khỏi tensor đưa vào model |
| `max_length` | Số nguyên 8–512 theo `RunConfig` | quick=128, full=256 | Truncation nếu văn bản dài; không vượt giới hạn DistilBERT |

### 4.2 Input Tensor và batch

| Tensor | Kích thước | Dtype kỳ vọng | Ý nghĩa |
|---|---|---|---|
| `input_ids` | `[B,L]` | integer / torch.long | ID subword theo vocabulary tokenizer |
| `attention_mask` | `[B,L]` | integer / torch.long | 1 là token hữu ích, 0 là padding |
| `labels` | `[B]` | integer / torch.long | Nhãn nhị phân cho cross-entropy, chỉ cần khi training/evaluation |

`B` là batch size thực (batch cuối có thể nhỏ hơn); `L <= max_length`, thay đổi theo batch do **dynamic padding** bằng `DataCollatorWithPadding`. Trong `tokenize_splits`, `padding=False`; không dùng padding cố định `max_length` ở bước map. Những trường hợp model không được cung cấp `labels` vẫn trả logits nhưng không có supervised loss. Special tokens như `[CLS]`/`[SEP]` được tokenizer thêm theo quy tắc của checkpoint.

### 4.3 Điều kiện và failure modes

- Tokenizer đúng checkpoint/revision, vocabulary/hash ổn định trong cùng run. Lệch vocab khiến IDs không còn tương ứng weights embedding.
- `max_length` quá nhỏ có thể làm mất ngữ cảnh; văn bản dài bị cắt (không tự nối sliding windows).
- Đầu vào không hợp lệ hoặc thiếu cột dataset gây exception từ tokenizer/datasets, không được mô tả như một output thành công.
- Dữ liệu nhãn ngoài 0/1 sẽ bị kiểm tra ở split và metrics; không giả định toàn pipeline tự xử lý nhãn đa lớp.

## 5. Đặc tả đầu ra

| Output | Kích thước/kiểu | Khi nào có | Cách dùng |
|---|---|---|---|
| `logits` | Float tensor `[B,2]` | Forward pass | Điểm thô cho Negative (cột 0), Positive (cột 1) |
| `loss` | Float scalar tensor | Khi truyền `labels` | Supervised cross-entropy trong Trainer |
| `probabilities` | Float `[B,2]`, tổng theo hàng xấp xỉ 1 | Inference sau softmax | So sánh confidence, xuất `p_positive` |
| `predicted_label_id` | Integer 0 hoặc 1 | `argmax(logits, axis=-1)` | Nhãn nhị phân |
| `label` | Chuỗi `NEGATIVE`/`POSITIVE` | `predict_texts` | Đọc từ `model.config.id2label` |
| `confidence` | Float trong [0,1] | `predict_texts` | Xác suất softmax tại lớp được chọn; không phải xác suất hiệu chuẩn |
| `p_positive` | Float trong [0,1] | `predict_texts` | Xác suất lớp 1, dùng ROC-AUC/report |

**Quy tắc toán học:** với logits `z=(z0,z1)`, xác suất `p_c = exp(z_c)/sum_j exp(z_j)`. Để tránh overflow khi xuất metrics, `evaluate.export_evaluation` tính `z' = z - max(z)` trước `exp`. Nhãn dự đoán `argmax(z)`. Loss là cross-entropy trên logits thô và nhãn đúng: không áp dụng softmax trước khi đưa logits cho model loss.

**Output ở mức artifact:** Exercise 1 lưu `predictions.json`; Exercise 2 sau train có `best_model/` và history/completed trong `artifacts/<run_id>/`, output test có `test_metrics.json`, `predictions.csv`, `errors.csv`, `confusion_matrix.png`, `history.png`, `new_review_predictions.json`, `REPORT.md`. Không phải mọi artifact weights đều nằm trong ZIP nộp.

## 6. Quy trình khởi tạo, training và inference

1. `load_imdb` nạp raw train/test; `prepare_raw_splits` tách validation từ train; giữ raw_test.
2. `load_tokenizer(BASE_MODEL, revision)` tải tokenizer cùng encoder nền.
3. `tokenize_splits` map text sang IDs, mask, labels; dùng batch collator để padding.
4. `build_model(BASE_MODEL, revision)` trả classification model có head hai nhãn; full fine-tuning không freeze.
5. `make_training_args` cấu hình optimizer/scheduler, validation/checkpoint theo epoch, metric chọn best là `f1`.
6. `Trainer.train` cập nhật model bằng loss; sau khi đủ epoch, lưu best model + tokenizer và markers.
7. `Trainer.predict(tokenized['test'])` sau khi chốt model; `export_evaluation` đối chiếu nhãn trước khi lưu.
8. Nạp lại từ `best_model/` và so sánh xác suất trước/sau trong sai số số học (notebook sử dụng atol=1e-6).

**Đường đi `train`/`resume`/`reuse`:** `train` yêu cầu run rỗng; `resume` yêu cầu contract và checkpoint chưa hoàn tất; `reuse` yêu cầu artifacts hoàn thành và best weights. Không biến một run quick thành full bằng cách đổi tên/đổi profile trên checkpoint cũ. Xem `03_engine.md`.

## 7. Cấu hình huấn luyện thực tế (từ `RunConfig` và `make_training_args`)

| Thuộc tính | Quick (mặc định) | Full (`for_profile('full')`) | Nguồn |
|---|---:|---:|---|
| Seed | 42 | 42 | RunConfig |
| Train / Val / Test | 2.000 / 500 / 1.000 | 20.000 / 5.000 / 25.000 | val_size=5000, subset limits |
| max_length | 128 | 256 | RunConfig |
| epochs | 2 | 3 | RunConfig |
| train batch | 16 | 16 | RunConfig |
| eval batch | 32 | 32 | RunConfig |
| learning rate | 2e-5 | 2e-5 | RunConfig |
| weight_decay | 0.01 | 0.01 | RunConfig |
| warmup_ratio | 0.1 | 0.1 | RunConfig |
| optimizer / scheduler | AdamW / linear | AdamW / linear | engine.make_training_args |
| eval/save strategy | mỗi epoch | mỗi epoch | engine.make_training_args |
| best model criterion | validation `f1` Positive | validation `f1` Positive | Trainer |
| gradient accumulation | 1 | 1 | RunConfig |
| gradient clipping | 1.0 | 1.0 | RunConfig |

`TrainingArguments` còn có `logging_steps=10`, `save_total_limit=2`, `load_best_model_at_end=True`, `report_to=['tensorboard']`, `fp16=False`, `bf16=False`. Trong báo cáo phải ghi cấu hình đã chạy thay vì xem preset là kết quả thực nghiệm.

## 8. Kiểm thử và bằng chứng xác thực

| Yêu cầu model | Test hiện hữu | Điểm kiểm tra |
|---|---|---|
| Mô hình local build được | `test_logits_loss_and_all_trainable` | `AutoModel...from_pretrained`, logits `(2,2)`, loss scalar |
| Không freeze tham số ở tiny fixture | `test_logits_loss_and_all_trainable` | `count_params()['frozen']==0` |
| Tokenization/schema batch | `test_tokenization_and_identity` | IDs/mask/labels, max_length |
| Save/reuse sau fine-tune | `test_real_trainer_resume_reuse_roundtrip` | Cùng xác suất `p_positive` trong atol=1e-7 |
| Phép đo từ logits | `test_hand_calculated_metrics` và bạn cùng file | Accuracy/F1/precision/recall, lỗi đầu vào |
| Notebook hợp lệ | `test_notebook_schema_and_python_cells` | nbformat + AST, **không thực thi inference** |

**Đề xuất bổ sung (chưa có test Python tương ứng):** test tokenizer/model revision mismatch; bài toán batch dài/rỗng; xác minh `id2label` ở model thật; so sánh CPU/GPU trong dung sai; pin SHA và kiểm tra drift revision. Đánh dấu rõ là *đề xuất*, không nhập vào báo cáo passed.

**Bằng chứng chạy lịch sử trong ZIP:** `reports/pytest_output.txt` ghi 24 passed (trong môi trường gốc); `reports/VALIDATION.md` xác nhận quick 1.000 test và accuracy 0.862. Đây không phải bằng chứng vừa chạy lại khi chỉnh tài liệu. Package ZIP hiện tại không chứa trọng số `best_model/model.safetensors`; muốn reuse thật cần cung cấp artifacts weights riêng hoặc chạy training theo notebook.

## 9. Ràng buộc, giới hạn và mở rộng

- Fine-tuning minh họa tiếng Anh; không khẳng định hoạt động tốt với tiếng Việt hoặc review ngoài miền IMDb.
- Quick chỉ là sample nhỏ, một seed, không phải full benchmark và không đủ chứng minh ưu thế thống kê.
- Softmax confidence không được calibration; ví dụ mỉa mai/phủ định/nhận xét pha trộn có thể gây lỗi.
- Không cung cấp threshold tuning, Neutral/multilabel, streaming text, deployment, LoRA/PEFT.
- Không dùng test set để chọn epoch/LR hoặc thay đổi tokenizer sau khi xem kết quả test.
- Model revision là `main`; muốn tái lập chính xác cần fixed commit SHA và version dependencies/dataset.

## 10. Liên kết triển khai

- Kế hoạch liên quan: [`../plans/phase2.md`](../plans/phase2.md) (tokenizer/model), [`phase3.md`](../plans/phase3.md) (Trainer), [`phase4.md`](../plans/phase4.md) (persist), [`phase5.md`](../plans/phase5.md) (evaluate).
- Đặc tả data `01_data.md`; engine `03_engine.md`; kết quả `05_evaluation_results.md`.
- Đặc tả test `tests/02_test_model_builder.md` và `tests/03_test_engine.md`; traceability `../analysts/requirements_traceability.md`.

## 11. Quyết định chọn hai checkpoint (v3.0)

**ADR-M01 – Hai checkpoint cho hai mục đích:** SST-2 đã fine-tuned phù hợp Exercise 1; DistilBERT-base pretrained chưa có head IMDb phù hợp Exercise 2. **Không** thay thế bằng cùng một model nếu mục tiêu giảng dạy là phân biệt dùng model có sẵn và tự fine-tune. Consequence: khi trình bày score, nêu domain/dataset khác, không so trực tiếp.

**ADR-M02 – `AutoModelForSequenceClassification` và label mapping cố định:** cho phép model class theo config; `num_labels=2`, `ID2LABEL={0:'NEGATIVE',1:'POSITIVE'}`. Contract bắt buộc logits `[B,2]` và scalar loss khi input có nhãn. `MODEL-01` chứng minh shape/loss với tiny config, không đo chất lượng pretrained.

**ADR-M03 – full fine-tuning (không đóng băng encoder):** training tất cả tham số làm mô hình có thể thích nghi domain IMDb nhưng tăng chi phí so head-only. Quick run reference có 66.955.010 trainable parameters, không có lớp frozen theo summary. Không tuyên bố freeze trong bài.

## 12. Kiểm toán tensor và những lỗi dễ gặp

| Điểm vào | Tensor shape minh họa | Lỗi nếu sai |
|---|---|---|
| Raw review | `list[str]` length N | Đưa thẳng str vào model thay vì tokenizer |
| Tokenizer | input_ids/attention_mask `[B,L]` | tokenizer lệch vocab/checkpoint làm ID sai ý nghĩa |
| Labels | `[B]`, 0/1 | num_labels không khớp, loss invalid |
| Encoder | hidden states theo mỗi token | sequence vượt max_length, OOM |
| Classifier | logits `[B,2]` | nhầm logits với xác suất |
| `predict_texts` | records text,label_id,label,confidence,p_positive | `max_length` không được dùng giống training dẫn tới khác phân phối |

`L` không cố định giữa batch do dynamic padding; trong test `B=2` có logits `(2,2)`. `max_length` tính cả special tokens. Khi cần xem padding mask đúng phải dựa vào batch thật, không suy rằng mọi mask có các số 0.

## 13. Phạm vi kiểm chứng model

- **Có trong code:** load pretrained checkpoint, model builder với id2label, count_params, tokenizer fingerprint; no frozen params mặc định.
- **Có test offline:** MODEL-01 cho input hợp lệ, logits `(2,2)`, scalar loss, frozen=0. Tiny model random có thể forward ngay nhưng không hiểu review thật.
- **Có output lịch sử:** Exercise 1 predictions và quick best validation/test summary trong outputs/reference run; notebook executed.
- **Thiếu trong ZIP:** weights best_model để người đọc tải lại mà không chạy. Trước buổi bảo vệ nên kiểm máy demo có cache hoặc checkpoint riêng, không dựa vào docs để nói “load được” nếu chưa chuẩn bị.
- **Test đề xuất:** mismatch tokenizer vocab; bất biến `id2label`; invalid labels; inference equivalence CPU/GPU trong dung sai; cấu hình `full`; latency/memory; tham số head/backbone.

## 14. So sánh lựa chọn và bài học

| Phương án | Ưu điểm | Nhược điểm | Quyết định |
|---|---|---|---|
| Pretrained SST-2 inference | Thực hành nhanh, minh họa pipeline | Không train, domain khác IMDb | Dùng Exercise 1 |
| Base pretrained + full fine-tune | Bám đúng mục tiêu chuyển giao/Trainer | Tốn CPU/RAM/checkpoint | Dùng Exercise 2 |
| Train random toàn bộ | Không cần pretrained weights | Không đúng tinh thần bài và chậm hơn | Không dùng |
| Head-only frozen encoder | Nhẹ hơn | Không phải luồng hiện tại; có thể kém hơn | Chỉ là thí nghiệm tương lai |
| `max_length` rất lớn | Giữ nhiều text | Chi phí attention tăng, OOM | Quick=128, full=256; cần validation để thay |

Để trình bày lý thuyết về self-attention, loss, distillation, xem [theory](../theory/00_theoretical_foundations.md). Ma trận mã: FR02/FR03/FR04/FR13.

# CƠ SỞ LÝ THUYẾT CỦA LAB 3 — TỪ NLP ĐẾN FINE-TUNING DISTILBERT

> **LAB3-THEORY-01 · v3.0, 13/11/2026**. Mục tiêu: giải thích bằng ngôn ngữ có thể thuyết trình được **vì sao** từng bước trong code tồn tại. Nội dung lý thuyết là kiến thức nền; các thông số của **run thực** lấy từ `going_modular/config.py` và artifacts, không phải những con số minh họa dưới đây.

## 1. Bài toán NLP: từ văn bản sang phân loại nhị phân

Input là review tiếng Anh độ dài thay đổi. Output là nhãn thuộc `0 = NEGATIVE`, `1 = POSITIVE`, kèm score cho hai lớp. Đây là **sequence classification**, không phải gán nhãn từng token hoặc sinh văn bản. Mô hình phải tổng hợp ngữ cảnh toàn câu/review trước khi đưa ra hai logits. Chẳng hạn “not bad” có từ “bad” nhưng ngữ nghĩa tổng thể thường tích cực; bag-of-words có thể bỏ qua tương tác, trong khi contextual encoder biểu diễn token dựa vào toàn chuỗi.

Điểm cần trình bày: classification 2 lớp **không** hỗ trợ neutral; khen/chê pha trộn có thể gây bất định. Dataset gán nhãn nhị phân; mô hình không có trách nhiệm suy luận mục đích người viết ngoài nhãn đã học.

## 2. Representation learning, pretrained model, fine-tuning

- **Pretraining:** mô hình học biểu diễn ngôn ngữ từ nguồn dữ liệu lớn trước bài toán đích. Các tham số encoder đã học cấu trúc/ngữ nghĩa thống kê trong ngôn ngữ.
- **Downstream fine-tuning:** bổ sung head phân loại và cập nhật (một phần/toàn bộ) trọng số theo nhãn IMDb với learning rate nhỏ; tận dụng prior từ pretrained.
- **Inference:** chạy forward với weights cố định (`eval()`, `inference_mode()`) để suy ra logits/score, không có backward hay optimizer.
- **Hai thí nghiệm trong Lab 3:** E1 load **mô hình đã fine-tune SST-2** và infer ngay; E2 load **DistilBERT base**, khởi tạo head hai lớp mới, sau đó train trên IMDb bằng `Trainer`. Số epochs thuộc E2, không áp vào E1.

Vì sao không train random từ đầu? Tập dữ liệu của một bài lab và tài nguyên máy thường không đủ để học các biểu diễn ngôn ngữ mạnh từ số 0. Pretraining chuyển tri thức đã học sang bài toán mới. Tuy nhiên pretrained cũng mang thiên lệch và không tự bảo đảm tốt ở ngôn ngữ/domain khác.

## 3. Tokenization, subword và các tensor

Bộ tokenizer DistilBERT-base-uncased xử lý văn bản tiếng Anh theo mô hình subword WordPiece. `AutoTokenizer` ánh xạ text → chuỗi token → vocabulary IDs. Một từ có thể tách thành nhiều subword; số token không bằng số từ. Các token đặc biệt giúp encoder xác định biên chuỗi (ví dụ `[CLS]`, `[SEP]`). `input_ids[B,L]` là **chỉ số rời rạc**, không phải số liên tục cần normalize như pixel. `attention_mask[B,L]` có 1 cho token thật và 0 cho token padding.

**Ví dụ khái niệm:** review ngắn có 6 token, review dài có 11 token. Khi padding theo batch, cả hai thành chiều dài 11, mask của chuỗi đầu có 5 số 0 ở cuối. `DataCollatorWithPadding` đệm theo độ dài lớn nhất của batch hiện tại, thay vì luôn đến 128/256; giúp bớt tính toán trên padding. `truncation=True` cắt các token vượt max_length, vì thế có thể làm mất kết luận ở cuối review.

**Quyết định data preprocessing của code:** thay `<br>` bằng khoảng trắng, giải mã HTML entities, gom khoảng trắng; không stopword removal/stemming, không bỏ phủ định hoặc dấu câu. Với self-attention, thông tin thứ tự/ngữ cảnh/negation là quan trọng; tiền xử lý quá mức có thể hại sentiment.

## 4. Transformer encoder, attention và bối cảnh

Transformer encoder gồm các khối self-attention và feed-forward. Với biểu diễn token đầu vào `X`, các ma trận học được tạo `Q=XW_Q`, `K=XW_K`, `V=XW_V`. Attention một head có dạng:

$$
\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V
$$

Trong đó `M` che các vị trí padding (về mặt tính toán thường thêm giá trị âm lớn). `QKᵀ` đo mức liên hệ giữa từng vị trí; chia `sqrt(d_k)` để tránh các logit attention quá lớn khi dimension tăng; softmax chuẩn hóa trọng số. Multi-head attention cho phép nhiều không gian tương tác khác nhau, sau đó nối/cộng tuyến tính các kết quả. Residual connections và normalization giúp huấn luyện sâu ổn định hơn; feed-forward biến đổi phi tuyến cho từng vị trí.

**Vì sao encoder phù hợp classification?** Mỗi biểu diễn token sau các block đã có ngữ cảnh hai chiều. DistilBERT classification head dùng biểu diễn ở vị trí token đầu tiên, đưa qua `pre_classifier → ReLU → dropout → classifier` thành 2 logits. Khối này không sinh chuỗi văn bản từng bước như autoregressive decoder.

## 5. DistilBERT và kiến trúc thực của bài

DistilBERT là biến thể rút gọn từ BERT bằng knowledge distillation; bản base dùng trong Lab 3 có **6 Transformer layers, hidden size 768, 12 attention heads, feed-forward intermediate 3072** và maximum positional embeddings 512. Mục tiêu distillation là giữ phần lớn khả năng biểu diễn của teacher với mô hình nhỏ hơn để giảm chi phí huấn luyện/inference. Không đồng nhất DistilBERT với kiến trúc 6 layer do sinh viên tự huấn luyện từ đầu.

Trong `config.py`:

```python
SENTIMENT_MODEL = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'
BASE_MODEL = 'distilbert/distilbert-base-uncased'
ID2LABEL = {0: 'NEGATIVE', 1: 'POSITIVE'}
```

`model_builder.build_model()` gọi `AutoModelForSequenceClassification.from_pretrained(...num_labels=2)`. Encoder lấy weights pretrained; head dùng cho downstream IMDb được khởi tạo theo cấu hình classification. Số tham số của **run quick được lưu** trong `reports/reference_run/config.json` là total=66,955,010, trainable=66,955,010, frozen=0. Đây là số từ run đã lưu, **không** phải số của tiny fixture.

Tiny offline fixture có `n_layers=1`, `dim=16`, `hidden_dim=32`, `n_heads=2`, vocab local 13 tokens; khác hẳn pretrained base. Mục tiêu tiny là xác minh shape/contract/resume chứ không đánh giá ngữ nghĩa.

## 6. Logits, softmax, nhãn và loss

Model trả hai **logits** `z0` và `z1` (chưa phải xác suất). Với nhãn lớp `k`, xác suất softmax là:

$$
p_k=\frac{e^{z_k}}{e^{z_0}+e^{z_1}}, \quad \hat y=\arg\max_k z_k
$$

Việc lấy argmax trực tiếp trên logits cho cùng nhãn với argmax softmax vì softmax đơn điệu theo từng logit. Để tránh tràn số, khi tự tính softmax nên trừ logit lớn nhất trước khi `exp`, giống cách `export_evaluation` đang làm.

Với mẫu có nhãn thật `y`, cross entropy:

$$
\mathcal{L}(z,y)=-\log p_y
$$

Loss trung bình trên batch là mục tiêu tối ưu của Trainer; giảm train loss không bảo đảm test accuracy tăng vì có thể overfit. `predict_texts` gọi `model.eval()` và `torch.inference_mode()`, còn `Trainer` tự điều phối chế độ train/eval.

**Nhầm lẫn hay gặp khi báo cáo:** confidence lấy từ `max(softmax(logits))` không phải xác suất đúng được hiệu chuẩn. Một mô hình có thể rất tự tin và sai, ví dụ review pha trộn trong error analysis.

## 7. Quy trình gradient và optimizer

Một optimizer step đi qua: forward → compute loss → backward → gradient (có thể tích lũy nhiều micro-batches) → clipping gradient norm → AdamW update → scheduler update LR. Trong code, `Trainer` làm việc này thay cho vòng lặp `loss.backward()` viết tay.

- `learning_rate=2e-5`: bước cập nhật nhỏ, phù hợp fine-tuning weights pretrained; **không phải** hằng số tốt nhất cho mọi dataset.
- `weight_decay=0.01`: regularization theo kiểu AdamW decoupled weight decay; khác việc cộng L2 vô điều kiện trực tiếp vào loss.
- `warmup_ratio=0.1`: LR tăng từ mức đầu đến target trong giai đoạn đầu (theo scheduler), rồi `linear` giảm dần.
- `max_grad_norm=1.0`: gradient clipping giảm nguy cơ gradient quá lớn.
- `gradient_accumulation_steps=1`: mỗi micro-batch tiến hành 1 optimizer step; khi >1, effective global batch liên quan số thiết bị và accumulation.

**Số bước ước lượng:** với train=2.000, batch 16, 1 thiết bị và accumulation=1, mỗi epoch khoảng `ceil(2000/16)=125` optimizer steps; hai epochs ≈250 steps, **phù hợp** completed marker run quick. Nếu huấn luyện có phân tán/độ dài drop_last khác thì công thức có thể thay đổi.

## 8. Train/validation/test và data leakage

| Split | Dùng để làm gì | Không được dùng để làm gì |
|---|---|---|
| Train | cập nhật parameters bằng gradient | không dùng như metric cuối độc lập |
| Validation | quan sát chất lượng, chọn best checkpoint/F1, quyết định siêu tham số | không gọi là test độc lập |
| Test | ước lượng cuối sau khi lựa chọn model | không dùng để thử đi thử lại LR/max_length rồi chọn tốt nhất |

`prepare_raw_splits` tạo validation từ IMDb train bằng `train_test_split(...stratify=labels,random_state=seed)`. `select_subset` tiếp tục lấy quick subset phân tầng; không lấy N dòng đầu (vì dữ liệu có thể sắp theo nhãn). Dataset sử dụng `sample_id` để truy vết từng dòng, và `split_manifest` lưu SHA-256 cho nội dung/nhãn. Khi đổi seed hoặc nội dung, manifest thay đổi, giúp phát hiện lệch contract. Nếu hai review trùng hệt ở hai splits, exact-text overlap có thể cảnh báo; nhưng paraphrase/gần trùng đòi công cụ khác.

## 9. Model selection, checkpoint và validation metric

`TrainingArguments` dùng `eval_strategy='epoch'`, `save_strategy='epoch'`, `load_best_model_at_end=True`, `metric_for_best_model='f1'`, `greater_is_better=True`. Có nghĩa: cuối mỗi epoch kiểm validation và save checkpoint; sau train Trainer nạp weights tốt nhất theo **validation F1 Positive** (không phải test F1). `save_total_limit=2` giới hạn số checkpoint giữ lại, cần thận trọng khi resume nếu thiếu optimizer/scheduler states.

Test được predict **sau** model selection trong notebook; các kết quả của test không dùng để chọn checkpoint trong code hiện tại. `reports/reference_run/completed.json` ghi best_metric của run quick (0.862823 theo báo cáo), tách biệt với test F1=0.860887.

## 10. Phương pháp đánh giá: accuracy, precision, recall, F1

Với Positive là lớp 1:

- **TP:** thật Positive, đoán Positive; **TN:** thật Negative, đoán Negative.
- **FP:** thật Negative, đoán Positive; **FN:** thật Positive, đoán Negative.
- **Accuracy**=`(TP+TN)/(TP+TN+FP+FN)`.
- **Precision Positive**=`TP/(TP+FP)` (có thể quy ước 0 khi mẫu số 0).
- **Recall Positive**=`TP/(TP+FN)`.
- **F1 Positive**=`2·Precision·Recall/(Precision+Recall)` khi có mẫu số khác 0.
- **Macro F1**: tính F1 cho mỗi lớp rồi lấy trung bình không trọng số theo lớp.

Dùng confusion matrix của quick: `[[435,65],[73,427]]` (hàng nhãn thật Negative/Positive; cột dự đoán Negative/Positive). Vậy `TN=435, FP=65, FN=73, TP=427`. Accuracy=`(435+427)/1000=0.862`. Precision Positive=`427/(427+65)=0.867886`; recall=`427/(427+73)=0.854`; F1≈0.860887. Có thể kiểm toán metric JSON bằng phép tính này khi báo cáo.

**Vì sao không chỉ accuracy?** Khi phân bố lớp lệch, đoán lớp đa số có thể accuracy cao nhưng bỏ sót lớp Positive. Precision/recall/F1 tách các kiểu lỗi. Dù quick có phân bố cân bằng, vẫn nên báo các chỉ số cho mục tiêu giảng dạy.

## 11. ROC-AUC và các chỉ số liên tục

ROC mô tả trade-off True Positive Rate vs False Positive Rate khi quét threshold. **ROC-AUC** đo khả năng xếp hạng score positive giữa hai lớp trên tập đánh giá; code dùng xác suất `probs[:,1]` thay vì nhãn argmax (đúng mục đích). AUC chỉ được tính khi test có cả hai lớp; code trả `None` nếu thiếu một lớp. Quick ROC-AUC=0.931748 từ `test_metrics.json`. AUC không chứng minh xác suất đã hiệu chuẩn; muốn đo calibration cần reliability diagrams/Brier score trên tập hợp lệ.

## 12. Error analysis: FP, FN, review dài, phủ định

`export_evaluation` sắp `errors.csv` theo confidence giảm dần và giữ tối đa 20 lỗi. Báo cáo lịch sử ghi 138/1000 review bị đoán sai: 65 FP, 73 FN. Error analysis minh họa hai review confidence cao nhưng sai, trong đó có review dài hơn max_length và review có khen/chê pha trộn. **Đây là giả thuyết nguyên nhân**, không phải kết luận nhân quả. Cần xây thí nghiệm trên validation để kiểm chứng việc tăng max_length hoặc chọn đoạn khác; không dùng test để tuning.

Phân loại lỗi có thể dùng khi thảo luận: negation, contrast (“great acting but...”), sarcasm, domain-specific words, text dài bị cắt, gán nhãn chủ quan. Không nên sao chép nguyên văn review có dữ liệu riêng tư vào slide nếu không cần.

## 13. Reproducibility, revision và hash

Seed kiểm soát nhiều thành phần stochastic nhưng không hứa chạy trên CPU và GPU hoặc khác phiên bản sẽ thu đúng các bit giống nhau. `RunConfig` là dataclass frozen; `config.json` ghi thông tin môi trường, SHA manifest, tokenizer fingerprint; run reference ghi model resolved SHA `12040acc...`. `model_revision='main'`/`dataset_revision='main'` là **địa chỉ di động**, do đó nếu tái lập nghiêm ngặt thì pin commit SHA của cả checkpoint và dataset cùng version các thư viện. JSON `save_json` dùng temporary file rồi replace để giảm nguy cơ file bị ghi dở; không thay thế backup/transaction mọi file.

## 14. Vòng đời artifacts và quyền giới hạn chứng cứ

`train` chỉ dùng run mới; `resume` phải có checkpoint (optimizer state) và hợp đồng khớp; `reuse` phải có best_model, config/history/completed. `check_action` từ chối mismatch để tránh trộn weights của dữ liệu/seed khác. Trong ZIP hiện tại **thiếu weights và optimizer checkpoint**, vì vậy metadata run quick chứng minh lịch sử huấn luyện, **không tự đủ để thực hiện `reuse` hoặc `resume` ngay trong ZIP**.

Khi mô tả chất lượng, phân tách 4 mức: (1) unit test offline, (2) integration tiny model, (3) pretrained Exercise 1 thật, (4) fine-tuning IMDb quick thật; **không có thực nghiệm full**.

## 15. Giới hạn, đạo đức và hướng nghiên cứu tiếp

Mô hình phân loại cảm xúc binary không hiểu bối cảnh ngoài chuỗi đầu vào; nhãn gốc phản ánh người gán nhãn và miền review phim tiếng Anh. Khi áp sang tiếng Việt, social media hoặc review sản phẩm, distribution shift có thể làm chất lượng giảm. Confidence cao sai có thể gây rủi ro nếu dùng quyết định thực tế; việc dùng chỉ cho học tập giảm yêu cầu production nhưng không miễn trách nhiệm giải thích. Kiểm thử bias/calibration/OOD chưa thực hiện. Mở rộng hợp lý: 3 seed, đánh giá max_length trên validation, phân tích lỗi có taxonomy, sensitivity theo độ dài text và so sánh base vs SST-2 trên **cùng** test protocol.

## 16. Câu hỏi nhanh để tự kiểm tra lý thuyết

1. **Tại sao E1 không train?** Vì checkpoint đã học sentiment trên SST-2, chỉ cần forward.
2. **Tại sao E2 phải gọi Trainer?** Cần cập nhật weights theo nhãn IMDb, log validation và checkpoint.
3. **Tại sao tokenizer phải cùng checkpoint?** ID→embedding phải tương ứng từ vựng và special tokens mà encoder mong đợi.
4. **Tại sao không xóa 'not'?** Vì đảo polarity, mất phủ định làm sai đặc trưng.
5. **Mask để làm gì?** Che padding, tránh coi token đệm là nội dung.
6. **Softmax có dùng trong loss không?** Cross-entropy tính ổn định từ logits, không cần tự softmax trước loss.
7. **Best metric là gì?** F1 Positive trên validation, không phải accuracy test.
8. **AUC khác accuracy chỗ nào?** AUC đánh giá xếp hạng qua threshold, accuracy ở một quyết định nhãn.
9. **Tại sao không nói quick=full?** Khác dữ liệu và max_length/epochs, chưa có full output.
10. **24 passed là gì?** Độ đúng các case phần mềm trong lần chạy lịch sử, không phải 24 câu review đúng hay 24 thí nghiệm.

## 17. Nguồn tham khảo để tự nghiên cứu

- Hugging Face Transformers documentation — AutoModel, Tokenizer, Trainer, TrainingArguments: <https://huggingface.co/docs/transformers/>
- Hugging Face Datasets documentation — dataset/split/batching: <https://huggingface.co/docs/datasets/>
- DistilBERT paper — Sanh et al., 2019, *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter*: <https://arxiv.org/abs/1910.01108>
- BERT paper — Devlin et al., 2018, *BERT: Pre-training of Deep Bidirectional Transformers*: <https://arxiv.org/abs/1810.04805>
- Attention Is All You Need — Vaswani et al., 2017: <https://arxiv.org/abs/1706.03762>
- IMDb Large Movie Review Dataset — Stanford (Maas et al., 2011): <https://ai.stanford.edu/~amaas/data/sentiment/>
- scikit-learn metrics reference: <https://scikit-learn.org/stable/modules/model_evaluation.html>

**Trong báo cáo nên phân biệt:** lý thuyết từ tài liệu/paper ↔ quyết định thiết kế của nhóm ↔ kết quả thực nghiệm trên máy. Liên kết trên để đọc nguồn, không có nghĩa ZIP đã kiểm chứng lại các trang web tại thời điểm chỉnh docs.

# LAB 3 — Hugging Face Sentiment Analysis & Fine-Tuning

> **Môn:** Deep Learning · **Bài thực hành:** Get Started with Hugging Face  
> **Bài toán:** Phân loại cảm xúc nhị phân của review tiếng Anh (NEGATIVE/POSITIVE)  
> **Cập nhật tài liệu:** 11/11/2026 · **Nguồn đặc tả:** [`docs/define&design/`](docs/define&design/)  
> **Tham số thực thi:** [`going_modular/config.py`](going_modular/config.py) (nguồn cấu hình có hiệu lực)

## 1. Mục tiêu và phạm vi

Lab 3 gồm **hai exercise riêng biệt**:

1. **Exercise 1 — Pretrained inference:** Tải checkpoint `distilbert/distilbert-base-uncased-finetuned-sst-2-english` đã được fine-tune sentiment trên SST-2; thử tokenize một câu, xem logits/softmax, suy luận thủ công và qua `pipeline('sentiment-analysis')`. **Không huấn luyện** trong exercise này.
2. **Exercise 2 — Fine-tuning:** Tải backbone pretrained `distilbert/distilbert-base-uncased` (classification head hai nhãn khởi tạo mới), xử lý dữ liệu IMDb, fine-tune bằng `Trainer`, chọn checkpoint theo F1 của validation, đánh giá cuối trên test độc lập, lưu model/báo cáo và nạp lại kiểm chứng.

Nhãn cố định trong Lab 3: `0 = NEGATIVE`, `1 = POSITIVE`. Cả hai checkpoint đều cho văn bản tiếng Anh; không có lớp trung tính. Notebook là entry point, các hàm chính nằm trong `going_modular/` để dễ test/tái sử dụng.

## 2. Bắt đầu nhanh trên VS Code

Chạy trong **thư mục gốc `Lab3/`** sau khi giải nén:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

Dành cho Linux/macOS: `source .venv/bin/activate` thay lệnh Activate.ps1. Dự án dùng Python 3.10–3.12 theo cấu hình gốc; nếu cài PyTorch GPU cần chọn wheel phù hợp CUDA/driver của máy. VS Code: chọn Python Interpreter `.venv`, cài extension Python và Jupyter, mở `notebooks/huggingface_sentiment.ipynb`, chọn kernel phù hợp rồi chạy từ đầu.

Notebook cung cấp các biến profile/action (xem code cell đầu) cho từng run; **không** tùy tiện reuse model quick với profile full hoặc run_id khác. Chỉ bắt đầu train sau khi kiểm tra đủ RAM/dung lượng, kết nối mạng lần tải model/dataset đầu tiên.

## 3. Cấu trúc dự án

```text
Lab3/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── going_modular/
│   ├── config.py            # RunConfig, quick/full, nhãn
│   ├── data_setup.py        # IMDb, split, clean, tokenize, manifest
│   ├── model_builder.py     # AutoTokenizer, AutoModel, param count
│   ├── engine.py            # TrainingArguments, Trainer, train/resume/reuse
│   ├── evaluate.py          # Metrics, inference, export CSV/PNG
│   ├── reporting.py         # REPORT.md từ metrics/history thật
│   └── utils.py             # JSON atomic, seed, hashes, contracts
├── notebooks/
│   ├── huggingface_sentiment.ipynb
│   └── huggingface_sentiment_executed.ipynb
├── tests/
│   ├── conftest.py
│   ├── test_data_setup.py
│   ├── test_model_builder.py
│   ├── test_engine.py
│   ├── test_utils.py
│   ├── test_evaluate.py
│   └── test_notebook.py
├── docs/
│   ├── README.md                            # Mục lục docs mới
│   ├── CHANGES_DOCS.md                     # Tóm tắt bản chỉnh lý
│   ├── analysts/                          # Yêu cầu, ADR và kiểm toán bằng chứng
│   │   ├── requirements_analysis.md
│   │   ├── requirements_traceability.md
│   │   ├── design_decisions.md
│   │   └── implementation_evidence_audit.md
│   ├── theory/                            # Cơ sở lý thuyết DistilBERT/NLP
│   │   └── 00_theoretical_foundations.md
│   ├── presentation/                      # Hướng dẫn bảo vệ/vấn đáp
│   │   └── defense_guide.md
│   ├── define&design/                     # CÂY ĐẶC TẢ CHÍNH ĐƯỢC GIỮ
│   │   ├── 00_lab3_description.md
│   │   ├── 01_data.md
│   │   ├── 02_model.md
│   │   ├── 03_engine.md
│   │   ├── 04_utils.md
│   │   ├── 05_evaluation_results.md
│   │   ├── 06_architecture_and_interfaces.md
│   │   └── tests/
│   │       ├── 00_test_plan.md
│   │       ├── 01_test_data_setup.md
│   │       ├── 02_test_model_builder.md
│   │       ├── 03_test_engine.md
│   │       ├── 04_test_utils.md
│   │       ├── 05_test_evaluate.md
│   │       ├── 06_test_notebook.md
│   │       └── 07_acceptance_scenarios.md
│   └── plans/
│       ├── implementation_plan.md         # Kế hoạch tổng, phân công và nghiệm thu
│       ├── phase0.md                      # Yêu cầu và môi trường
│       ├── phase1.md                      # IMDb data
│       ├── phase2.md                      # Model/tokenizer/Exercise 1
│       ├── phase3.md                      # Trainer và fine-tuning
│       ├── phase4.md                      # Checkpoint/resume/reuse
│       ├── phase5.md                      # Evaluation/error analysis
│       ├── phase6.md                      # Notebook/README/báo cáo
│       ├── phase7.md                      # Test và bàn giao
│       └── team_workflow_and_log.md      # Phân công và nhật ký mẫu
├── reports/                               # Validation, log và thuyết minh gốc
└── outputs/                               # Artifacts từ lần chạy quick có sẵn
```

**Quy ước:** Chỉ có một thư mục đặc tả `Lab3/docs/define&design/`. Không tạo lại `define&designt` hoặc cây `lab3/` khác; chú ý tên viết hoa/thường khi push GitHub, đặc biệt `README.md`.

## 4. Kế hoạch triển khai theo phase và đặc tả

Nhóm trưởng có thể bắt đầu từ [`docs/plans/implementation_plan.md`](docs/plans/implementation_plan.md), sau đó giao/cập nhật checklist trong từng phase:

| Phase | Công việc | File kế hoạch |
|---|---|---|
| P0 | Phân tích đề, dependencies và cấu hình | [`phase0.md`](docs/plans/phase0.md) |
| P1 | IMDb train/val/test, cleaning và manifest | [`phase1.md`](docs/plans/phase1.md) |
| P2 | Pretrained sentiment, tokenizer và model contract | [`phase2.md`](docs/plans/phase2.md) |
| P3 | TrainingArguments, Trainer và best validation model | [`phase3.md`](docs/plans/phase3.md) |
| P4 | Lifecycle artifacts, checkpoint/resume/reuse | [`phase4.md`](docs/plans/phase4.md) |
| P5 | Metrics, test once, confusion matrix và lỗi | [`phase5.md`](docs/plans/phase5.md) |
| P6 | Notebook, tái lập, tài liệu và báo cáo | [`phase6.md`](docs/plans/phase6.md) |
| P7 | Test, nghiệm thu, review và bàn giao GitHub | [`phase7.md`](docs/plans/phase7.md) |

**Đọc tài liệu kỹ thuật:** [`02_model.md`](docs/define&design/02_model.md) mô tả model ID, ngày/phiên bản tài liệu, kiến trúc, input/output, quick/full, lifecycle và test liên quan. [`03_engine.md`](docs/define&design/03_engine.md) giải thích `Trainer`. Các đặc tả test ở [`tests/00_test_plan.md`](docs/define&design/tests/00_test_plan.md) liên kết tới các cases trong source. [`requirements_traceability.md`](docs/analysts/requirements_traceability.md) kết nối yêu cầu đề bài → code → phase → test → artifacts.

## 5. Cấu hình thực nghiệm từ code

| Thuộc tính | Quick | Full |
|---|---:|---:|
| Train / Validation / Test | 2.000 / 500 / 1.000 | 20.000 / 5.000 / 25.000 |
| Epochs | **2** | **3** |
| Max input length | 128 | 256 |
| Train batch size | 16 | 16 |
| Eval batch size | 32 | 32 |
| Learning rate | 2e-5 | 2e-5 |
| Seed | 42 | 42 |
| Weight decay | 0.01 | 0.01 |
| Warmup ratio | 0.1 | 0.1 |
| Model | DistilBERT base + 2-label head | Như quick |

`val_size=5000` được tách từ train IMDb gốc trước khi lấy subset. `tokenize_splits` dùng `truncation=True`, `padding=False`; **dynamic padding** diễn ra ở `DataCollatorWithPadding` theo chiều dài lớn nhất của từng batch (không phải `padding='max_length'`). `input_ids`/`attention_mask`/`labels` phục vụ Trainer; raw `text`/`sample_id` giữ để đối chiếu lỗi. Optimizer AdamW, linear scheduler; model tốt nhất chọn theo **F1 lớp Positive trên validation**.

## 6. Cách chạy kiểm thử

```bash
python -m pytest -q
python -m pytest tests/test_data_setup.py -v
python -m pytest tests/test_model_builder.py -v
python -m pytest tests/test_engine.py -v
python -m pytest tests/test_utils.py -v
python -m pytest tests/test_evaluate.py -v
python -m pytest tests/test_notebook.py -v
```

File `reports/pytest_output.txt` trong ZIP gốc ghi nhận **24 pytest cases passed, 1 warning** trong môi trường tác giả chạy trước đó. Đó **không phải kết quả chạy mới** khi chỉ bổ sung tài liệu. Suite dùng model tiny random và dữ liệu synthetic offline để kiểm tra tính đúng của code, không phải accuracy IMDb. Tài liệu test phân biệt `ĐÃ CÓ TRONG CODE` và `CHƯA TRIỂN KHAI`.

## 7. Bằng chứng thực nghiệm có sẵn (không phải kết quả kỳ vọng)

Run quick đã lưu tại `outputs/2026-11-11/distilbert_imdb_quick/183159-290735/`:

| Chỉ số | Giá trị từ lần chạy quick |
|---|---:|
| Test samples | 1.000 |
| Accuracy | **0.8620 (86,20%)** |
| Precision Positive | 0.867886 |
| Recall Positive | 0.854000 |
| F1 Positive | **0.860887** |
| Macro F1 | 0.861991 |
| ROC-AUC | 0.931748 |
| Confusion matrix (true hàng / pred cột) | `[[435,65],[73,427]]` |

Các số trên lấy từ file kết quả quick trong ZIP đầu vào và đối chiếu trong `reports/VALIDATION.md`; chúng không đại diện benchmark full. `reports/reference_run/` lưu config, history, split manifest và marker completed của lần chạy tham chiếu. `notebooks/huggingface_sentiment_executed.ipynb` là snapshot đã chạy, còn notebook không hậu tố là bản để chạy mới.

**Quan trọng về weights:** ZIP đầu vào không kèm `best_model/model.safetensors` hay checkpoint optimizer đầy đủ, vì thế **không thể `reuse` trực tiếp từ ZIP này** chỉ nhờ `reports/reference_run/`. Để chạy inference với model IMDb đã fine-tune, cần lưu kèm weights/artifacts từ máy đã train, hoặc train lại trong notebook rồi lưu `best_model/` tương ứng. Khi train lại, tạo run mới và đối chiếu các phiên bản library/model/dataset; kết quả có thể chênh nhẹ.

## 8. Test và kết quả cần phân biệt khi báo cáo nhóm

- **Test phần mềm:** pytest kiểm các invariants: split, logits `[B,2]`, save/reuse, metrics, notebook AST. Không đánh giá năng lực model pretrained ngoài đời thực.
- **Validation trong training:** F1 trên validation để chọn checkpoint; không dùng test để chọn siêu tham số.
- **Test IMDb cuối:** bộ quick 1.000 review; accuracy 86,20% ở run lưu sẵn. Không có kết quả full trong bản nộp.
- **Error analysis:** `errors.csv` chứa tối đa 20 lỗi có confidence cao nhất; ví dụ chỉ giúp đặt giả thuyết về phủ định/mỉa mai, không kết luận chắc chắn nguyên nhân.

## 9. Lỗi thường gặp và cách xử lý

| Vấn đề | Cách kiểm tra |
|---|---|
| `ModuleNotFoundError` / import error | Chọn đúng `.venv`, chạy `python -m pip install -r requirements.txt` |
| Torch không nhận GPU | Kiểm `python -c "import torch; print(torch.cuda.is_available())"`; cài wheel đúng CUDA |
| Hugging Face tải chậm/mạng lỗi | Kiểm Internet, cache model/dataset và revision; không sửa manual metrics |
| `CUDA out of memory` | Cân nhắc run mới với batch/max_length thấp hơn; hợp đồng run cũ không được thay khi resume |
| `FileExistsError` khi train | Run ID đã có file: đổi run_id hoặc chọn resume/reuse khi đủ điều kiện |
| `FileNotFoundError` khi reuse | Cần đủ `completed.json`, history và `best_model/` chứa safetensors/tokenizer |
| Notebook không import `going_modular` | Đảm bảo root `Lab3/` được đưa vào `sys.path` theo cell setup |

## 10. Nghiệm thu và quy ước commit

Trước khi nộp, xem checklist P7, chạy pytest trong môi trường đủ dependencies, đọc log thực tế và so sánh `README.md`, model spec với `RunConfig`. Nếu chỉ sửa đặc tả, Git diff nên chỉ chứa các file Markdown liên quan, **không chỉnh code hoặc ghi đè outputs/ bằng kết quả bịa**. Pull Request nên mô tả cụ thể 8 phase, test specs, bổ sung model, chỉnh README và giới hạn chưa thực nghiệm.

## Hồ sơ docs phục vụ báo cáo

Bắt đầu từ [mục lục tài liệu Lab 3](docs/README.md), [ma trận FR đã đồng bộ](docs/analysts/requirements_traceability.md) và [hướng dẫn vấn đáp](docs/presentation/defense_guide.md). Các tài liệu nêu rõ ranh giới bằng chứng quick/full, 24 pytest cases lịch sử và những artifacts chưa có trong ZIP.

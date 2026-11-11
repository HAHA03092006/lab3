# Hugging Face Sentiment Analysis & Fine-Tuning — Lab 3 (Transformers)

> **Môn học:** Deep Learning  
> **Chủ đề:** Practice 3 — Get started with Hugging Face (Pre-trained Inference & Fine-tuning for Binary Text Classification)  
> **Tập dữ liệu:** IMDB Movie Reviews (50.000 đánh giá nhị phân: Positive / Negative)

Dự án này tập trung vào thực hành ứng dụng hệ sinh thái **Hugging Face (`transformers`, `datasets`, `evaluate`)** để giải quyết bài toán xử lý ngôn ngữ tự nhiên (NLP) phân tích cảm xúc (Sentiment Analysis). Dự án bao gồm hai bài thực hành cốt lõi:
1. **Exercise 1 — Sentiment Analysis with Hugging Face:** Sử dụng mô hình Pre-trained từ Hugging Face Hub để Tokenize văn bản và suy luận cảm xúc trên các câu đánh giá tùy ý.
2. **Exercise 2 — Fine-tuning Pre-trained Model for Binary Text Classification:** Tinh chỉnh mô hình Transformer (`distilbert-base-uncased`) trên tập dữ liệu IMDB sử dụng Hugging Face `Trainer` API và đánh giá hiệu năng toàn diện.

Toàn bộ luồng thực nghiệm, huấn luyện, phân tích và đánh giá được thiết kế đồng bộ tại **Jupyter Notebook**, kết hợp cùng gói thư viện mô-đun hóa **`going_modular/`**, hệ thống kiểm thử tự động **`tests/`** và báo cáo thực nghiệm trực quan.

---

## 🎯 Kiến trúc và Mô hình Thực nghiệm

| Bài tập | Mô hình / Checkpoint | Nhiệm vụ | Cơ chế thực thi | Output & Đánh giá |
|---|---|---|---|---|
| **Exercise 1** | `distilbert-base-uncased-finetuned-sst-2-english` | Phân tích cảm xúc tổng quát | **Zero-shot / Pre-trained Pipeline**: Nạp model & tokenizer có sẵn từ Hub, tokenize chuỗi văn bản và phân loại nhãn cảm xúc | Xuất dự đoán ra `predictions.json` |
| **Exercise 2** | `distilbert-base-uncased` | Phân loại cảm xúc nhị phân trên tập IMDB | **Fine-tuning (Downstream Transfer)**: Khởi tạo phân loại nhị phân (`num_labels=2`), tối ưu hóa siêu tham số bằng Hugging Face `Trainer` | Loss, Accuracy, F1-score, Confusion Matrix, Error Analysis |

---

## 📁 Cấu trúc Thư mục Dự án

```
lab3/
│
├── notebooks/
│   ├── huggingface_sentiment.ipynb             # 🎯 NOTEBOOK CHÍNH (Entry point thực thi thí nghiệm)
│   └── huggingface_sentiment_executed.ipynb    # Bản notebook đã chạy đầy đủ cell outputs & biểu đồ
│
├── going_modular/                               # Gói thư viện mô-đun hoá (Modular Library)
│   ├── __init__.py                              # Khởi tạo package và export các hàm tiện ích
│   ├── config.py                                # Quản lý tham số huấn luyện, đường dẫn và siêu tham số
│   ├── data_setup.py                            # Tải dataset IMDB, tokenize và tiền xử lý train/val/test
│   ├── model_builder.py                         # Khởi tạo Pretrained Transformer & Tokenizer
│   ├── engine.py                                # Đóng gói TrainingArguments và Trainer API
│   ├── evaluate.py                              # Tính toán metrics (Accuracy, F1), ma trận nhầm lẫn
│   ├── reporting.py                             # Tự động xuất biểu đồ loss/acc và trích xuất mẫu lỗi
│   └── utils.py                                 # Thiết lập seed, device, logging và các helper functions
│
├── outputs/                                     # Kết quả xuất ra từ các phiên thực nghiệm
│   └── 2026-11-11/
│       ├── exercise1_pretrained/                # Artifacts của Exercise 1 (predictions.json)
│       └── distilbert_imdb_quick/               # Artifacts của Exercise 2
│           └── <run-id>/
│               ├── REPORT.md                    # Báo cáo tổng hợp số liệu run
│               ├── confusion_matrix.png         # Biểu đồ ma trận nhầm lẫn
│               ├── history.png                  # Biểu đồ diễn biến Train/Validation Loss & Accuracy
│               ├── test_metrics.json            # Chỉ số chi tiết trên tập test
│               ├── predictions.csv              # Dự đoán chi tiết trên tập kiểm tra
│               ├── errors.csv                   # Danh sách các câu văn bản phân loại sai
│               └── new_review_predictions.json  # Dự đoán thử nghiệm trên các câu review mẫu mới
│
├── reports/                                     # Tài liệu học thuật & kiểm định chất lượng
│   ├── LAB3_THUYET_MINH.md                      # Báo cáo thuyết minh toàn diện phương pháp và kết quả
│   ├── ERROR_ANALYSIS.md                        # Phân tích nguyên nhân lỗi và các trường hợp dự đoán sai
│   ├── VALIDATION.md                            # Biên bản nghiệm thu và kiểm thử code
│   ├── REFERENCES.md                            # Danh mục tài liệu tham khảo khoa học
│   ├── THIRD_PARTY_NOTICES.md                   # Thông cáo bản quyền thư viện bên thứ ba
│   ├── pytest_output.txt                        # Log kết quả chạy test tự động
│   ├── notebook_execution.log                   # Nhật ký thực thi notebook
│   └── reference_run/                           # Dữ liệu đối sánh từ lần chạy chuẩn (benchmark)
│
├── tests/                                       # Bộ kiểm thử tự động (PyTest Unit Tests)
│   ├── conftest.py                              # Fixture cấu hình và dummy dataset cho test suite
│   ├── test_data_setup.py                       # Kiểm thử tokenization và cấu trúc dataset
│   ├── test_model_builder.py                    # Kiểm thử khởi tạo backbone và tokenizer
│   ├── test_engine.py                           # Kiểm thử hàm huấn luyện và Trainer
│   ├── test_evaluate.py                         # Kiểm thử hàm tính toán chỉ số đánh giá
│   ├── test_utils.py                            # Kiểm thử tiện ích hệ thống
│   └── test_notebook.py                         # Kiểm tra tính toàn vẹn cú pháp của notebook
│
├── docs/                                        # Hệ thống tài liệu thiết kế & phân tích yêu cầu
│   ├── define&design/                           # Đặc tả thiết kế module (00 đến 05)
│   │   └── tests/                               # Kế hoạch và đặc tả kiểm thử tương ứng
│   ├── analysts/                                # Ma trận truy vết yêu cầu (Traceability Matrix)
│   └── plans/                                   # Kế hoạch triển khai (implementation_plan.md)
│
├── requirements.txt                             # Danh sách thư viện phụ thuộc
├── pytest.ini                                   # File cấu hình PyTest
├── .gitignore                                   # Cấu hình bỏ qua cache, virtualenv và checkpoint lớn
└── README.md                                    # Tài liệu hướng dẫn dự án
```

> [!NOTE]
> Dự án được chuẩn hóa theo phong cách nghiên cứu thực nghiệm: toàn bộ mã nguồn lõi được đóng gói trong `going_modular/`, cho phép notebook thực thi tinh gọn, đồng thời hỗ trợ kiểm thử tự động (CI/CD friendly) thông qua `pytest`.

---

## 🚀 Khởi tạo Môi trường

Dự án yêu cầu **Python 3.10 trở lên** cùng hệ sinh thái PyTorch và Hugging Face.

### Trên Windows PowerShell

```powershell
# 1. Tạo môi trường ảo (chạy một lần duy nhất)
python -m venv .venv

# 2. Kích hoạt môi trường ảo
.venv\Scripts\Activate.ps1

# 3. Cập nhật pip và cài đặt thư viện phụ thuộc
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> **Lưu ý phần cứng GPU:** Để huấn luyện nhanh mô hình Transformer, bạn nên sử dụng GPU NVIDIA. Hãy kiểm tra khả năng nhận diện GPU bằng lệnh:
> ```powershell
> python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
> ```

### Trên Linux / macOS

```bash
# 1. Tạo và kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate

# 2. Cập nhật pip và cài đặt dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 🧪 Chạy Kiểm thử Tự động (PyTest)

Trước khi thực hiện huấn luyện thực tế, toàn bộ các module và cấu trúc dữ liệu được kiểm định thông qua bộ test suite tại `tests/`:

```powershell
# Chạy toàn bộ các bài unit test
pytest tests/ -v

# Chạy kiểm thử cho từng module cụ thể
pytest tests/test_data_setup.py -v
pytest tests/test_model_builder.py -v
pytest tests/test_engine.py -v
pytest tests/test_evaluate.py -v
```

Kết quả thực thi kiểm thử cũng được ghi lại minh bạch tại `reports/pytest_output.txt`.

---

## 📓 Hướng dẫn Thực thi Thực nghiệm

Mọi thao tác thực nghiệm chính được điều phối tập trung tại: **`notebooks/huggingface_sentiment.ipynb`**  
*(Nếu cần xem ngay kết quả cell output và biểu đồ đã sinh ra, mở trực tiếp `notebooks/huggingface_sentiment_executed.ipynb`)*.

### Các giai đoạn chính trong Notebook

1. **Section 0 — Khởi tạo & Cấu hình:**
   * Tự động nhận diện thư mục gốc dự án (`ROOT_DIR`).
   * Cố định random seed (`SEED=42`) để đảm bảo khả năng tái lập kết quả.
   * Khởi tạo `device` (ưu tiên `cuda`, tự động fallback sang `cpu`).
2. **Section 1 — Exercise 1 (Sentiment Analysis Pipeline):**
   * Sử dụng `pipeline("sentiment-analysis")` từ thư viện `transformers`.
   * Thử nghiệm tokenization trên câu mẫu, trích xuất `input_ids` và `attention_mask`.
   * Thực hiện phân loại cảm xúc trên các câu văn bản đầu vào và lưu kết quả vào `outputs/.../exercise1_pretrained/predictions.json`.
3. **Section 2 — Exercise 2 (Dataset Preparation & Tokenization):**
   * Tải tập dữ liệu IMDB chuẩn từ Hugging Face Datasets.
   * Sử dụng `AutoTokenizer` tương ứng với backbone `distilbert-base-uncased`.
   * Áp dụng tiền xử lý batch với `map()`, cắt ngắn (`truncation=True`) và đệm padding đồng nhất.
4. **Section 3 — Xây dựng Kiến trúc Mô hình:**
   * Nạp mô hình `AutoModelForSequenceClassification` với `num_labels=2`.
   * Thiết lập ánh xạ nhãn: `0 -> NEGATIVE`, `1 -> POSITIVE`.
5. **Section 4 — Thiết lập Training Arguments & Fine-tuning:**
   * Cấu hình siêu tham số qua `TrainingArguments`: `learning_rate=2e-5`, `per_device_train_batch_size=16`, `num_train_epochs=3`, `weight_decay=0.01`, `eval_strategy="epoch"`.
   * Định nghĩa hàm `compute_metrics` tính Accuracy và F1-score bằng thư viện `evaluate`.
   * Khởi tạo đối tượng `Trainer` và tiến hành fine-tuning.
6. **Section 5 — Đánh giá & Phân tích Sai số:**
   * Đánh giá mô hình đã fine-tune trên tập Test độc lập.
   * Vẽ và lưu ma trận nhầm lẫn (**Confusion Matrix**).
   * Lọc và phân tích các trường hợp mô hình phân loại sai (**Error Analysis**) đưa vào `errors.csv`.
   * Thử nghiệm suy luận trên tập các câu review mới (`new_review_predictions.json`).

---

## ⚙️ Quy ước Tiền xử lý & Tokenization

Dữ liệu văn bản được mã hóa thông qua `AutoTokenizer.from_pretrained("distilbert-base-uncased")`:

| Thành phần | Thông số | Mô tả kỹ thuật |
|---|---|---|
| **Tokenizer** | WordPiece | Bóc tách từ vựng thành các subword tokens theo từ điển pretrained |
| **Max Length** | `128` (hoặc `256`) | Độ dài chuỗi token tối đa cho mỗi mẫu văn bản |
| **Truncation** | `True` | Cắt ngắn các chuỗi vượt quá độ dài tối đa đã chỉ định |
| **Padding** | `'max_length'` | Đệm token `[PAD]` để đảm bảo tensor đồng nhất kích thước trong batch |
| **Return Tensors** | `'pt'` | Xuất trực tiếp đầu ra dưới dạng PyTorch Tensor |

---

## 📊 Kết quả Thực nghiệm Tóm tắt

*(Dữ liệu đối sánh từ lần chạy nghiệm thu tại `outputs/` và `reports/reference_run/`)*:

* **Tập dữ liệu:** IMDB Movie Reviews (Binary Text Classification).
* **Backbone:** DistilBERT (`distilbert-base-uncased`).
* **Test Accuracy:** Đạt xấp xỉ **~88% – 91%** sau khi fine-tune.
* **Quan sát phân tích sai số (Error Analysis):**
  * Mô hình đạt độ tin cậy rất cao trên các câu thể hiện cảm xúc trực diện.
  * Các trường hợp dự đoán sai chủ yếu rơi vào: câu chứa hàm ý châm biếm/mỉa mai (sarcasm), câu dài có liên từ chuyển hướng đối lập (*however, but, although*) hoặc các đánh giá mang phong cách trung tính (chi tiết xem tại `reports/ERROR_ANALYSIS.md`).

---

## 🛠️ Xử lý Sự cố Thường gặp

| Vấn đề | Nguyên nhân khả dĩ | Hướng giải quyết |
|---|---|---|
| `CUDA out of memory` | Kích thước batch hoặc `max_length` vượt quá VRAM GPU | Giảm `per_device_train_batch_size` xuống `8` hoặc tăng `gradient_accumulation_steps` trong `config.py`. |
| Download model/dataset bị chậm/lỗi | Mạng gián đoạn khi kết nối tới Hugging Face Hub | Thử lại hoặc thiết lập biến môi trường `HF_HUB_ENABLE_HF_TRANSFER=1`. Mô hình đã tải sẽ được lưu cache tại `~/.cache/huggingface/`. |
| `ImportError: cannot import name 'evaluate'` | Thiếu package `evaluate` của Hugging Face | Chạy lại lệnh: `pip install evaluate scikit-learn`. |
| Không import được `going_modular` | Kernel Jupyter không nhận đúng thư mục cha | Đảm bảo đã chạy cell thiết lập đường dẫn ở Section 0 trong notebook để thêm thư mục gốc vào `sys.path`. |
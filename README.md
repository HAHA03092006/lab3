# Lab 3 — Get started with Hugging Face

**Deep Learning · GV: TS. Nguyễn Thị Khánh Tiên**  
**Đề:** Chương 4, trang 25, Exercise 1 + Exercise 2.  
**Cách tổ chức tham chiếu:** [Lab 2](https://github.com/toan58936/lab2), commit `93d255b`.

Bài làm gồm mã nguồn, notebook có giải thích, đặc tả thiết kế, kiểm thử và hướng dẫn báo cáo.
Trạng thái thực thi được ghi riêng tại [reports/VALIDATION.md](reports/VALIDATION.md).
Không có số liệu accuracy giả định; notebook tự xuất báo cáo từ kết quả chạy thực tế.

## 1. Bắt đầu từ đâu?

1. Đọc README này và [mô tả tổng quan](docs/define&designt/00_lab3_description.md).
2. Mở [notebook chính](notebooks/huggingface_sentiment.ipynb).
3. Chạy `quick` để kiểm tra luồng; chọn `full` để huấn luyện và đánh giá trên toàn bộ dữ liệu đã định nghĩa.
4. Sau khi chạy, xem `outputs/<ngày>/<run_id>/<phiên>/REPORT.md` cùng metrics và biểu đồ.

## 2. Hai bài tập

| Bài | Phương pháp | Đầu vào → đầu ra |
|---|---|---|
| Exercise 1 | DistilBERT đã fine-tune SST-2, inference thủ công + pipeline | Câu tiếng Anh → token IDs/mask → nhãn và confidence |
| Exercise 2 | Fine-tune DistilBERT nền bằng Hugging Face Trainer trên IMDb | Reviews + nhãn → model đã học → đánh giá test |

Model bài 1: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`.  
Model bài 2: `distilbert/distilbert-base-uncased`.  
Dataset: `stanfordnlp/imdb`; nhãn 0 = NEGATIVE, 1 = POSITIVE.

## 3. Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `notebooks/huggingface_sentiment.ipynb` | Entry point, hai bài tập, giải thích, biểu đồ và báo cáo |
| `going_modular/config.py` | RunConfig, profiles, checkpoint IDs |
| `going_modular/data_setup.py` | Clean, split, subset, tokenize, manifest |
| `going_modular/model_builder.py` | Auto model/tokenizer, thống kê tham số |
| `going_modular/engine.py` | TrainingArguments, Trainer, train/resume/reuse |
| `going_modular/evaluate.py` | Suy luận, metrics, confusion matrix, CSV |
| `going_modular/utils.py` | Seed, JSON atomic, bảo vệ artifacts, metadata |
| `going_modular/reporting.py` | Tạo báo cáo từ số liệu thực |
| `docs/define&designt/00–05` | Đặc tả tổng quan và chi tiết từng module |
| `docs/define&designt/tests/` | Kế hoạch và tiêu chí kiểm thử |
| `docs/plans/` | Thứ tự thực hiện và chạy thí nghiệm |
| `docs/analysts/` | Đối chiếu Lab 2 → Lab 3 và truy vết đề |
| `reports/` | Thuyết minh, kiểm chứng và tài liệu tham khảo |
| `tests/` | Unit tests và tích hợp Trainer offline |
| `artifacts/`, `outputs/`, `logs/` | Trạng thái train, kết quả đánh giá, TensorBoard sinh khi chạy |

Giữ tên `define&designt` theo repo tham chiếu để nhóm dễ đối chiếu; đây là thư mục tài liệu.

## 4. Chạy trên Windows / VS Code

Mở terminal ở thư mục `lab3`:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m ipykernel install --user --name lab3 --display-name "Python (Lab 3)"
.venv\Scripts\python.exe -m pytest -q
```

Chọn kernel **Python (Lab 3)** trong notebook. Không cần activate nên tránh lỗi execution policy PowerShell.
Dùng Python 3.10–3.12. Với NVIDIA, cài torch theo [hướng dẫn PyTorch](https://pytorch.org/get-started/locally/) phù hợp CUDA trước khi cài requirements. Kiểm tra `torch.cuda.is_available()`.

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

## 5. Chạy trên Google Colab

1. Giải nén ZIP ở máy, upload `notebooks/huggingface_sentiment.ipynb` vào Colab.
2. Bật GPU. Chạy setup; khi hỏi, upload lại **ZIP toàn bộ Lab 3** để lấy package/code.
3. Cell setup cài requirements, mount Drive, lưu artifacts tại `MyDrive/lab3`.
4. Chạy tuần tự từ đầu. Dataset/Hub cache nằm trên runtime; checkpoint và output nằm trên Drive.
5. Sau khi Colab ngắt: chạy lại setup/data/tokenize, đặt `ACTION='resume'` rồi chạy phần train.
6. Nếu run đã hoàn tất: `ACTION='reuse'`. Không cần huấn luyện lại.

Không có repo Lab 3 giả định; không cần đổi URL GitHub để notebook chạy.
Để giữ cache qua phiên, có thể đổi `cache_dir` sang Drive, nhưng truy cập Drive chậm hơn runtime.

## 6. Profiles và hyperparameters

| Profile | Train | Validation | Test | max_length | Epochs | Train/eval batch |
|---|---:|---:|---:|---:|---:|---:|
| quick | 2.000 | 500 | 1.000 | 128 | 2 | 16/32 |
| full | 20.000 | 5.000 | 25.000 | 256 | 3 | 16/32 |

Cả hai: seed 42, LR 2e-5, AdamW, weight decay 0.01, linear scheduler, warmup_ratio 0.1, clip norm 1.0.
Cấu hình này là điểm khởi đầu thực hành, không phải cấu hình tối ưu đã được chứng minh.
Quick lấy mẫu phân tầng **sau khi** tách validation; full dùng nguyên test chuẩn.
Thay cấu hình thì đổi `run_id` bằng `dataclasses.replace(CFG, run_id='ten_moi', learning_rate=...)`.

## 7. Lưu kết quả và resume

- `artifacts/<run_id>/config.json`: cấu hình, contract dữ liệu/tokenizer, môi trường.
- `split_manifest.json`: sample IDs, số mẫu, nhãn, hash nội dung và thống kê exact duplicates.
- `checkpoints/checkpoint-*`: Trainer state, optimizer, scheduler, RNG để resume.
- `best_model/`: model.safetensors, config và tokenizer để inference/reuse.
- `history.json`, `completed.json`: lịch sử và trạng thái hoàn tất.
- `outputs/<ngày>/<run_id>/<phiên>/`: test_metrics.json, predictions.csv, errors.csv, PNG, REPORT.md.
- `logs/<run_id>/`: TensorBoard. Mở bằng `tensorboard --logdir=logs` khi chạy local.

`train` từ chối **mọi thư mục run không rỗng**, kể cả lần train trước dang dở. Không tự xóa dữ liệu.
`resume` đòi cùng cấu hình và cùng dữ liệu. Không tăng epochs khi resume vì scheduler đã được tính cho tổng bước ban đầu.
`reuse` đòi completed marker và model/tokenizer đã export đầy đủ.
Checkpoint lưu cuối mỗi epoch: nếu ngắt giữa epoch đầu chưa có checkpoint, dùng run_id mới để train lại.

## 8. Kiểm thử và giới hạn

```bash
python -m pytest -q
```

Tests không tải model/dataset từ mạng. Tích hợp tạo **DistilBERT nhỏ, trọng số ngẫu nhiên**, tokenizer local và dữ liệu tổng hợp,
chạy Trainer thật để kiểm tra checkpoint/resume/reuse. Đây **không phải kết quả sentiment trên IMDb**.
Không dùng unit tests để chứng minh accuracy của mô hình thực tế. Xem `reports/VALIDATION.md`.

Text models không cần torchvision. Nếu Colab có sẵn torchvision/librosa lỗi tương thích và import Transformers lỗi,
hãy tạo runtime sạch hoặc gỡ đúng thư viện phụ không dùng, rồi restart; không sửa ngẫu nhiên version trong khi train.
OOM: dùng batch 8 và gradient accumulation 2 trong run mới; giữ effective batch 16. CPU chạy được nhưng full rất chậm.
Hub lỗi mạng: kiểm tra kết nối, cache và dung lượng; không tự thay bằng model random rồi báo là pretrained.

## 9. Nộp bài

Nộp source + notebook đã chạy + báo cáo tự sinh + metrics/biểu đồ. Đọc errors.csv để bổ sung phân tích lỗi có ví dụ.
Không commit cache, dataset, checkpoint nặng hoặc secrets lên GitHub. Lưu model trên Drive nếu cần chứng minh reuse.
Tên thành viên/mã lớp không được cung cấp nên tài liệu không tự điền thông tin cá nhân.

## 10. Các gói bàn giao

- `LAB3_HUGGING_FACE_COMPLETE.zip`: toàn bộ source, docs, tests, notebook mẫu và bản đã chạy, kết quả quick thật.
  Gói source không chứa cache/dataset/checkpoints nặng; bản sao cấu hình thực nghiệm nằm tại reports/reference_run/.
- `LAB3_TRAINED_MODEL_QUICK.zip`: model/tokenizer quick đã huấn luyện và artifacts cần cho reuse.
  Giải nén vào cùng thư mục cha với gói source để hợp nhất cây lab3/artifacts/distilbert_imdb_quick/.
  Sau đó mở notebook mẫu, giữ PROFILE='quick', đổi ACTION='reuse'.
  Trên Colab với USE_DRIVE=True, thư mục model phải nằm ở
  `MyDrive/lab3/artifacts/distilbert_imdb_quick/` (không chỉ ở /content/lab3).

Nếu chỉ giải nén source, giữ ACTION='train'. Nếu đã giải nén model, dùng ACTION='reuse' hoặc đổi run_id để train mới.
Model đã hoàn tất được bàn giao phục vụ inference/reuse; checkpoint optimizer giữa các epoch không đóng gói để giảm dung lượng.
Không thể resume một run đã hoàn tất; reuse không cần optimizer state.

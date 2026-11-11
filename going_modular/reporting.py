"""Sinh nhận xét chỉ từ metrics thực tế; không chèn kết quả kỳ vọng."""
from pathlib import Path


def write_report(output_dir, cfg, metrics, history, completed):
    overlap = metrics['metadata'].get('duplicate_text_overlap', {})
    rows = [x for x in history if 'eval_loss' in x]
    trend = 'Chưa đủ điểm validation để kết luận xu hướng qua epoch.'
    if len(rows) >= 2:
        trend = f"Validation loss đầu/cuối: {rows[0]['eval_loss']:.4f} / {rows[-1]['eval_loss']:.4f}."
        if rows[-1]['eval_loss'] > rows[0]['eval_loss']:
            trend += ' Loss validation tăng; cần xem đồng thời train loss trước khi kết luận overfitting.'
    text = f'''# Báo cáo kết quả Lab 3 — {cfg.run_id}

## 1. Mục tiêu và phương pháp
Fine-tune {cfg.model_id} cho phân loại cảm xúc IMDb. Nhãn 0 = NEGATIVE, 1 = POSITIVE.
Đầu vào là văn bản; tokenizer tạo input_ids và attention_mask; model tạo hai logits.
Trainer tối ưu cross-entropy bằng AdamW và linear scheduler có warmup.
Chọn checkpoint theo F1 lớp Positive trên validation; test chỉ chạy sau khi chốt model.

## 2. Cấu hình thực nghiệm
- Profile: **{cfg.profile}**. Kết quả chỉ đại diện tập test thực sự đã dùng.
- Seed: {cfg.seed}; max_length: {cfg.max_length}; epochs yêu cầu: {cfg.epochs}.
- Learning rate: {cfg.learning_rate}; batch: {cfg.batch_size}; weight decay: {cfg.weight_decay}.
- Số bước optimizer hoàn thành: {completed['global_step']}.
- F1 validation tốt nhất: {completed['best_metric']:.4f}.
- Exact-text overlap giữa các split: {overlap}. Đây là chẩn đoán, không sửa benchmark dựa vào test.

## 3. Kết quả đo trên test
| Chỉ tiêu | Giá trị |
|---|---:|
| Số mẫu | {metrics['num_samples']} |
| Accuracy | {metrics['accuracy']:.4f} |
| Precision (Positive) | {metrics['precision']:.4f} |
| Recall (Positive) | {metrics['recall']:.4f} |
| F1 (Positive) | {metrics['f1']:.4f} |
| Macro F1 | {metrics['macro_f1']:.4f} |

## 4. Nhận xét và giới hạn
{trend}
Confusion matrix, predictions.csv và errors.csv là bằng chứng để xem loại lỗi và ví dụ cụ thể.
Không suy ra mô hình mới chắc chắn tốt hơn bản SST-2 nếu chưa đánh giá cả hai trên cùng tập test.
Một seed và một lần chia không đủ để kết luận ưu thế thống kê. Văn bản dài bị cắt ở max_length;
phủ định, mỉa mai và cảm xúc pha trộn cần phân tích thủ công. Mô hình tiếng Anh không được đánh giá
cho tiếng Việt. Confidence softmax không phải bảo đảm xác suất đúng đã được hiệu chuẩn.

## 5. Tái lập
Xem config.json, split_manifest.json, history.json, completed.json và best_model/ trong artifacts.
Dùng action='reuse' để tải lại model/tokenizer; giữ profile, seed, cấu hình dữ liệu như lần train.
'''
    path = Path(output_dir)/'REPORT.md'
    path.write_text(text,encoding='utf-8')
    return path

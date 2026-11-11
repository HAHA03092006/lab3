# Kiểm thử model_builder

Dựng DistilBERT local: 1 layer, dim 16, hidden_dim 32, 2 heads; vocabulary nhỏ và head 2 lớp.
Trọng số random có chủ đích, fixture save_pretrained để kiểm tra đường đi Auto.from_pretrained thực.

1. Collator tạo batch có labels/mask/IDs.
2. build_model đọc config và safetensors local.
3. Forward trả logits shape (2,2), loss scalar.
4. count_params báo frozen=0, phù hợp full fine-tuning.
5. Inference/save/load tương đương được kiểm tra tích hợp ở test_engine.

Không kiểm tra chất lượng ngữ nghĩa trên model random. Việc tải encoder pretrained từ Hub thuộc notebook thật.

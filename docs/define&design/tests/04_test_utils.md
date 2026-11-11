# Kiểm thử utils/config

- save_json ghi dict hợp lệ; read_json trả đúng nội dung.
- Ghi NaN gây ValueError; file cũ giữ nguyên và không còn .tmp.
- check_action train vào folder nonempty gây FileExistsError.
- resume contract seed khác gây ValueError; cùng seed được qua guard.
- RunConfig từ chối path traversal trong run_id, epochs=0, max_length>512, warmup_ratio=1.

Các bảo vệ này nhằm tránh mất kết quả hoặc resume sai thí nghiệm; không yêu cầu người dùng xác nhận thêm trong code.

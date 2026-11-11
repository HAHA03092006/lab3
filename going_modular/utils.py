"""Seed, JSON nguyên tử, dấu vết phiên chạy và bảo vệ train/resume/reuse."""
import hashlib
import importlib.metadata
import json
import platform
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    try:
        temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def seed_everything(seed=42):
    from transformers import set_seed
    set_seed(seed)


def environment_info():
    import torch
    info = {'python': platform.python_version(), 'cuda_available': torch.cuda.is_available(),
            'device': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}
    for package in ('torch', 'transformers', 'datasets', 'evaluate', 'accelerate', 'numpy', 'scikit-learn'):
        try:
            info[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            info[package] = 'not installed'
    return info


def new_output_dir(root, run_id):
    now = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh'))
    path = Path(root) / now.strftime('%Y-%m-%d') / run_id / now.strftime('%H%M%S-%f')
    path.mkdir(parents=True, exist_ok=False)
    return path


def check_action(run_dir, action, contract):
    """Không xóa kết quả. Contract loại action/đường dẫn/giờ chạy ngay từ thiết kế."""
    run_dir = Path(run_dir)
    if action not in ('train', 'resume', 'reuse'):
        raise ValueError('action phải là train, resume hoặc reuse.')
    if action == 'train':
        if run_dir.exists() and any(run_dir.iterdir()):
            raise FileExistsError(f'{run_dir} đã có dữ liệu. Đổi run_id hoặc chọn resume/reuse.')
        return
    config_file = run_dir / 'config.json'
    if not config_file.is_file():
        raise FileNotFoundError(f'Thiếu {config_file}')
    if read_json(config_file)['contract'] != contract:
        raise ValueError('Cấu hình/dataset/tokenizer đã đổi. Tạo run_id mới; không resume/reuse nhầm run.')
    if action == 'resume' and (run_dir / 'completed.json').exists():
        raise ValueError('Run đã hoàn tất; chọn reuse.')
    if action == 'reuse':
        required = ['completed.json', 'history.json', 'best_model/config.json',
                    'best_model/model.safetensors', 'best_model/tokenizer_config.json']
        missing = [p for p in required if not (run_dir / p).is_file()]
        if missing:
            raise FileNotFoundError(f'Artifacts chưa hoàn tất: {missing}')

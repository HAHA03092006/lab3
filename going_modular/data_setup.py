"""IMDb -> chia phân tầng -> token IDs/mask; giữ raw text riêng để phân tích lỗi."""
import hashlib
import html
import re
from collections import Counter
import numpy as np
from sklearn.model_selection import train_test_split
from .utils import digest


def clean_text(text):
    # Giữ phủ định, dấu câu và thứ tự từ. Không bỏ stopwords/stemming.
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<br\s*/?>', ' ', text, flags=re.I))).strip()


def stratified_indices(labels, val_size, seed=42):
    labels = np.asarray(labels)
    if labels.ndim != 1 or set(labels.tolist()) != {0, 1}:
        raise ValueError('Cần nhãn nhị phân 0/1, có cả hai lớp.')
    if not isinstance(val_size, int) or not 2 <= val_size <= len(labels) - 2:
        raise ValueError('val_size phải chừa cả hai lớp cho train và validation.')
    train, val = train_test_split(np.arange(len(labels)), test_size=val_size,
                                 random_state=seed, stratify=labels)
    return sorted(train.tolist()), sorted(val.tolist())


def select_subset(dataset, limit, seed):
    if limit is None or limit == len(dataset):
        return dataset
    if not 2 <= limit < len(dataset):
        raise ValueError('Giới hạn tập con không hợp lệ.')
    # Không select(range(N)): IMDb thường sắp theo nhãn.
    selected, _ = train_test_split(np.arange(len(dataset)), train_size=limit,
                                  random_state=seed, stratify=dataset['label'])
    return dataset.select(sorted(selected.tolist()))


def prepare_raw_splits(raw, cfg):
    from datasets import DatasetDict
    train = raw['train'].add_column('sample_id', [f'train:{i}' for i in range(len(raw['train']))])
    test = raw['test'].add_column('sample_id', [f'test:{i}' for i in range(len(raw['test']))])
    train_idx, val_idx = stratified_indices(train['label'], cfg.val_size, cfg.seed)
    splits = DatasetDict(train=train.select(train_idx), validation=train.select(val_idx), test=test)
    for name, limit in [('train', cfg.train_limit), ('validation', cfg.val_limit), ('test', cfg.test_limit)]:
        splits[name] = select_subset(splits[name], limit, cfg.seed)
        splits[name] = splits[name].map(lambda row: {'text': clean_text(row['text'])})
    return splits


def split_manifest(splits):
    """Ghi cả ID và hash nội dung/nhãn: phát hiện dữ liệu đổi dù kích thước không đổi."""
    result = {}
    hashes = {}
    for name, dataset in splits.items():
        hashes[name] = {hashlib.sha256(x.encode()).hexdigest() for x in dataset['text']}
        result[name] = {'size': len(dataset), 'labels': dict(Counter(map(str, dataset['label']))),
                        'sample_ids': list(dataset['sample_id']),
                        'content_sha256': digest(list(zip(dataset['text'], dataset['label'])))}
    result['duplicate_text_overlap'] = {
        f'{a}__{b}': len(hashes[a] & hashes[b])
        for a, b in [('train', 'validation'), ('train', 'test'), ('validation', 'test')]}
    # Giữ split chuẩn của benchmark; công khai exact duplicates, không dùng test để sửa train.
    return result


def tokenize_splits(splits, tokenizer, max_length):
    def tokenize(batch):
        return tokenizer(batch['text'], truncation=True, max_length=max_length, padding=False)
    return splits.map(tokenize, batched=True,
                      remove_columns=['text', 'sample_id']).rename_column('label', 'labels')


def load_imdb(cfg, cache_dir=None):
    from datasets import load_dataset
    raw = load_dataset(cfg.dataset_id, revision=cfg.dataset_revision, cache_dir=cache_dir)
    return prepare_raw_splits(raw, cfg)

"""Cấu hình thí nghiệm: một nguồn dùng chung cho notebook, engine và kiểm thử."""
from dataclasses import asdict, dataclass

SENTIMENT_MODEL = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'
BASE_MODEL = 'distilbert/distilbert-base-uncased'
ID2LABEL = {0: 'NEGATIVE', 1: 'POSITIVE'}

@dataclass(frozen=True)
class RunConfig:
    run_id: str = 'distilbert_imdb_quick'
    model_id: str = BASE_MODEL
    model_revision: str = 'main'
    dataset_id: str = 'stanfordnlp/imdb'
    dataset_revision: str = 'main'
    profile: str = 'quick'
    seed: int = 42
    val_size: int = 5000
    train_limit: int | None = 2000
    val_limit: int | None = 500
    test_limit: int | None = 1000
    max_length: int = 128
    epochs: int = 2
    batch_size: int = 16
    eval_batch_size: int = 32
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    gradient_accumulation_steps: int = 1
    max_grad_norm: float = 1.0

    def __post_init__(self):
        if not self.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in self.run_id):
            raise ValueError('run_id chỉ gồm chữ, số, gạch ngang hoặc gạch dưới.')
        for key in ('val_size', 'epochs', 'batch_size', 'eval_batch_size', 'gradient_accumulation_steps'):
            if getattr(self, key) <= 0:
                raise ValueError(f'{key} phải dương.')
        if not 8 <= self.max_length <= 512:
            raise ValueError('max_length phải trong [8, 512] với DistilBERT.')
        if self.learning_rate <= 0 or self.weight_decay < 0 or self.max_grad_norm <= 0:
            raise ValueError('Sai learning_rate, weight_decay hoặc max_grad_norm.')
        if not 0 <= self.warmup_ratio < 1:
            raise ValueError('warmup_ratio phải trong [0, 1).')
        for key in ('train_limit', 'val_limit', 'test_limit'):
            if getattr(self, key) is not None and getattr(self, key) < 2:
                raise ValueError(f'{key} phải >= 2 hoặc None.')

    def to_dict(self):
        return asdict(self)

    @classmethod
    def for_profile(cls, profile='quick'):
        if profile == 'quick':
            return cls()
        if profile == 'full':
            return cls(run_id='distilbert_imdb_full', profile='full', train_limit=None,
                       val_limit=None, test_limit=None, max_length=256, epochs=3)
        raise ValueError('Chọn quick hoặc full.')

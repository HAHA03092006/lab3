"""Auto classes: ghép đúng tokenizer với checkpoint, logits [B,2]."""
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from .config import ID2LABEL


def load_tokenizer(model_id, revision='main'):
    return AutoTokenizer.from_pretrained(model_id, revision=revision, use_fast=True)


def build_model(model_id, revision='main'):
    return AutoModelForSequenceClassification.from_pretrained(
        model_id, revision=revision, num_labels=2,
        id2label=ID2LABEL, label2id={v: k for k, v in ID2LABEL.items()})


def count_params(model):
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {'total': total, 'trainable': trainable, 'frozen': total-trainable}


def tokenizer_identity(tokenizer):
    from .utils import digest
    return {'name': tokenizer.name_or_path, 'vocab_sha256': digest(tokenizer.get_vocab()),
            'special_tokens': tokenizer.special_tokens_map, 'padding_side': tokenizer.padding_side,
            'truncation_side': tokenizer.truncation_side}

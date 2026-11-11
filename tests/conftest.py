from pathlib import Path
import pytest
import torch
from datasets import Dataset, DatasetDict
from transformers import DistilBertConfig, DistilBertForSequenceClassification, DistilBertTokenizerFast
from going_modular.config import RunConfig
from going_modular.data_setup import prepare_raw_splits, tokenize_splits, split_manifest

torch.set_num_threads(2)

@pytest.fixture
def tiny_bundle(tmp_path):
    model_dir = tmp_path/'tiny_model'
    model_dir.mkdir()
    vocab = ['[PAD]','[UNK]','[CLS]','[SEP]','[MASK]','good','bad','movie','this','is','very','not','.']
    (model_dir/'vocab.txt').write_text('\n'.join(vocab),encoding='utf-8')
    tokenizer = DistilBertTokenizerFast(vocab_file=str(model_dir/'vocab.txt'), do_lower_case=True)
    tokenizer.save_pretrained(model_dir)
    model = DistilBertForSequenceClassification(DistilBertConfig(vocab_size=len(vocab),
        dim=16, hidden_dim=32, n_layers=1, n_heads=2, max_position_embeddings=64,
        num_labels=2, dropout=0, attention_dropout=0, seq_classif_dropout=0,
        id2label={0:'NEGATIVE',1:'POSITIVE'},label2id={'NEGATIVE':0,'POSITIVE':1}))
    model.save_pretrained(model_dir)
    def dataset(n):
        return Dataset.from_dict({'text':['this is a '+('good' if i%2 else 'bad')+f' movie {i}' for i in range(n)],
                                  'label':[i%2 for i in range(n)]})
    raw = DatasetDict(train=dataset(24),test=dataset(8))
    cfg = RunConfig(run_id='tiny_integration',model_id=str(model_dir), profile='synthetic_test',
                    val_size=8, train_limit=None,val_limit=None,test_limit=None,
                    epochs=2,batch_size=4,eval_batch_size=4,max_length=32)
    splits=prepare_raw_splits(raw,cfg)
    encoded=tokenize_splits(splits,tokenizer,cfg.max_length)
    return cfg,tokenizer,splits,encoded,split_manifest(splits)

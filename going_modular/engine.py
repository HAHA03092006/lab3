"""Trainer orchestration. Test set không được đưa vào Trainer khi train."""
from pathlib import Path
import math
import torch
from transformers import Trainer, TrainingArguments, DataCollatorWithPadding, AutoModelForSequenceClassification
from transformers.trainer_utils import get_last_checkpoint
from .evaluate import compute_metrics
from .model_builder import build_model, count_params, tokenizer_identity
from .utils import check_action, digest, environment_info, read_json, save_json, seed_everything


def make_training_args(cfg, run_dir, logging_dir):
    return TrainingArguments(
        output_dir=str(Path(run_dir)/'checkpoints'), logging_dir=str(logging_dir),
        num_train_epochs=cfg.epochs, learning_rate=cfg.learning_rate,
        per_device_train_batch_size=cfg.batch_size, per_device_eval_batch_size=cfg.eval_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        weight_decay=cfg.weight_decay, warmup_ratio=cfg.warmup_ratio,
        lr_scheduler_type='linear', optim='adamw_torch', max_grad_norm=cfg.max_grad_norm,
        eval_strategy='epoch', save_strategy='epoch', logging_strategy='steps', logging_steps=10,
        logging_first_step=True, save_total_limit=2, load_best_model_at_end=True,
        metric_for_best_model='f1', greater_is_better=True,
        report_to=['tensorboard'], seed=cfg.seed, data_seed=cfg.seed,
        fp16=False, bf16=False, dataloader_num_workers=0,
        dataloader_pin_memory=torch.cuda.is_available(), push_to_hub=False,
        save_safetensors=True)


def run_experiment(cfg, tokenized, tokenizer, manifest, artifact_root, log_root, action='train', callbacks=None):
    """Trả Trainer đã nạp best weights, history, run_dir. Không đánh giá test ở đây."""
    run_dir = Path(artifact_root)/cfg.run_id
    contract = {'run_config': cfg.to_dict(), 'data_sha256': digest(manifest),
                'tokenizer': tokenizer_identity(tokenizer)}
    check_action(run_dir, action, contract)
    checkpoint = None
    if action == 'resume':
        checkpoint = get_last_checkpoint(str(run_dir/'checkpoints')) if (run_dir/'checkpoints').exists() else None
        if checkpoint is None:
            raise FileNotFoundError('Không có checkpoint-* để resume; checkpoint được lưu cuối mỗi epoch.')
        state = read_json(Path(checkpoint)/'trainer_state.json')
        if state.get('epoch',0) >= cfg.epochs:
            raise ValueError('Checkpoint đã đủ epoch nhưng export chưa hoàn tất. Xem docs/03_engine.md để phục hồi.')
    seed_everything(cfg.seed)
    if action == 'reuse':
        model = AutoModelForSequenceClassification.from_pretrained(run_dir/'best_model')
    else:
        model = build_model(cfg.model_id, cfg.model_revision)
    args = make_training_args(cfg, run_dir, Path(log_root)/cfg.run_id)
    trainer = Trainer(model=model, args=args, train_dataset=tokenized['train'],
                      eval_dataset=tokenized['validation'], processing_class=tokenizer,
                      data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
                      compute_metrics=compute_metrics, callbacks=callbacks)
    if action == 'reuse':
        return trainer, read_json(run_dir/'history.json'), run_dir
    if action == 'train':
        run_dir.mkdir(parents=True,exist_ok=True)
        save_json(run_dir/'config.json', {'contract':contract, 'environment':environment_info(),
                  'parameters':count_params(model), 'resolved_model_revision':getattr(model.config,'_commit_hash',None)})
        save_json(run_dir/'split_manifest.json', manifest)
    trainer.train(resume_from_checkpoint=checkpoint)
    history = trainer.state.log_history
    save_json(run_dir/'history.json', history)
    # Nếu callback/người dùng dừng sớm, không gắn nhãn run đã hoàn tất.
    if (trainer.state.epoch or 0) + 1e-8 < cfg.epochs:
        raise InterruptedError('Train dừng trước đủ epoch; dùng resume để tiếp tục từ checkpoint gần nhất.')
    trainer.save_model(str(run_dir/'best_model'))
    tokenizer.save_pretrained(run_dir/'best_model')
    trainer.save_state()
    save_json(run_dir/'completed.json', {'epoch':trainer.state.epoch, 'global_step':trainer.state.global_step,
              'best_metric':trainer.state.best_metric, 'best_checkpoint':trainer.state.best_model_checkpoint})
    return trainer, history, run_dir

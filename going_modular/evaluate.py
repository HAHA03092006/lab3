"""Độ đo nhị phân, suy luận theo batch và xuất bằng chứng thực nghiệm."""
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_auc_score
from .utils import save_json
from .config import ID2LABEL


def metrics_from_logits(logits, labels):
    logits, labels = np.asarray(logits), np.asarray(labels)
    if logits.ndim != 2 or logits.shape[1] != 2 or labels.shape != (len(logits),) or not len(labels):
        raise ValueError('Cần logits [N,2] và labels [N], N>0.')
    if not np.isfinite(logits).all() or not set(labels.tolist()) <= {0, 1}:
        raise ValueError('Logits/labels không hợp lệ.')
    pred = logits.argmax(axis=-1)
    p, r, f, _ = precision_recall_fscore_support(labels, pred, average='binary', zero_division=0)
    macro = precision_recall_fscore_support(labels, pred, average='macro', labels=[0,1], zero_division=0)[2]
    return {'accuracy': float(accuracy_score(labels, pred)), 'precision': float(p),
            'recall': float(r), 'f1': float(f), 'macro_f1': float(macro)}


def compute_metrics(eval_prediction):
    logits = eval_prediction.predictions
    if isinstance(logits, tuple):
        logits = logits[0]
    return metrics_from_logits(logits, eval_prediction.label_ids)


def predict_texts(model, tokenizer, texts, max_length=128, batch_size=16):
    import torch
    if not texts or batch_size <= 0:
        raise ValueError('texts phải khác rỗng; batch_size phải dương.')
    model.eval()
    device = next(model.parameters()).device
    rows = []
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            group = texts[start:start+batch_size]
            inputs = tokenizer(group, truncation=True, padding=True, max_length=max_length, return_tensors='pt')
            probs = model(**{k:v.to(device) for k,v in inputs.items()}).logits.softmax(-1).cpu()
            for text, prob in zip(group, probs):
                pred = int(prob.argmax())
                rows.append({'text': text, 'label_id': pred, 'label': model.config.id2label[pred],
                             'confidence': float(prob[pred]), 'p_positive': float(prob[1])})
    return rows


def export_evaluation(prediction, raw_test, output_dir, metadata):
    import pandas as pd
    import matplotlib.pyplot as plt
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logits = prediction.predictions[0] if isinstance(prediction.predictions, tuple) else prediction.predictions
    labels = np.asarray(prediction.label_ids)
    if not np.array_equal(labels, np.asarray(raw_test['label'])):
        raise ValueError('Thứ tự nhãn dự đoán không khớp raw test.')
    metrics = metrics_from_logits(logits, labels)
    z = logits - logits.max(axis=1, keepdims=True)
    probs = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
    pred = logits.argmax(-1)
    cm = confusion_matrix(labels, pred, labels=[0,1])
    metrics.update({'num_samples': len(labels), 'confusion_matrix': cm.tolist(),
                    'roc_auc': float(roc_auc_score(labels, probs[:,1])) if len(set(labels)) == 2 else None,
                    'trainer_metrics': {k:float(v) for k,v in prediction.metrics.items()}, 'metadata': metadata})
    save_json(output_dir / 'test_metrics.json', metrics)
    frame = pd.DataFrame({'sample_id': raw_test['sample_id'], 'text': raw_test['text'],
                          'y_true': labels, 'y_pred': pred, 'p_positive': probs[:,1],
                          'confidence': probs.max(axis=1)})
    frame.to_csv(output_dir / 'predictions.csv', index=False)
    frame[frame.y_true != frame.y_pred].sort_values('confidence', ascending=False).head(20).to_csv(output_dir/'errors.csv', index=False)
    fig, ax = plt.subplots(figsize=(5,4))
    ax.imshow(cm, cmap='Blues')
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i,j]), ha='center', va='center', color='white' if cm[i,j]>cm.max()/2 else 'black')
    ax.set(xticks=[0,1], yticks=[0,1], xticklabels=['Negative','Positive'],
           yticklabels=['Negative','Positive'], xlabel='Predicted', ylabel='True', title='IMDb test confusion matrix')
    fig.tight_layout(); fig.savefig(output_dir/'confusion_matrix.png', dpi=160); plt.close(fig)
    return metrics


def plot_history(history, output_path):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1,2,figsize=(11,4))
    for key, ax in [('loss',axes[0]), ('eval_loss',axes[0]), ('eval_accuracy',axes[1]), ('eval_f1',axes[1])]:
        rows = [r for r in history if key in r]
        if rows:
            ax.plot([r.get('epoch',r['step']) for r in rows], [r[key] for r in rows], marker='o',label=key)
    for ax in axes:
        ax.set_xlabel('Epoch'); ax.grid(alpha=.25)
        if ax.lines: ax.legend()
    axes[0].set_title('Loss'); axes[1].set_title('Validation metrics')
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    fig.tight_layout();fig.savefig(output_path,dpi=160);plt.close(fig)

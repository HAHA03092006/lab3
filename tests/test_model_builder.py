from transformers import DataCollatorWithPadding
from going_modular.model_builder import build_model, count_params

def test_logits_loss_and_all_trainable(tiny_bundle):
    cfg,tok,_,encoded,_=tiny_bundle
    model=build_model(cfg.model_id)
    batch=DataCollatorWithPadding(tok)([encoded['train'][0],encoded['train'][1]])
    result=model(**batch)
    assert tuple(result.logits.shape)==(2,2)
    assert result.loss.ndim==0
    assert count_params(model)['frozen']==0

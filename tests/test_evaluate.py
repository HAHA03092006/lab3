from types import SimpleNamespace
import numpy as np
import pytest
from going_modular.evaluate import metrics_from_logits, compute_metrics, export_evaluation

def test_hand_calculated_metrics():
    logits=np.array([[2,0],[0,2],[2,0],[0,2]])
    labels=np.array([0,1,1,1])
    result=metrics_from_logits(logits,labels)
    assert result['accuracy']==.75
    assert result['precision']==1
    assert result['recall']==pytest.approx(2/3)
    assert result['f1']==pytest.approx(.8)
    assert result==compute_metrics(SimpleNamespace(predictions=logits,label_ids=labels))

def test_missing_predicted_class_no_nan():
    r=metrics_from_logits([[2,0],[2,0]],[0,1])
    assert r['precision']==0 and r['f1']==0

@pytest.mark.parametrize('logits,labels',[([],[]),([[1,2,3]],[0]),([[float('nan'),1]],[1]),([[1,2]],[2])])
def test_bad_metrics_inputs(logits,labels):
    with pytest.raises(ValueError):metrics_from_logits(logits,labels)

def test_export_and_alignment(tiny_bundle,tmp_path):
    _,_,raw,_,_=tiny_bundle
    labels=np.asarray(raw['test']['label'])
    logits=np.eye(2)[labels]*2
    p=SimpleNamespace(predictions=logits,label_ids=labels,metrics={'test_loss':.1})
    result=export_evaluation(p,raw['test'],tmp_path/'eval',{'kind':'synthetic'})
    assert result['accuracy']==1
    assert (tmp_path/'eval/confusion_matrix.png').is_file()
    p.label_ids=1-labels
    with pytest.raises(ValueError):export_evaluation(p,raw['test'],tmp_path/'bad',{})

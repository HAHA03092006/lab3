import numpy as np
import pytest
from transformers import TrainerCallback
from going_modular.engine import run_experiment
from going_modular.evaluate import predict_texts
from going_modular.utils import read_json

class StopAfterFirstCheckpoint(TrainerCallback):
    def on_save(self,args,state,control,**kwargs):
        if state.epoch >= 1:control.should_training_stop=True
        return control


def test_real_trainer_resume_reuse_roundtrip(tiny_bundle,tmp_path):
    cfg,tok,raw,data,manifest=tiny_bundle
    args=(cfg,data,tok,manifest,tmp_path/'artifacts',tmp_path/'logs')
    with pytest.raises(InterruptedError):
        run_experiment(*args,action='train',callbacks=[StopAfterFirstCheckpoint()])
    run=tmp_path/'artifacts'/cfg.run_id
    assert not (run/'completed.json').exists()
    assert (run/'checkpoints/checkpoint-4/optimizer.pt').is_file()
    trainer,history,_=run_experiment(*args,action='resume')
    assert trainer.state.global_step==8
    assert trainer.state.epoch==2
    assert read_json(run/'completed.json')['global_step']==8
    before=predict_texts(trainer.model,tok,['good movie','bad movie'])
    reused,loaded,_=run_experiment(*args,action='reuse')
    after=predict_texts(reused.model,tok,['good movie','bad movie'])
    assert np.allclose([x['p_positive'] for x in before],[x['p_positive'] for x in after],atol=1e-7)
    assert history==loaded
    assert len([x for x in history if 'eval_f1' in x])==2
    with pytest.raises(FileExistsError):run_experiment(*args,action='train')
    with pytest.raises(ValueError):run_experiment(*args,action='resume')

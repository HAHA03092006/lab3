import pytest
from going_modular.utils import save_json,read_json,check_action
from going_modular.config import RunConfig

def test_atomic_json_preserves_original(tmp_path):
    p=tmp_path/'value.json'
    save_json(p,{'ok':1})
    with pytest.raises(ValueError):save_json(p,{'bad':float('nan')})
    assert read_json(p)=={'ok':1}
    assert not p.with_suffix('.json.tmp').exists()

def test_guard_nonempty_and_config_mismatch(tmp_path):
    run=tmp_path/'run';run.mkdir()
    save_json(run/'config.json',{'contract':{'seed':42}})
    with pytest.raises(FileExistsError):check_action(run,'train',{})
    with pytest.raises(ValueError):check_action(run,'resume',{'seed':43})
    check_action(run,'resume',{'seed':42})

@pytest.mark.parametrize('kw',[{'run_id':'../x'},{'epochs':0},{'max_length':513},{'warmup_ratio':1}])
def test_config_validation(kw):
    with pytest.raises(ValueError):RunConfig(**kw)

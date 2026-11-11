import pytest
from going_modular.data_setup import stratified_indices, clean_text, split_manifest

def test_split_balanced_disjoint_reproducible():
    labels=[0]*50+[1]*50
    train,val=stratified_indices(labels,20,42)
    assert set(train).isdisjoint(val)
    assert sorted(train+val)==list(range(100))
    assert sum(labels[i] for i in val)==10
    assert (train,val)==stratified_indices(labels,20,42)
    assert val!=stratified_indices(labels,20,43)[1]

@pytest.mark.parametrize('labels,size',[([],2),([0,0,0,0],2),([0,1,0,1],1),([0,1,0,1],4),([0,2,0,2],2)])
def test_invalid_split(labels,size):
    with pytest.raises(ValueError):stratified_indices(labels,size)

def test_clean_keeps_negation():
    assert clean_text(' Not<br /> bad &amp; good!  ')=='Not bad & good!'

def test_tokenization_and_identity(tiny_bundle):
    cfg,tok,raw,encoded,manifest=tiny_bundle
    assert len(raw['train'])==16 and len(raw['validation'])==8
    assert set(raw['train']['sample_id']).isdisjoint(raw['validation']['sample_id'])
    assert set(encoded['train'].column_names)=={'input_ids','attention_mask','labels'}
    assert max(map(len,encoded['train']['input_ids']))<=cfg.max_length
    assert manifest==split_manifest(raw)

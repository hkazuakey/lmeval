from lmeval import LMModel
from lmeval.enums import Modality
def test_lmmodel():
    mdl = LMModel(name='test', publisher='publisher', modalities=[Modality.text])
    json = mdl.model_dump_json()
    mdl2 = LMModel.model_validate_json(json)
    assert Modality.text.value in mdl2.modalities
    assert len(mdl2.modalities) == 1
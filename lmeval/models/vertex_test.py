from lmeval.models.vertex import VertexModel
from lmeval.evaluator import Evaluator
from .tests_utils import eval_single_text_generation, eval_batch_text_generation, eval_image_analysis


def test_vertex_single_text_generation():
    eval_single_text_generation(VertexModel())

def test_vertex_batch_text_generation():
    eval_batch_text_generation(VertexModel())

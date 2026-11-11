from pathlib import Path
import ast
import nbformat

def test_notebook_schema_and_python_cells():
    path=Path(__file__).resolve().parents[1]/'notebooks/huggingface_sentiment.ipynb'
    nb=nbformat.read(path,as_version=4)
    nbformat.validate(nb)
    for c in nb.cells:
        if c.cell_type=='code':ast.parse(c.source)

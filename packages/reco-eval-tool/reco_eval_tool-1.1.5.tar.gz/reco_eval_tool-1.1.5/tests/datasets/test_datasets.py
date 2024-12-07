import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2])) 

import reco_eval_tool


demo_path = Path.joinpath(Path(__file__).resolve().parents[0], 'demo')
file1_path = Path.joinpath(demo_path, 'file1.tsv')

df = reco_eval_tool.datasets.load_file(file1_path)
print(df)
assert df.shape == (2, 2)

df = reco_eval_tool.datasets.load_dir(demo_path)
print(df)
assert df.shape == (4, 2)

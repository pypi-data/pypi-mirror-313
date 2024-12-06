
```python

>>> from argparse import Namespace
>>> from src.virulencefinder.cge.config import Config
>>> import os
>>> db = os.environ.get("CGE_VIRULENCEFINDER_DB")
>>> class TestArgs():
...     def __init__(self):
...             self.inputfasta = "./tests/data/test_isolate_02.fa"
...             self.inputfastq = None
...             self.outputPath = "./tests/tmp_out/"
...             self.blastPath = None
...             self.kmaPath = None
...             self.databases = None
...             self.min_cov = None
...             self.threshold = None
...             self.nanopore = False     # Tested?
...             self.out_json = None      # Tested?
...             self.db_path = db
...             self.speciesinfo_json = None
...             self.nanopore = False
...             self.tmp_dir = None
...             self.extended_output = None
...             self.db_path_vir_kma = None  
...             self.overlap = 30          
>>> args = TestArgs()
>>> conf = Config(args)

```

## Test - get_software_exec_res

```python
>>> from src.virulencefinder.helper_scripts.software_executions import get_software_exec_res
>>> assert list(get_software_exec_res(conf).keys()) == ['type', 'command', 'parameters', 'key']
>>> assert list(get_software_exec_res(conf).get("parameters").keys()) ==  ['virulence_finder_root', 'env_var_file', 'outputPath', 'tmp_dir', 'out_json', 'speciesinfo_json', 'inputfastq_1', 'inputfasta', 'outPath_blast', 'sample_name', 'blast', 'kma', 'aligner', 'db_path_vir', 'db_path_vir_kma', 'db_config_file', 'db_notes_file', 'min_cov', 'min_id', 'overlap', 'databases', 'species'], "Actual keys are: " + str(list(get_software_exec_res(conf).get("parameters").keys()))

```

# PhenotypeResult tests

## General setup for tests

```python
>>> import os
>>> import json
>>> from src.virulencefinder.cge.phenotype_scraping import PhenotypeResult
>>> from src.virulencefinder.cge.config import Config

>>> with open(os.path.join(os.getcwd(), "tests", "data", "example_res.json"), "r") as f:
...     res = json.load(f)
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
...             self.db_path = db # needs to be 
...             self.speciesinfo_json = None
...             self.nanopore = False
...             self.tmp_dir = None
...             self.extended_output = None
...             self.db_path_vir_kma = None  
...             self.overlap = 30          
>>> args = TestArgs()
>>> conf = Config(args)

```

## Test - General functionality

```python
>>> TestPheno = PhenotypeResult(region_key = "stx1;;1;;M24352_1", region_name = "stx1", db_notes_file = conf.db_notes_file)

```

## Test Protein Function isolation

```python
>>> TestPheno = PhenotypeResult(region_key = "astA;;1;;AF161000", region_name = "astA", db_notes_file = conf.db_notes_file)
>>> TestPheno["function"]
'Heat-stable enterotoxin EAST-1'

```

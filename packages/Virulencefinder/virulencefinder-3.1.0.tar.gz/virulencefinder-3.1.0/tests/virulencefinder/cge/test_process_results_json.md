# process_results_json test

## Setup

```python
>>> import os
>>> import json
>>> from virulencefinder.cge.config import Config
>>> from cgecore.output.result import Result

>>> with open(os.path.join(os.getcwd(), "tests", "data", "res_collection_example.json"), "r") as f:
...     res_collection_data = json.load(f)
>>> with open(os.path.join(os.getcwd(), "tests", "data", "example_result_handler.json"), "r") as f:
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
...             self.db_path = db
...             self.speciesinfo_json = None
...             self.nanopore = False
...             self.tmp_dir = None
...             self.extended_output = None
...             self.db_path_vir_kma = None  
...             self.overlap = 30          
>>> args = TestArgs()
>>> conf = Config(args)

>>> res_collection = Result.init_software_result(name="VirulenceFinder", gitdir=None)
>>> res_collection.update(res_collection_data)

```

## Test - General functionality

```python
>>> from virulencefinder.cge.process_results_json import VirulenceFinderResultHandler
>>> from virulencefinder.__init__ import __version__
>>> from cgecore.output.result import Result 

>>> std_result = Result.init_software_result(
...        name="VirulenceFinder",
...        gitdir=f"{os.getcwd()}/../../")
>>> init_result_data = {
...        "software_version": __version__,
...        "key": f"VirulenceFinder-{__version__}",}
>>> std_result.init_database("VirulenceFinder", conf.db_path_vir)

>>> TestVir = VirulenceFinderResultHandler.standardize_results(res_collection = std_result, results = res, conf=conf)

```


## Test - add_gene_result_if_key_not_None 

Test for key = None. That means that the function returns nothing

```python	

>>> from src.virulencefinder.cge.process_results_json import add_gene_result_if_key_not_None
>>> from src.virulencefinder.cge.gene_result import GeneResult
>>> with open(os.path.join(os.getcwd(), "tests", "data", "example_res.json"), "r") as f: res_single = json.load(f)
>>> gene_result_blast = GeneResult(res_collection=res_collection, res=res_single, ref_db_name="VirulenceFinder", ref_db_sub="test", conf=conf)
>>> gene_result_blast["key"] = None
>>> add_gene_result_if_key_not_None(gene_result_blast,res_collection, "seq_regions")

```

## Test2 - add gene_result_if_key_not_None
Test for if key not in res_collection

```python
>>> res_collection["seq_regions"] = "asdjkladf"
>>> gene_result_blast = GeneResult(res_collection = std_result,res = res_single, ref_db_name = "VirulenceFinder", ref_db_sub="test", conf=conf)
>>> gene_result_blast["key"] = "test"
>>> add_gene_result_if_key_not_None(gene_result_blast,std_result, "seq_regions")
>>> assert std_result["seq_regions"]["test"] == gene_result_blast

```



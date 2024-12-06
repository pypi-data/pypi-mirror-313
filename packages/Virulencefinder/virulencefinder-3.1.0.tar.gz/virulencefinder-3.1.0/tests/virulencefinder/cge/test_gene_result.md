# Test GeneResult class

## Setup

```python
>>> import os
>>> import json
>>> import subprocess
>>> from cgecore.output.result import Result
>>> from virulencefinder.cge.gene_result import GeneResult
>>> from virulencefinder.cge.config import Config
>>> with open(os.path.join(os.getcwd(), "tests", "data", "example_res.json"), "r") as f:
...     res = json.load(f)
>>> with open(os.path.join(os.getcwd(), "tests", "data", "res_collection_example.json"), "r") as f:
...     res_collection_data = json.load(f)
>>> db = os.environ.get("CGE_VIRULENCEFINDER_DB")
>>> ref_db_path = db # needs to be adjusted

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

>>> res_collection = Result.init_software_result(name="VirulenceFinder", gitdir=None)
>>> res_collection.update(res_collection_data)

```

## Test - General functionality

```python
>>> gene_result_blast = GeneResult(res_collection=res_collection, res=res, ref_db_name="VirulenceFinder", ref_db_sub="test", conf=conf)
>>> keys_result = list(gene_result_blast.keys())
>>> assert "gene" in keys_result
>>> assert "name" in keys_result
>>> assert "identity" in keys_result
>>> assert "ref_database" in keys_result
>>> assert "alignment_length" in keys_result
>>> assert "ref_seq_length" in keys_result
>>> assert "ref_start_pos" in keys_result
>>> assert "ref_end_pos" in keys_result
>>> assert "query_id" in keys_result
>>> assert "query_start_pos" in keys_result
>>> assert "query_end_pos" in keys_result
>>> assert "phenotypes" in keys_result
>>> assert "grade" in keys_result
>>> assert "coverage" in keys_result
>>> assert "key" in keys_result

```



### remove_NAs()

```python
>>> gene_result_blast["test_NA"] = "NA"
>>> gene_result_blast["test_None"] = None
>>> gene_result_blast.remove_NAs()
>>> assert("test_NA" not in gene_result_blast)
>>> assert("test_None" not in gene_result_blast)

```

### calc_gene_grade(coverage: float, identity: float) -> int

```python

>>> GeneResult.calc_gene_grade(coverage=100, identity=100)
3
>>> GeneResult.calc_gene_grade(coverage=100, identity=22.5)
2
>>> GeneResult.calc_gene_grade(coverage=10.1, identity=0)
1

```

## Test - random_string

```python
length_string = 5
rand_string = GeneResult(res_collection = res_collection,res = res, ref_db_path = ref_db_path, alignments = True).random_string(str_len = length_string)
print(len(rand_string))
length_string

```

### _get_unique_gene_key(res_collection, delimiter)

```python

>>> import copy
>>> res_unique_gene_test_blast = copy.deepcopy(res_collection)

>>> gene_result_blast._get_unique_gene_key(res_unique_gene_test_blast)
'astA;;1;;AF161000'
>>> from cgecore.output.result import Result
>>> res_unique_gene_test_blast = Result.init_software_result(name="ResFinder", gitdir=".")
>>> res_unique_gene_test_blast.add_class(cl="seq_regions", **gene_result_blast)
>>> gene_result_blast["query_id"] = "Contig02"
>>> output = gene_result_blast._get_unique_gene_key(res_unique_gene_test_blast)
>>> rand_string = output.split(";;")[-1]
>>> assert output == 'astA;;1;;AF161000;;' + rand_string  
	
```

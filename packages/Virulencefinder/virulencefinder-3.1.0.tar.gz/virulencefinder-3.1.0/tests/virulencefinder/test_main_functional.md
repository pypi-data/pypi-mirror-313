# Functional tests

These tests are meant to test the general functionality of the program. Thus, they look at the input and output and verify if a test run works. This is indicated by the output "CompletedProcess" and the presence of returncode=0.

**NOTE** CGE_VIRULENCEFINDER_DB must be defined as an environment variable for the tests to work. Further the database needs to be indexed with kma before you can run these tests.

## Setup

kma path

```python
>>> import os
>>> import subprocess
>>> kma_path = os.environ.get('CGE_KMA')
>>> if kma_path is None:
...     kma_path = "kma"
>>> db = os.environ.get("CGE_VIRULENCEFINDER_DB")

``` 

```python
if not os.path.isdir("./tests/tmp_out"):
    os.makedirs("./tests/tmp_out")

```

## Test - Listeria - GCF_000196035.1

```python
>>> import subprocess
>>> import json
>>> input_fastq1 = "tests/data/listeria/test_isolate_listeria_ne_1.fq.gz"
>>> input_fastq2 = "tests/data/listeria/test_isolate_listeria_ne_2.fq.gz"
>>> script_path = "src.virulencefinder.__main__"

>>> result = subprocess.run(["pdm", "run", "python","-m", script_path, "-ifq", input_fastq1, input_fastq2, "-p", db, "-k", kma_path, "-o", "./tests/tmp_out", "-d", "listeria"])

>>> expected_args = ['pdm', 'run', 'python', '-m', 'src.virulencefinder.__main__', '-ifq', 'tests/data/listeria/test_isolate_listeria_ne_1.fq.gz', 'tests/data/listeria/test_isolate_listeria_ne_2.fq.gz', '-p', db, '-k', kma_path, '-o', './tests/tmp_out', '-d', 'listeria']

>>> assert result.args == expected_args
>>> assert result.returncode == 0
>>> with open("tests/tmp_out/test_isolate_listeria_ne_1.json", "r") as f:
...     output = json.load(f)
>>> assert len(output["seq_regions"]) != 0

```

```python
>>> import shutil
>>> import glob
>>> shutil.rmtree("tests/tmp_out/virulencefinder_kma")
>>> import os
>>> for file in glob.glob("./tests/tmp_out/*.json"):
...     os.remove(file)

```

## Test - s_aureus - GCF_02055555.1



```python
>>> import subprocess
>>> input_fastq1 = "tests/data/s_aureus/test_isolate_s_aureus_ne_1.fq.gz"
>>> input_fastq2 = "tests/data/s_aureus/test_isolate_s_aureus_ne_2.fq.gz"
>>> script_path = "src.virulencefinder.__main__"
>>> result = subprocess.run(["pdm", "run", "python","-m", script_path, "-ifq", input_fastq1, input_fastq2, "-p", db, "-k", kma_path, "-o", "./tests/tmp_out", "-d", "s.aureus_exoenzyme,s.aureus_hostimm,s.aureus_toxin"])
>>> expected_args = ['pdm', 'run', 'python', '-m', 'src.virulencefinder.__main__', '-ifq', 'tests/data/s_aureus/test_isolate_s_aureus_ne_1.fq.gz', 'tests/data/s_aureus/test_isolate_s_aureus_ne_2.fq.gz', '-p', db, '-k', kma_path, '-o', './tests/tmp_out', '-d', 's.aureus_exoenzyme,s.aureus_hostimm,s.aureus_toxin']
>>> assert result.args == expected_args
>>> assert result.returncode == 0
>>> with open("tests/tmp_out/test_isolate_s_aureus_ne_1.json", "r") as f:
...     output = json.load(f)
>>> assert len(output["seq_regions"]) != 0

```

```python
>>> import shutil
>>> import glob
>>> shutil.rmtree("tests/tmp_out/virulencefinder_kma")
>>> for file in glob.glob(".tests/tmp_out/*.json"):
...     os.remove(file)

```

## Test - e_coli - GCF_0300134435.1

```python
>>> import subprocess
>>> input_fastq1 = "tests/data/e_coli/test_isolate_e_coli1_ne.fq.gz"
>>> input_fastq2 = "tests/data/e_coli/test_isolate_e_coli2_ne.fq.gz"
>>> script_path = "src.virulencefinder.__main__"
>>> result = subprocess.run(["pdm", "run", "python","-m", script_path, "-ifq", input_fastq1, input_fastq2, "-p", db, "-k", kma_path, "-o", "./tests/tmp_out", "-d", "virulence_ecoli"])
>>> expected_args = ['pdm', 'run', 'python', '-m', 'src.virulencefinder.__main__', '-ifq', 'tests/data/e_coli/test_isolate_e_coli1_ne.fq.gz', 'tests/data/e_coli/test_isolate_e_coli2_ne.fq.gz', '-p', db, '-k', kma_path, '-o', './tests/tmp_out', '-d', 'virulence_ecoli']
>>> assert result.args == expected_args
>>> assert result.returncode == 0
>>> with open("tests/tmp_out/test_isolate_e_coli1_ne.json", "r") as f:
...     output = json.load(f)
>>> assert len(output["seq_regions"]) != 0 # print seq_regions to see that it found something

```

```python
>>> import shutil
>>> import glob
>>> shutil.rmtree("tests/tmp_out/virulencefinder_kma")
>>> for file in glob.glob(".tests/tmp_out/*.json"):
...     os.remove(file)

```

## Test - Enterococcus - GCF_009697285.1

```python
>>> import subprocess
>>> input_fastq1 = "tests/data/enterococcus/test_isolate_enterococcus_1_ne.fq.gz"
>>> input_fastq2 = "tests/data/enterococcus/test_isolate_enterococcus_2_ne.fq.gz"
>>> script_path = "src.virulencefinder.__main__"
>>> result = subprocess.run(["pdm", "run", "python","-m", script_path, "-ifq", input_fastq1, input_fastq2, "-p", db, "-k", kma_path, "-o", "./tests/tmp_out", "-d", "virulence_entfm_entls"])
>>> expected_args = ['pdm', 'run', 'python', '-m', 'src.virulencefinder.__main__', '-ifq', 'tests/data/enterococcus/test_isolate_enterococcus_1_ne.fq.gz', 'tests/data/enterococcus/test_isolate_enterococcus_2_ne.fq.gz', '-p', db, '-k', kma_path, '-o', './tests/tmp_out', '-d', 'virulence_entfm_entls']
>>> assert result.args == expected_args
>>> assert result.returncode == 0
>>> with open("tests/tmp_out/test_isolate_enterococcus_1_ne.json", "r") as f:
...     output = json.load(f)
>>> assert len(output["seq_regions"]) != 0 # print seq_regions to see that it found something

```

### Test general output

```python
>>> keys_regions = list(output.keys())
>>> assert "type" in keys_regions
>>> assert "databases" in keys_regions
>>> assert "seq_regions" in keys_regions
>>> assert "software_executions" in keys_regions
>>> assert "seq_variations" in keys_regions
>>> assert "phenotypes" in keys_regions

```


```python
>>> import shutil
>>> import glob
>>> shutil.rmtree("tests/tmp_out/virulencefinder_kma")
>>> for file in glob.glob("./tests/tmp_out/*.json"):
...     os.remove(file)

```


## Test output flag

```python
>>> import os
>>> input_fasta = os.path.join(os.getcwd(), "tests", "data", "test_isolate_02.fa")
>>> result = subprocess.run(["pdm", "run","python", "-m", "src.virulencefinder.__main__", "-p", db, "-o", "tmp", "-ifa", input_fasta, '-o', './tests/tmp_out'])
>>> expected_args = ['pdm', 'run', 'python', '-m', 'src.virulencefinder.__main__', '-p', db, '-o', 'tmp', '-ifa', input_fasta, '-o', './tests/tmp_out']
>>> assert result.args == expected_args
>>> assert result.returncode == 0

```



## Test database

```python
>>> import os
>>> input_fasta = os.path.join(os.getcwd(), "tests", "data", "test_isolate_02.fa")
>>> result = subprocess.run(["pdm", "run","python", "-m", "src.virulencefinder.__main__", "-d", "all", "-p", db, "-o", "tmp", "-ifa", input_fasta, '-o', './tests/tmp_out'])
>>> expected_args = ['pdm', 'run', 'python', '-m', 'src.virulencefinder.__main__', '-d', 'all', "-p", db, '-o', 'tmp', '-ifa', input_fasta, '-o', './tests/tmp_out']
>>> assert result.args == expected_args
>>> assert result.returncode == 0

```
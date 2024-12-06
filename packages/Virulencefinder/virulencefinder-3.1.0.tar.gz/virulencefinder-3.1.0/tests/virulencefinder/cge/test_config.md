# Config class tests

```python

>>> import os
>>> your_db_path = os.environ.get("CGE_VIRULENCEFINDER_DB")

```

```python
>>> from virulencefinder.cge.config import Config
>>> import os
>>> import subprocess
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
...             self.db_path = your_db_path # needs to be 
...             self.speciesinfo_json = None
...             self.nanopore = False
...             self.tmp_dir = None
...             self.extended_output = None
...             self.db_path_vir_kma = None  
...             self.overlap = 30          
>>> args = TestArgs()
>>> TestPath = Config(args)

```


### Test method: get_abs_path_and_check

```python
>>> test_abs_path = os.path.realpath("README.md")
>>> TestPath.get_abs_path_and_check(test_abs_path)
'.../README.md'

```

```python
>>> test_abs_path = os.path.abspath("not_exist.py")
>>> TestPath.get_abs_path_and_check(test_abs_path, allow_exit = False)
Traceback (most recent call last):
...
FileNotFoundError

```

### Test method: set_default_and_env_vals

```python
test_with_not_exist_param = os.path.join(os.path.dirname(os.path.abspath(".")), "data","environment_variables.md")
TestPath.set_default_and_env_vals(args, env_def_filepath=test_with_not_exist_param)
Traceback (most recent call last):
SystemExit:...
```



### Test get_prg_path

```python
>>> TestPath.get_prg_path("asfdjkalewjfklwefjwkefl")
Traceback (most recent call last):
...
FileNotFoundError:...

```

```python
>>> blast = os.environ.get("CGE_BLASTN")
>>> result = subprocess.run([f'{blast} -help > /dev/null 2>&1'], shell=True)  # Run 'blastn -help' instead of just 'blastn'
>>> expected_args = [blast, '-help']
>>> assert result.returncode == 0

```

### Test set_path_virfinderdb

```python
>>> args.db_path = your_db_path
>>> TestPath.set_path_virfinderdb(args)

```

### default databases

```python
>>> assert "virulencefinder_db" in TestPath.db_path_vir

```
res = {'evalue': 3.02706e-57,
     'sbjct_header':'astA:1:AF161000',
     'bit': 217.178, 'perc_ident': 100.0,
     'sbjct_length': 117,
     'sbjct_start': 1,
     'sbjct_end': 117,
     'gaps': 0,
     'query_string': 'ATGCCATCAACACAGTATATCCGGAGACCCACATCCAGTTATGCATCGTGCATATGGTGCGCAACAGTCTGCGCTTCGTGTCATGGAAGGACTACAAAGCCGTCACTCGCGACCTGA', 
     'homo_string': '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||',
     'sbjct_string': 'ATGCCATCAACACAGTATATCCGGAGACCCACATCCAGTTATGCATCGTGCATATGGTGCGCAACAGTCTGCGCTTCGTGTCATGGAAGGACTACAAAGCCGTCACTCGCGACCTGA',
     'contig_name': 'astA:1:AF161000',
     'query_start': 1,
     'query_end': 117,
     'HSP_length': 117,
     'coverage': 1.0,
     'cal_score': 100.0, 
     'hit_id': 'astA:1:AF161000:1..117:astA:1:AF161000:100.000000', 
     'strand': 0, 'perc_coverage': 100.0}

import json
file_ = "example_res.json"
with open(file_, 'w') as json_file:
    json.dump(res, json_file)
# ubiquitous-garbanzo
Temporal solution for DBS3 validation/invalidation after DBS migration to GO language.

## Cause of Issue:
According to Valentin, there was an upgrade on the DBSWriter. Now it is Go-based code.

### How to reproduce it?

Use the 8 years old script DBS3SetFileStatus.py

https://github.com/CMSCompOps/TransferTeam/blob/master/dbs/DBS3SetFileStatus.py

On the DBSWriter logs it appears:
'''
HTTP/1.1 200 PUT /dbs/prod/global/DBSWriter/files?logical_file_name=['/store/mc/RunIISummer20UL16RECOAPV/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/AODSIM/106X_mcRun2_asymptotic_preVFP_v8-v3/100000/FC9DF411-A5E7-AE48-AE3E-1C82A876E276.root']&lost=0&is_file_valid=0 
'''
and the syntax is not accepted anymore.


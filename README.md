# ubiquitous-garbanzo
Temporal solution for DBS3 validation/invalidation after DBS migration to GO language.

## Cause of Issue:
According to Valentin, there was an upgrade on the DBSWriter around 2022-April. Now it is a Go-based code.

### How to reproduce it

Use the 8 years old script [DBS3SetFileStatus.py](https://github.com/CMSCompOps/TransferTeam/blob/master/dbs/DBS3SetFileStatus.py
)[1] to create the request to change the status of the file.

On the DBSWriter logs it appears:

```
HTTP/1.1 200 PUT /dbs/prod/global/DBSWriter/files?logical_file_name=['/store/mc/RunIISummer20UL16RECOAPV/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/AODSIM/106X_mcRun2_asymptotic_preVFP_v8-v3/100000/FC9DF411-A5E7-AE48-AE3E-1C82A876E276.root']&lost=0&is_file_valid=0 
```
and the syntax is not accepted anymore.
As user of [1], you don't receive any confirmation/error message.

# Solution

## The new DBS3-Client
I followed the [BDS3-CLIENT](https://github.com/dmwm/DBSClient)[2] documentation to install: 

## 1. Install Libcurl


Redhat Base
`sudo yum install libcurl-devel`
Debian Base
`sudo apt-get install libcurl-devel`

## 2. Install Python 3.8 on LXPlus
The best is to create a virtual environment to store python 3.8.

```sh
mkdir $HOME/dbs3env/
cd $HOME/dbs3env/
wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
tar zxfv Python-3.8.2.tgz
find $HOME/python -type d | xargs chmod 0755
cd Python-3.8.2
./configure --prefix=$HOME/dbs3env/
make && make install
export PATH=$HOME/dbs3env/Python-3.8.2/:$PATH
export PYTHONPATH=$HOME/dbs3env/Python-3.8.2
```

### 2.1 PIP
Install pip 21.2.2 or higher:
```sh
export PATH=$HOME/dbs3env/bin:$PATH
pip3 install pip==21.2.2
```
Check that Python3.8 and PIP 21.2.2+ are installed
```sh
python --version
pip --version
```
Then export the following paths
```sh
export PATH=$HOME/dbs3env/Python-3.8.2/:$HOME/.local/bin:$PATH
export PYTHONPATH=$HOME/dbs3env/Python-3.8.2/:$PYTHONPATH
export LD_LIBRARY_PATH="$(python -c 'import site; print(site.getsitepackages()[0])')":$LD_LIBRARY_PATH
```
### 2.2 pycurl
Use pip to install pycurl 7.43.0.6
```sh
export PYCURL_SSL_LIBRARY=nss
pip install --compile --install-option="--with-nss" --no-cache-dir pycurl==7.43.0.6
```
### 2.3 dbs3-client
Use pip one more time:
```sh
export PYCURL_SSL_LIBRARY=nss
pip install --compile --install-option="--with-nss" --no-cache-dir pycurl==7.43.0.6
```


## 3 Script to launch the working environment

I have created a small script to load all the necessary paths to launch the dbs3-client on the python3.8 environment and do the VOMS authentication.

```sh
# DBS_Environment.sh

cwd=$PWD
export PATH=$HOME/dbs3env/Python-3.8.2/:$HOME/.local/bin:$PATH
export PATH=$HOME/dbs3env/bin:$PATH
export PATH=$HOME/dbs3env/scripts:$PATH
export PYTHONPATH=$HOME/dbs3env/Python-3.8.2:$PYTHONPATH
export LD_LIBRARY_PATH="$(python3 -c 'import site; print(site.getsitepackages()[0])')":$LD_LIBRARY_PATH

export PYCURL_SSL_LIBRARY=nss
export DBS3_CLIENT_ROOT="$(python3 -c 'import site; print(site.getsitepackages()[0])')"/dbs/


#voms-proxy-init -voms cms:/cms/Role=production
voms-proxy-init -voms cms -rfc -valid 192:00


export X509_USER_CERT=$HOME/.globus/usercert.pem
export X509_USER_KEY=$HOME/.globus/new_userkey.pem

#voms-proxy-init -voms cms:/cms/Role=production
cd $cwd
export PS1="(PYTHON38dbs3) [\u@\h \W]\$ "
```


## 4 Test / Usage

I have saved the `scripts/` folder inside the `dbs3env/` folder. By default it uses the `TEST_url` in the `urls.py` file, for production just use `url`.


Lets use the following LFN as example:
```
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ Test_LFN='/store/mc/RunIISummer20UL16RECOAPV/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/AODSIM/106X_mcRun2_asymptotic_preVFP_v8-v3/100000/FC9DF411-A5E7-AE48-AE3E-1C82A876E276.root'
```
### 4.1 Get File Info
Once the dbs3env is active, you should be able to get the file information with `dbs2go_DBS3_get_file_info.py`:
```
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ python dbs2go_DBS3_get_file_info.py -f $Test_LFN
{'adler32': '9e88cfb8', 'auto_cross_section': 0, 'block_id': 25404425, 'block_name': '/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v3/AODSIM#7d0009d6-0959-4b86-bdbf-2612fe604aa4', 'branch_hash_id': None, 'check_sum': '292542651', 'create_by': None, 'creation_date': None, 'dataset': '/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v3/AODSIM', 'dataset_id': 14273627, 'event_count': 4000, 'file_id': 734480277, 'file_size': 1215429328, 'file_type': 'EDM', 'file_type_id': 1, 'is_file_valid': 1, 'last_modification_date': 1634669357, 'last_modified_by': 'wmagent@vocms0280.cern.ch', 'logical_file_name': '/store/mc/RunIISummer20UL16RECOAPV/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/AODSIM/106X_mcRun2_asymptotic_preVFP_v8-v3/100000/FC9DF411-A5E7-AE48-AE3E-1C82A876E276.root', 'md5': None}
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ 
```
### 4.2 Change DBS file status to INVALID
Use `dbs2go_DBS3_file_invalidation.py`:
```
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ python dbs2go_DBS3_file_invalidation.py -f $Test_LFN
[]
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ 
```
This is the output for a good invalidation. If we have a different response, the script will raise an exception.

### 4.3 Change DBS file status to VALID
Use `dbs2go_DBS3_file_revalidation.py`:
```
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ python dbs2go_DBS3_file_revalidation.py -f $Test_LFN
[]
(PYTHON38dbs3) [fgomezco@lxplus7104 scripts]$ 
```
This is the output for a good validation or revalidation. If we have a different response, the script will raise an exception.

## About the API

The python client (python2go) code is here [3]. It is fully documented.

```
    @split_calls
    def listFiles(self, **kwargs):
    ...
        validParameters = ['dataset', 'block_name', 'logical_file_name',
                          'release_version', 'pset_hash', 'app_name',
                          'output_module_label', 'run_num',
                          'origin_site_name', 'lumi_list', 'detail', 'validFileOnly', 'sumOverLumi']
    ...
    
    @split_calls
    def updateFileStatus(self, **kwargs):
    ...
        validParameters = ['logical_file_name', 'is_file_valid', 'lost', 'dataset']

        requiredParameters = {'forced': ['is_file_valid'], 'multiple': ['logical_file_name', 'dataset']}
    ...    

```


## References

[1] https://github.com/CMSCompOps/TransferTeam/blob/master/dbs/DBS3SetFileStatus.py

[2] https://github.com/dmwm/DBSClient

[3] https://github.com/dmwm/DBSClient/blob/main/src/python/dbs/apis/dbsClient.py

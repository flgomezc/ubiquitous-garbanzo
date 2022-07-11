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

## 3 Testing

Lets use the following LFN as example:

```
Test_LFN='/store/mc/RunIISummer20UL16RECOAPV/HscalarToTTTo1L1Nu2J_m365_w36p5_res_TuneCP5_13TeV-madgraph_pythia8/AODSIM/106X_mcRun2_asymptotic_preVFP_v8-v3/100000/FC9DF411-A5E7-AE48-AE3E-1C82A876E276.root'
```

TO COMPLETE LATER

## 4 Script to launch the working environment

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




## References

[1] https://github.com/CMSCompOps/TransferTeam/blob/master/dbs/DBS3SetFileStatus.py
[2] https://github.com/dmwm/DBSClient

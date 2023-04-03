#!/usr/bin/env python3

from optparse import OptionParser
import logging
import os
import sys

from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException

TEST_url="https://cmsweb-testbed.cern.ch/dbs2go-writer"
url="https://cmsweb.cern.ch/dbs/prod/global/DBSWriter"

dbsApi = DbsApi(url=url) # 'TEST_URL' or just 'url'

def main():
    usage="%prog <options>"
    parser = OptionParser(usage=usage)

    parser.add_option("-f", "--file", dest="lfn",
                      help="file list to be be invalidated",
                      metavar="<lfn or filename>")
    #set default values
    parser.set_defaults(lfn=0)
    (opts, args) = parser.parse_args()

    fstatus=0
    lost=0
    result=0
    lfn=0

    if opts.lfn:
        try:
            with open(opts.lfn,'r') as f:
                lfns=f.readlines()
            for lfn in lfns:
                lfn=lfn.strip()
                try:
                    dbsApi.updateFileStatus(logical_file_name=lfn, is_file_valid=fstatus, lost=lost)
                except Exception as ex:
                    print("Invalidation FAILED for file: ", lfn)
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    main()
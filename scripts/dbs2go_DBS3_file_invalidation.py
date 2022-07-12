#!/usr/bin/env python3

from optparse import OptionParser
import logging
import os
import sys

from urls import *

from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException


dbsApi = DbsApi(url=TEST_url) # 'TEST_URL' or just 'url'

def main():
    usage="%prog <options>"
    parser = OptionParser(usage=usage)

    parser.add_option("-f", "--file", dest="lfn",
                      help="file be invalidated",
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
            lfn=opts.lfn
            result = dbsApi.updateFileStatus(logical_file_name=lfn, is_file_valid=fstatus, lost=lost)
            print(result)
        except:
            lfn=0
    if result == []:
        print("invalidation OK for:", lfn)
    else:
        print("FAILED for:", lfn)

if __name__ == "__main__":
    main()

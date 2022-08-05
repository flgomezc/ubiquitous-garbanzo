from optparse import OptionParser
import logging
import os
import sys

from urls import *

from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException


dbsApi = DbsApi(url=TEST_url) # 'TEST_URL' or just 'url'

FILEVALID = 1
FILEINVALID = 0
lost = 0 
def main():
    usage="%prog <options>"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--dataset", dest="dataset",
                      help="file be invalidated",
                      metavar="<lfn or filename>")
    #set default values
    parser.set_defaults(lfn=0)
    (opts, args) = parser.parse_args()

    if opts.dataset:
        try:
            dataset=opts.dataset
            listFiles = dbsApi.listFiles(dataset=dataset, detail=True)
            n_files = len(listFiles)
            result = dbsApi.updateFileStatus(dataset=dataset, is_file_valid=FILEINVALID, lost=lost) #INVALIDATE just files in dataset, not recursive       
            print(result)
        except:
            print("Failed to get the list of files in "+dataset)
            print("INVALIDATION ERROR")
    if result == []:
        print("invalidation OK for:", dataset)
        print("{} files in the dataset. All of them are now invalid.".format(n_files))
    else:
        print("FAILED for:", dataset)

if __name__ == "__main__":
    main()

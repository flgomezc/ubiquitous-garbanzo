# This script cannot recognize if a dataset exists or not.
# Python 3.8.2
import argparse
import logging
import os
import sys

from urls import *

from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException


dbsApi = DbsApi(url=url) # 'TEST_URL' or just 'url'

# DBS Constants
FILEVALID = 1
FILEINVALID = 0
VALID   = 1
INVALID = 0
DATASETINVALID = "INVALID"
LOST = 0

def main():
    """
    Invalidates Dataset(PheDex)/Container(Rucio) on DBS using the pbs2go api
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dataset", dest="dataset", type=str,
                      help="Introduce the Dataset(PheDex)/Container(Rucio) to be invalidated",
                      metavar="<CMS container>")

    parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    try:
        args = parser.parse_args()
    except ValueError:
        parser.print_help()
        sys.exit(0)

    if args.dataset:
        try:
            dataset=args.dataset
            list_files = dbsApi.listFiles(dataset=dataset, detail=True)
            n_files = len(list_files)
            file_invalidation = dbsApi.updateFileStatus(dataset=dataset, 
                                                        is_file_valid=FILEINVALID, lost=LOST)
            if file_invalidation == []:
                print(f"    INVALIDATION OK: {n_files} files invalidated in {dataset}")
            dataset_invalidation = dbsApi.updateDatasetType(dataset=dataset,
                                                            dataset_access_type=DATASETINVALID)
            if (dataset_invalidation == []) and (file_invalidation == []):
                print(f"DATASET INVALIDATION OK: {dataset}")

        except ConnectionError:
            print("ERROR: Failed to invalidate files or dataset ", dataset)
            logging.error('Failed to invalidate files or dataset')

        if dataset_invalidation != []:
            print(f"ERROR: cannot update dataset status of {dataset}")
        if file_invalidation != []:
            print(f"ERROR: cannot update file status for files in {dataset}")

if __name__ == "__main__":
    main()

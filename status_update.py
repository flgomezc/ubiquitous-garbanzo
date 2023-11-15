"""
Updates the DBS status of files (lfns) and datasets(PheDex)/containers(Rucio)
"""
# Python 3.8.2
import argparse
import logging
import sys

from dbs.apis.dbsClient import DbsApi
#from dbs.exceptions.dbsClientException import dbsClientException

# DBS Constants
FILEINVALID = 0
FILEVALID = 1
DATASETINVALID = "INVALID"
DATASETVALID  = "VALID"
DATASETPRODUCTION = "PRODUCTION"
LOST = 0 # default lost=0 to indicate a file is not lost in transfer
TEST_URL="https://cmsweb-testbed.cern.ch/dbs/int/global/DBSWriter/"
PROD_URL="https://cmsweb.cern.ch/dbs/prod/global/DBSWriter"

dbsApi = DbsApi(url=PROD_URL) # Select the production server
# dbsApi = DbsApi(url=TEST_URL) # Select the test server

def single_file_status_update(lfn, f_status, n_status):
    """
    Update the status of a single lfn: VALID or INVALID. 
    The script does not check if the file exists on DBS
    """
    try:
        result = dbsApi.updateFileStatus(logical_file_name=lfn, 
                                         is_file_valid=f_status, lost=LOST)
    except ConnectionError:
        logging.error('FAILED to update the state of lfn %s', lfn)

    if result == []:
        print(f"Status updated to {n_status} for file {lfn}")
    else:
        print(f"ERROR updating status for {lfn}")
    return 0

def multiple_file_status_update(filelist, f_status, n_status):
    """
    Update the status of a bulk of lfns (VALID or INVALID) stored in a UTF-8
    textfile. The script does not check if the lfns are registered on DBS.
    """
    try:
        with open(filelist, 'r', encoding='utf-8') as f:
            lfns = f.readlines()
            for lfn in lfns:
                lfn = lfn.strip()
                print(lfn)
    except IOError:
        logging.error("Error while opening %s", filelist)
        print(f"Error opening file {filelist}")
        return None
    print(f"Attemping to update {len(lfns)} lfns:")
    for lfn in lfns:
        # Non-proper way (working):
        single_file_status_update(lfn, f_status, n_status)
    # Proper way, (not-working):
    #dbsApi.updateFileStatus(logical_file_name=lfns, is_file_valid=f_status, lost=LOST)
    return 0

def single_dataset_status_update(dataset, status):
    """
    So far, only dataset invalidation is available.
    It is done using dbsAPI.updateDatasetType
    """
    if status == DATASETINVALID:
        single_dataset_invalidation(dataset, DATASETINVALID)
    if status == DATASETVALID:
        single_dataset_validation(dataset, DATASETVALID)
    if status == DATASETPRODUCTION:
        single_dataset_production(dataset, DATASETPRODUCTION)

def single_dataset_invalidation(dataset, status=DATASETINVALID):
    """
    Invalidate a single Dataset(PheDex)/Container(Rucio)
    The script does not check if the dataset exists on DBS
    """
    try:
        list_files = dbsApi.listFiles(dataset=dataset, detail=True)
        n_files = len(list_files)
        file_invalidation = dbsApi.updateFileStatus(dataset=dataset, 
                                    is_file_valid=FILEINVALID, lost=LOST)
        if file_invalidation == []:
            print(f"INVALIDATION OK: {n_files} files invalidated in {dataset}")
        dataset_invalidation = dbsApi.updateDatasetType(dataset=dataset,
                                             dataset_access_type=status)
        if (dataset_invalidation == []) and (file_invalidation == []):
            print(f"DATASET INVALIDATION OK: {dataset}")
    except ConnectionError:
        print("ERROR: Failed to invalidate files or dataset ", dataset)
        logging.error('Failed to invalidate files or dataset %s', dataset)
    if dataset_invalidation != []:
        print(f"ERROR: cannot update dataset status of {dataset}")
    if file_invalidation != []:
        print(f"ERROR: cannot update file status for files in {dataset}")
    return 0

def single_dataset_validation(dataset, status=DATASETVALID):
    """
    Not inmplemented:
    DAS does not return the list of invalid files. Unless you manually validate
    the list of files, you should not update the dataset status to VALID
    with
    dbsApi.updateDatasetType(dataset=dataset,
                             dataset_access_type=DATASETVALID)
    """
    print("ERROR: function not implemented")
    raise NotImplementedError

def single_dataset_production(dataset, status=DATASETPRODUCTION):
    """
    Not inmplemented:
    DAS does not return the list of invalid files. Unless you manually validate
    the list of files, you should not update the dataset status to PRODUCTION
    with
    dbsApi.updateDatasetType(dataset=dataset,
                             dataset_access_type=DATASETPRODUCTION)
    """
    print("ERROR: function not implemented")
    raise NotImplementedError

def main():
    """Main function"""
    parser = argparse.ArgumentParser()

    validgroup = parser.add_mutually_exclusive_group(required=True)
    validgroup.add_argument("--invalid", action="store_true",
                help="mark INVALID file or dataset on DBS")
    validgroup.add_argument("--valid", action="store_true",
                help="mark VALID file or dataset on DBS")
    validgroup.add_argument("--production", action="store_true",
                help="mark only datasets in PRODUCTION, not used for lfns")


    namegroup = parser.add_mutually_exclusive_group(required=True)
    namegroup.add_argument("--lfn", metavar="/xxx/../yyy/zzz.root", type=str,
                help="filename or CMS lfn to act on")
    namegroup.add_argument("--filelist", metavar="filelist.txt", type=str,
                help="archive with the list of CMS lfns to act on")
    namegroup.add_argument("--dataset", metavar="/xx/../yy", type=str,
                help="CMS dataset to invalidate")


    parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    try:
        args = parser.parse_args()
    except ValueError:
        parser.print_help()
        sys.exit(0)

    if args.lfn:
        lfn = args.lfn
        if args.valid:
            single_file_status_update(lfn, FILEVALID, "VALID")
        elif args.invalid:
            single_file_status_update(lfn, FILEINVALID, "INVALID")
        else:
            print("single_file_status_update works only with --valid or \
                  --invalid options")
            logging.error("--lfn used with no valid/invalid option")
            raise NotImplementedError

    if args.filelist:
        filelist = args.filelist
        if args.valid:
            multiple_file_status_update(filelist, FILEVALID, "VALID")
        elif args.invalid:
            multiple_file_status_update(filelist, FILEINVALID, "INVALID")
        else:
            print("multiple_file_status_update works only with --valid or \
                  --invalid options")
            logging.error("--lfn used with no valid/invalid option")
            raise NotImplementedError

    if args.dataset:
        dataset = args.dataset
        if args.invalid:
            single_dataset_invalidation(dataset, DATASETINVALID)
        if args.valid:
            single_dataset_validation(dataset, DATASETVALID)
        if args.production:
            single_dataset_production(dataset, DATASETPRODUCTION)

if __name__ == "__main__":
    main()

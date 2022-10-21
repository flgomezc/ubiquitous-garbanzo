# This script cannot recognize if a dataset exists or not.
# Python 3.8.2
from optparse import OptionParser                                                                                                           
import logging                                                                                                                              
import os                                                                                                                                   
import sys                                                                                                                                  
                                                                                                                                            
from urls import *                                                                                                                          
                                                                                                                                            
from dbs.apis.dbsClient import DbsApi                                                                                                       
from dbs.exceptions.dbsClientException import dbsClientException                                                                            
                                                                                                                                            
                                                                                                                                            
dbsApi = DbsApi(url=url) # 'TEST_URL' or just 'url'                                                                                         
                                                                                                                                            
FILEVALID = 1                                                                                                                               
FILEINVALID = 0                                                                                                                             
VALID   = 1                                                                                                                                 
INVALID = 0                                                                                                                                 
                                                                                                                                            
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
                                                                                                                                            
            file_invalidation    = dbsApi.updateFileStatus(dataset=dataset, is_file_valid=FILEINVALID, lost=lost) #INVALIDATE just files in\
 dataset, not recursive                                                                                                                     
            dataset_invalidation = dbsApi.updateDatasetType(dataset=dataset, dataset_access_type="INVALID")  # INVALID DELETED DEPRECATED
                                                                                                                                            
        except:                                                                                                                             
            result = 0                                                                                                                      
            print("ERROR: Failed to invalidate", dataset)                                                                                   
                                                                                                                                            
        if (dataset_invalidation == []) and (file_invalidation == []):                                                                      
            print("INVALIDATION OK: Dataset and files are invalid. {} files in {}".format(n_files, dataset))                                
        else:                                                                                                                               
            if(dataset_invalidation != []):                                                                                                 
                print("ERROR: cannot update dataset status of ", dataset)                                                                   
                                                                                                                                            
            if(file_invalidation != []):                                                                                                    
                print("ERROR: cannot update file status for files in ", dataset)                                                            
                                                                                                                                            
if __name__ == "__main__":                                                                                                                  
    main()    

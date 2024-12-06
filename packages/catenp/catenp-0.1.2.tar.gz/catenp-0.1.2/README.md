
DESCRIPTION
===========

Python client for extracting data from CATE archives to numpy arrays

INSTALLATION
------------


    pip install catenp


USAGE
-----

See also `catenp.catenumpy.Example`


    from catenp import Authenticate,ArchiveInfo,DatabaseInfo,GetData

    # Authenticate to the server
    tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
   
    # Get basic archive infor like channel raneg and sample rate
    info = ArchiveInfo(serverAddress,serverPort,cateUserName)
    print("Info: ")
    for kk in info: print(kk,":",info[kk])
   
   
    # Get database info and broad archive coverage
    info = DatabaseInfo(serverAddress,serverPort,cateUserName)
    print("Info: ")
    for kk in info: 
        if kk !="segments": 
            print("  ",kk,":",info[kk])
        else:
            print("  segments:")
            for xx in info[kk]:
                for ll in xx: print("    ",ll,":",xx[ll]) 
            print("")


    # Get detailed database coverage in a time and channel range 
    cov = DatabaseCoverage(serverAddress,serverPort,cateUserName,
                            "2024-05-01T08:30:00+00:00",
                            "2024-05-01T09:30:00+00:00",
                            0,16000
                            )
    print("Info: ")
    for xx in cov["query"]: 
        print("\n")
        for kk in xx:
            if kk!="row_series_info": 
                print(kk,":",xx[kk])
            else:
                print("row_series_info:")
                for rr in xx["row_series_info"]:
                    print(rr["min_time"],rr["max_time"],rr["min_channel"],rr["max_channel"],rr["data_url"])
                    
                    
    # Extract some data for a time and channel range  
    arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)

# Copyright 2023 Motion Signal Technologies Limited
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Python client for extracting data from CATE archives to numpy arrays


------------
INSTALLATION
------------

-----
USAGE
-----

..

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

'''


import requests
import json
import numpy as np


CATE_Session_Tokens={}
'''
Session token for accessing the CATE server
'''

CATE_Parameters={}
'''
Archive parameters
'''


class ExceptionCATENPNoData(Exception):
    '''
    Exception classs for absence of data
    '''

def GetServerURL(cateServer,cateServerPort):
    '''
    Returns the server URL string
    '''
    url=""
    if cateServer.lower().startswith("http")==True:
        # Server is provided as and address
        url=cateServer
    else:
        # Server is provided as domain or IP
        url="http://"+cateServer
    if cateServerPort!=None: url.rstrip('/')+":"+str(cateServerPort)+'/'
        
    return url

def Authenticate(cateServer,cateServerPort,username,password):
    '''
    Returns a session token for the CATE server and saves the result in a module variable
    '''

    resp=requests.post(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/token", 
                       headers={"accept":"application/json",
                                "Content-Type": "application/x-www-form-urlencoded"
                                },
                       data={"username":str(username),"password":str(password)},
                       )   

    if resp.status_code!=200: raise Exception( "ERROR in CATE login message: "+resp.content.decode() )

    global CATE_Session_Tokens
    
    
    
    rr=json.loads(resp.content)
    CATE_Session_Tokens[(cateServer,cateServerPort,username)]=rr["access_token"]
    
    return CATE_Session_Tokens[(cateServer,cateServerPort,username)]

def DatabaseInfo(cateServer,cateServerPort,username,detail=False):
    '''
    Get database coverage information from the server. Use detail=True to provide a comprehensive list
     the default is to show main data chunks (typically 1hr)
     
    @param cateServer: cate server address
    @type cateServer: str

    @param cateServer: cate server port
    @type cateServer: int
  
    @param username: cate server user name
    @type username: str
     
    '''
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    
    resp=requests.get(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/archive_db_info", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       params={"detail": detail}
                       )   
    
    if resp.status_code!=200: raise Exception( "ERROR in CATE login message: "+resp.content.decode() )
    return json.loads(resp.content)

def ArchiveInfo(cateServer,cateServerPort,username):
    '''
    Returns archive info including version, and sample rate etc.
    '''
    
    if (cateServer,cateServerPort,username) in CATE_Parameters: return CATE_Parameters[(cateServer,cateServerPort,username)]
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    
    resp=requests.get(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/archive_info", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       )   
    
    if resp.status_code!=200: raise Exception( "ERROR in CATE login message: "+resp.content.decode() )
    CATE_Parameters[(cateServer,cateServerPort,username)] = json.loads(resp.content)

    return CATE_Parameters[(cateServer,cateServerPort,username)]

def DatabaseCoverage(cateServer,cateServerPort,username,tmin,tmax,cmin,cmax):
    '''
    Get database coverage information from the server with a time and channel range Use detail=True to provide 
     a comprehensive list the default is to show main data chunks (typically 1hr)
     
    @param cateServer: cate server address
    @type cateServer: str

    @param cateServer: cate server port
    @type cateServer: int
  
    @param username: cate server user name
    @type username: str

    @param tmin,tmax: start stop time as isoformat time string 
    @type tmin,tmax: str

    @param cmin,cmax: start stop channels 
    @type cmin,cmax: integer
     
    '''
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    
    resp=requests.get(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/query_data_segments", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       params={
                                #"detail": detail,
                               "tmin": tmin,
                               "tmax": tmax,
                               "cmin": cmin,
                               "cmax": cmax,                               
                               }
                       )   
    
    if resp.status_code!=200: raise Exception( "ERROR in CATE login message: "+resp.content.decode() )
    return json.loads(resp.content)

def GetData(cateServer,cateServerPort,username,
            tstart,tstop,
            cstart,cstop
            ):
    '''
    Query and download data from the CATE server
    
    @param cateServer: cate server address
    @type cateServer: str

    @param cateServer: cate server port
    @type cateServer: int
  
    @param username: cate server user name
    @type username: str

    @param tstart: isoformat time string for start of data (first sample)
    @type tstart: str

    @param tstop: isoformat time string for stop of data (last sample)
    @type tstop: str

    @param cstart: channel number for start of data
    @type cstart: int

    @param cstop: channel number for stop of data (inclusive)
    @type cstop: int
    
    '''
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    
    # Intitial query
    resp=requests.get(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/get_data_segments", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       params={
                            "tmin":tstart,
                            "tmax": tstop,
                            "cmin": cstart,
                            "cmax": cstop
                       }
                       )   

    
    if resp.status_code!=200: raise Exception( "ERROR in CATE from CATE server: "+resp.content.decode() )
    rr=json.loads(resp.content)
    if len(rr)==0: raise ExceptionCATENPNoData("No data available for request")
    if "message" in rr:
        if rr["message"]=="No data found for requested interval":
            raise ExceptionCATENPNoData("No data available for request")
    

    # Make the output data array
    #start_row=min([xx["output_start_row"] for xx in rr])
    stop_row=max([xx["output_stop_row"] for xx in rr])
    nRow=stop_row+1
    
    #start_col=min([xx["output_start_column"] for xx in rr])
    stop_col=max([xx["output_stop_column"] for xx in rr])
    nCol=stop_col+1
    dataType=rr[0]["dtype"]
    dataArray = np.zeros([nRow,nCol],dtype=dataType)
    #print("Output data shape=",dataArray.shape)

    # Download the data segments and place into output
    for xx in rr:

        # Download the data
        if "download_url" in xx:
            # Server provides a download URL
            
            if "$SERVER_ADDRESS$" in xx["download_url"]:
                # URL on the server
                url=xx["download_url"].replace("$SERVER_ADDRESS$",str(cateServer)).replace("$SERVER_PORT$",str(cateServerPort))
                dresp=requests.get(url,headers={"Authorization": "Bearer "+sessionToken},)
            else:
                # Simple signed URL
                dresp=requests.get(xx["download_url"]) 
        else:
            # Legacy sever user /get_data
            dresp=requests.get(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/get_data",
                           headers={"Authorization": "Bearer "+sessionToken},
                           params={ "data_key": xx["data_key"] }
                          ) 
    
        if dresp.status_code!=200: 
            raise Exception( "ERROR in CATE data retrieval for data segment error code="+dresp.content.decode() )   
        
        # Un pack the data and place into output
        arr = np.frombuffer(dresp.content,dtype=xx["dtype"])
        arr.shape=(
                   xx["input_stop_row"]-xx["input_start_row"]+1,
                   xx["input_stop_column"]-xx["input_start_column"]+1
                   )

        dataArray[ xx["output_start_row"]:xx["output_stop_row"]+1, 
                   xx["output_start_column"]:xx["output_stop_column"]+1 
                 ] = arr

    return dataArray

def RequestUploads(cateServer,cateServerPort,username,
                   segmentList,
                   timeOutCloud=180.,
                   timeOutCloudToOnsite=120.,
                   verbose=False,
                   check_for_existing_segments=True,
                   **kwargs):
    '''
    Requests upload data segments from an upstream server
    
    @param cateServer: address for the cate server
    @type cateServer: string

    @param cateServerPort: port for the CATE server
    @type cateServerPort: integer

    @param username: user name for server (if login required)
    @type username: string
    
    @param segmentList: List of segments to check for and upload if nec. (tmin:str , tmax:str , cmin:int , cmax:int)
    @type segmentList: []

    @param timeOutCloud: time out for requests to the cloud server (should be >timeOutCloudToOnsite)
    @type timeOutCloud: float

    @param timeOutCloudToOnsite: time out for requests to the onsite server from cloud 
    @type timeOutCloudToOnsite: float
    
    @param check_for_existing_segments: check the cloud server fo data and only request missing segments from onsite
    @type check_for_existing_segments: bool
    
    '''
   
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    endPoint=GetServerURL(cateServer,cateServerPort).rstrip('/')+"/request_mpart_upload_from_upstream"
    
    if verbose==True:
        print("Endpoint: ",endPoint," with timeout=",timeOutCloudToOnsite,flush=True)
    
    # Try the multipart request 
    resp=requests.post(endPoint, 
                       headers={"Authorization": "Bearer "+sessionToken},
                       data=json.dumps({"data":segmentList}),
                       params={
                           "timeout": timeOutCloudToOnsite,
                           "checkForExistingSegments": check_for_existing_segments
                           },
                       timeout=timeOutCloud
                       ) 

    if resp.status_code==404:
        if verbose==True: print("WARNING - The initial upload request failed with 404 error. This could be because the CATE server is old. Retrying as separate requests with a legacy endpoint",flush=True) 
        
        for xx in segmentList:
    
            pp={ 
                "tmin": str(xx[0]),
                "tmax": str(xx[1]),
                "cmin": int(xx[2]),
                "cmax": int(xx[3]),
                "checkForExistingSegments": True,
                "timeout":  timeOutCloudToOnsite                         
               }
    
            if verbose==True: print("\nRequesting: ",pp," with timeout=",timeOutCloud,flush=True)
            
            endPoint=GetServerURL(cateServer,cateServerPort).rstrip('/')+"/request_upload_from_upstream"
            resp=requests.get(endPoint, 
                           headers={"Authorization": "Bearer "+sessionToken},
                           params=pp,
                           timeout=timeOutCloud
                           )   
    
            if resp.status_code!=200: 
                raise Exception( "ERROR in CATE request_upload_from_upstream message: "+resp.content.decode() )
    elif resp.status_code!=200: 
        raise Exception("ERROR in CATE request_mpart_upload_from_upstream message: "+resp.content.decode() )

def CheckPointsCoverage(cateServer,cateServerPort,username,points):
    '''
    Queries the server to check if a list of points are covered
    
    @param cateServer: address for the cate server
    @type cateServer: string

    @param cateServerPort: port for the CATE server
    @type cateServerPort: integer

    @param username: user name for server (if login required)
    @type username: string
    
    @param points:   List of points to check are covered nec. (tmin:str , tmax:str , cmin:int , cmax:int)
    @type points: 
    '''
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    resp = requests.post(GetServerURL(cateServer,cateServerPort).rstrip('/')+"/check_points_coverage",
                         headers={"Authorization": "Bearer "+sessionToken},
                         data=json.dumps({"data": points})
                         )
    if resp.status_code!=200:
        raise Exception("ERROR in CATE check_points_coverage message: "+resp.content.decode() )
    
    return json.loads(resp.content)
    
def Example():
    '''
    Simple test / example functionality
    '''

    print("\n*********************\nTest/ Example functionality\n******************\n")

    print("\n*********************\nRead in server data")

    with open("./test-data.txt") as fd:
        serverAddress = fd.readline().rstrip()           # CATE Server address (example 1.2,3,4)
        serverPort = int(fd.readline().rstrip())         # CATE Server port (example 8000)
        cateUserName = fd.readline().rstrip()            # User name on the server
        catePassword = fd.readline().rstrip()            # Password on the server
        
        tstart = fd.readline().rstrip()                  # Start of time interval to get
        tstop = fd.readline().rstrip()                   # Stop of time interval to get
        cstart = int( fd.readline().rstrip() )           # Start of channel interval to gets
        cstop = int( fd.readline().rstrip() )            # End of channel interval to get
      
        
    print("Got server details:")
    print("   Server=",serverAddress)  
    print("   port=",serverPort)  
    print("   User=",cateUserName)  
    
    
    print("\n*********************\nAuthenticate")
    tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
    print("Got session token: ",tk)
    
    print("\n*********************\nArchive info")
    info = ArchiveInfo(serverAddress,serverPort,cateUserName)
    print("Info: ")
    for kk in info:
        print(kk,":",info[kk])
    
    print("\n*********************\nDatabase info")
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
    
    
    print("\n*********************\nDatabase Coverage")
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
    
    
    # Get some data
    print("\n*********************\nGetting Data:")
    print("Interval: ")
    print("   tstart=",tstart)  
    print("   tstop=",tstop)  
    print("   cstart=",cstart) 
    print("   cstop=",cstop) 
    
    arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)
    
    print("Got data:")
    print("  arr.shape=",arr.shape)
    print("  arr.dtype=",arr.dtype)
    print("  range=",np.min(arr),np.max(arr))    

def Example2():
    '''
    Simple test / example functionality using a url end point
    '''

    print("\n*********************\nTest/ Example functionality\n******************\n")

    print("\n*********************\nRead in server data")

    with open("./test-data2.txt") as fd:
        serverAddress = fd.readline().rstrip()           # CATE Server address (example http://blahbalh.myserver/endppoint/)
        serverPort=None                                  # Use none for the server port to assume http
        cateUserName = fd.readline().rstrip()            # User name on the server
        catePassword = fd.readline().rstrip()            # Password on the server
        
        tstart = fd.readline().rstrip()                  # Start of time interval to get
        tstop = fd.readline().rstrip()                   # Stop of time interval to get
        cstart = int( fd.readline().rstrip() )           # Start of channel interval to gets
        cstop = int( fd.readline().rstrip() )            # End of channel interval to get
      
        
    print("Got server details:")
    print("   Server=",serverAddress)  
    print("   port=",serverPort)  
    print("   User=",cateUserName)  
    
    
    print("\n*********************\nAuthenticate")
    tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
    print("Got session token: ",tk)
    
    print("\n*********************\nArchive info")
    info = ArchiveInfo(serverAddress,serverPort,cateUserName)
    print("Info: ")
    for kk in info:
        print(kk,":",info[kk])

    print("\n*********************\nDatabase info")
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
    
    
    print("\n*********************\nDatabase Coverage")
    cov = DatabaseCoverage(serverAddress,serverPort,cateUserName,
                            "2023-02-06T17:00:00+00:00",
                            "2023-02-06T17:30:00+00:00",
                            0,12000
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
    
    
    # Get some data
    tstart="2023-02-06T17:00:00+00:00"
    tstop="2023-02-06T17:00:30+00:00"
    cstart=5000
    cstop=6000
    
    print("\n*********************\nGetting Data:")
    print("Interval: ")
    print("   tstart=",tstart)  
    print("   tstop=",tstop)  
    print("   cstart=",cstart) 
    print("   cstop=",cstop) 
    
    arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)
    
    print("Got data:")
    print("  arr.shape=",arr.shape)
    print("  arr.dtype=",arr.dtype)
    print("  range=",np.min(arr),np.max(arr))    

if __name__ == '__main__':
    
    
    Example()
    
    
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

   from catenp import Authenticate,DatabaseInfo,GetData

   # Authenticate to the server
   tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
   
   # Optional get server info
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
   
   
   # Exract some data    
   arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)

'''

from .catenumpy  import Authenticate,DatabaseInfo,GetData,DatabaseCoverage



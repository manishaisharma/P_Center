# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:45:58 2020

@author: msharm77
"""


import cx_Oracle
from testconfig import config

import csv
import datacompy
import pandas as pd
import sys
import nose
import coverage
#python -m unittest test1.TestStringMethods.test_connection
#python -m unittest -v test1



        
def repo_scan():
      
        objects_changed=0
        LOCATION = "/usr/lib/oracle/19.3/client64/lib"
        src_files=""   
        REPO_QUERY_LOCATION=config['myreposcan']['sql']
        db_credentials_filename="/data/masharma/Jenkins/J_Informatica/creds_repo.prm"
        creds = open(db_credentials_filename, 'r')
        lines = creds.readline()
        columns = lines.split(" ")
        user= columns[0]
        password=columns[1]    
        host= columns[2]
        SID=columns[3]
        connection_string = user+'/'+password +'''@(DESCRIPTION=
                                                            (ADDRESS_LIST=
                                                                (ADDRESS=
                                                                    (PROTOCOL=TCP)
                                                                    (HOST=''' +host+''')
                                                                    (PORT=1521)
                                                                )
                                                            )
                                                            (CONNECT_DATA=
                                                                (SID='''+SID+''')
                                                            )
                                                        )'''
        connection = cx_Oracle.connect(connection_string)
        cursor = connection.cursor()
        with open(REPO_QUERY_LOCATION,'r') as SQL:            
                result=cursor.execute(SQL)

        for row in result:
            objects_changed=row[0]
           
            
        cursor.close()
        connection.close()
        assertGreater(objects_changed, 0)
        

# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:45:58 2020

@author: msharm77
"""


import cx_Oracle

import csv
import datacompy
import pandas as pd
import sys
import nose
import coverage
#python -m unittest test1.TestStringMethods.test_connection
#python -m unittest -v test1



        
def test_connection():
      
        
        LOCATION = "/usr/lib/oracle/19.3/client64/lib"
        src_files=""   
        
        filename="/data/masharma/Jenkins/J_Unit_Testing/DB_Output.csv"
        user='Infa_user'
        password='India123'
        
        connection_string = user+'/'+password +'''@(DESCRIPTION=
                                                    (ADDRESS_LIST=
                                                        (ADDRESS=
                                                            (PROTOCOL=TCP)
                                                            (HOST=10.100.253.11)
                                                            (PORT=1521)
                                                        )
                                                    )
                                                    (CONNECT_DATA=
                                                        (SID=ORA12C)
                                                    )
                                                )'''
        connection = cx_Oracle.connect(connection_string)
        SQL="SELECT SOURCE_ROW_NUM, SOURCE_ID, CUSTOMER_NAME, CUSTOMER_AGE, CUSTOMER_ADDRESS, CUSTOMER_GENDER, CUSTOMER_BILLING_AMOUNT FROM TGT_CUSTOMER_DATA"
        cursor = connection.cursor()
        cursor.execute(SQL)
        with open(filename, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow([ i[0] for i in cursor.description ]) # heading row
            writer.writerows(cursor.fetchall())    
            
        cursor.close()
        connection.close()
        fout.close()
        assert (cursor)
        
def test_idatacompare():
        df1 = pd.read_csv('/data/masharma/Jenkins/J_Unit_Testing/Source_data.csv')
        df2 = pd.read_csv('/data/masharma/Jenkins/J_Unit_Testing/DB_Output.csv')
        compare = datacompy.Compare(
            df1,
            df2,
            join_columns=['SOURCE_ROW_NUM', 'SOURCE_ID', 'CUSTOMER_NAME', 'CUSTOMER_AGE','CUSTOMER_ADDRESS', 'CUSTOMER_GENDER', 'CUSTOMER_BILLING_AMOUNT'],  #You can also specify a list of columns eg ['policyID','statecode']
            abs_tol=0, #Optional, defaults to 0
            rel_tol=0, #Optional, defaults to 0
            df1_name='Source_Data', #Optional, defaults to 'df1'
            df2_name='Database_Data' #Optional, defaults to 'df2'
        )
        
        f1 = open('/data/masharma/Jenkins/J_Unit_Testing/compare_Report.txt','w')
        print(compare.report(),file=f1)
        f1.close()
        assert (compare.matches())  



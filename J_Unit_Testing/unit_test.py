# -*- coding: utf-8 -*-
"""
Created on Wed May 13 23:41:18 2020

@author: msharm77
"""

import cx_Oracle
import os
import csv
import datacompy
import pandas  as pd
import sys

LOCATION = "/data/masharma/Jenkins/J_OracleInstantClient/instantclient_19_6"
src_files=""   

filename="/data/masharma/Jenkins/J_Unit_Testing/DB_Output.csv"
##FILE=open(filename,"w");
#output=csv.writer(FILE, dialect='excel')

os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

user=sys.argv[1]
password=sys.argv[2]

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

#
#for row in cursor:
#    output.writerow(row)  
#    
with open(filename, 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow([ i[0] for i in cursor.description ]) # heading row
    writer.writerows(cursor.fetchall())    
    
cursor.close()
connection.close()
fout.close()


##############COMAPRING DATA####################



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



f2 = open('/data/masharma/Jenkins/J_Unit_Testing/compare_Report_True_False.txt','w')
print(compare.matches(),file=f2)
f2.close()
#
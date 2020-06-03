# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:45:58 2020

@author: msharm77
"""


import cx_Oracle
from testconfig import config
import petl as etl
import csv
import datacompy
import pandas as pd
import sys
import nose
import coverage
#python -m unittest test1.TestStringMethods.test_connection
#python -m unittest -v test1



        
def test_connection_load_target_data():
      
        
        LOCATION = "/usr/lib/oracle/19.3/client64/lib"
        src_files=""   
        
        
        db_credentials_filename=config['myjob2']['dbcredsfile']
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
        
        
        REPO_QUERY_LOCATION=config['myjob2']['tgtsqlfilename']
        with open(REPO_QUERY_LOCATION,'r') as SQL:            
            for statement in SQL:
                cursor.execute(statement)
                
        db_output_filename=config['myjob2']['dboutputfile']
        with open(db_output_filename, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow([ i[0] for i in cursor.description ]) # heading row
            writer.writerows(cursor.fetchall())    
            
            
            
        REPO_QUERY_LOCATION2=config['myjob2']['stagesqlfilename']
        with open(REPO_QUERY_LOCATION2,'r') as SQL:            
            for statement in SQL:
                cursor.execute(statement)
                
        db_stageoutput_filename2=config['myjob2']['stageoutputfile']
        with open(db_stageoutput_filename2, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow([ i[0] for i in cursor.description ]) # heading row
            writer.writerows(cursor.fetchall())   
            
        
            
        cursor.close()
        connection.close()
        fout.close()
        assert (cursor)
        
        
def prepare_source_data():
        srcfilename=config['myjob2']['srcfilename']
        stageoutputfile=config['myjob2']['stageoutputfile']
        Key=config['myjob2']['Key']
        df3 = pd.read_csv(srcfilename)
        df4 = pd.read_csv(stageoutputfile)
        
        frames = [df3,df4]
        df_inner = pd.merge(df3, df4, on=Key, how='inner')
        df_inner['Date_received']=df_inner['Date_received'].str.slice(6)
        agg=df_inner.groupby(["RAND_CLIENT", "Date_received"])["Complaint_ID"].count()>2
        agg2=df_inner.groupby(["RAND_CLIENT", "Date_received"])["Complaint_ID"].count().reset_index(name='counts')
        agg2=agg2.loc[agg.values==True]
        aggsrcdata = agg2  #[agg2.counts >2]
        agg2.to_csv('/data/masharma/dd.csv', index=False)
       
        
        
          

        
#def test_idatacompare():
#        aggsrcfilename=config['myjob2']['aggsrcfilename']
        tgtcsvfarme=config['myjob2']['dboutputfile']
        joincolumns=config['myjob2']['joincolumns']
        df1 = pd.read_csv(aggsrcdata)
        df2 = pd.read_csv(tgtcsvfarme)
        col = joincolumns.strip('][').split(',') 
        compare = datacompy.Compare(
            df1,
            df2,
            join_columns=col,  #You can also specify a list of columns eg ['policyID','statecode']
            abs_tol=0, #Optional, defaults to 0
            rel_tol=0, #Optional, defaults to 0
            df1_name='Source_Data', #Optional, defaults to 'df1'
            df2_name='Database_Data' #Optional, defaults to 'df2'
        )
        output_report_filename=config['myjob2']['comparereport']
        f1 = open(output_report_filename,'w')
        print(compare.report(),file=f1)
        f1.close()
        assert (compare.matches())  

    
import pandas as pd
from datetime import datetime
from dateutil.tz import gettz
from collections import OrderedDict
from rubberduckie.cdsw.hadoop import (
    execute_db_query,
    insert_df_to_table,
)

def create_runtime_monitor_table(conn=None, db_table_name=None, drop_existing=False):
    if drop_existing:
        sql_drop = f"""
        DROP TABLE IF EXISTS {db_table_name};
        """
        execute_db_query(conn, sql_drop)
        print("Table was dropped.")
    sql_create = f"""
    CREATE TABLE IF NOT EXISTS {db_table_name} ( 
        project_name STRING
       ,project_status STRING
       ,task_date TIMESTAMP
       ,task_desc STRING
       ,task_func_name STRING
       ,task_seq INT
       ,task_runtime STRING
       ,task_start_time TIMESTAMP
       ,task_end_time TIMESTAMP
       ,task_duration_in_sec BIGINT
       ,task_status STRING
       ,tag_1 STRING
       ,tag_2 STRING
       ,tag_3 STRING
    );
    """
    execute_db_query(conn, sql_create)
    print("Table as created.")
    
# Decorator function
def monitor_runtime(project_name=None, project_status=None, task_date=None, tz=None, task_desc=None, task_seq=None, task_runtime='cdsw', tag_1=None, tag_2=None, tag_3=None, **kwargs):
    """Log python function execution time. This function can be used
       to monitor the runtime of any AI project. You need to write
       each task you would like to monitor as python function, then 
       use this function as a decorator.

       Author: Colin Li @ 2024-05
    """
    # Preparation
    conn = kwargs['conn']
    db_table_name = kwargs['db_table_name']
    if tz is None:
        tz = gettz('Australia/Sydney')
    if task_date is None:
        task_date = datetime.today().astimezone(tz).replace(tzinfo=None, microsecond=0).date()
        
    def decorate_func(func):
        """decorator function"""
        
        def wrap_func(*args, **kwargs):
            """wrapper function"""
            
            # Initialise vars
            task_func_name = func.__name__
            task_start_time = None
            task_end_time = None
            task_duration_in_sec = None
            task_status = 'running'

            # Define some nested util functions 
            def _update_record():
                """Update record to be printed/inserted (internal)"""
                list_of_tuple_log = [
                    ('project_name',project_name),
                    ('project_status', project_status),
                    ('task_date', task_date),
                    ('task_desc',task_desc),
                    ('task_func_name',task_func_name),
                    ('task_seq',task_seq),
                    ('task_runtime',task_runtime),
                    ('task_start_time',task_start_time),
                    ('task_end_time', task_end_time),
                    ('task_duration_in_sec', task_duration_in_sec),
                    ('task_status', task_status),
                    ('tag_1', tag_1),
                    ('tag_2', tag_2),
                    ('tag_3', tag_3),
                ]
                return OrderedDict(list_of_tuple_log)
                
            def _calculate_duration():
                """Calculate task duration in seconds (internal)"""
                task_duration = task_end_time - task_start_time
                return task_duration.seconds
                
            # Record start time
            task_start_time = datetime.today().astimezone(tz).replace(tzinfo=None, microsecond=0)
            df_rec = pd.DataFrame([_update_record()])
            insert_df_to_table(df=df_rec, conn=conn, db_table_name=db_table_name, nrow_per_insert=1)
            try:
                display(df_rec)
            except:
                print(df_rec)

            # Run function passed in
            try:

                # output is the return value from the func, which needs to be returned
                output = func(*args, **kwargs)
                task_end_time = datetime.today().astimezone(tz).replace(tzinfo=None, microsecond=0)
                task_duration_in_sec = _calculate_duration()
                task_status = 'success'
                df_rec = pd.DataFrame([_update_record()])
                insert_df_to_table(df=df_rec, conn=conn, db_table_name=db_table_name, nrow_per_insert=1)
                try:
                    display(df_rec)
                except:
                    print(df_rec)
                finally:
                    return output
                    
            except Exception as e:
                
                task_end_time = datetime.today().astimezone(tz).replace(tzinfo=None, microsecond=0)
                task_duration_in_sec = _calculate_duration()
                task_status = 'fail' 
                df_rec = pd.DataFrame([_update_record()])
                insert_df_to_table(df=df_rec, conn=conn, db_table_name=db_table_name, nrow_per_insert=1)
                try:
                    display(df_rec)
                except:
                    print(df_rec)
                finally:
                    raise RuntimeError(f"Check function{task_func_name}")
                    
                print(f"WARNING: {type(e).__name__} was raised {e}")
        return wrap_func
    return decorate_func
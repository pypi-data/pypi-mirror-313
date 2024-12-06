import os
import math
import numpy as np
import pandas as pd
from tqdm import tqdm
import cml.data_v1 as cmldata

DEBUG = False

if DEBUG:
    print("DB tools are loaded!")

def prepare_connection(host:str="idp-impala-preprd1"):
    """Prepare connection to Cloudera IDP (in Azure) in CDSW

    Author:
        Colin Li, Justin Trinh, Stephen Oates @ 2024-12

    Args:
        host (str): connection name

    Returns:
        cml.data_v1.impalaconnection.ImpalaConnection: connection to Cloudera IDP in Azure
    """
    conn = None
    try:
        conn = cmldata.get_connection(host)
    except:
        try:
            username = os.environ.get('HADOOP_USER_NAME')
            password = os.environ.get('WORKLOAD_PASSWORD').encode('utf-8').decode('unicode_escape')
            conn = cmldata.get_connection(host, {"USERNAME": username, "PASSWORD": password})
        except:
            print("Please ensure that the environment variable:\n"
                  "1. 'HADOOP_USER_NAME' contains your LAN ID and \n"
                  "2. 'WORKLOAD_PASSWORD' holds your workload password provided by the IDP Team.")
            return None
    return conn

def execute_db_query(conn, query: str):
    """Execute database query for IDP in Azure

    Author:
        Colin Li, Justin Trinh, Stephen Oates @ 2024-12

    Args:
        conn (impala.dbapi.connect): connection
        query (str): can be either a string or a sql file path
    """
    if os.path.isfile(query) and query[-4:] == ".sql":
        query_path = query
        with open(query_path, "r") as f:
            query = f.read()
        print(f"Executing task {query_path}")
    tasks = query.split(";")
    for i, t in enumerate(tasks):
        if t.replace(" ", "").replace("\n", "") == "":
            continue
        else:
            print(f"Executing subtask {i+1}")
            db_cursor = conn.get_cursor()
            db_cursor.execute(t)
    print(f"Task is completed!")

def extract_db_data(conn, query: str):
    """Extract data from IDP in Azure as pandas dataframe

    Author:
        Colin Li, Justin Trinh, Stephen Oates @ 2024-12

    Args:
        conn (cml.data_v1.impalaconnection.ImpalaConnection): connection
        query (str): 'select' query which can be either a string or a sql file path

    Returns:
        pandas.DataFrame: Pandas dataframe containing database data
    """
    if os.path.isfile(query) and query[-4:] == ".sql":
        query_path = query
        with open(query_path, "r") as f:
            query = f.read()
            print(f"Obtained query from {query_path}")
    df = conn.get_pandas_dataframe(query)
    return df

def generate_sql_row(row):
    """Generate one sql row used in sql insert statement
    Author:
        Colin Li @ 2023-02
    Args:
        row (pd.Series): pandas data series
    Returns:
        str: one sql row used in sql insert statement
    """
    tb_row_s0 = row.tolist()
    for i, c in enumerate(tb_row_s0):
        if isinstance(c, str):
            tb_row_s0[i] = '"' + str(c) + '"'
        elif isinstance(c, (int, np.integer)):
            tb_row_s0[i] = str(c)
        elif isinstance(c, (float, np.float32)):
            if math.isnan(c):
                tb_row_s0[i] = "NULL"
            else:
                tb_row_s0[i] = str(c)[:10]
        elif pd.isnull(c) or c is None:
            tb_row_s0[i] = "NULL"
        else:
            tb_row_s0[i] = '"' + str(c) + '"'
    tb_row_s1 = "(" + ",".join(tb_row_s0) + ")"
    return tb_row_s1

def insert_one_row(row, conn, db_table_name):
    """Insert one row into IDP table in Azure
    Author:
        Colin Li @ 2024-12
    Args:
        row (_type_): _description_
        conn (_type_): _description_
        db_table_name (_type_): _description_
    """
    with conn.get_cursor() as cursor:
        t = (f"INSERT INTO {db_table_name} VALUES" + row)
        cursor.execute(t)

def insert_rows_to_table(tasks_insert: list, conn, db_table_name, nrow_per_insert=20):
    """Insert rows to IDP table in Azure

    Author:
        Colin Li @ 2023-02

    Args:
        tasks_insert (list): list of strings which is the output from
            function generate_sql_row
        conn (impala.hiveserver2.HiveServer2Connection):
            connetion to hive/impala
        db_table_name (str): database and tablename joined by dot '.'
        nrow_per_insert (int, optional): Number of rows per insert.
            Defaults to 20.
    """
    tasks_size = len(tasks_insert)
    print(f"Rows to insert: {tasks_size}")
    n, rem = divmod(tasks_size, nrow_per_insert)
    st = 0
    tqdm._instances.clear()
    if n > 0:
        for i in tqdm(range(n)):
            rows = tasks_insert[st : st + nrow_per_insert]
            if len(rows) > 1:
                insert_one_row(",".join(rows), conn, db_table_name)
            else:
                insert_one_row(rows[0], conn, db_table_name)
            st += nrow_per_insert
    if rem != 0:
        rows = tasks_insert[st:tasks_size]
        if len(rows) > 1:
            insert_one_row(",".join(rows), conn, db_table_name)
        else:
            insert_one_row(rows[0], conn, db_table_name)

def insert_df_to_table(df, conn, db_table_name, nrow_per_insert=20):
    """Insert pandas dataframe rows into IDP table in Azure
    Author:
        Colin Li @ 2024-05
    Args:
        df (pandas.DataFrame): pandas dataframe
        conn (impala.hiveserver2.HiveServer2Connection):
            connetion to hive/impala
        db_table_name (str): database and tablename joined by dot '.'
        nrow_per_insert (int, optional): Number of rows per insert.
            Defaults to 20.
    """
    tasks_insert = df.apply(generate_sql_row, axis=1).tolist()
    insert_rows_to_table(
        tasks_insert,
        conn=conn,
        db_table_name=db_table_name,
        nrow_per_insert=nrow_per_insert,
    )

if __name__ == "__main__":
    pass

import pyodbc
import pandas as pd

def get_conection():

    #with open('db_config.json', 'r') as outfile:
    #     creds = json.load(outfile)

    creds = dict(
        driver='{ODBC Driver 17 for SQL Server}',
        server='srvvotorantimcrm.database.windows.net',
        port='1433',
        database='dbcrm',
        user='user',
        passwd='pass',
        encrypt='yes',
        trustServerCertificate='no'
           )

    params = 'Driver=' + creds['driver'] + ';' \
             'Server=' + creds['server'] + ';' \
             'Database=' + creds['database'] + ';' \
             'Uid=' + creds['user'] + ';' \
             'Pwd=' + creds['passwd'] + ';' \
             'Port=' + creds['port'] + ';' \
             'Encrypt=' + creds['encrypt'] + ';' \
             'TrustServerCertificate=' + creds['trustServerCertificate'] + ';' 

    conn = pyodbc.connect(params)

    return conn

def get_df_table(table_name):
    conn = get_conection()

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + table_name)
    columns = [column[0] for column in cursor.description]

    r_list = list()
    while True:
        row = cursor.fetchone()
        if not row:
            break
        else:
            r_list.append(list(row))

    conn.close()

    df = pd.DataFrame(r_list, columns=columns)
    return df
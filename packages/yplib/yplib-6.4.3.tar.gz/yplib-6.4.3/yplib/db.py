from yplib.index import *
from yplib.http_util import *
import pymysql

import threading

# 创建一个线程本地存储对象
thread_local_yp_lib = threading.local()


# 有关数据库操作的类
def get_connect(database=None, user=None, password=None, charset='utf8mb4', port=3306, host=None):
    return pymysql.connect(database=database, user=user, password=password, charset=charset, port=port, host=host)


def get_connect_from_config(db_config='stock_db', database=None, user=None, password=None, charset=None, port=None, host=None):
    config_db = get_config_data(db_config)
    database = database if database is not None else config_db['database']
    user = user if user is not None else config_db['user']
    host = host if host is not None else config_db['host']
    password = password if password is not None else config_db['password']
    port = port if port is not None else config_db['port'] if 'port' in config_db else 3306
    charset = charset if charset is not None else config_db['charset'] if 'charset' in config_db else 'utf8mb4'
    return get_connect(database=database, user=user, password=password, charset=charset, port=port, host=host)


# 执行 sql 语句, 并且提交, 默认值提交的了
# sql             : 需要执行的 sql
# db_conn         : sql 连接
# db_config       : 连接所在的配置文件
# commit          : 是否提交
# is_log          : 是否记录到 log
# database        : 具体的数据库,会覆盖 db_config 中的
# save_to_thread  : 是否将连接信息保存到 thread 中, 这样, 就不用, 每次都建立连接了
def exec_sql(sql='', db_conn=None, db_config='stock_db', commit=True, is_log=False, database=None, save_to_thread=False):
    db_cursor = None
    try:
        if db_conn is None:
            if save_to_thread:
                thread_key = db_config + '_' + database if database is not None else db_config
                if not hasattr(thread_local_yp_lib, 'mysql_conn'):
                    thread_local_yp_lib.mysql_conn = {}
                if thread_key not in thread_local_yp_lib.mysql_conn:
                    thread_local_yp_lib.mysql_conn[thread_key] = get_connect_from_config(db_config, database=database)
                db_conn = thread_local_yp_lib.mysql_conn[thread_key]
            else:
                db_conn = get_connect_from_config(db_config, database=database)
        if sql is None or sql == '':
            if is_log:
                to_log_file("db_conn is None or sql is None or sql == '', so return")
            return
        db_cursor = db_conn.cursor()
        if isinstance(sql, list) or isinstance(sql, set):
            for s in sql:
                if is_log:
                    to_log_file(s)
                db_cursor.execute(s)
        else:
            if is_log:
                to_log_file(sql)
            db_cursor.execute(str(sql))
        if commit:
            db_conn.commit()
    finally:
        if not save_to_thread:
            if db_cursor is not None:
                db_cursor.close()
            if db_conn is not None:
                db_conn.close()


def get_doris_conn(db_config='doris'):
    # config_db = get_config_data(db_config)
    # my_uri = config_db['uri']
    # my_db_kwargs = {
    #     adbc_driver_manager.DatabaseOptions.USERNAME.value: config_db['username'],
    #     adbc_driver_manager.DatabaseOptions.PASSWORD.value: config_db['password'],
    # }
    # conn = flight_sql.connect(uri=my_uri, db_kwargs=my_db_kwargs, autocommit=True)
    return get_connect_from_config(db_config)


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_doris_sql(sql='', db_config='wh_doris', database='mx_risk'):
    exec_sql(sql, db_config=db_config, database=database)
    # conn = get_doris_conn(db_config)
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # cursor.close()
    # conn.close()


def get_data_from_doris(sql='', db_config='doris'):
    if not hasattr(thread_local_yp_lib, 'conn_doris'):
        thread_local_yp_lib.conn_doris = get_doris_conn(db_config)
    conn_doris = thread_local_yp_lib.conn_doris
    cursor = conn_doris.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
    # arrow_data = cursor.fetchallarrow()
    # dataframe = arrow_data.to_pandas()
    # json_data = dataframe.to_json(orient='records', date_format='iso')
    # return json.loads(json_data)


def get_data_line_one_from_doris(sql='', db_config='doris'):
    data_list = get_data_from_doris(sql, db_config=db_config)
    if len(data_list):
        return list(data_list[0])
    return None


# 执行 sql 语句, 不提交
def exec_sql_un_commit(sql='', db_conn=None, database=None):
    exec_sql(sql=sql, db_conn=db_conn, commit=False, database=database)


# 执行 sql 获得 数据
def get_data_from_sql(sql='', db_conn=None, db_config='stock_db', is_log=False, database=None, save_to_thread=False):
    db_cursor = None
    try:
        if db_conn is None:
            if save_to_thread:
                thread_key = db_config + '_' + database if database is not None else db_config
                if not hasattr(thread_local_yp_lib, 'mysql_conn'):
                    thread_local_yp_lib.mysql_conn = {}
                if thread_key not in thread_local_yp_lib.mysql_conn:
                    thread_local_yp_lib.mysql_conn[thread_key] = get_connect_from_config(db_config, database=database)
                db_conn = thread_local_yp_lib.mysql_conn[thread_key]
            else:
                db_conn = get_connect_from_config(db_config, database=database)
        if sql is None or sql == '':
            if is_log:
                to_log_file("db_conn is None or sql is None or sql == '', so return")
            return
        db_cursor = db_conn.cursor()
        if is_log:
            to_log_file(sql)
        db_cursor.execute(str(sql))
        data = db_cursor.fetchall()
    finally:
        if not save_to_thread:
            if db_cursor is not None:
                db_cursor.close()
            if db_conn is not None:
                db_conn.close()
    return data

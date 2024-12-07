# coding:utf-8
from tools_hjh.ThreadPool import ThreadPool


class DBConn:
    """ 维护一个关系型数据库连接池，目前支持oracle，pgsql，mysql，sqlite；支持简单的sql执行 """
    
    ORACLE = 'oracle'
    PGSQL = 'pgsql'
    MYSQL = 'mysql'
    SQLITE = 'sqlite'

    def __init__(self, dbtype, host=None, port=None, db=None, username=None, password=None, poolsize=2, encoding='UTF-8', lib_dir=None, options=None):
        """ 初始化连接池
                如果是sqlite，db这个参数是要显示给入的，内存数据库 db=':memory:'
                如果是oracle，db给入的是sid或是servername都是可以的 """
                
        self.dbtype = dbtype
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.poolsize = poolsize
        self.encoding = encoding
        self.lib_dir = lib_dir
        self.options = options
        self.creator = ''
        
        self.runtp = ThreadPool(1)
        self.dbpool = None
        
        self.config = {
            'host':self.host,
            'port':self.port,
            'database':self.db,
            'user':self.username,
            'password':self.password,
            'maxconnections':self.poolsize,  # 最大连接数
            'blocking':True,  # 连接数达到最大时，新连接是否可阻塞
            'reset':False,
            'options':self.options
        }
        
        if self.dbtype == 'pgsql' or self.dbtype == 'mysql' or self.dbtype == 'oracle':
            from dbutils.pooled_db import PooledDB

        if self.dbtype == "pgsql":
            import psycopg2
            self.config['dbname'] = self.config['database']
            self.config.pop('database')
            self.dbpool = PooledDB(psycopg2, **self.config)
            self.creator = 'psycopg2'
        elif self.dbtype == "mysql":
            import pymysql
            self.config.pop('options')
            self.dbpool = PooledDB(pymysql, **self.config)
            self.creator = 'pymysql'
        elif self.dbtype == "sqlite":
            self.config.pop('options')
            if self.db is None:
                self.db = ':memory:'
            import sqlite3
            from dbutils.persistent_db import PersistentDB
            self.dbpool = PersistentDB(sqlite3, database=self.db)
            self.creator = 'sqlite3'
        elif self.dbtype == "oracle":
            import cx_Oracle
            self.config.pop('host')
            self.config.pop('port')
            self.config.pop('database')
            self.config.pop('options')
            if lib_dir is not None:
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            try:
                dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.db)
                self.dbpool = PooledDB(cx_Oracle, **self.config, dsn=dsn)
            except:
                dsn = cx_Oracle.makedsn(self.host, self.port, sid=self.db)
                self.dbpool = PooledDB(cx_Oracle, **self.config, dsn=dsn)
            self.creator = 'cx_Oracle'
                
    def run_procedure(self, sql, param=None, auto_commit=True):
        # 替换占位符
        if self.dbtype == 'pgsql' or self.dbtype == 'mysql':
            sql = sql.replace('?', '%s')
        elif self.dbtype == 'oracle':
            sql = sql.replace('?', ':1')            
        else:
            pass
                
        # 获取连接
        conn = self.dbpool.connection()
        cur = conn.cursor()
                
        # 执行非SELECT语句
        sql = sql.strip()
        if type(param) == list:
            cur.executemany(sql, param)
        elif type(param) == tuple:
            cur.execute(sql, param)
        elif param is None:
            cur.execute(sql)
        if auto_commit: 
            if sql.lower().strip().startswith("update") or sql.lower().strip().startswith("delete") or sql.lower().strip().startswith("insert"):
                conn.commit()
        rownum = cur.rowcount
        rs = rownum
        cur.close()
        conn.close()
        return rs
    
    def __run(self, sqls, param=None, auto_commit=True):

        # 替换占位符
        if self.dbtype == 'pgsql' or self.dbtype == 'mysql':
            sqls = sqls.replace('?', '%s')
        elif self.dbtype == 'oracle':
            sqls = sqls.replace('?', ':1')            
        else:
            pass
        
        sql_list = []
        
        # sql只有一行
        if not '\n' in sqls:
            sql_list.append(sqls.rstrip(';'))
            
        # sql有多行
        else:
            # 去掉每行的首尾空格、换行，再去掉最后一个;,去掉--开头的行
            str2 = ''
            for line in sqls.split('\n'):
                line = line.strip()
                if not line.startswith('--') and len(line) > 0:
                    str2 = str2 + line + '\n'
            for sql in str2.split(';\n'):
                if sql is not None and sql != '' and len(sql) > 0:
                    sql_list.append(sql)
        
        # 获取连接
        conn = self.dbpool.connection()
        cur = conn.cursor()
        
        for sql in sql_list:
            # 执行SELECT语句
            if sql.lower().strip().startswith("select") or (sql.lower().strip().startswith("with") and 'select' in sql.lower()):
                sql = sql.strip()
                if param is None:
                    cur.execute(sql)
                elif type(param) == tuple:
                    cur.execute(sql, param)
                rs = QueryResults(cur, conn)
                
            # 执行非SELECT语句
            elif not sql.lower().strip().startswith("select"):
                sql = sql.strip()
                if type(param) == list:
                    cur.executemany(sql, param)
                elif type(param) == tuple:
                    cur.execute(sql, param)
                elif param is None:
                    cur.execute(sql)
                if auto_commit: 
                    if sql.lower().strip().startswith("update") or sql.lower().strip().startswith("delete") or sql.lower().strip().startswith("insert"):
                        conn.commit()
                rownum = cur.rowcount
                rs = rownum
                try:
                    cur.close()
                except:
                    pass
                try:
                    conn.close()
                except:
                    pass
        return rs

    def run(self, sql, param=None, auto_commit=True):
        return self.__run(sql, param, auto_commit)

    def pg_copy_from(self, table_name, rows, cols_description):
        conn = self.dbpool.connection()
        cur = conn.cursor()
        cols = []
        int_cols = []
        for c in cols_description:
            if 'NUMBER' in str(c[1]) and c[5] == 0:
                int_cols.append(c[0])
            elif 'INT' in str(c[1]):
                int_cols.append(c[0])
            cols.append(c[0])
        
        try:
            if self.creator == 'psycopg2':
                import pandas
                from _io import StringIO
                from psycopg2 import sql
                data1 = pandas.DataFrame(rows)
                data1.columns = cols
                data1[int_cols] = data1[int_cols].astype('Int64')
                output = StringIO()
                # data1.to_csv(output, sep='\t', index=False, header=False, na_rep='', quoting=csv.QUOTE_NONE, escapechar='\\')
                data1.to_csv(output, sep='\t', index=False, header=False, na_rep='', quotechar='"')
                # data1.to_csv('1.csv', sep='\t', index=False, header=False, na_rep='', quotechar='"')
                csv_file = output.getvalue()
                # if "b'\\x" in csv_file:
                    # pass
                    
                # cur.copy_from(StringIO(csv_file), table_name, null='', sep='\t')
                option_values = [
                    "format CSV",
                    "NULL ''",
                    "delimiter '\t'",
                    "quote '\"'"
                ]
                copy_options = sql.SQL(', '.join(
                    n for n in option_values)
                )
                copy_cmd = sql.SQL(
                    "copy {} from stdin with ({})"
                ).format(
                    sql.Identifier(table_name),
                    copy_options
                )
                cur.copy_expert(sql=copy_cmd, file=StringIO(csv_file))
                num = len(data1)
            elif self.creator == 'psycopg':
                with cur.copy('COPY' + table_name + ' FROM STDIN') as copy:
                    for row in rows:
                        copy.write_row(row)
                num = len(rows)
            conn.commit()
            return num
        
        except Exception as _:
            conn.rollback()
            try:
                cur.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass
            raise _
        finally:
            try:
                cur.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass
        
    def close(self):
        try:
            self.dbpool.close()
        except:
            pass
        finally:
            self.dbpool = None
    
    def __del__(self):
        self.close()
    
        
class QueryResults:

    def __init__(self, cur, conn):
        self.cur = cur
        self.conn = conn
        self.rows = ''
        self.is_close = False

    def get_cols(self):
        if self.is_close:
            return []
        col = []
        for c in self.cur.description:
            col.append(c[0])
        return tuple(col)
    
    def get_cols_description(self):
        if self.is_close:
            return []
        return self.cur.description
    
    def get_rows(self, rownum='all'):
        if self.is_close:
            return []
        
        # 判断字段类型有没有Oracle大字段
        lob_exists = False
        for c in self.cur.description:
            if 'LOB' in str(c[1]) or 'RAW' in str(c[1]) or 'LONG' in str(c[1]):
                lob_exists = True
                
        if type(rownum) != int:
            rows = self.cur.fetchall()
        elif rownum == 1:
            rows = self.cur.fetchone()
        else:
            rows = self.cur.fetchmany(int(rownum))
            
        if len(rows) == 0:
            self.close()
            return rows
                
        rows_new = [] 
        if lob_exists:
            import cx_Oracle
            for row in rows:
                row_new = []
                for cell in row:
                    if type(cell) == cx_Oracle.LOB:
                        cell_new = cell.read()
                    else:
                        cell_new = cell
                    row_new.append(cell_new)
                rows_new.append(row_new)
        else:
            rows_new = rows
            
        if type(rownum) != int:
            self.close()
        elif type(rownum) == int and len(rows_new) < rownum:
            self.close()
            
        return rows_new

    def close(self):
        self.is_close = True
        try:
            self.cur.close()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass
        
    def __del__(self):
        self.close()


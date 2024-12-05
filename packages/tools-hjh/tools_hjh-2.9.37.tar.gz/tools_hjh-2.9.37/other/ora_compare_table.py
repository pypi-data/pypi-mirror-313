# coding:utf-8
from tools_hjh import DBConn, Tools
from tools_hjh import OracleTools
import sys

help_mess = '''使用方法
python3 ora_compare_table.py example.conf
'''

try:
    config_file = sys.argv[1]
except:
    config_file = None
    
if config_file == None or config_file == 'help':
    print(help_mess)
    sys.exit()

conf = Tools.cat(config_file)
conf_map = {}
for line in conf.split('\n'):
    if '=' in line and '#' not in line:
        key = line.split('=', 1)[0].strip()
        val = line.split('=', 1)[1].strip()
        conf_map[key] = val
        
src_ip = conf_map['src_ip']
src_port = int(conf_map['src_port'])
src_database = conf_map['src_db']
src_username = conf_map['src_username']
src_password = conf_map['src_password']

tables = conf_map['tables']

dst_ip = conf_map['dst_ip']
dst_port = int(conf_map['dst_port'])
dst_database = conf_map['dst_db']
dst_username = conf_map['dst_username']
dst_password = conf_map['dst_password']


# 主控制程序
def main():
    src_db = DBConn('oracle', src_ip, src_port, src_database, src_username, src_password, poolsize=4)
    dst_db = DBConn('oracle', dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=4)
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        compare(src_db, table_map[0], table_map[1], dst_db, table_map[0], table_map[1])
        
    src_db.close()
    dst_db.close()


def compare(src_conn, src_username, src_table_name, dst_conn, dst_username, dst_table_name):
    mess, is_same = OracleTools.compare_table(src_conn, src_username, src_table_name, dst_conn, dst_username, dst_table_name, no_fk=False)
    if not is_same:
        rs = 0
        print('\n')
        print(rs, src_username + '.' + src_table_name)
        print('\n')
        print(mess)
    else:
        rs = 1
        print(rs, src_username + '.' + src_table_name)


def get_table_map_list(src_db):
    # 解析出需要迁移的表以及映射关系
    table_map_list = []
    for table_mess in tables.split(','):
        table_mess = table_mess.strip()
        src_schema = table_mess.split('.')[0].strip().upper()
        src_table = table_mess.split('.')[1].strip()
        
        if src_table == '*':
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema + "' order by 1 desc"
            tables_from_sql = src_db.run(select_tables_sql).get_rows()
            for table_from_sql in tables_from_sql:
                table_map = (src_schema, table_from_sql[0])
                if table_map not in table_map_list:
                    table_map_list.append(table_map)
        else:
            table_map = (src_schema, src_table)
            if table_map not in table_map_list:
                table_map_list.append(table_map)
    return table_map_list

            
if __name__ == '__main__': 
    main()

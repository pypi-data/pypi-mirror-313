# coding:utf-8
from tools_hjh import DBConn, Tools, ProcessPool
from tools_hjh.Tools import locatdate
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import OracleTools
import time
from math import ceil
import sys
from uuid import uuid4

help_mess = '''Version 1.4.5

使用方法
python3 ora2pg.py example.conf run_mode example.log
example.log会被清空重写

run_mode : ↓
copy_table 复制表结构，包括表、分区和注释，也包括列上的默认值和非空约束 
copy_data 复制数据，tables参数的对象必须是自己库的表、视图或同义词等，不能是引用其他库的dblink
copy_index 复制索引
copy_pk 复制主键
copy_fk 复制外键
copy_uk 复制唯一键
copy_sequence 复制序列
copy_from_sql 根据给入的SQL去Oracle查询，结果复制数据到PG
compare_data_number 统计每个表在Oracle和PG端的数据量是否一致，但是不会校对数据
compare_index 统计每个表在Oracle和PG端的索引量是否一致（不包含约束自带的索引），但是不会比较索引列
compare_constraint 统计每个表在Oracle和PG端的主键+外键+唯一键数量是否一致
get_table_ddl 得到copy_table的PG端的SQL到日志文件
get_table_oracle_ddl 得到copy_table的Oracle端的SQL到日志文件
drop_fk 删除PG端已存在的外键

注意事项：
copy_table，表名列名无论oracle中是大小写，转为pg中一律为小写
copy_table，if_clear=true会提前drop table，如果表存在外键关联第一次可能删不掉，多执行几次copy_table即可
copy_table，rowid类型会转为varchar(18)，而不是oid，转为oid数据迁移不过去
copy_data，oracle中的chr(0)会被强行替换为chr(32)
copy_data，oracle中date和timestamp类型中的0000年会被强行替换为0001年，00月替换为01月，00日替换为01日
copy_data，收集元数据时，会count表，if_count_full=true则强制走全表，避免索引与表不同步的情况，因此大表可能比较慢
copy_index，if_clear决定是否会先drop已存在索引
copy_index，如果索引名已被占用（被其他对象占用），且if_clear=true会自动重命名
copy_index，对于分区表的唯一索引，会自动在末尾加入分区字段
copy_index，sys_op_c2c(cols)函数会被去掉，仅索引cols
copy_pk、copy_fk、copy_uk，使用命名模式，重名会失败
copy_pk、copy_fk、copy_uk，if_clear决定是否会先drop已存在约束
copy_pk、copy_uk，对于分区表的主键和唯一键，会自动在末尾加入分区字段
compare_data_number，只会比较两端每个表行数是否一致，而无法校对数据
compare_index、compare_constraint，只会比较两端每个表的索引数量、键数量是否一致，而不会去比较被索引或被键的字段
copy_from_sql，不支持并行
drop_fk，重建pk的时候如果有外键依赖则删除不了，所以设置删除外键的选项

目前已发现的容易出问题的情况有：
1.被索引字段含有函数
2.默认值含有函数
3.Oracle中存在大小写不同但是名字相同的表，于是出现多对一的情况
4.对于tables中的对象是视图的情况，可以同步表结构和数据，但是无法同步分区、注释、索引、约束等信息
5.如果tables中的源表是一个通过dblink同步过来的视图或同义词，copy_data会失败，但是却可以通过copy_from_sql抽取
'''

date = locatdate().replace('-', '')

try:
    run_mode = sys.argv[2]
except:
    run_mode = None
try:
    config_file = sys.argv[1]
except:
    config_file = None
try:
    log_file = sys.argv[3]
except:
    log_file = date + '.log'
    
if config_file == None or config_file == 'help':
    print(help_mess)
    sys.exit()

Tools.rm(log_file)
log = Log(log_file)

conf = Tools.cat(config_file)
conf_map = {}
for line in conf.split('\n'):
    if '=' in line and '#' not in line:
        key = line.split('=', 1)[0].strip()
        val = line.split('=', 1)[1].strip()
        conf_map[key] = val

forever_number_to_numeric = conf_map['forever_number_to_numeric']
if forever_number_to_numeric == 'true':
    forever_number_to_numeric = True
else:
    forever_number_to_numeric = False

if_auto_count = conf_map['if_auto_count']
if_count_full = conf_map['if_count_full']
smallest_object = conf_map['smallest_object']
if_only_insert = conf_map['if_only_insert']
if_clear = conf_map['if_clear']
if_only_scn = conf_map['if_only_scn']
if_optimize_clob = conf_map['if_optimize_clob']

src_db_type = conf_map['src_db_type']
src_ip = conf_map['src_ip']
src_port = int(conf_map['src_port'])
src_database = conf_map['src_db']
src_read_username = conf_map['src_read_username']
src_read_password = conf_map['src_read_password']

tables = conf_map['tables']
exclude_tables = conf_map['exclude_tables']
sqls = conf_map['copy_from_sql']

dst_db_type = conf_map['dst_db_type']
dst_ip = conf_map['dst_ip']
dst_port = int(conf_map['dst_port'])
dst_database = conf_map['dst_db']
dst_username = conf_map['dst_username']
dst_password = conf_map['dst_password']

parallel_num = int(conf_map['parallel_num'])
if parallel_num < 1:
    parallel_num = 1
    
max_page_num = int(conf_map['page_num'])
if max_page_num < 1:
    max_page_num = 1
if max_page_num > parallel_num:
    max_page_num = parallel_num - 1

save_parallel = 3

once_mb = 20
once_num_normal = 50000
once_num_lob = 10000

input_global_scn = conf_map['scn']

tables_data_num = {}
tasks = []

scn_time = 0
get_matedata_over = False


# 主控制程序
def main():
    if run_mode == 'copy_data':
        copy_data()
        
    elif run_mode == 'copy_table' or run_mode == 'get_table_ddl':
        copy_table(run_mode)
        
    elif run_mode == 'copy_index':
        copy_index()
        
    elif run_mode == 'copy_pk' or run_mode == 'copy_uk' or run_mode == 'copy_fk' or run_mode == 'drop_fk':
        copy_constraint(run_mode)
        
    elif run_mode == 'copy_sequence':
        copy_sequence()
        
    elif run_mode == 'compare_data_number':
        compare_data_number()
        
    elif run_mode == 'compare_index':
        compare_index()
        
    elif run_mode == 'compare_constraint':
        compare_constraint()
        
    elif run_mode == 'copy_from_sql':
        copy_from_sql()
    
    elif run_mode == 'get_table_oracle_ddl':
        get_table_oracle_ddl()
    
    else:
        print(help_mess)


def get_table_map_list(src_db):
    # 解析出需要迁移的表以及映射关系
    table_map_list = []
    for table_mess in tables.split('[--split--]'):
        table_mess = table_mess.strip()
        src_where = '1=1'
        if '-->' in table_mess:
            if 'where' in table_mess:
                src_schema = table_mess.split('-->')[0].split('.')[0].strip().upper()
                src_table = table_mess.split('-->')[0].split('.')[1].split('where')[0].strip()
                src_where = table_mess.split('-->')[0].split('.')[1].split('where')[1].strip()
            else:
                src_schema = table_mess.split('-->')[0].split('.')[0].strip().upper()
                src_table = table_mess.split('-->')[0].split('.')[1].strip()
            dst_schema = table_mess.split('-->')[1].split('.')[0].strip()
            dst_table = table_mess.split('-->')[1].split('.')[1].strip()
        else:
            if 'where' in table_mess:
                src_schema = table_mess.split('.')[0].strip().upper()
                src_table = table_mess.split('.')[1].split('where')[0].strip()
                src_where = table_mess.split('.')[1].split('where')[1].strip()
            else:
                src_schema = table_mess.split('.')[0].strip().upper()
                src_table = table_mess.split('.')[1].strip()
            dst_schema = src_schema.lower()
            dst_table = src_table.lower()
            
        if src_table == '*':
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema + "' order by 1 desc"
            tables_from_sql = src_db.run(select_tables_sql).get_rows()
            for table_from_sql in tables_from_sql:
                if '-->' in table_mess:
                    table_map = (src_schema, table_from_sql[0], dst_schema, table_from_sql[0].lower(), src_where)
                else:
                    table_map = (src_schema, table_from_sql[0], src_schema.lower(), table_from_sql[0].lower(), src_where)
                if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                    table_map_list.append(table_map)
        else:
            table_map = (src_schema, src_table, dst_schema, dst_table, src_where)
            if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                table_map_list.append(table_map)
    return table_map_list

        
def copy_data():
        
    # 获取连接
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 1)
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    # 清理表
    if if_clear == 'true':
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 1)
        tp = ThreadPool(parallel_num)
        for table_map in table_map_list:
            tp.run(truncate_table, (dst_db, table_map))
        tp.wait()
        dst_db.close()
            
    # 获取scn，如果需要
    if if_only_scn == 'true' and len(input_global_scn) == 0:
        global scn_time
        global_scn, scn_time = src_db.run("select to_char(current_scn),to_char(SYSTIMESTAMP(6),'yyyy-mm-dd hh24:mi:ss.ff6') from v$database").get_rows()[0]
    elif if_only_scn == 'true' and len(input_global_scn) > 0:
        global_scn = input_global_scn
    else:
        global_scn = None
    
    # 多线程启动表分析程序    
    def run_get_table_metadata(tp, src_db):
        try:
            global get_matedata_over
            for table_map in table_map_list:
                qrs = src_db.run('select * from ' + table_map[0] + '."' + table_map[1] + '" where rownum = 1')
                col_desc = qrs.get_cols_description()
                rows = qrs.get_rows()
                if len(rows) > 0:
                    tp.run(get_table_metadata, (src_db, table_map, global_scn, col_desc), name=table_map[0] + '.' + table_map[1])
            
            # 监控元数据获取未完成的表
            log.info('获取元数据任务全部分配完成。')
            while True:
                if tp.get_running_num() > 0 and tp.get_running_num() <= parallel_num:
                    log.info('获取元数据，正在执行的表：' + str(set(tp.get_running_name())))
                    
                if tp.get_running_num() > 0:
                    time.sleep(5)
                else:
                    break
            
            # 等待获取元数据完全完成
            tp.wait()
            src_db.close()
            get_matedata_over = True
            log.info('获取元数据任务全部执行完成。')
        except Exception as _:
            log.error(str(_))
        
    tp = ThreadPool(parallel_num)
    ttp = ThreadPool(1)
    ttp.run(run_get_table_metadata, (tp, src_db,))
    # ttp.wait()
    
    def error_callback(e):
        log.error(str(e))
    
    # 多进程启动导数
    pp = ProcessPool(parallel_num)
    already_run_tasks = []
    while True:
        time.sleep(3)
        for task in tasks.copy():
            if task not in already_run_tasks:
                already_run_tasks.append(task)
                pp.run(get_data_from_oracle, task, name=task[1], error_callback=error_callback)
    
        if len(tasks) == len(already_run_tasks) and get_matedata_over:
            log.info('导数任务全部分配完成。')
            break
    
    while True:
        if len(set(pp.get_running_name())) > 0 and len(set(pp.get_running_name())) <= parallel_num:
            log.info('导数任务，正在执行的任务：' + str(len(set(pp.get_running_name()))) + '个' + '，' + str(set(pp.get_running_name())))
        else:
            log.info('导数任务，正在执行的任务：' + str(len(set(pp.get_running_name()))) + '个')
            
        if pp.get_running_num() > 0:
            time.sleep(5)
        else:
            break
        
    pp.wait()
    log.info('导数任务全部执行完成。')
    
    # 获取输出报告
    if if_auto_count == 'true':
        compare_data_number()


def truncate_table(dst_db, table_map):
    try:
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        truncate_table_sql = 'truncate table ' + dst_schema + '."' + dst_table.lower() + '" cascade'
        dst_cur = dst_conn.cursor()
        dst_cur.execute(truncate_table_sql)
        dst_conn.commit()
        log.info('PG执行SQL成功', truncate_table_sql)
    except Exception as _:
        log.warning('PG执行SQL失败', truncate_table_sql, str(_))
    finally:
        dst_cur.close()
        dst_conn.close()


# 表分析程序
def get_table_metadata(src_db, table_map, global_scn, col_desc):

    def fenye(table_map, mess, table_scn, table_metadata):
        my_once_num = once_num_normal
        for c in col_desc:
            if 'LOB' in str(c[1]) or 'RAW' in str(c[1]) or 'LONG' in str(c[1]):
                my_once_num = once_num_lob
                break
        
        if max_page_num == 1:
            if if_count_full == 'true':
                count_sql = 'select /*+full(t) parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            else:
                count_sql = 'select /*+parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            src_num = src_db.run(count_sql).get_rows()[0][0]
            tasks.append((table_map, mess, table_scn, col_desc, table_metadata, None, None))
        else:
            # 分页
            if if_count_full == 'true':
                count_sql = 'select /*+full(t) parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            else:
                count_sql = 'select /*+parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            src_num = src_db.run(count_sql).get_rows()[0][0]
            log.info('获取源端数据量成功', mess, str(src_num))
            if src_num < my_once_num * max_page_num:
                tasks.append((table_map, mess, table_scn, col_desc, table_metadata, None, None))
            else:
                page_rn = ceil(src_num / max_page_num)
                for page in range(1, max_page_num + 1):
                    tasks.append((table_map, mess, table_scn, col_desc, table_metadata, page, page_rn))
        return src_num
    
    try:
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        src_where = table_map[4]

        # 如果没有scn，则此处获取
        if global_scn is None:
            table_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        else:
            table_scn = global_scn
            
        # 判定“表”是什么
        object_type = ''
        sql = 'select wm_concat(distinct object_type) from dba_objects where owner = ? and object_name = ?'
        rows = src_db.run(sql, (src_schema, src_table)).get_rows()
        if len(rows) == 0:
            object_type = 'other'
        elif 'TABLE' in str(rows[0]):
            object_type = 'table'
            table_metadata = OracleTools.get_table_metadata(src_db, src_schema, src_table, partition=True)
        elif 'VIEW' in str(rows[0]):
            object_type = 'view'
        elif 'SYNONYM' in str(rows[0]):
            object_type = 'synonym'
        else:
            object_type = 'other'
                
        report_table_id = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table
        # 如果是表，获取表元数据信息，遍历分区子分区，多进程分配查询任务及后续任务
        if object_type == 'table':
            src_num = 0
            partition_mess = table_metadata['partition']
            if partition_mess is not None and smallest_object != 'table':
                for partition in partition_mess['partitions']:
                    partition_name = partition['name']
                    subpartitions = partition['subpartitions']
                    # 子分区
                    if len(subpartitions) > 0 and smallest_object == 'subpartition':
                        for subpartition in subpartitions:
                            subpartition_name = subpartition['name']
                            mess = src_schema + '."' + src_table + '" subpartition(' + subpartition_name + ')'
                            src_num = src_num + fenye(table_map, mess, table_scn, table_metadata)
                    # 分区
                    else:
                        mess = src_schema + '."' + src_table + '" partition(' + partition_name + ')'
                        src_num = src_num + fenye(table_map, mess, table_scn, table_metadata)
            # 单表
            else:
                mess = src_schema + '."' + src_table + '"'
                src_num = fenye(table_map, mess, table_scn, table_metadata)
        # 其他类型
        else:
            table_metadata = None
            mess = src_schema + '."' + src_table + '"'
            src_num = fenye(table_map, mess, table_scn, table_metadata)
        tables_data_num[report_table_id] = [table_scn, src_num, None]
        log.info('获取表元数据成功', src_schema + '.' + src_table)
    except Exception as _:
        log.error('获取表元数据失败', src_schema + '.' + src_table, str(_))


def get_data_from_oracle(table_map, mess, table_scn, col_desc, table_metadata=None, page=None, page_rn=None):
    src_where = table_map[4]
    dst_schema = table_map[2]
    select_sql = ''
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=save_parallel + 1, options='-c search_path=' + dst_schema + ',public')
        
        # copy中转为csv要用
        cols_for_copy = col_desc
        # cols_for_copy = src_db.run('select * from ' + mess + ' where rownum = 1').get_cols_description()
        if table_metadata is not None:
            idx = 0
            for col in table_metadata['columns']:
                virtual = col['virtual']
                if virtual == 'YES':
                    cols_for_copy.pop(idx)
                idx = idx + 1
        
        # 解析列，用于拼接cols_str和merge_col，处理char，拆分clob
        if_exists_clob = False
        if_exists_blob = False
        cols_str = ''
        idx = 0
        idx2 = 0
        merge_col = []
        once_num = once_num_normal
        for col in cols_for_copy:
            merge_col.append([])
            if 'CHAR' in str(col[1]):
                merge_col[idx] = [idx2]
                idx2 = idx2 + 1
                cols_str = cols_str + 'translate("' + col[0] + '",chr(0),chr(32)),' 
            elif 'CLOB' in str(col[1]) and if_optimize_clob == 'true':
                if_exists_clob = True
                once_num = once_num_lob
                merge_col[idx] = []
                sql = 'select nvl(max(length(' + col[0] + ')),0) from ' + mess + ' as of scn ' + table_scn
                max_len = src_db.run(sql).get_rows()[0][0]
                col_split_num = ceil(int(max_len) / 1300)
                for sub_idx in range(1, col_split_num + 1):
                    cols_str = cols_str + 'nvl(translate(to_char(substr(' + col[0] + ',' + str(sub_idx - 1) + "*1300+1,1300)),chr(0),chr(32)),''),"
                    merge_col[idx].append(idx2)
                    idx2 = idx2 + 1
            elif 'CLOB' in str(col[1]) and if_optimize_clob != 'true':
                if_exists_clob = True
                once_num = once_num_lob
                merge_col[idx] = [idx2]
                idx2 = idx2 + 1
                cols_str = cols_str + 'replace("' + col[0] + '",chr(0),chr(32)),' 
            elif 'DATE' in str(col[1]):
                merge_col[idx] = [idx2]
                idx2 = idx2 + 1
                cols_str = cols_str + '''replace(replace(replace(to_char("''' + col[0] + '''",'yyyy-mm-dd hh24:mi:ss'),'0000-','0001-'),'-00-','-01-'),'-00','-01'),'''
            elif 'TIMESTAMP' in str(col[1]):
                merge_col[idx] = [idx2]
                idx2 = idx2 + 1
                cols_str = cols_str + '''replace(replace(replace(to_char("''' + col[0] + '''",'yyyy-mm-dd hh24:mi:ss.ff9'),'0000-','0001-'),'-00-','-01-'),'-00','-01'),'''
            elif 'BLOB' in str(col[1]) or 'RAW' in str(col[1]):
                if_exists_blob = True
                once_num = once_num_lob
                merge_col[idx] = [idx2]
                idx2 = idx2 + 1
                cols_str = cols_str + '"' + col[0] + '",' 
            else:
                merge_col[idx] = [idx2]
                idx2 = idx2 + 1
                cols_str = cols_str + '"' + col[0] + '",' 
            idx = idx + 1
        cols_str = cols_str[:-1]
        
        # 组装抽数sql
        if page is None:
            select_sql = 'select /*+full(t)*/ ' + cols_str + '  from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
        else:
            select_sql = '''
                select ''' + cols_str + ''' from (
                    select /*+full(t)*/ t.*,rownum rn 
                    from ''' + mess + ''' 
                    as of scn ''' + str(table_scn) + ''' t
                    where rownum <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                    and ''' + src_where + '''
                ) where rn <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                and rn > ''' + str(page - 1) + ''' * ''' + str(page_rn) + '''
            '''
            
        # 开始抽数
        rs = src_db.run(select_sql)
        i = 1
        tp = ThreadPool(save_parallel)
        while True:
            if page is None:
                my_mess = mess + '(' + str(i) + ')'
            else:
                my_mess = mess + '(' + str(page) + '-' + str(i) + ')'
            time_start = time.time()
            rows = []
            rows_new = []
            while True:
                rss = rs.get_rows(once_num)
                if len(rss) == 0:
                    break
                else:
                    rows.extend(rss)
                if len(str(rows).encode('utf-8')) / 1024 / 1024 >= once_mb:
                    break
            # 如果含有clob，且之前有做拆分，此处再拼接回来
            if if_exists_clob and if_optimize_clob == 'true':
                for row in rows:
                    idx = 0
                    row_new = []
                    for cols_idx in merge_col:
                        if len(cols_idx) == 1:
                            cell = row[cols_idx[0]]
                        else:
                            cell = None
                            for col_idx in cols_idx:
                                if row[col_idx] is None:
                                    pass
                                elif type(row[col_idx]) == str:
                                    if type(cell) != str:
                                        cell = ''
                                    cell = cell + row[col_idx]
                                elif type(row[col_idx]) == bytes:
                                    if type(cell) != bytes:
                                        cell = b''
                                    cell = cell + row[col_idx]
                        row_new.append(cell)
                        idx = idx + 1
                    rows_new.append(row_new)
            else:
                rows_new = rows
                    
            select_time = time.time() - time_start
            if len(rows_new) == 0:
                break
            else:
                tp.run(save_to_pg, (dst_db, table_map, rows_new, cols_for_copy, my_mess, select_time, table_scn, if_exists_blob))
                # save_to_pg(dst_db, table_map, rows_new, cols_for_copy, my_mess, select_time, table_scn, if_exists_blob)
            i = i + 1
        tp.wait()
    except Exception as _:
        log.error('到Oracle获取数据失败', mess, str(_), select_sql)
    finally:
        src_db.close()
        dst_db.close()

        
def get_data_from_sql(table_map): 
    dst_schema = table_map[2].lower()
    dst_table = table_map[3].lower()
    select_sql = table_map[1]
    mess = select_sql + '-->' + dst_schema + '.' + dst_table
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=save_parallel + 1, options='-c search_path=' + dst_schema + ',public')
                
        rs = src_db.run(select_sql)
        cols = rs.get_cols_description()
        if_exists_blob = False
        
        if 'LOB' in str(cols):
            once_num = once_num_lob
        else:
            once_num = once_num_normal
        
        i = 1
        tp = ThreadPool(save_parallel)
        while True:
            time_start = time.time()
            rows = []
            while True:
                rss = rs.get_rows(once_num)
                if len(rss) == 0:
                    break
                else:
                    rows.extend(rss)
                if len(str(rows).encode('utf-8')) / 1024 / 1024 >= once_mb:
                    break
            select_time = time.time() - time_start
            if len(rows) == 0:
                break
            tp.run(save_to_pg, (dst_db, table_map, rows, cols, mess, select_time, '', if_exists_blob))
            i = i + 1
        tp.wait()
    except Exception as _:
        log.error('通过SQL获取数据失败', dst_schema + '.' + dst_table, str(_))
    finally:
        src_db.close()
        dst_db.close()

        
def save_to_pg(dst_db, table_map, rows, cols, mess, select_time, table_scn, if_exists_blob):
    rows_size = len(str(rows).encode('utf-8')) / 1024 / 1024
    dst_owner = table_map[2]
    dst_table = table_map[3]
    src_where = table_map[4]
    time_start = time.time()
    
    wenhaos = ''
    for _ in cols:
        wenhaos = wenhaos + '?,'
    wenhaos = wenhaos[0:-1]
    
    cols_str = ''
    for col in cols:
        cols_str = cols_str + '"' + col[0].lower() + '",'
    cols_str = cols_str[0:-1]
    
    insert_sql = 'insert into ' + dst_owner + '."' + dst_table + '"(' + cols_str + ') values(' + wenhaos + ')'
    
    if if_only_insert == 'true' or if_exists_blob:
        try:
            num = dst_db.run(insert_sql, rows)
            if num == -1:
                raise Exception('unknown error, num = -1')
            num = str(num) + '(insert)' 
        except Exception as _:
            log.error('写入PG失败', mess, str(_))
            return
    else:
        try:
            num = dst_db.pg_copy_from(dst_table.lower(), rows, cols)
            num = str(num) + '(copy)' 
        except Exception as _:
            log.warning('写入PG失败，改为insert重试', mess, str(_))
            try:
                num = dst_db.run(insert_sql, rows)
                if num == -1:
                    raise Exception('unknown error, num = -1')
                num = str(num) + '(insert)' 
            except Exception as _:
                log.error('写入PG失败', mess, str(_))
                return

    save_time = time.time() - time_start
    if src_where == '1=1':
        src_where = ''
    try:
        read_speed = str(round(rows_size / select_time, 2))
    except:
        read_speed = '∞'
    try:
        write_speed = str(round(rows_size / save_time, 2))
    except:
        write_speed = '∞'
    log.info('写入PG成功', mess, src_where, num, '大小=' + str(round(rows_size, 2)) + 'MB', '读速=' + read_speed + 'MB/s', '写速=' + write_speed + 'MB/s', 'scn=' + table_scn)


def copy_from_sql():
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 1)
        
    table_map_list = []
    for table_mess in sqls.split('[--split--]'):
        dst_schema = table_mess.split('-->')[1].split('.')[0].lower()
        dst_table = table_mess.split('-->')[1].split('.')[1].lower()
        src_sql = table_mess.split('-->')[0]
        table_map_list.append((None, src_sql, dst_schema, dst_table, None))
        
    # 清理表
    if if_clear == 'true':
        tp = ThreadPool(parallel_num)
        for table_map in table_map_list:
            tp.run(truncate_table, (dst_db, table_map,))
        tp.wait()
        
    # 多进程启动导数
    pp = ProcessPool(parallel_num)
    for table_map in table_map_list:
        pp.run(get_data_from_sql, (table_map,))
    pp.wait()
    
    dst_db.close()

    
def copy_index():

    def copy_one_index(table_map):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
        
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2].lower()
        dst_table = table_map[3].lower()
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        
        # 删除此表已存在的索引
        if if_clear == 'true':
            select_exists_index = "select indexname from pg_indexes t where not exists(select 1 from information_schema.constraint_table_usage t2 where t2.table_catalog = ? and t2.table_schema = t.schemaname and t2.table_name = t.tablename and t2.constraint_name = t.indexname) and t.schemaname = '" + dst_schema + "' and t.tablename = '" + dst_table + "'"
            rss = dst_db.run(select_exists_index, (dst_database,)).get_rows()
            for rs in rss:
                drop_index_sql = 'drop index ' + dst_schema + '."' + rs[0] + '"'
                try:
                    dst_cur.execute(drop_index_sql)
                    dst_conn.commit()
                    log.info('PG执行SQL成功', drop_index_sql)
                except Exception as _:
                    log.error('PG执行SQL失败', drop_index_sql, str(_))
                
        sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, forever_number_to_numeric=forever_number_to_numeric)
        for sql in sqls:
            if sql.startswith('create table '):
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                sql = sql.replace(' ' + src_schema.lower() + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table.lower() + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info('PG执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and if_clear == 'true':
                        log.warning('PG存在重名对象，自动改名重试', sql, str(_))
                        index_name = sql.split(' on ')[0].split(' ')[-1].strip('"')
                        index_name_new = 'idx_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' index "' + index_name, ' index "' + index_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info('PG执行SQL成功', sql)
                        except Exception as _:
                            log.error('PG执行SQL失败', sql, str(_))
                    else:
                        log.error('PG执行SQL失败', sql, str(_))
            elif sql.startswith('comment on '):
                pass
            elif sql.startswith('alter table ') and ' foreign key (' in sql:
                pass
            else:
                pass
        
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        dst_schema = table_map[2]
        dst_cur.execute('create schema if not exists ' + dst_schema)
        dst_conn.commit()
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(copy_one_index, (table_map,))
    tp.wait()
        
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()

    
def copy_table(run_mode):

    def copy_one_table(src_db, dst_db, table_map, run_mode):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2].lower()
        dst_table = table_map[3].lower()
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        is_suc = True
    
        drop_sql = 'drop table if exists ' + dst_schema + '."' + dst_table + '"'
        if run_mode == 'copy_table':
            try:
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info('PG执行SQL成功', drop_sql)
            except Exception as _:
                log.error('PG执行SQL失败', drop_sql, str(_))
        elif run_mode == 'get_table_ddl':
            log.out(drop_sql + ' ;')
            
        try:
            sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, forever_number_to_numeric=forever_number_to_numeric)
        except Exception as _:
            log.error('元数据获取失败', src_schema + '.' + src_table, str(_))
            return
        
        for sql in sqls:
            if sql.startswith('alter table') and ' foreign key (' in sql:
                pass
            elif sql.startswith('alter table') and ' primary key (' in sql:
                pass
            elif sql.startswith('alter table') and ' unique (' in sql:
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                pass
            else:
                sql = sql.replace(' ' + src_schema.lower() + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table.lower() + '"', '."' + dst_table + '"')
                if run_mode == 'copy_table':
                    try:
                        dst_cur.execute(sql)
                        dst_conn.commit()
                    except Exception as _:
                        is_suc = False
                        if sql.startswith('create table ') and 'partition of' not in sql:
                            log.error('PG创建表失败', sql, str(_))
                            break
                        log.error('PG执行SQL失败', sql, str(_))
                elif run_mode == 'get_table_ddl':
                    log.out(sql + ' ;')
                    
        if run_mode == 'copy_table' and is_suc: 
            log.info('PG创建表成功', src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table)
        if run_mode == 'get_table_ddl':
            log.out('')
        
        dst_cur.close()
        dst_conn.close()
            
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 1)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 1)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    if run_mode == 'copy_table':
        for table_map in table_map_list:
            dst_schema = table_map[2]
            dst_cur.execute('create schema if not exists ' + dst_schema)
            dst_conn.commit()
    
    if run_mode == 'get_table_ddl':
        tp = ThreadPool(1)
    elif run_mode == 'copy_table': 
        tp = ThreadPool(parallel_num)
        
    for table_map in table_map_list:
        tp.run(copy_one_table, (src_db, dst_db, table_map, run_mode))
    tp.wait()
    
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def copy_constraint(run_mode):
    
    def clear_k(table_map, run_mode):
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        
        dst_schema = table_map[2].lower()
        dst_table = table_map[3].lower()
        
        sql = '''
            select con.conname
            from pg_catalog.pg_constraint con
            inner join pg_catalog.pg_class rel on rel.oid = con.conrelid
            inner join pg_catalog.pg_namespace nsp on nsp.oid = connamespace
            where nsp.nspname = ?
            and rel.relname = ?
            and contype = ?
        '''
        
        if run_mode == 'copy_pk':
            rss = dst_db.run(sql, (dst_schema, dst_table, 'p')).get_rows()
        if run_mode == 'copy_uk':
            rss = dst_db.run(sql, (dst_schema, dst_table, 'u')).get_rows()
        if run_mode == 'copy_fk' or run_mode == 'drop_fk':
            rss = dst_db.run(sql, (dst_schema, dst_table, 'f')).get_rows()
        
        for rs in rss:
            try:
                drop_sql = 'alter table ' + dst_schema + '.' + dst_table + ' drop constraint "' + rs[0] + '"'
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info('PG执行SQL成功', drop_sql)
            except Exception as _:
                log.error('PG执行SQL失败', drop_sql, str(_))
        
        dst_cur.close()
        dst_conn.close()
        dst_db.close()

    def copy_k(table_map, run_mode):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
    
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2].lower()
        dst_table = table_map[3].lower()
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, forever_number_to_numeric=forever_number_to_numeric)
        for sql in sqls:
            if sql.startswith('create table '):
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                pass
            elif sql.startswith('comment on '):
                pass
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' foreign key (' in sql and run_mode == 'copy_fk':
                sql = sql.replace(' ' + src_schema.lower() + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table.lower() + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info('PG执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and if_clear == 'true':
                        log.warning('PG存在重名对象，自动改名重试', sql, str(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'fk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info('PG执行SQL成功', sql)
                        except Exception as _:
                            log.error('PG执行SQL失败', sql, str(_))
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' unique (' in sql and run_mode == 'copy_uk':
                sql = sql.replace(' ' + src_schema.lower() + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table.lower() + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info('PG执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and if_clear == 'true':
                        log.warning('PG存在重名对象，自动改名重试', sql, str(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'uk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info('PG执行SQL成功', sql)
                        except Exception as _:
                            log.error('PG执行SQL失败', sql, str(_))
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' primary key (' in sql and run_mode == 'copy_pk':
                sql = sql.replace(' ' + src_schema.lower() + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table.lower() + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info('PG执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and if_clear == 'true':
                        log.warning('PG存在重名对象，自动改名重试', sql, str(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'pk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info('PG执行SQL成功', sql)
                        except Exception as _:
                            log.error('PG执行SQL失败', sql, str(_))
                    
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        dst_schema = table_map[2]
        dst_cur.execute('create schema if not exists ' + dst_schema)
        dst_conn.commit()
    
    tp = ThreadPool(parallel_num)
    
    if if_clear == 'true' or run_mode == 'drop_fk':
        for table_map in table_map_list:
            tp.run(clear_k, (table_map, run_mode))
        tp.wait()
    
    if run_mode != 'drop_fk':
        for table_map in table_map_list:
            tp.run(copy_k, (table_map, run_mode))
        tp.wait()
        
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()

    
def copy_sequence():
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    table_map_list = get_table_map_list(src_db)
    sql = 'select * from dba_sequences where sequence_owner = ?'
    
    schemas = []
    for table_map in table_map_list:
        if (table_map[0], table_map[2]) not in schemas:
            schemas.append((table_map[0], table_map[2]))
            
    for schema in schemas:
        src_schema = schema[0]
        dst_schema = schema[1]        
        rows = src_db.run(sql, (src_schema,)).get_rows()
        for row in rows:
            # sequence_owner = row[0]
            sequence_name = row[1]
            min_value = row[2]
            max_value = row[3]
            increment_by = row[4]
            cycle_flag = row[5]
            # order_flag = row[6]
            cache_size = row[7]
            last_number = row[8]
            if max_value > 9223372036854775807:
                max_str = 'no maxvalue'
            else:
                max_str = 'maxvalue ' + str(max_value)
            if cache_size == 0:
                cache_str = ''
            else:
                cache_str = 'cache ' + str(cache_size)
            if cycle_flag == 'N':
                cycle_str = ''
            else:
                cycle_str = 'cycle'
            drop_sql = 'drop sequence if exists ' + dst_schema.lower() + '.' + sequence_name.lower()
            dst_cur.execute(drop_sql)
            dst_conn.commit()
            log.info('PG执行SQL成功', drop_sql)
            create_sql = 'create sequence ' + dst_schema.lower() + '.' + sequence_name.lower() + ' increment ' + str(increment_by) + ' minvalue ' + str(min_value) + ' ' + max_str + ' start ' + str(last_number) + ' ' + cache_str + ' ' + cycle_str 
            create_sql = Tools.merge_spaces(create_sql).strip()
            try:
                dst_cur.execute(create_sql)
                dst_conn.commit()
                log.info('PG执行SQL成功', create_sql)
            except Exception as _:
                log.error('PG执行SQL失败', create_sql, str(_))
            
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def compare_data_number():
    tp = ThreadPool(parallel_num)

    def count(table_map, src_db, dst_db, global_scn):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        src_where = table_map[4]
        
        report_table_id = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table
        if report_table_id in tables_data_num:
            table_scn = tables_data_num[report_table_id][0]
        else:
            table_scn = global_scn
        
        if if_count_full == 'true':
            src_sql = 'select /*+full(t) parallel(1)*/ count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + table_scn + ' t where ' + src_where
        else:
            src_sql = 'select /*+parallel(1)*/ count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + table_scn + ' t where ' + src_where
        dst_sql = 'select count(1) from ' + dst_schema + '."' + dst_table.lower() + '"'
        
        e1 = ''
        e2 = ''
        try:
            src_num = None
            if report_table_id in tables_data_num:
                src_num = tables_data_num[report_table_id][1]
            if src_num is None:
                src_num = int(src_db.run(src_sql).get_rows()[0][0])
        except Exception as _:
            src_num = -1
            e1 = str(_)
        try:
            dst_num = int(dst_db.run(dst_sql).get_rows()[0][0])
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        
        tables_data_num[report_table_id] = [table_scn, src_num, dst_num]
        log.info('表数据量是否一致：' + str(tables_data_num[report_table_id][1] == tables_data_num[report_table_id][2]), report_table_id, 'src=' + str(tables_data_num[report_table_id][1]), 'dst=' + str(tables_data_num[report_table_id][2]), 'scn=' + table_scn, str(e1), str(e2))

    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 1)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 1)
    except Exception as _:
        log.error('连接数据库失败', str(_))
        
    # 如果没有scn，则此处获取
    if len(input_global_scn) == 0:
        global_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
    else:
        global_scn = input_global_scn
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    error_table = ''
    for table_map in table_map_list:
        tp.run(count, (table_map, src_db, dst_db, global_scn))
    tp.wait()
        
    for k in tables_data_num:
        if tables_data_num[k][1] != tables_data_num[k][2]:
            error_table = error_table + k + '[--split--]'
    error_table = error_table[:-11]
            
    log.info('数据量不一致的表：' + error_table)
    
    if scn_time != 0 and if_only_scn == 'true' and run_mode == 'copy_data':
        log.info('数据版本时间：' + str(scn_time))
        
    src_db.close()
    dst_db.close()

        
def compare_index():

    def compare_index_one(src_db, dst_db, table_map):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2].lower()
        dst_table = table_map[3].lower()
        
        e1 = ''
        e2 = ''
        src_sql = "select count(distinct t.index_name) from dba_indexes t where not exists(select 1 from dba_constraints t2 where t2.owner = t.table_owner and t2.table_name = t.table_name and t2.constraint_name = t.index_name) and t.index_type not in('LOB') and t.table_owner = '" + src_schema + "' and t.table_name = '" + src_table + "'"
        dst_sql = "select count(distinct t.indexname) from pg_indexes t where not exists(select 1 from information_schema.constraint_table_usage t2 where t2.table_catalog = ? and t2.table_schema = t.schemaname and t2.table_name = t.tablename and t2.constraint_name = t.indexname) and t.schemaname = '" + dst_schema + "' and t.tablename = '" + dst_table + "'"
        try:
            src_num = src_db.run(src_sql).get_rows()[0][0]
        except Exception as _: 
            src_num = -1
            e1 = str(_)
        try:
            dst_num = dst_db.run(dst_sql, (dst_database,)).get_rows()[0][0]
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        log.info('表索引数量是否一致：' + str(src_num == dst_num), src_schema + '.' + src_table, 'src=' + str(src_num), 'dst=' + str(dst_num), str(e1), str(e2))
    
    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 1)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 1)
    except Exception as _:
        log.error('比较索引数量时，Oracle连接失败', str(_))
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(compare_index_one, (src_db, dst_db, table_map))
    tp.wait()

    src_db.close()
    dst_db.close()

    
def compare_constraint():

    def compare_constraint_one(src_db, table_map):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2].lower()
        dst_table = table_map[3].lower()
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, options='-c search_path=' + dst_schema + ',public')
        e1 = ''
        e2 = ''
        src_sql = "select count(distinct constraint_name) from dba_constraints where constraint_type in('P','U','R') and owner = ? and table_name = ?"
        dst_sql = "select count(distinct constraint_name) from information_schema.table_constraints where constraint_type != 'CHECK' and table_catalog = '" + dst_database + "' and table_schema = '" + dst_schema + "' and table_name = '" + dst_table + "'"
        try:
            src_num = src_db.run(src_sql, (src_schema, src_table)).get_rows()[0][0]
        except Exception as _: 
            src_num = -1
            e1 = str(_)
        try:
            dst_num = dst_db.run(dst_sql).get_rows()[0][0]
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        log.info('表键数量是否一致：' + str(src_num == dst_num), src_schema + '.' + src_table, 'src=' + str(src_num), 'dst=' + str(dst_num), str(e1), str(e2))
        dst_db.close()
    
    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 1)
    except Exception as _:
        log.error('比较键数量时，Oracle连接失败', str(_))
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(compare_constraint_one, (src_db, table_map,))
    tp.wait()

    src_db.close()


def get_table_oracle_ddl():
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
    table_map_list = get_table_map_list(src_db)
    for table_map in table_map_list:
        src_schema = table_map[0]
        src_table = table_map[1]
        sqls = OracleTools.get_table_ddl(src_db, src_schema, src_table)
        for sql in sqls:
            log.out(sql + ';')
        log.out()

            
if __name__ == '__main__': 
    main()

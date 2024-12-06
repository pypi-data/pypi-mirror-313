# coding:utf-8
from tools_hjh.DBConn import DBConn
from tools_hjh.Tools import line_merge_align, locatdate, merge_spaces, analysis_hosts, locattime
from tools_hjh import Tools
import math
import re


def main():
    s = "TRUNC(ABC)"
    fun = 'TRUNC'
    rs = Tools.get_fun_content(s, fun)
    print(rs)
    

class OracleTools:
    """ 用于Oracle的工具类 """

    @staticmethod
    def get_table_metadata(ora_conn, username, table, partition=True):
        """得到表结构，索引、约束、分区等情况"""
        username = username.upper()
        table = table
        mess_map = {}
        mess_map['owner'] = username
        mess_map['name'] = table
        comments = None
        rs = ora_conn.run('select comments from dba_tab_comments where owner = ? and table_name = ?', (username, table)).get_rows()
        if len(rs) > 0:
            comments = rs[0][0]
        mess_map['comments'] = comments
        mess_map['columns'] = []
        mess_map['indexes'] = []
        mess_map['constraints'] = []
        mess_map['partition'] = None
        
        # 列 类型 非空约束 默认值
        mess_map['columns'] = []
        sql = '''
            select t.column_name, 
                case 
                    when data_type = 'VARCHAR2' or data_type = 'CHAR' or data_type = 'RAW' then 
                        data_type || '(' || data_length || ')'
                    when data_type = 'NVARCHAR2' or data_type = 'NCHAR' then 
                        data_type || '(' || char_length || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale > 0 then 
                        data_type || '(' || data_precision || ', ' || data_scale || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale = 0 then 
                        data_type || '(' || data_precision || ')'
                    when data_type = 'NUMBER' and data_precision = 0 and data_scale = 0 then 
                        data_type
                    else data_type 
                end column_type, t.nullable, t.data_default, t2.comments, t.virtual_column
            from dba_tab_cols t, dba_col_comments t2
            where t.owner = ?
            and t.table_name = ?
            and t.owner = t2.owner
            and t.table_name = t2.table_name
            and t.column_name = t2.column_name
            and t.column_name not like '%$%' 
            order by t.column_id
        '''
        cols_ = ora_conn.run(sql, (username, table)).get_rows()
        lenNum = 0
        for col_ in cols_:
            if lenNum < len(col_[0]):
                lenNum = len(col_[0])
        for col_ in cols_:
            colstr = col_[0]
            typestr = col_[1]
            
            if col_[2] == 'N':
                nullable = False
            else:
                nullable = True
                
            if col_[3] != 'None':
                data_default = col_[3]
            else:
                data_default = None
            
            if col_[4] != 'None':
                comments = col_[4]
            else:
                comments = None
            
            if col_[5] != 'None':
                virtual = col_[5]
            else:
                virtual = None
                
            mess_map['columns'].append({'name':colstr, 'type':typestr, 'nullable':nullable, 'default_value':data_default, 'comments':comments, 'virtual':virtual})
            
        # 索引 类型 列和列排序
        sql = '''
            select t.index_name
            , t.index_type
            , t2.column_name
            , t3.column_expression
            , t2.descend
            , t2.column_position
            , t.uniqueness
            , t.owner
            , t.partitioned
            , t4.locality
            from dba_indexes t, dba_ind_columns t2, dba_ind_expressions t3, dba_part_indexes t4
            where t.table_owner = ?
            and not exists(select 1 from dba_constraints t4 where t4.owner = t.owner and t4.table_name = t.table_name and t4.constraint_name = t.index_name)
            and t.table_name = ?
            and t.owner = t2.index_owner
            and t.table_owner = t2.table_owner
            and t.index_name = t2.index_name
            and t.table_name = t2.table_name
            and t2.index_owner = t3.index_owner(+)
            and t2.table_owner = t3.table_owner(+)
            and t2.index_name = t3.index_name(+)
            and t2.table_name = t3.table_name(+)
            and t2.column_position = t3.column_position(+)
            and t.owner = t4.owner(+)
            and t.index_name = t4.index_name(+)
            and t.table_name = t4.table_name(+)
            order by t.index_type, t2.column_position
        '''
        qrs = ora_conn.run(sql, (username, table))
        col = qrs.get_cols()
        rows = qrs.get_rows()
        
        if len(rows) > 0:
            mdb = DBConn('sqlite', db=':memory:')
            sql1 = 'drop table if exists t_idx'
            sql2 = 'create table t_idx ('
            sql3 = 'insert into t_idx values('
            for col_ in col:
                sql2 = sql2 + col_ + ' text, \n'
                sql3 = sql3 + '?' + ', '
            sql2 = sql2.strip().strip(',') + ')'
            sql3 = sql3.strip().strip(',') + ')'
            mdb.run(sql1)
            mdb.run(sql2)
            mdb.run(sql3, rows)
            
            # 降序索引也体现为函数索引，列名会用"col_name"，而字符串用'str'
            sql = '''
                select distinct index_name
                , group_concat(
                    replace(case when column_name like 'SYS_%$' then column_expression else column_name end, '"', '')
                    || ' ' || descend
                ) over(
                    partition by index_name 
                    order by column_position 
                    rows between unbounded preceding and unbounded following
                ) index_str
                , uniqueness, index_type, owner, partitioned, locality
                from t_idx order by 2,5,1
            '''
            rss = mdb.run(sql).get_rows()
            mdb.close()
            for rs in rss:
                name = rs[0]
                col = rs[1]
                idx_owner = rs[4]
                partitioned = rs[5]
                if partition:
                    locality = rs[6]
                else:
                    locality = None
                
                if rs[3] == 'BITMAP':
                    idx_type = rs[3]
                elif rs[2] == 'UNIQUE':
                    idx_type = rs[2]
                else:
                    idx_type = 'NORMAL'
                    
                mess_map['indexes'].append({'name':name, 'columns':col, 'type':idx_type, 'owner':idx_owner, 'partitioned':partitioned, 'locality':locality})
                
        # 约束 类型 列和列排序
        sql = '''
            select constraint_name, constraint_type
            , max(cols), r_owner, r_constraint_name
            from (
                select t.constraint_name, t.constraint_type
                , to_char(
                    wm_concat(t2.column_name)
                    over(partition by t.constraint_name order by t2.position)
                ) cols, t.r_owner, t.r_constraint_name
                from dba_constraints t, dba_cons_columns t2
                where t.owner = ?
                and t.table_name = ?
                and t.owner = t2.owner
                and t.constraint_name = t2.constraint_name
                and t.table_name = t2.table_name
                and t.constraint_type in('P','U','R')
            ) group by constraint_name, constraint_type, r_owner, r_constraint_name
            order by 2, 3
        '''
        rss = ora_conn.run(sql, (username, table)).get_rows()
        for rs in rss:
            name = rs[0]
            c_type = rs[1]
            cols = rs[2]
            r_table = None
            r_cols = None
            r_constraint_name = None
            if c_type == 'U':
                constraint_type = 'unique'
            elif c_type == 'P':
                constraint_type = 'primary_key'
            elif c_type == 'R':
                r_owner = rs[3]
                r_constraint_name = rs[4]
                sql = '''
                    select table_name, max(cols)
                    from (
                        select t.constraint_name, t.table_name
                        , to_char(
                            wm_concat(t2.column_name)
                            over(partition by t.constraint_name order by t2.position)
                        ) cols
                        from dba_constraints t, dba_cons_columns t2
                        where t.owner = ?
                        and t.constraint_name = ?
                        and t.owner = t2.owner
                        and t.constraint_name = t2.constraint_name
                        and t.table_name = t2.table_name
                        and t.constraint_type in('P','U','R')
                    ) group by table_name'''
                rs = ora_conn.run(sql, (r_owner, r_constraint_name)).get_rows()[0]
                constraint_type = 'foreign_key'
                r_table = r_owner + '.' + rs[0]
                r_cols = rs[1]
            else:
                constraint_type = None
            
            mess_map['constraints'].append({'name':name, 'columns':cols, 'type':constraint_type, 'r_table':r_table, 'r_constraint':r_constraint_name, 'r_cols':r_cols})
        
        # 表分区
        rss = ora_conn.run('select partitioning_type, subpartitioning_type, interval from dba_part_tables where owner = ? and table_name = ?', (username, table)).get_rows()
        if len(rss) > 0 and partition:
            rs = rss[0]
            if rs[0] == 'NONE':
                partitioning_type = None
            else:
                partitioning_type = rs[0]
            if rs[1] == 'NONE':
                subpartitioning_type = None
            else:
                subpartitioning_type = rs[1]
            if rs[2] == 'NONE':
                interval = None
            else:
                interval = rs[2]
            
            rss = ora_conn.run("select column_name from dba_part_key_columns where owner = ? and name = ? and object_type = 'TABLE' order by column_position", (username, table)).get_rows()
            partition_cols = ''
            for rs in rss:
                partition_cols = partition_cols + rs[0] + ', '
            partition_cols = partition_cols[:-2]
            
            rss = ora_conn.run('select partition_name,high_value from dba_tab_partitions where table_owner = ? and table_name = ? order by partition_position', (username, table)).get_rows()
            partitions = []
            for rs in rss:
                partitions.append({'name':rs[0], 'value':rs[1], 'subpartitions':[]})
                
            subpartition_cols = ''
            if subpartitioning_type != None:
                rss = ora_conn.run('select column_name from dba_subpart_key_columns where owner = ? and name = ? order by column_position', (username, table)).get_rows()
                for rs in rss:
                    subpartition_cols = subpartition_cols + rs[0] + ', '
                subpartition_cols = subpartition_cols[:-2]
                
                for partition in partitions:
                    partition_name = partition['name']
                    rss = ora_conn.run('select subpartition_name,high_value from dba_tab_subpartitions where table_owner = ? and table_name = ? and partition_name = ? order by subpartition_position', (username, table, partition_name)).get_rows()
                    for rs in rss:
                        partition['subpartitions'].append({'name':rs[0], 'value':rs[1]})
            
            mess_map['partition'] = {'partition_type':partitioning_type, 'partition_columns':partition_cols, 'subpartition_type':subpartitioning_type, 'subpartition_columns':subpartition_cols, 'interval':interval, 'partitions':partitions}
        
        return mess_map
    
    @staticmethod
    def desc(ora_conn, username, table, simple_mode=True, no_fk=False):
        """得到表结构，包括索引、约束和默认值情况"""
        metadata = OracleTools.get_table_metadata(ora_conn, username, table, partition=False)
        mess = 'table: ' + table + '\n'
        
        # 列 类型 非空约束 默认值
        cols_ = metadata['columns']
        for col_ in cols_:
            colstr = col_['name']
            typestr = col_['type']
            colstr = colstr + ' ' + typestr
            if not col_['nullable']:
                nullable = ' not null'
            else:
                nullable = ''
            if col_['default_value'] != None and col_['virtual'] == 'NO':
                data_default = ' default ' + col_['default_value'].replace('''/* GOLDENGATE_DDL_REPLICATION */''', '').strip().strip('\n')
            elif col_['default_value'] != None and col_['virtual'] == 'YES':
                data_default = ' as (' + col_['default_value'].strip().strip('\n') + ')'
            else:
                data_default = ''
            if col_['virtual'] == 'NO':
                mess = mess + 'column: ' + colstr + nullable + data_default + '\n'
            else:
                mess = mess + 'column: ' + col_['name'] + data_default + '\n'
            
        # 索引 类型 列和列排序
        rss = metadata['indexes']
        for rs in rss:
            name = rs['name']
            col = rs['columns']
            if rs['type'] == 'BITMAP':
                idx_type = ' bitmap'
            elif rs['type'] == 'UNIQUE':
                idx_type = ' unique'
            else:
                idx_type = ''
            if simple_mode:
                ss = 'index: (' + col.replace(' asc', '').replace(',', ', ') + ')' + idx_type
            else:
                ss = 'index: ' + name + ' (' + col.replace(' asc', '').replace(',', ', ') + ')' + idx_type
            mess = mess + ss + '\n'    
                
        # 约束 类型 列和列排序
        rss = metadata['constraints']
        for rs in rss:
            name = rs['name']
            c_type = rs['type']
            cols = rs['columns']
            if c_type == 'unique':
                constraint_type = ' unique'
            elif c_type == 'primary_key':
                constraint_type = ' pk'
            elif c_type == 'foreign_key' and not no_fk:
                r_table = rs['r_table']
                constraint_type = ' fk references ' + r_table + '(' + rs['r_cols'] + ')'
            elif c_type == 'foreign_key' and no_fk:
                continue
            else:
                constraint_type = ''
            if simple_mode:
                mess = mess + 'constraint: (' + cols + ')' + constraint_type + '\n'
            else:
                mess = mess + 'constraint: ' + name + ' (' + cols + ')' + constraint_type + '\n'
        
        return mess.strip('\n')

    @staticmethod
    def compare_table(src_conn, src_username, src_table_name, dst_conn, dst_username, dst_table_name, no_fk=True):
        """ 比较两个表，根据desc方法得到的字符串去比较 """
        src_username = src_username.upper()
        dst_username = dst_username.upper()

        src_desc = OracleTools.desc(src_conn, src_username, src_table_name, simple_mode=True, no_fk=no_fk)
        dst_desc = OracleTools.desc(dst_conn, dst_username, dst_table_name, simple_mode=True, no_fk=no_fk)
        mess = line_merge_align(str_1=src_username + '.' + src_table_name + '\n' + src_desc
                                       , str_2=dst_username + '.' + dst_table_name + '\n' + dst_desc
                                       , iscompare=True) + '\n\n'
        return mess, '\t*' not in mess

    @staticmethod
    def get_table_ddl(dba_conn, username, table, no_fk=False, partition=True):
        """得到某个表的全部ddl语句"""
        sql_list = []
        metadata = OracleTools.get_table_metadata(dba_conn, username, table, partition=partition)
        
        create_table_sql = 'create table ' + metadata['owner'] + '."' + metadata['name'] + '"'
        
        create_table_sql = create_table_sql + '\n(\n'
        for col in metadata['columns']:
            name = str(col['name'])
            type_ = str(col['type'])
            if col['default_value'] != None and col['virtual'] == 'NO':
                default_value = 'default ' + str(col['default_value'])
            elif col['default_value'] != None and col['virtual'] == 'YES':
                default_value = 'as (' + str(col['default_value']) + ')'
            else:
                default_value = ''
            if col['nullable']:
                nullable = ''
            else:
                nullable = 'not null'
            if col['virtual'] == 'NO':
                create_table_sql = create_table_sql + '[--gt--]"' + name + '"' + ' ' + type_ + ' ' + default_value + ' ' + nullable + ',\n'
            else:
                create_table_sql = create_table_sql + '[--gt--]"' + name + '"' + ' ' + default_value + ',\n'
        create_table_sql = Tools.merge_spaces(create_table_sql.rstrip().rstrip(',')).replace(' ,', ',').replace('[--gt--]', '  ')
        create_table_sql = create_table_sql + '\n)'
        
        part_str = ''
        if metadata['partition'] != None:
            partition = metadata['partition']
            part_str = part_str + ' partition by ' + partition['partition_type'] + ' (' + partition['partition_columns'] + ')\n'
            if partition['interval'] != None:
                part_str = part_str + 'interval(' + partition['interval'] + ')\n'
            if partition['subpartition_type'] != None:
                part_str = part_str + 'subpartition by ' + partition['subpartition_type'] + ' (' + partition['subpartition_columns'] + ')\n(\n'
            else:
                part_str = part_str + '(\n'
                
            for part in partition['partitions']:
                
                if partition['partition_type'] == 'RANGE':
                    part_str = part_str + '  partition ' + part['name'] + ' values less than (' + part['value'] + ')'
                    if len(part['subpartitions']) > 0:
                        part_str = part_str + '\n  (\n'
                        for subpart in part['subpartitions']:
                            if partition['subpartition_type'] == 'RANGE':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ' values less than (' + subpart['value'] + '),\n'
                            if partition['subpartition_type'] == 'LIST':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ' values (' + subpart['value'] + '),\n'
                            if partition['subpartition_type'] == 'HASH':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ',\n'
                        part_str = part_str.rstrip().rstrip(',')
                        part_str = part_str + '\n  ),\n'
                    else:
                        part_str = part_str + ',\n'
                                
                elif partition['partition_type'] == 'LIST':
                    part_str = part_str + '  partition ' + part['name'] + ' values (' + part['value'] + ')'
                    if len(part['subpartitions']) > 0:
                        part_str = part_str + '\n  (\n'
                        for subpart in part['subpartitions']:
                            if partition['subpartition_type'] == 'RANGE':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ' values less than (' + subpart['value'] + '),\n'
                            if partition['subpartition_type'] == 'LIST':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ' values (' + subpart['value'] + '),\n'
                            if partition['subpartition_type'] == 'HASH':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ',\n'
                        part_str = part_str.rstrip().rstrip(',')
                        part_str = part_str + '\n  ),\n'
                    else:
                        part_str = part_str + ',\n'
                                
                elif partition['partition_type'] == 'HASH':
                    part_str = part_str + '  partition ' + part['name']
                    if len(part['subpartitions']) > 0:
                        part_str = part_str + '\n  (\n'
                        for subpart in part['subpartitions']:
                            if partition['subpartition_type'] == 'RANGE':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ' values less than (' + subpart['value'] + '),\n'
                            if partition['subpartition_type'] == 'LIST':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ' values (' + subpart['value'] + '),\n'
                            if partition['subpartition_type'] == 'HASH':
                                part_str = part_str + '    subpartition ' + subpart['name'] + ',\n'
                        part_str = part_str.rstrip().rstrip(',')
                        part_str = part_str + '\n  ),\n'
                    else:
                        part_str = part_str + ',\n'
                        
            part_str = part_str.rstrip().rstrip(',')
            part_str = part_str + '\n)'
            
            create_table_sql = create_table_sql + part_str
        sql_list.append(create_table_sql)
        
        if metadata['comments'] != None:
            comments_str = ''
            comments_str = 'comment on table ' + username + '."' + table + '"' + " is '" + metadata['comments'] + "'"
            sql_list.append(comments_str)
            
        for col in metadata['columns']:
            comments_str = ''
            name = col['name']
            comments = col['comments']
            if comments != None:
                if '&' in comments:
                    pass
                    # comments = comments.split('&')[0] + "'||'" + '&' + "'||'" + comments.split('&')[1]
                comments_str = comments_str + 'comment on column ' + username + '."' + table + '"."' + name + '"' + " is '" + comments + "'"
                sql_list.append(comments_str)
        
        for idx in metadata['indexes']:
            index_str = ''
            name = idx['name']
            type_ = idx['type']
            if type_ == 'NORMAL':
                type_ = ''
            cols = idx['columns']
            cols_new = ''
            if cols is not None:
                for col in cols.split(','):
                    cols_new = cols_new + '"' + col.split(' ')[0] + '" ' + col.split(' ')[1] + ', '
                cols_new = cols_new[:-2]
            locality = idx['locality']
            if locality == None:
                locality = ''
            owner = idx['owner']
            index_str = index_str + 'create ' + type_ + ' index ' + owner + '.' + name + ' on ' + username + '."' + table + '" (' + cols_new.replace(' ASC', '') + ') ' + locality
            index_str = Tools.merge_spaces(index_str)
            sql_list.append(index_str)
        
        for constraint in metadata['constraints']:
            k_str = ''
            name = constraint['name']
            cols = constraint['columns']
            cols_new = ''
            if cols is not None:
                for col in cols.split(','):
                    cols_new = cols_new + '"' + col + '"' + ', '
                cols_new = cols_new[:-2]
            type_ = constraint['type']
            r_table = constraint['r_table']
            r_cols = constraint['r_cols']
            r_cols_new = ''
            if r_cols is not None:
                for col in r_cols.split(','):
                    r_cols_new = r_cols_new + '"' + col + '"' + ', '
                r_cols_new = r_cols_new[:-2]
            if type_ == 'primary_key':
                k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint ' + name + ' primary key (' + cols_new + ')'
            elif type_ == 'unique':
                k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint ' + name + ' unique (' + cols_new + ')'
            elif type_ == 'foreign_key' and not no_fk and r_cols is not None:
                k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint ' + name + ' foreign key (' + cols_new + ') references ' + r_table + ' (' + r_cols_new + ')'
            
            if k_str != '':
                sql_list.append(k_str)
            
        return sql_list
    
    @staticmethod
    def get_table_ddl_pg(dba_conn, username, table, forever_number_to_numeric=True):
        sql_list = []
        metadata = OracleTools.get_table_metadata(dba_conn, username, table)
        
        create_table_sql = 'create table ' + metadata['owner'].lower() + '."' + metadata['name'].lower() + '"'
        
        create_table_sql = create_table_sql + '\n(\n'
        for col in metadata['columns']:
            name = str(col['name']).lower().strip()
            type_ = str(col['type'])
            
            # 列类型
            if 'VARCHAR' in type_:
                type_ = type_.replace('VARCHAR2', 'VARCHAR')
                type_ = type_.replace('NVARCHAR', 'VARCHAR')
                type_ = type_.replace('NVARCHAR2', 'VARCHAR')
            elif 'CHAR' in type_:
                type_ = type_.replace('NCHAR', 'CHAR')
            elif 'NUMBER' in type_:
                if '(' in type_ and ',' in type_:
                    size_1 = int(type_.split('(')[1].split(')')[0].split(',')[0].strip())
                    size_2 = int(type_.split('(')[1].split(')')[0].split(',')[1].strip())
                    if size_2 > size_1:
                        type_ = 'NUMERIC'
                    else:
                        type_ = type_.replace('NUMBER', 'NUMERIC')
                elif not forever_number_to_numeric and '(' in type_ and ',' not in type_:
                    size_ = int(type_.split('(')[1].split(')')[0])
                    if size_ <= 4:
                        type_ = 'SMALLINT'
                    elif size_ > 4 and size_ <= 9: 
                        type_ = 'INT'
                    elif size_ > 9 and size_ <= 18: 
                        type_ = 'BIGINT'
                    else:
                        type_ = type_.replace('NUMBER', 'NUMERIC')
                else:
                    type_ = type_.replace('NUMBER', 'NUMERIC')
            elif 'RAW' in type_:
                type_ = 'BYTEA'
            elif type_.startswith('TIMESTAMP(') and 'WITH LOCAL TIME ZONE' in type_:
                type_ = 'TIMESTAMPTZ'
            elif type_.startswith('INTERVAL DAY('):
                second_ = type_.split(' TO ')[1].strip()
                type_ = 'INTERVAL DAY TO ' + second_
            else:
                type_ = type_.replace('BINARY_INTEGER', 'INTEGER')
                type_ = type_.replace('BINARY_FLOAT', 'FLOAT')
                type_ = type_.replace('DATE', 'TIMESTAMP(0)')
                type_ = type_.replace('NCLOB', 'TEXT')
                type_ = type_.replace('CLOB', 'TEXT')
                type_ = type_.replace('LONG', 'TEXT')
                type_ = type_.replace('BLOB', 'BYTEA')
                type_ = type_.replace('LONG RAW', 'BYTEA')
                
                # 暂定
                type_ = type_.replace('UROWID', 'VARCHAR(18)')
                type_ = type_.replace('ROWID', 'VARCHAR(18)')
                
            # 默认值
            if col['default_value'] != None:
                # to_number
                if 'to_number(' in col['default_value'].lower():
                    to_number_content = Tools.get_fun_content(col['default_value'], 'to_number'.upper())
                    a1 = col['default_value'].split('TO_NUMBER(' + to_number_content + ')')[0]
                    a2 = col['default_value'].split('TO_NUMBER(' + to_number_content + ')')[1]
                    col['default_value'] = a1 + to_number_content + '::numeric' + a2
                
                # ''值不可在非字符类型上
                if col['default_value'].strip() == "''" and ('VARCHAR' not in type_ or type_ != 'TEXT'):
                    col['default_value'] = 'NULL'
                    
                col['default_value'] = re.sub('sys_guid', 'uuid_generate_v4', col['default_value'], flags=re.IGNORECASE)
                col['default_value'] = re.sub('systimestamp', 'current_timestamp', col['default_value'], flags=re.IGNORECASE)
                col['default_value'] = re.sub('sysdate', 'statement_timestamp()', col['default_value'], flags=re.IGNORECASE)
                
                # 时间加减
                if str(col['default_value']).startswith('statement_timestamp()-'):
                    jz = str(col['default_value']).split('-')[1].strip()
                    col['default_value'] = "statement_timestamp() - interval '" + jz + " days'"
                elif str(col['default_value']).startswith('statement_timestamp()+'):
                    jz = str(col['default_value']).split('+')[1].strip()
                    col['default_value'] = "statement_timestamp() + interval '" + jz + " days'"
                    
                # 虚拟列
                if col['virtual'] == 'NO':
                    default_value = 'default ' + str(col['default_value']).strip()
                else:
                    for col2 in metadata['columns']:
                        col2_name = str(col2['name'])
                        if '"' + col2_name.upper() + '"' in str(col['default_value']):
                            col['default_value'] = col['default_value'].replace(col2_name.upper(), col2_name.lower())
                    default_value = 'generated always as (' + col['default_value'] + ') stored'
            else:
                default_value = ''

            # 非空
            if col['nullable']:
                nullable = ''
            else:
                nullable = 'not null'
                
            if col['virtual'] == 'NO':
                create_table_sql = create_table_sql + '[--gt--]"' + name + '"' + ' ' + type_ + ' ' + default_value + ' ' + nullable + ',\n'
            else:
                create_table_sql = create_table_sql + '[--gt--]"' + name + '"' + ' ' + type_ + ' ' + default_value + ',\n'
            
        create_table_sql = Tools.merge_spaces(create_table_sql.rstrip().rstrip(',')).replace(' ,', ',').replace('[--gt--]', '  ')
        create_table_sql = create_table_sql + '\n)'
        
        pk_add_cols_list = []
        
        partition_columns = ''
        partitions = []
        if metadata['partition'] != None:
            partition = metadata['partition']
            partitions = partition['partitions']
            partition_type = partition['partition_type']
            partition_columns = partition['partition_columns']
            for col in partition_columns.split(','):
                col = col.strip().lower()
                if col not in pk_add_cols_list:
                    pk_add_cols_list.append(col)
            subpartition_type = partition['subpartition_type']
            subpartition_columns = partition['subpartition_columns']
            create_table_sql = create_table_sql + ' partition by ' + partition_type + ' (' + partition_columns.lower() + ')'
        sql_list.append(create_table_sql)    
        
        # 分区
        q_val = None
        idx = 0
        for part in partitions:
            name = (table + '_part' + str(idx)).lower()
            value = part['value']
            if partition_type == 'RANGE':
                if value.startswith("TIMESTAMP' "):
                    value = value.replace("TIMESTAMP", '')
                if value.startswith("TO_DATE(' "):
                    value = value.split(',')[0].replace('TO_DATE(', '')
                if q_val is None:
                    q_val = 'MINVALUE'
                part_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + table.lower() + '" for values from (' + q_val + ') to (' + value + ')'
                q_val = value
            elif partition_type == 'HASH':
                part_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + table.lower() + '" for values with (modulus ' + str(len(partitions)) + ', remainder ' + str(idx) + ')'
            elif partition_type == 'LIST':
                if value.lower() == 'default':
                    part_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + table.lower() + '" default'
                else:
                    part_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + table.lower() + '" for values in (' + value + ')'
            if subpartition_type is not None:
                for col in subpartition_columns.split(','):
                    col = col.strip().lower()
                    if col not in pk_add_cols_list:
                        pk_add_cols_list.append(col)
                part_sql = part_sql + ' partition by ' + subpartition_type.lower() + ' (' + subpartition_columns.lower() + ')'
            idx = idx + 1
            sql_list.append(part_sql)
            
        # 子分区
        q_val = None
        idx = 0
        for part in partitions:
            sub_idx = 0
            par_name = (table + '_part' + str(idx)).lower()
            for subpar in part['subpartitions']:
                name = (par_name + '_subpart' + str(sub_idx)).lower()
                value = subpar['value']
                if subpartition_type == 'RANGE':
                    if value.startswith("TIMESTAMP' "):
                        value = value.replace("TIMESTAMP", '')
                    if value.startswith("TO_DATE(' "):
                        value = value.split(',')[0].replace('TO_DATE(', '')
                    if q_val is None:
                        q_val = 'MINVALUE'
                    subpar_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + par_name.lower() + '" for values from (' + q_val + ') to (' + value + ')'
                    q_val = value
                elif subpartition_type == 'HASH':
                    subpar_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + par_name.lower() + '" for values with (modulus ' + str(len(part['subpartitions'])) + ', remainder ' + str(sub_idx) + ')'
                elif subpartition_type == 'LIST':
                    if value.lower() == 'default':
                        subpar_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + par_name.lower() + '" default'
                    else:
                        subpar_sql = 'create table ' + username.lower() + '."' + name + '" partition of ' + username.lower() + '."' + par_name.lower() + '" for values in (' + value + ')'
                sub_idx = sub_idx + 1
                sql_list.append(subpar_sql)
            idx = idx + 1
            
        # 注释
        if metadata['comments'] != None:
            comments_str = ''
            comments_str = 'comment on table ' + username.lower() + '."' + table.lower() + '"' + " is '" + metadata['comments'].replace('\\u', '\\\\u').replace("'", "''") + "'"
            sql_list.append(comments_str)
            
        for col in metadata['columns']:
            comments_str = ''
            name = col['name'].lower().strip()
            comments = col['comments']
            if comments != None: 
                comments_str = comments_str + 'comment on column ' + username.lower() + '."' + table.lower() + '"."' + name.lower() + '"' + " is '" + comments.replace('\\u', '\\\\u').replace("'", "''") + "'"
                sql_list.append(comments_str)
                
        # 索引
        for idx in metadata['indexes']:
            index_str = ''
            name = idx['name']
            type_ = idx['type']
            my_cols_ = idx['columns']
            
            my_cols = ''
            for col in my_cols_.split(','):
                is_asc_or_desc = ''
                if col.endswith(' ASC'):
                    is_asc_or_desc = 'ASC'
                elif col.endswith(' DESC'):
                    is_asc_or_desc = 'DESC'
                col = col.replace(' ASC', '').replace(' DESC', '').strip()
                
                # 索引字段是数字
                if col.isdigit():
                    col = '(' + col + ') ' + is_asc_or_desc
                # 索引字段是字符串（列写错成字符串）
                if col.startswith("'") and col.endswith("'"):
                    col = '"' + col.strip("'").lower() + '" ' + is_asc_or_desc
                # 索引字段是 case when then
                if 'case' in col.lower() and 'when' in col.lower() and 'then' in col.lower():
                    col = '(' + col + ') ' + is_asc_or_desc
                # 索引字段是||连接
                if '||' in col:
                    col = '(' + col + ') ' + is_asc_or_desc
                # 索引字段是 trunc() 函数
                if 'trunc(' in col:
                    fun_content = Tools.get_fun_content(col, 'trunc')
                    col = col.split('trunc')[0] + "date_trunc('day', " + fun_content + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                if 'TRUNC(' in col:
                    fun_content = Tools.get_fun_content(col, 'TRUNC')
                    col = col.split('TRUNC')[0] + "date_trunc('day', " + fun_content + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                # 索引字段是 to_number() 函数
                if 'to_number(' in col:
                    fun_content = Tools.get_fun_content(col, 'to_number')
                    col = col.split('to_number')[0] + '(' + fun_content + '::numeric ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                if 'TO_NUMBER(' in col:
                    fun_content = Tools.get_fun_content(col, 'TO_NUMBER')
                    col = col.split('TO_NUMBER')[0] + '(' + fun_content + '::numeric ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                # 索引字段是 to_char() 函数，且不是日期格式化
                if 'to_char(' in col and ',' not in col:
                    fun_content = Tools.get_fun_content(col, 'to_char')
                    col = col.split('to_char')[0] + '(' + fun_content + '::varchar ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                if 'TO_CHAR(' in col and ',' not in col:
                    fun_content = Tools.get_fun_content(col, 'TO_CHAR')
                    col = col.split('TO_CHAR')[0] + '(' + fun_content + '::varchar ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                # 索引字段是 sys_op_c2c() 函数
                if 'sys_op_c2c(' in col:
                    fun_content = Tools.get_fun_content(col, 'sys_op_c2c')
                    col = col.split('sys_op_c2c')[0] + fun_content + col.split(fun_content + ')')[1] + ' ' + is_asc_or_desc
                if 'SYS_OP_C2C(' in col:
                    fun_content = Tools.get_fun_content(col, 'SYS_OP_C2C')
                    col = col.split('SYS_OP_C2C')[0] + fun_content + col.split(fun_content + ')')[1] + ' ' + is_asc_or_desc
                
                my_cols = my_cols + col + ', '
            my_cols = my_cols[:-2]
            
            if type_ == 'UNIQUE' and metadata['partition'] != None:
                cols_partition_columns = ''
                my_cols_list = []
                for col in my_cols.split(','):
                    if not (col.lower().startswith('(case ') and 'when' in col.lower() and 'then' in col.lower()):
                        col = col.strip().lower()
                        if ' ' in col:
                            col = col.split(' ')[0]
                        if col not in my_cols_list:
                            my_cols_list.append(col)
                    else:
                        col = col.strip().lower()
                        if ') ' in col:
                            col = col.split(') ')[0] + ')'
                        if col not in my_cols_list:
                            my_cols_list.append(col)
                pk_cols_list = my_cols_list.copy()
                for col in pk_add_cols_list:
                    if col not in pk_cols_list:
                        pk_cols_list.append(col)
                for col in pk_cols_list:
                    cols_partition_columns = cols_partition_columns + col + ', '
                cols_partition_columns = cols_partition_columns[:-2]
                
            if type_ == 'NORMAL':
                type_ = ''
                
            if type_ == 'UNIQUE' and metadata['partition'] != None:
                cols = cols_partition_columns
            else:
                cols = my_cols.replace(',', ', ')
            
            # if type_ == 'BITMAP':
                # index_str = index_str + 'create index "' + name.lower() + '" on ' + username.lower() + '."' + table.lower() + '" using gin(' + cols.lower() + ') '
            index_str = index_str + 'create ' + type_ + ' index "' + name.lower() + '" on ' + username.lower() + '."' + table.lower() + '" (' + cols.lower() + ') '
            
            index_str = Tools.merge_spaces(index_str)
            index_str = index_str.replace(' asc', '')
            sql_list.append(index_str)

        # 约束（主键、唯一、外键）
        for constraint in metadata['constraints']:
            k_str = ''
            name = constraint['name']
            my_cols_ = constraint['columns']
            
            my_cols = ''
            for col in my_cols_.split(','):
                if col.replace(' ASC', '').replace(' DESC', '').strip().isdigit() and len(col.split(' ')) == 2:
                    col = '(' + col.split(' ')[0] + ') ' + col.split(' ')[1]
                elif 'case' in col.lower() and 'when' in col.lower() and 'then' in col.lower() and 'else' in col.lower():
                    col = '(' + col + ') '
                my_cols = my_cols + col + ', '
            my_cols = my_cols[:-2]
            
            type_ = constraint['type']
            r_table = constraint['r_table']
            r_cols = constraint['r_cols']
            
            if type_ == 'primary_key' or type_ == 'unique':
                cols_partition_columns = ''
                my_cols_list = []
                for col in my_cols.split(','):
                    col = col.strip().lower()
                    if ' ' in col:
                        col = col.split(' ')[0]
                    if col not in my_cols_list:
                        my_cols_list.append(col)
                pk_cols_list = my_cols_list.copy()
                for col in pk_add_cols_list:
                    if col not in pk_cols_list:
                        pk_cols_list.append(col)
                for col in pk_cols_list:
                    cols_partition_columns = cols_partition_columns + col + ', '
                cols_partition_columns = cols_partition_columns[:-2]
            
            if type_ == 'primary_key' and metadata['partition'] != None:
                k_str = k_str + 'alter table ' + username.lower() + '."' + table.lower() + '" add constraint ' + name + ' primary key (' + cols_partition_columns.lower() + ')'
            if type_ == 'primary_key' and metadata['partition'] == None:
                k_str = k_str + 'alter table ' + username.lower() + '."' + table.lower() + '" add constraint ' + name + ' primary key (' + my_cols.lower() + ')'
            elif type_ == 'unique' and metadata['partition'] != None:
                k_str = k_str + 'alter table ' + username.lower() + '."' + table.lower() + '" add constraint ' + name + ' unique (' + cols_partition_columns.lower() + ')'
            elif type_ == 'unique' and metadata['partition'] == None:
                k_str = k_str + 'alter table ' + username.lower() + '."' + table.lower() + '" add constraint ' + name + ' unique (' + my_cols.lower() + ')'
            elif type_ == 'foreign_key':
                k_str = k_str + 'alter table ' + username.lower() + '."' + table.lower() + '" add constraint ' + name + ' foreign key (' + my_cols.lower() + ') references ' + r_table.lower() + ' (' + r_cols.lower() + ')'
            sql_list.append(k_str)
        return sql_list
    
    @staticmethod
    def get_table_size(dba_conn, username, table):
        """得到一个表相关对象的容量分布情况"""
        sql = '''
            select t.owner owner
                  ,t.segment_name table_name
                  ,t.segment_name obj_name
                  ,t.segment_type "TYPE"
                   ,sum(t.bytes) / 1024 / 1024 size_m
            from dba_segments t
            where 1 = 1
            and t.owner = ?
            and t.segment_name = ?
            group by t.owner, t.segment_name, '', t.segment_type
            union all
            select t.owner
                  ,t.table_name
                  ,t.column_name
                  ,t2.segment_type
                  ,sum(t2.bytes) / 1024 / 1024
            from dba_lobs t, dba_segments t2
            where t.owner = t2.owner
            and t.segment_name = t2.segment_name
            and t.owner = ?
            and t.table_name = ?
            group by t.owner, t.table_name, t.column_name, t2.segment_type
            union all
            select t.owner
                  ,t.table_name
                  ,t.index_name
                  ,t2.segment_type
                  ,sum(t2.bytes) / 1024 / 1024
            from dba_indexes t, dba_segments t2
            where t.owner = t2.owner
            and t.index_name = t2.segment_name
            and t.owner = ?
            and t.table_name = ?
            group by t.owner, t.table_name, t.index_name, t2.segment_type
        '''
        rows = dba_conn.run(sql, (username, table, username, table, username, table)).get_rows()
        return rows
    
    @staticmethod
    def get_sids_by_host(host_conn):
        """ 根据给入的tools_hjh.SSHConn对象获取这台主机运行的全部SID实例名称 """
        sids = []
        pros = host_conn.exec_command("ps -ef | grep ora_smon | grep -v grep | awk '{print $8}'").split('\n')
        for pro in pros:
            sids.append(pro.replace('ora_smon_', ''))
        return sids
    
    @staticmethod
    def _get_data_file_size(dba_conn):
        """ 得到数据文件大小 """
        sql = '''
            select (select utl_inaddr.get_host_address from dual) ip
            , (select global_name from global_name) service_name
            , t2.tablespace_name 
            , t2.file_name
            , t2.file_id
            , t2.bytes / 1024 / 1024 all_size_m
            , max(t.block_id) * 8 / 1024 occupy_size_m
            , sum(t.bytes) / 1024 / 1024 use_size_m
            from dba_extents t, dba_data_files t2
            where t.file_id = t2.file_id
            group by t2.tablespace_name, t2.file_name, t2.file_id, t2.bytes
        '''
        return dba_conn.run(sql)
    
    @staticmethod   
    def expdp_estimate(host_conn, sid, users='', estimate='statistics'):
        """ 评估导出的dmp文件大小, users不填会使用full=y, estimate=statistics|blocks """
        date_str = locatdate()
        ip = host_conn.host
        if users == '':
            sh = '''
                source ~/.bash_profile
                export ORACLE_SID=''' + sid + '''
                expdp \\'/ as sysdba\\' \\
                compression=all \\
                cluster=n \\
                parallel=8 \\
                full=y \\
                estimate_only=y \\
                estimate=''' + estimate + '''
            '''
        else:
            sh = '''
                source ~/.bash_profile
                export ORACLE_SID=''' + sid + '''
                expdp \\'/ as sysdba\\' \\
                compression=all \\
                cluster=n \\
                parallel=8 \\
                schemas=''' + users + ''' \\
                estimate_only=y \\
                estimate=''' + estimate + '''
            '''  
        mess = host_conn.exec_script(sh)
        size = None
        rs_list = []
        if 'successfully completed' in mess:
            size = mess.split('method: ')[-1].split('\n')[0]
            lines = mess.replace('\n', '').split('.  estimated')
            for line in lines:
                if 'Total' in line or 'expdp' in line:
                    pass
                else:
                    line = merge_spaces(line.replace('"', '')).strip()
                    user_name = line.split(' ')[0].split('.')[0]
                    obj_name = line.split(' ')[0].split('.')[1]
                    obj_size = line.split(' ')[1]
                    dw = line.split(' ')[2]
                    if ':' in obj_name:
                        fq_name = obj_name.split(':')[1]
                        tab_name = obj_name.split(':')[0]
                    else:
                        tab_name = obj_name
                        fq_name = tab_name
                    if dw == 'GB':
                        obj_size = float(obj_size) * 1024
                    elif dw == 'KB':
                        obj_size = float(obj_size) / 1024
                    rs_list.append((date_str, ip, sid, user_name, tab_name, fq_name, obj_size))
        elif 'elapsed 0' in mess:
            size = mess.split('TATISTICS : ')[-1].split('\n')[0]
            lines = mess.split('\n')
            
            for line in lines:
                if '.   "' in line:
                    line = merge_spaces(line.replace('"', '').replace('\n', '')).strip()
                    user_name = line.split(' ')[1].split('.')[0]
                    obj_name = line.split(' ')[1].split('.')[1]
                    obj_size = line.split(' ')[2]
                    dw = line.split(' ')[3]
                    if ':' in obj_name:
                        fq_name = obj_name.split(':')[1]
                        tab_name = obj_name.split(':')[0]
                    else:
                        tab_name = obj_name
                        fq_name = tab_name
                    if dw == 'GB':
                        obj_size = float(obj_size) * 1024
                    elif dw == 'KB':
                        obj_size = float(obj_size) / 1024
                    rs_list.append((date_str, ip, sid, user_name, tab_name, fq_name, obj_size))
                    
        size = size.replace('\n', '').strip()
        return size, rs_list, mess
    
    @staticmethod
    def insert_not_exists_by_dblink(ora_conn, src_link, username, table):
        """通过dblink补充某个表中唯一键缺少的记录"""
        mess = OracleTools.desc(ora_conn, username, table)
        cols_list = None
        cols_num = math.inf
        for line in mess.split('\n'):
            if line.startswith('index') and line.endswith('unique'):
                cols_ = line.split('(')[1].split(')')[0]
                cols_num_ = len(cols_.split(', '))
                if cols_num_ < cols_num:
                    cols_num = cols_num_
                    cols_list = cols_.split(', ')
        if cols_list == None:
            cols_list = []
            for line in mess.split('\n'):
                if line.startswith('column'):
                    col = line.split(' ')[1]
                    cols_list.append(col)
        left_sql = ''
        right_sql = ''
        for col in cols_list:
            left_sql = left_sql + 't.' + col + '||'
            right_sql = right_sql + 't2.' + col + '||'
        where_sql = left_sql[0:-2] + ' = ' + right_sql[0:-2]
        
        sql = 'insert into {username}.{table} \nselect * from {username}.{table}@{src_link} t where not exists(select 1 from {username}.{table} t2 where {where_sql})'
        sql = sql.replace('{username}', username).replace('{table}', table).replace('{src_link}', src_link).replace('{where_sql}', where_sql)
        return sql
    
    @staticmethod
    def analysis_tns(host_conn):
        """ 解析Oracle tnsnames.ora文件 """
        """ tns_name, ip, port, sid, service_name """
        host_map = analysis_hosts(host_conn)
        cmd = '''source ~/.bash_profile;cat $ORACLE_HOME/network/admin/tnsnames.ora'''
        tns_str = host_conn.exec_command(cmd)
        tns_str2 = ''
        tns_list = []
        tnss = {}
        for line in tns_str.split('\n'):
            if not line.startswith('#'):
                tns_str2 = tns_str2 + line + '\n'
        tns_str2 = tns_str2.replace('\n', ' ')
        tns_str2 = merge_spaces(tns_str2)
        for s in tns_str2.split(') ) )'):
            s = s.replace(' ', '')
            if len(s) > 0:
                tns_list.append(s + ')))')
        for tns_s in tns_list:
            sid = ''
            service_name = ''
            tns_name = tns_s.split('=')[0]
            tns_s = tns_s.replace(tns_name + '=', '')  # 避免tns_name里面含有关键字
            if 'SID=' in tns_s:
                sid = tns_s.split('SID=')[1].split(')')[0]
            elif 'SERVICE_NAME=' in tns_s:
                service_name = tns_s.split('SERVICE_NAME=')[1].split(')')[0]
            tns_host = tns_s.split('HOST=')
            for idx in range(1, len(tns_host)):
                host = tns_host[idx].split(')')[0]
                try:
                    host = host_map[host]
                except:
                    pass
                port = tns_s.split('PORT=')[idx].split(')')[0]
                tnss[tns_name.lower()] = (host, port, service_name.lower(), sid.lower())
        return tnss

    @staticmethod     
    def analysis_ogg_status(host_conn):
        """ 进入主机全部找到的ggsci，执行info all 返回结果 """
        
        class QueryResults2:

            def __init__(self, cols=(), rows=[]):
                self.cols = cols
                self.rows = rows
        
            def get_cols(self):
                return self.cols
        
            def get_rows(self):
                return self.rows
            
            def set_cols(self, cols):
                self.cols = cols
                
            def set_rows(self, rows):
                self.rows = rows

        query_time = locattime()
        host = host_conn.host
        username = host_conn.username
        
        # 进程状态 
        # 查询时间 ogg所在主机HOST ggsci所在路径 进程类型 进程状态 进程名称 lag_at_chkpt time_since_chkpt
        ogg_status = QueryResults2()
        ogg_status.get_rows().clear()
        ogg_status.set_cols(('query_time', 'host', 'ggsci_path', 'type', 'status', 'name', 'lag_at_chkpt', 'time_since_chkpt'))
        
        # 解析进程状态 
        cmd = 'find / -name *ggsci'
        paths = host_conn.exec_command(cmd)
        for path in paths.split('\n'):
            if username == 'oracle':
                cmd = 'source ~/.bash_profile;echo "info all" | ' + path
            else:
                cmd = '''su - oracle -c 'source ~/.bash_profile;echo "info all" | ''' + path + '\''
            mess = host_conn.exec_command(cmd)
            for line in mess.split('\n'):
                if line.startswith('MANAGER'):
                    lines = merge_spaces(line).split(' ')
                    ogg_status.get_rows().append((query_time, host, path, lines[0].lower(), lines[1].lower()))
                elif line.startswith('EXTRACT') or line.startswith('REPLICAT'):
                    lines = merge_spaces(line).split(' ')
                    ogg_status.get_rows().append((query_time, host, path, lines[0].lower(), lines[1].lower(), lines[2].lower(), lines[3], lines[4]))
        
        return ogg_status
    
    @staticmethod     
    def analysis_ogg_info(host_conn):
        """ 对主机所有找到的ggsci，搜寻全部ogg进程的基本信息 """
        host = host_conn.host
        tns_list = OracleTools.analysis_tns(host_conn)
        
        # 进程状态 
        # 查询时间 ogg所在主机HOST ggsci所在路径 进程类型 进程状态 进程名称 lag_at_chkpt time_since_chkpt
        ogg_status = OracleTools.analysis_ogg_status(host_conn)
        
        # 进程信息 
        ogg_info = []
        
        # ORACLE_SID
        default_sid = host_conn.exec_command('source ~/.bash_profile;echo $ORACLE_SID')
        
        # 解析进程信息
        for ogg in ogg_status.get_rows():
            if ogg[3] != 'manager':
                ggsci_path = ogg[2]
                pro_name = ogg[5]
                cmd1 = 'source ~/.bash_profile;echo "view param ' + pro_name + '" | ' + ggsci_path
                cmd2 = 'source ~/.bash_profile;echo "info ' + pro_name + ' showch" | ' + ggsci_path
                param = host_conn.exec_command(cmd1)
                showch = host_conn.exec_command(cmd2)
                
                ogg_type = ''
                
                for line in param.split('\n'):
                    line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                    if line_.startswith('extract '):
                        ogg_type = 'ext_or_dmp'
                    elif line_.startswith('replicat '):
                        ogg_type = 'rep_or_rep2kafka'
                    elif line_.startswith('rmthost ') and ogg_type == 'ext_or_dmp':
                        ogg_type = 'dmp'
                        break
                    elif line_.startswith('exttrail ') and ogg_type == 'ext_or_dmp':
                        ogg_type = 'ext'
                        break
                    elif line_.startswith('userid ') and ogg_type == 'rep_or_rep2kafka':
                        ogg_type = 'rep'
                        break
                    elif line_.startswith('targetdb ') and ogg_type == 'rep_or_rep2kafka':
                        ogg_type = 'rep2kafka'
                        break
                
                if ogg_type == 'ext':
                    ext_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'ora_host':'', 'ora_port':'', 'ora_service_name':'', 'ora_sid':'', 'read_tables':[], 'write_file':''}
                    ext_info['host'] = host
                    ext_info['ggsci_path'] = ggsci_path
                    ext_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('extract '):
                            ext_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('userid '):
                            if '@' in line_:
                                tns_name = (line_.split(',')[0].split(' ')[1].split('@')[1]).lower()
                                try:
                                    ext_info['ora_host'] = tns_list[tns_name][0]
                                    ext_info['ora_port'] = tns_list[tns_name][1]
                                    ext_info['ora_service_name'] = tns_list[tns_name][2]
                                    ext_info['ora_sid'] = tns_list[tns_name][3]
                                except:
                                    ext_info['ora_host'] = ''
                                    ext_info['ora_port'] = ''
                                    ext_info['ora_service_name'] = ''
                                    ext_info['ora_sid'] = ''
                            else:
                                ext_info['ora_host'] = host
                                ext_info['ora_port'] = '1521'
                                ext_info['ora_service_name'] = ''
                                ext_info['ora_sid'] = default_sid
                        elif line_.startswith('table '):
                            ext_info['read_tables'].append(line_.split(' ')[1].replace(';', '').replace('"', '').strip().lower())
                    # write_file
                    try:
                        write_ = showch.split('Write Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if write_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            write_ = write_.replace('./', base_path)
                    except:
                        write_ = ''
                    ext_info['write_file'] = write_
                    ogg_info.append(ext_info)
                    # print(ext_info)
                    
                elif ogg_type == 'dmp':
                    dmp_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'ora_host':'', 'ora_port':'', 'ora_service_name':'', 'ora_sid':'', 'read_tables':[], 'read_file':'', 'write_host':'', 'write_port':'', 'write_file':''}
                    dmp_info['host'] = host
                    dmp_info['ggsci_path'] = ggsci_path
                    dmp_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('extract '):
                            dmp_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('userid '):
                            if '@' in line_:
                                tns_name = (line_.split(',')[0].split(' ')[1].split('@')[1]).lower()
                                try:
                                    dmp_info['ora_host'] = tns_list[tns_name][0]
                                    dmp_info['ora_port'] = tns_list[tns_name][1]
                                    dmp_info['ora_service_name'] = tns_list[tns_name][2]
                                    dmp_info['ora_sid'] = tns_list[tns_name][3]
                                except:
                                    dmp_info['ora_host'] = ''
                                    dmp_info['ora_port'] = ''
                                    dmp_info['ora_service_name'] = ''
                                    dmp_info['ora_sid'] = ''
                            else:
                                dmp_info['ora_host'] = host
                                dmp_info['ora_port'] = '1521'
                                dmp_info['ora_service_name'] = ''
                                dmp_info['ora_sid'] = default_sid
                        elif line_.startswith('table '):
                            dmp_info['read_tables'].append(line_.split(' ')[1].replace(';', '').replace('"', '').strip().lower())
                        elif line_.startswith('rmthost '):
                            try:
                                dmp_info['write_host'] = line_.split(',')[0].split(' ')[1]
                                dmp_info['write_port'] = line_.split(',')[1].split(' ')[1]
                            except:
                                dmp_info['write_host'] = line_.split(' ')[1]
                                dmp_info['write_port'] = line_.split(' ')[3]
                    # read_file
                    try:
                        read_ = showch.split('Read Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if read_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            read_ = read_.replace('./', base_path)
                    except:
                        read_ = ''
                    dmp_info['read_file'] = read_
                    # write_file
                    try:
                        write_ = showch.split('Write Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if write_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            write_ = write_.replace('./', base_path)
                    except:
                        write_ = ''
                    dmp_info['write_file'] = write_
                    ogg_info.append(dmp_info)
                    # print(dmp_info)
                    
                elif ogg_type == 'rep':
                    rep_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'ora_host':'', 'ora_port':'', 'ora_service_name':'', 'ora_sid':'', 'read_file':'', 'write_table_maps':[], 'exclude_table_maps':[]}
                    rep_info['host'] = host
                    rep_info['ggsci_path'] = ggsci_path
                    rep_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('replicat '):
                            rep_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('userid '):
                            if '@' in line_:
                                tns_name = (line_.split(',')[0].split(' ')[1].split('@')[1]).lower()
                                try:
                                    rep_info['ora_host'] = tns_list[tns_name][0]
                                    rep_info['ora_port'] = tns_list[tns_name][1]
                                    rep_info['ora_service_name'] = tns_list[tns_name][2]
                                    rep_info['ora_sid'] = tns_list[tns_name][3]
                                except:
                                    rep_info['ora_host'] = ''
                                    rep_info['ora_port'] = ''
                                    rep_info['ora_service_name'] = ''
                                    rep_info['ora_sid'] = ''
                            else:
                                rep_info['ora_host'] = host
                                rep_info['ora_port'] = '1521'
                                rep_info['ora_service_name'] = ''
                                rep_info['ora_sid'] = default_sid
                        elif line_.startswith('map ') and 'target ' in line_:
                            line_ = line_.replace(',', ' ')
                            line_ = merge_spaces(line_)
                            m = line_.split(' ')[1].replace('"', '')
                            t = line_.split(' ')[3].replace(';', '').replace('"', '').strip().lower()
                            rep_info['write_table_maps'].append((m, t))
                        elif line_.startswith('mapexclude '):
                            t = line_.split(' ')[1].replace(';', '').strip().lower()
                            rep_info['exclude_table_maps'].append(t)
                    # read_file
                    try:
                        read_ = showch.split('Read Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if read_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            read_ = read_.replace('./', base_path)
                    except:
                        read_ = ''
                    rep_info['read_file'] = read_
                    ogg_info.append(rep_info)
                    # print(rep_info)
                            
                elif ogg_type == 'rep2kafka':
                    rep2kafka_info = {'host':'', 'ggsci_path':'', 'ogg_type':'', 'ogg_name':'', 'read_file':'', 'write_table_maps':[], 'exclude_table_maps':[]}
                    rep2kafka_info['host'] = host
                    rep2kafka_info['ggsci_path'] = ggsci_path
                    rep2kafka_info['ogg_type'] = ogg_type
                    for line in param.split('\n'):
                        line_ = merge_spaces(line).strip().lower().replace(', ', ',').replace('; ', ';')
                        if line_.startswith('replicat '):
                            rep2kafka_info['ogg_name'] = line_.split(' ')[1]
                        elif line_.startswith('map ') and 'target ' in line_:
                            line_ = line_.replace(',', ' ')
                            line_ = merge_spaces(line_)
                            m = line_.split(' ')[1].replace('"', '')
                            t = line_.split(' ')[3].replace(';', '').replace('"', '').strip().lower()
                            rep2kafka_info['write_table_maps'].append((m, t))
                        elif line_.startswith('mapexclude '):
                            t = line_.split(' ')[1].replace(';', '').strip().lower()
                            rep2kafka_info['exclude_table_maps'].append(t)
                    # read_file
                    try:
                        read_ = showch.split('Read Checkpoint #1')[1].split('Extract Trail: ')[1].split('\n')[0]
                        if read_.startswith('./'):
                            base_path = ggsci_path.replace('ggsci', '')
                            read_ = read_.replace('./', base_path)
                    except:
                        read_ = ''
                    rep2kafka_info['read_file'] = read_
                    ogg_info.append(rep2kafka_info)
                    # print(rep2kafka_info)
                    
        return ogg_info


if __name__ == '__main__':
    main()
    
'''
alter system set sga_max_size=18g scope=spfile;
alter system set sga_target=18g scope=spfile;
alter system set pga_aggregate_target=6g scope=both;
alter system set "_partition_large_extents"=false scope=both sid='*';
alter system set "_index_partition_large_extents"=false scope=both sid='*';
alter system set audit_trail=false scope=spfile;
alter profile default limit password_grace_time 9999;
alter profile default limit password_life_time unlimited;
alter profile default limit password_verify_function null;
alter profile default limit password_reuse_max unlimited;
alter profile default limit password_reuse_time unlimited;
alter system set processes=6000 scope=spfile;
alter system set sessions=6605 scope=spfile;
alter system set db_recovery_file_dest_size='9999999G';
alter system set enable_goldengate_replication=true scope=both;
alter system set recyclebin=off scope=spfile;
alter system set audit_trail=db scope=spfile;
'''

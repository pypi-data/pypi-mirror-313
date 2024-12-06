# coding:utf-8

from tools_hjh import Tools

db = []
db.append(('risk_rule', '11.111.26.138', 'extjczx', 'dmpjczx', 'repjczxa-e', 'extdcuz', 'dmpdcuzj', 'repdcuzc', 'dpdb'))
db.append(('risk_flow', '11.111.26.138', 'extjcrb', 'dmpjcrb', 'repjcrba-e', 'extdcuz', 'dmpdcuzj', 'repdcuzc', 'dpdb'))
db.append(('risk_busdata', '11.111.26.138', 'extjcrb', 'dmpjcrb', 'repjcrba-e', 'extdcuz', 'dmpdcuzj', 'repdcuzc', 'dpdb'))
db.append(('afs', '11.111.28.111', 'extlwdsp', 'dmplwdsp', 'replwdsp', 'extdcuy', 'dmpdcuy', 'repdcuyb', 'bdpdb'))
db.append(('aml', '11.111.28.111', 'extlwdsp', 'dmplwdsp', 'replwdsp', 'extdcuy', 'dmpdcuy', 'repdcuyb', 'bdpdb'))
db.append(('warn', '11.111.28.111', 'extlwdsp', 'dmplwdsp', 'replwdsp', 'extdcuy', 'dmpdcuy', 'repdcuyb', 'bdpdb'))
db.append(('pmml_user', '11.111.28.111', 'extlwdsp', 'dmplwdsp', 'replwdsp', 'extdcuy', 'dmpdcuy', 'repdcuyb', 'bdpdb'))
db.append(('cis', '11.111.27.126', 'ext-cis', 'dmp-cis', 'repcis', 'extdcis', 'dmpdcis', 'repdcis4', 'edzxdb'))
db.append(('psbcap', '11.111.26.5', 'ext-psb', 'dmppsbc', 'repsp6a-e', 'extdcsp', 'dmpdcsp', 'repdcspz', 'psbc'))
db.append(('pls', '11.111.25.9', 'ext-pls', 'dmp-pls', 'reppls', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'zyxfjr'))
db.append(('juphoon', '11.111.25.9', 'ext-pls', 'dmp-pls', 'reppls', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'zyxfjr'))
db.append(('upmp_data', '11.111.27.126', 'ext-ulcp', 'dmp-ulcp', 'repulcp', 'extdcuz', 'dmpdcuz', 'repdcuze', 'edzxdb'))
db.append(('collectsm', '11.111.28.227', 'ext-cs', 'dmp-cs', 'repcs1-8', 'extdcuz', 'dmpdcuz', 'repdcuzd', 'csmdb'))
db.append(('smartc', '11.111.6.135', 'extxygw', 'dmpxygwb', 'repxygw', 'extdcuz', 'dmpdcuz', 'repdcuzd', 'smartc'))
db.append(('robot', '22.223.7.196', 'extjqr', 'dmpjqr', 'repjqr', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'jqrdb'))
db.append(('itmusr', '22.223.7.196', 'extjqr', 'dmpjqr', 'repjqr', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'jqrdb'))
db.append(('ai_robot', '22.223.7.196', 'extjqr', 'dmpjqr', 'repjqr', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'jqrdb'))
db.append(('acct_facade', '11.111.28.107', 'ext-hs', 'dmp-hs', 'rephes1-16', 'extdcuz', 'dmpdcuzh', 'repdcuzf', 'hszxdb'))
db.append(('basc_info', '11.111.28.107', 'ext-hs', 'dmp-hs', 'rephes1-16', 'extdcuz', 'dmpdcuzh', 'repdcuzf', 'hszxdb'))
db.append(('common_service', '11.111.28.107', 'ext-hs', 'dmp-hs', 'rephesu', 'extdcuy', 'dmpdcuy', 'repdcuyc', 'hszxdb'))
# db.append(('ycuser', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('ycuser', '22.223.7.196', 'extyy', 'dmpyy', 'repcall', 'extdcub', 'dmpdcub', 'repdcubd', 'yydb'))
db.append(('dmp', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx1-4', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('wcp', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('uasc_acct_own', '11.111.29.194', 'extzwt', 'dmpzwt', 'repzwta-p', 'extdczw', 'dmpdczw', 'repdczwc', 'zwzxdb'))
db.append(('bcp_fe', '11.111.29.194', 'extzwt', 'dmpzwt', 'repzwta-p', 'extdczw', 'dmpdczw', 'repdczwc3', 'zwzxdb'))
db.append(('zyxf', '11.111.6.72', 'ext-all', 'dpe-all', 'repdall', 'extdcua', 'dmpdcua', 'repdcuad', 'zyxfchnl'))
db.append(('qfcenter', '11.111.25.7', 'extums', 'dmpums', 'repums', 'extdcub', 'dmpdcub', 'repdcubd', 'zyxfjr'))
db.append(('fmsmid', '11.111.25.7', 'extums', 'dmpums', 'repums', 'extdcub', 'dmpdcub', 'repdcubd', 'zyxfjr'))
db.append(('reporter', '11.111.25.7', 'extrep', 'dmprep', 'reprep', 'extdcub', 'dmpdcub', 'repdcubd', 'zyxfjr'))
db.append(('ffzx', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('imop_security', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('imop_salesman', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('imop_coupon', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('imop_base', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('dzxyxt', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('magicbox', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('upmp_credit', '11.111.27.126', 'ext-ulcp', 'dmp-ulcp', 'repulcp', 'extdcuz', 'dmpdcuz', 'repdcuze', 'edzxdb'))
db.append(('afms', '11.111.27.62', 'ext-fqz', 'dmp-fqz', 'repfqz', 'extdcub', 'dmpdcub', 'repdcubb', 'fqzdb'))
db.append(('uc_center', '11.111.28.117', 'ext-uc', 'dmp-uc', 'repyhzx1-8', 'extdcuy', 'dmpdcuy', 'repdcuye', 'yhzxdb'))
db.append(('apcusr', '11.111.28.117', 'ext-uc', 'dmp-uc', 'repyhzx1-8', 'extdcuy', 'dmpdcuy', 'repdcuye', 'yhzxdb'))
db.append(('ucqi', '11.111.28.112', 'extucq', 'dmpucq', 'repucq', 'extdcuz', 'dmpdcuz', 'repdcuze', 'bdpdb'))
db.append(('zycrm', '11.111.6.202', 'extzysho', 'dmpzysho', 'repzysho', 'extdcuz', 'dmpdcuz', 'repdcuze', 'immall'))
db.append(('imop_activity', '11.111.6.202', 'extffzx', 'dmpffzx', 'repffzx', 'extdcub', 'dmpdcub', 'repdcubd', 'immall'))
db.append(('activity', '11.111.6.72', 'ext-ac', 'dpe-ac', 'repqdac', 'extdcub', 'dmpdcub', 'repdcubd', 'zyxfchnl'))
db.append(('core_processing', '11.111.28.219', 'extcore', 'dmpcore', 'repcore1-4', 'extdczw', 'dmpdczw', 'repdczw1', 'xxdb'))
db.append(('lwdsp', '11.111.28.112', 'extlwdsp', 'dmplwdsp', 'replwdsp', 'extdcuy', 'dmpdcuy', 'repdcuyb', 'bdpdb'))
db.append(('ai_scene', '11.111.28.112', 'extlwdsp', 'dmplwdsp', 'replwdsp', 'extdcuy', 'dmpdcuy', 'repdcuyb', 'bdpdb'))
db.append(('ycmgr', '11.111.6.38', 'ext_nkf', 'dmp_nkf', 'repnkf', 'extdcuz', 'dmpdcuz', 'repdcuze', 'nkfdb'))
db.append(('zyxfnfs', '11.111.6.79', 'ext-tyxx', 'dpe-tyxx', 'reptyxxa-h', 'extdcuz', 'dmpdcuz', 'repdcuzn', 'kfdb'))
db.append(('mop', '11.111.6.72', 'ext-mop', 'dmp-mop', 'repdmop', 'extdcuy', 'dmpdcuy', 'repdcuyg', 'zyxfchnl'))
db.append(('ffkfqz', '11.111.6.72', 'extkfqz', 'dpekfqz', 'repkfqz', 'extdcuz', 'dmpdcuz', 'repdcuze', 'zyxfchnl'))
db.append(('ums', '11.111.25.9', 'extums', 'dmpums', 'repums', 'extdcuy', 'dmpdcuy', 'repdcuyc', 'zyxfjr'))
db.append(('ucpayusr', '11.111.28.211', 'ext-zf', 'dmp-zf', 'rezfucp', 'extdcua', 'dmpdcua', 'repdcuac', 'ucpaydb'))
db.append(('map', '11.111.6.79', 'ext-tyxx', 'dpe-tyxx', 'reptyxx', 'extdcuz', 'dmpdcuz', 'repdcuzn', 'kfdb'))
db.append(('fap', '11.111.25.9', 'extums', 'dmpums', 'repums', 'extdcuy', 'dmpdcuy', 'repdcuyc', 'zyxfjr'))
db.append(('ibsuser', '11.111.25.9', 'extums', 'dmpums', 'repums', 'extdcuz', 'dmpdcuz', 'repdcuze', 'zyxfjr'))
db.append(('limit_center', '11.111.27.81', 'ext-edzx', 'dmp-edzx', 'repedzxa-e', 'extdcub', 'dmpdcub', 'repdcubc', 'edzxdb'))
db.append(('i9_lab', '11.111.28.121', 'exti9', 'dmpi9', 'repi9', 'extdcuy', 'dmpdcuy', 'repdcuyc', 'fwbz'))
db.append(('crs', '11.111.28.121', 'extcrs', 'dmpcrs', 'repcrs', 'extdcuy', 'dmpdcuy', 'repdcuyc', 'fwbz'))
db.append(('settle', '11.111.25.9', 'extzy', 'dmpzy', 'repzy', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'zyxfjr'))
db.append(('crcdata', '11.111.25.9', 'extzy', 'dmpzy', 'repzy', 'extdcuy', 'dmpdcuy', 'repdcuyh', 'zyxfjr'))

link_sids = ['yhzxdb', 'ucpaydb', 'csmdb', 'psbc', 'zwzxdb', 'dpdb']
link_users = []
for conn in db:
    if conn[8] in link_sids and conn[0] not in link_users:
        link_users.append(conn[0])

exists_user = []
for u in db:
    exists_user.append(u[0])

date_str = Tools.locatdate().replace('-', '')

tables = '''
CRCDATA.PBC_PUBLIC_CUST_INFO
CRCDATA.PBC_CUST_INFO
CRCDATA.PBC_ORG_LEGAL_PERSON_INFO
CRCDATA.PBC_BRANCH_INFO
CRCDATA.PBC_LOAN_WITHDRAW_LOG
CRCDATA.PBC_LOAN_INFO
CRCDATA.PBC_LOAN_PRIN_BAL
CRCDATA.PBC_INBANK_DEPOSIT_TRANS_LOG
CRCDATA.PBC_INBANK_DEPOSIT_INFO
CRCDATA.PBC_INBANK_DEPOSIT_BAL
CRCDATA.PBC_INBANK_LOAN_TRANS_LOG
CRCDATA.PBC_INBANK_LOAN_INFO
CRCDATA.PBC_INBANK_LOAN_BAL
CRCDATA.PBC_FTP_DETAIL
CRCDATA.PBC_RATE_EXRATE_REPORT
CRCDATA.PBC_RATE_CHECK_ERR_LOG
CRCDATA.PBC_RPT_ENT_CNY_FLR_RNG_NR01
CRCDATA.PBC_RPT_CNY_FLR_DDLN_STR_NR02
CRCDATA.PBC_RPT_CNY_FLR_RNG_NR03
CRCDATA.PBC_RPT_CNY_FXR_DDLN_STR_NR04
CRCDATA.PBC_RPT_CNY_FXR_RNG_NR05
CRCDATA.PBC_RPT_CNY_DSCR_LV_NR06
CRCDATA.PBC_RPT_MKT_OFR_R_STAT_NR07
CRCDATA.PBC_RPT_HSE_FLR_LV_NR11
CRCDATA.PBC_RPT_HSE_FLR_RNG_NR12
CRCDATA.PBC_RPT_HSE_FXR_LV_NR13
CRCDATA.PBC_RPT_HSE_FXR_RNG_NR14
CRCDATA.PBC_RPT_ARGM_R_MON_NR20
CRCDATA.PBC_RPT_FIN_IBK_DP_R_LV_NR21
CRCDATA.PBC_RPT_IBK_LOAN_R_NR22
CRCDATA.PBC_RPT_CNY_DP_R_AP_NR31
CRCDATA.PBC_RPT_USD_R_MON_NR51
CRCDATA.PBC_RPT_EUR_R_MON_NR52
CRCDATA.PBC_RPT_JPY_R_MON_NR53
CRCDATA.PBC_RPT_HKD_R_MON_NR54
'''


def main():
    
    script_str = ''
    
    # 从tables找出用户.表，用户
    table_list = []
    user_list = []
    for table in tables.lower().split('\n'):
        if ' ' in table:
            print('表中存在空格：' + table)
            return
        if '.' in table:
            table_list.append(table.strip())
            user = table.split('.')[0]
            if user not in user_list:
                user_list.append(user)
                
    # 校验映射关系是否全部存在
    all_exists = True
    for user in user_list:
        if user in exists_user:
            pass
        else:
            all_exists = False
            print(user + ':不存在')
    if not all_exists:
        exit
   
    # 业务库到ODS库
    for user in user_list:
        script_str = script_str + '----------------------------------------------------------------------------------------------------------------------------------\n\n'
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                
        if str(ogg_mess[1]).startswith('11.111'):
            beijin = True
        else:
            beijin = False
            
        if beijin:
            script_str = script_str + '-- ' + user + ' 相关需求表 业务库到ODS库' + '\n'
            script_str = script_str + 'ssh oracle@' + ogg_mess[1] + '\n\n'        
        else:
            script_str = script_str + '-- ' + user + ' 相关需求表 业务库到ODS库' + '\n'
            script_str = script_str + 'ssh ' + ogg_mess[1] + '\nsu - oracle\n\n'
            
        # 查询业务库表大小
        script_str = script_str + '-- 查询业务库表大小' + '\n'
        get_table_size_sql = 'sqlplus / as sysdba\ncol table_name format a50;\n'
        for table in table_list:
            if user == table.split('.')[0]:
                get_table_size_sql = get_table_size_sql + "select '" + table + "' table_name, (select sum(t.bytes)/1024/1024 from dba_segments t where t.owner = '" + table.split('.')[0].upper() + "' and t.segment_name = '" + table.split('.')[1].upper() + "') size_m, (select count(1) from dba_tables t2 where t2.owner = '" + table.split('.')[0].upper() + "' and t2.table_name = '" + table.split('.')[1].upper() + "') tab_exists, (select count(1) from dba_indexes t3 where t3.table_owner = '" + table.split('.')[0].upper() + "' and t3.table_name = '" + table.split('.')[1].upper() + "' and t3.uniqueness = 'UNIQUE') unique_idx_num from dual union all\n"
        script_str = script_str + get_table_size_sql.rstrip('all\n').rstrip(' union') + ';\n\nexit\n\n'
        
        # 查询表是否已经配置OGG、或者被屏蔽、或者配置了*
        script_str = script_str + '-- 查询表是否已经配置OGG、或者被屏蔽、或者配置了*' + '\n'
        for table in table_list:
            if user == table.split('.')[0]:
                script_str = script_str + '/odc/ogg_pre_check.sh ' + table + ' $ORACLE_SID\n'
        script_str = script_str + '\n'
        
        for table in table_list:
            if user == table.split('.')[0]:
                script_str = script_str + 'grep -i \'' + table + '\' /odc/dirprm/*.prm\n'
        script_str = script_str + '\n'
        
        # 备份配置文件
        script_str = script_str + '-- 备份配置文件\n'
        if beijin:
            script_str = script_str + 'cp /odc/dirprm/' + ogg_mess[2] + '.prm /odc/dirprm/bak/' + ogg_mess[2] + '.prm.' + date_str + '\n'
            script_str = script_str + 'cp /odc/dirprm/' + ogg_mess[3] + '.prm /odc/dirprm/bak/' + ogg_mess[3] + '.prm.' + date_str + '\n\n'
        else:
            script_str = script_str + 'cp /odc/ogg/dirprm/' + ogg_mess[2] + '.prm /odc/ogg/dirprm/bak/' + ogg_mess[2] + '.prm.' + date_str + '\n'
            script_str = script_str + 'cp /odc/ogg/dirprm/' + ogg_mess[3] + '.prm /odc/ogg/dirprm/bak/' + ogg_mess[3] + '.prm.' + date_str + '\n\n'
            
        # 加trandata
        if beijin:
            script_str = script_str + '-- 加trandata\n/odc/ggsci\nview param ' + ogg_mess[2] + '\ndblogin\n'
        else:
            script_str = script_str + '-- 加trandata\n/odc/ogg/ggsci\nview param ' + ogg_mess[2] + '\ndblogin\n'
        add_trandata = ''
        for table in table_list:
            if user == table.split('.')[0]:
                add_trandata = add_trandata + "add trandata " + table + "\n"
        script_str = script_str + add_trandata + '\n'
        
        # 编辑ext
        script_str = script_str + '-- 编辑ext\nedit param ' + ogg_mess[2] + '\n'
        for table in table_list:
            if user == table.split('.')[0]:
                script_str = script_str + "include objname " + table + " &\n"
        script_str = script_str + '\n-- ' + date_str + '\n'
        for table in table_list:
            if user == table.split('.')[0]:
                script_str = script_str + "table " + table + " ;\n"
        
        # 编辑dmp
        script_str = script_str + '\n-- 编辑dmp\nedit param ' + ogg_mess[3] + '\n'
        script_str = script_str + '\n-- ' + date_str + '\n'
        for table in table_list:
            if user == table.split('.')[0]:
                script_str = script_str + "table " + table + " ;\n"
        
        # 重启ext、dmp
        script_str = script_str + '\n-- 重启ext、dmp\nstop ' + ogg_mess[2] + '\nstop ' + ogg_mess[3] + '\n\nstart ' + ogg_mess[2] + '\nstart ' + ogg_mess[3]
        script_str = script_str + '\n\nexit\n'
        
        # 到ODS库备份配置文件，停rep进程
        script_str = script_str + '\n-- 到ODS库备份配置文件，停rep进程\n'
        script_str = script_str + 'ssh oracle@11.111.24.149\n'
        if str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == 'a':
            rep_name = ogg_mess[4].split('a-')[0]
            begin_num = ord(str(ogg_mess[4])[-3])
            end_num = ord(str(ogg_mess[4])[-1]) + 1
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'cp /odc/dirprm/' + rep_name + '' + chr(idx) + '.prm /odc/dirprm/bak/' + rep_name + '' + chr(idx) + '.prm.' + date_str + '\n'
            
            script_str = script_str + '\n/odc/ggsci\n'
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'stop ' + rep_name + '' + chr(idx) + '\n'
            
            script_str = script_str + '\nexit\n'
        elif str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(str(ogg_mess[4])[-1]) + 1
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'cp /odc/dirprm/' + rep_name + '' + str(idx) + '.prm /odc/dirprm/bak/' + rep_name + '' + str(idx) + '.prm.' + date_str + '\n'
            
            script_str = script_str + '\n/odc/ggsci\n'
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'stop ' + rep_name + '' + str(idx) + '\n'
            
            script_str = script_str + '\nexit\n'
        elif str(ogg_mess[4])[-3] == '-':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-2]) * 10 + int(ogg_mess[4][-1]) + 1
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'cp /odc/dirprm/' + rep_name + '' + str(idx) + '.prm /odc/dirprm/bak/' + rep_name + '' + str(idx) + '.prm.' + date_str + '\n'
            
            script_str = script_str + '\n/odc/ggsci\n'
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'stop ' + rep_name + '' + str(idx) + '\n'
            
            script_str = script_str + '\nexit\n'
        else:
            script_str = script_str + 'cp /odc/dirprm/' + ogg_mess[4] + '.prm /odc/dirprm/bak/' + ogg_mess[4] + '.prm.' + date_str + '\n'
            script_str = script_str + '/odc/ggsci\nstop ' + ogg_mess[4] + '\n\nexit\n'
        
        # 业务库查询scn_number
        script_str = script_str + '\n-- 业务库查询scn_number\n'
        script_str = script_str + 'ssh oracle@' + ogg_mess[1] + '\nsqlplus / as sysdba\nselect to_char(current_scn) from v$database;\n-- scn_number_' + user + '_2ods\nexit\n'
        
        # 导出dmp文件
        script_str = script_str + '\n-- 导出dmp文件\n'
        table_str = ''
        for t in table_list:
            if t.split('.')[0] == user:
                table_str = table_str + t + ','
        table_str = table_str.strip(',')
        expdp = 'expdp \\"/ as sysdba \\" directory=dump dumpfile=expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_%U.dmp logfile=expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_.log tables=' + table_str + ' cluster=n parallel=8 compression=all flashback_scn=scn_number_' + user + '_2ods '
        script_str = script_str + expdp
        
        # scp到ODS库
        if beijin:
            script_str = script_str + '\n\n-- 传到ODS库 11.111.64.3上操作\n'
            script_str = script_str + 'scp oracle@' + ogg_mess[1] + ':/dbbak/dump/expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_*.dmp /tmp\n'
            script_str = script_str + 'scp /tmp/expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_*.dmp oracle@11.111.24.149:/dbbak/dump\n'
        else:
            script_str = script_str + '\n\n-- 想办法把文件传到ODS库 6.53操作\n'
            script_str = script_str + 'scp ' + ogg_mess[1] + ':/dbbak/dump/expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_*.dmp /tmp/\n'
            script_str = script_str + 'scp /tmp/expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_*.dmp 14.32.5.1:/tmp/\n'
            script_str = script_str + 'ssh 14.32.5.1\n'
            script_str = script_str + 'chown oracle:oinstall /tmp/expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_*.dmp\n'
            script_str = script_str + 'exit\n\n'
            script_str = script_str + '-- ods库操作\n'
            script_str = script_str + 'scp -P 7859 oracle@14.32.5.1:/tmp/expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_*.dmp /dbbak/dump\n'
        '''
        # ODS库编辑rep配置文件
        script_str = script_str + '\n-- ODS库编辑rep配置文件\nssh oracle@11.111.24.149\n/odc/ggsci\n'
        if str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == 'a':
            rep_name = ogg_mess[4].split('a-')[0]
            begin_num = ord(str(ogg_mess[4])[-3])
            end_num = ord(str(ogg_mess[4])[-1]) + 1
            max_num = end_num - begin_num
            
            for idx in range(begin_num, end_num):
                editrep = '\nedit param ' + rep_name + '' + chr(idx) + '\n'
                editrep = editrep + '-- ' + date_str + '\n'
                map_ = ''
                for t in table_list:
                    if user == t.split('.')[0]:
                        map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + '), filter(@range(' + str(idx - 96) + ', ' + str(max_num) + '));\n'
                map_ = map_.strip('\n')
                editrep = editrep + map_ + '\n'
                script_str = script_str + editrep
        elif str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-1]) + 1
            max_num = end_num - begin_num
            
            for idx in range(begin_num, end_num):
                editrep = '\nedit param ' + rep_name + '' + str(idx) + '\n'
                editrep = editrep + '-- ' + date_str + '\n'
                map_ = ''
                for t in table_list:
                    if user == t.split('.')[0]:
                        map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + '), filter(@range(' + str(idx) + ', ' + str(max_num) + '));\n'
                map_ = map_.strip('\n')
                editrep = editrep + map_ + '\n'
                script_str = script_str + editrep
        elif str(ogg_mess[4])[-3] == '-' and str(ogg_mess[4])[-4] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-2]) * 10 + int(ogg_mess[4][-1]) + 1
            max_num = end_num - begin_num
            
            for idx in range(begin_num, end_num):
                editrep = '\nedit param ' + rep_name + '' + str(idx) + '\n'
                editrep = editrep + '-- ' + date_str + '\n'
                map_ = ''
                for t in table_list:
                    if user == t.split('.')[0]:
                        map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + '), filter(@range(' + str(idx) + ', ' + str(max_num) + '));\n'
                map_ = map_.strip('\n')
                editrep = editrep + map_ + '\n'
                script_str = script_str + editrep
        else:
            editrep = '\nedit param ' + ogg_mess[4] + '\n'
            editrep = editrep + '-- ' + date_str + '\n'
            map_ = ''
            for t in table_list:
                if user == t.split('.')[0]:
                    map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + ');\n'
            map_ = map_.strip('\n')
            editrep = editrep + map_    
            script_str = script_str + editrep
        '''    
        # ODS库编辑rep配置文件
        script_str = script_str + '\n-- ODS库编辑rep配置文件\nssh oracle@11.111.24.149\n/odc/ggsci\n'
        if str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == 'a':
            rep_name = ogg_mess[4].split('a-')[0]
            begin_num = ord(str(ogg_mess[4])[-3])
            end_num = ord(str(ogg_mess[4])[-1]) + 1
            max_num = end_num - begin_num
            
            for idx in range(begin_num, end_num):
                editrep = '\necho \'\n'
                editrep = editrep + '-- ' + date_str + '\n'
                map_ = ''
                for t in table_list:
                    if user == t.split('.')[0]:
                        map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + '), filter(@range(' + str(idx - 96) + ', ' + str(max_num) + '));\n'
                map_ = map_.strip('\n')
                editrep = editrep + map_ + '\' >> /odc/dirprm/' + rep_name + chr(idx) + '.prm\n'
                script_str = script_str + editrep
        elif str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-1]) + 1
            max_num = end_num - begin_num
            
            for idx in range(begin_num, end_num):
                editrep = '\necho \'\n'
                editrep = editrep + '-- ' + date_str + '\n'
                map_ = ''
                for t in table_list:
                    if user == t.split('.')[0]:
                        map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + '), filter(@range(' + str(idx) + ', ' + str(max_num) + '));\n'
                map_ = map_.strip('\n')
                editrep = editrep + map_ + '\' >> /odc/dirprm/' + rep_name + str(idx) + '.prm\n'
                script_str = script_str + editrep
        elif str(ogg_mess[4])[-3] == '-' and str(ogg_mess[4])[-4] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-2]) * 10 + int(ogg_mess[4][-1]) + 1
            max_num = end_num - begin_num
            
            for idx in range(begin_num, end_num):
                editrep = '\necho \'\n'
                editrep = editrep + '-- ' + date_str + '\n'
                map_ = ''
                for t in table_list:
                    if user == t.split('.')[0]:
                        map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + '), filter(@range(' + str(idx) + ', ' + str(max_num) + '));\n'
                map_ = map_.strip('\n')
                editrep = editrep + map_ + '\' >> /odc/dirprm/' + rep_name + str(idx) + '.prm\n'
                script_str = script_str + editrep
        else:
            editrep = '\nedit param ' + ogg_mess[4] + '\n'
            editrep = editrep + '-- ' + date_str + '\n'
            map_ = ''
            for t in table_list:
                if user == t.split('.')[0]:
                    map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_' + user + '_2ods' + ');\n'
            map_ = map_.strip('\n')
            editrep = editrep + map_    
            script_str = script_str + editrep
            
        script_str = script_str + '\n\n-- 如果需要屏蔽表\n'
        mapexclude_ = '-- ' + date_str + '\n'
        for t in table_list:
            if user == t.split('.')[0]:
                mapexclude_ = mapexclude_ + 'mapexclude ' + t + ';\n'
        mapexclude_ = mapexclude_.strip('\n')
        script_str = script_str + mapexclude_ + '\n\n'
        
        tableexclude_ = '-- ' + date_str + '\n'
        for t in table_list:
            if user == t.split('.')[0]:
                tableexclude_ = tableexclude_ + 'tableexclude ' + t + ';\n'
        tableexclude_ = tableexclude_.strip('\n')
        script_str = script_str + tableexclude_
        
        script_str = script_str + '\n\nexit\n'
        
        # 查询目标库表情况
        script_str = script_str + '\n-- 查询目标库表情况' + '\n'
        get_table_size_sql = 'sqlplus / as sysdba\ncol table_name format a50;\n'
        for table in table_list:
            if user == table.split('.')[0]:
                get_table_size_sql = get_table_size_sql + "select '" + table + "' table_name, (select sum(t.bytes)/1024/1024 from dba_segments t where t.owner = '" + table.split('.')[0].upper() + "' and t.segment_name = '" + table.split('.')[1].upper() + "') size_m, (select count(1) from dba_tables t2 where t2.owner = '" + table.split('.')[0].upper() + "' and t2.table_name = '" + table.split('.')[1].upper() + "') tab_exists, (select count(1) from dba_indexes t3 where t3.table_owner = '" + table.split('.')[0].upper() + "' and t3.table_name = '" + table.split('.')[1].upper() + "' and t3.uniqueness = 'UNIQUE') unique_idx_num from dual union all\n"
        script_str = script_str + get_table_size_sql.rstrip('all\n').rstrip(' union') + ';\n\nexit\n\n'
        
        # 导入ODS库
        script_str = script_str + '\n-- 导入ODS库\n'
        script_str = script_str + 'impdp \\"/ as sysdba \\" directory=dump dumpfile=expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_%U.dmp logfile=expdp_2ogg_scn_number_' + user + '_2ods_' + date_str + '_.log cluster=n parallel=8\n'
        
        script_str = script_str + '\n-- 如果表空间不存在\n'
        script_str = script_str + "create tablespace XXX datafile '+DATAXX/' size 32760M autoextend off;\n"
        
        script_str = script_str + '\n-- 如果表用户不存在\n'
        script_str = script_str + "create user XXX identified by XXX default tablespace XXX;\n"
        script_str = script_str + "grant connect, resource to XXX;\n"
        
        # 启动rep进程
        script_str = script_str + '\n-- 启动rep进程\n/odc/ggsci\n'
        if str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == 'a':
            rep_name = ogg_mess[4].split('a-')[0]
            begin_num = ord(str(ogg_mess[4])[-3])
            end_num = ord(str(ogg_mess[4])[-1]) + 1
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'start ' + rep_name + '' + chr(idx) + '\n'
            script_str = script_str + '\n'   
        elif str(ogg_mess[4])[-2] == '-' and str(ogg_mess[4])[-3] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-1]) + 1
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'start ' + rep_name + '' + str(idx) + '\n'
            script_str = script_str + '\n'   
        elif str(ogg_mess[4])[-3] == '-' and str(ogg_mess[4])[-4] == '1':
            rep_name = ogg_mess[4].split('1-')[0]
            begin_num = 1
            end_num = int(ogg_mess[4][-2]) * 10 + int(ogg_mess[4][-1]) + 1
            
            for idx in range(begin_num, end_num):
                script_str = script_str + 'start ' + rep_name + '' + str(idx) + '\n'
            script_str = script_str + '\n'   
        else:
            startrep = 'start ' + ogg_mess[4] + '\n\nexit\n\n'
            script_str = script_str + startrep
    
    # ODS库到探查库
    script_str = script_str + '----------------------------------------------------------------------------------------------------------------------------------\n\n'
    script_str = script_str + '-- 相关需求表 ODS库到探查库' + '\n\n'
    
    script_str = script_str + '-- dblink部分' + '\n'
    script_str = script_str + 'ssh oracle@11.111.24.149\n'
    script_str = script_str + 'ssh -p 7859 oracle@14.32.5.1\n'
    script_str = script_str + 'sqlplus / as sysdba\n'
    for link_user in link_users:
        if link_user in user_list:
            user_list.remove(link_user)
            ogg_mess = ''
            for ogg_mess_ in db:
                if link_user == ogg_mess_[0]:
                    ogg_mess = ogg_mess_
            for table in table_list:
                if link_user == table.split('.')[0]:
                    if table.split('.')[1].upper() not in('NETAFS_REQUEST_COMPORE_INFO'):
                        table_list.remove(table)
                        # script_str = script_str + 'create synonym ' + table + ' for ' + table + '@' + ogg_mess[8] + ';\n'
                        script_str = script_str + 'create view ' + table + ' as select * from ' + table + '@dblk_' + ogg_mess[8] + ';\n'
    script_str = script_str + 'exit;\n\n'
    
    # 查询业务库表大小
    script_str = script_str + '-- 查询业务库表大小' + '\n'
    get_table_size_sql = 'sqlplus / as sysdba\ncol table_name format a50;\n'
    for table in table_list:
        get_table_size_sql = get_table_size_sql + "select '" + table + "' table_name, (select sum(t.bytes)/1024/1024 from dba_segments t where t.owner = '" + table.split('.')[0].upper() + "' and t.segment_name = '" + table.split('.')[1].upper() + "') size_m, (select count(1) from dba_tables t2 where t2.owner = '" + table.split('.')[0].upper() + "' and t2.table_name = '" + table.split('.')[1].upper() + "') tab_exists, (select count(1) from dba_indexes t3 where t3.table_owner = '" + table.split('.')[0].upper() + "' and t3.table_name = '" + table.split('.')[1].upper() + "' and t3.uniqueness = 'UNIQUE') unique_idx_num from dual union all\n"
    script_str = script_str + get_table_size_sql.rstrip('all\n').rstrip(' union') + ';\n\nexit\n\n'

    # 查询表是否已经配置OGG、或者被屏蔽、或者配置了*
    script_str = script_str + '-- 查询表是否已经配置OGG、或者被屏蔽、或者配置了*' + '\n'
    for table in table_list:
        script_str = script_str + '/odc/ogg_pre_check.sh ' + table + ' $ORACLE_SID\n'
    script_str = script_str + '\n'
    
    for table in table_list:
        script_str = script_str + 'grep -i \'' + table + '\' /odc/dirprm/*.prm\n'
    script_str = script_str + '\n'
    
    # 备份配置文件
    script_str = script_str + '-- 备份配置文件\n'
    o5 = []
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if ogg_mess[5] not in o5:
                    script_str = script_str + 'cp /odc/dirprm/' + ogg_mess[5] + '.prm /odc/dirprm/bak/' + ogg_mess[5] + '.prm.' + date_str + '\n'
                    script_str = script_str + 'cp /odc/dirprm/' + ogg_mess[6] + '.prm /odc/dirprm/bak/' + ogg_mess[6] + '.prm.' + date_str + '\n'
                    o5.append(ogg_mess[5])
                        
    # 加trandata
    script_str = script_str + '\n-- 加trandata\n/odc/ggsci\nview param ' + ogg_mess[5] + '\ndblogin\n'
    add_trandata = ''
    for table in table_list:
        add_trandata = add_trandata + "add trandata " + table + "\n"
    script_str = script_str + add_trandata + '\n'
    
    # 编辑ext
    script_str = script_str + '-- 编辑ext\n'
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                script_str = script_str + '\nedit param ' + ogg_mess[5] + '\n'
                for table in table_list:
                    if user == table.split('.')[0]:
                        script_str = script_str + "include objname " + table + " &\n"
                script_str = script_str + '\n-- ' + date_str + '\n'
                for table in table_list:
                    if user == table.split('.')[0]:
                        script_str = script_str + "table " + table + " ;\n"
    
    # 编辑dmp
    script_str = script_str + '\n-- 编辑dmp'
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                script_str = script_str + '\nedit param ' + ogg_mess[6] + '\n'
                script_str = script_str + '\n-- ' + date_str + '\n'
                for table in table_list:
                    if user == table.split('.')[0]:
                        script_str = script_str + "table " + table + " ;\n"
                
    # 重启ext、dmp
    script_str = script_str + '\n-- 重启ext、dmp\n'
    o5 = []
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if ogg_mess[5] not in o5:
                    script_str = script_str + 'stop ' + ogg_mess[5] + '\nstop ' + ogg_mess[6] + '\n'
                    o5.append(ogg_mess[5])
    script_str = script_str + '\n'
    o5 = []
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if ogg_mess[5] not in o5:
                    script_str = script_str + 'start ' + ogg_mess[5] + '\nstart ' + ogg_mess[6] + '\n'
                    o5.append(ogg_mess[5])

    script_str = script_str + '\nexit\n'
                    
    # 到探查库备份配置文件，停rep进程
    script_str = script_str + '\n-- 到探查库备份配置文件，停rep进程\n'
    script_str = script_str + 'ssh -p 7859 oracle@14.32.5.1\n'
    
    o7 = []
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if ogg_mess[7] not in o7:
                    if str(ogg_mess[7])[-2] == '-':
                        rep_name = ogg_mess[7].split('a-')[0]
                        begin_num = ord(str(ogg_mess[7])[-3])
                        end_num = ord(str(ogg_mess[7])[-1]) + 1
                        
                        for idx in range(begin_num, end_num):
                            script_str = script_str + 'cp /odc/dirprm/' + rep_name + '' + chr(idx) + '.prm /odc/dirprm/bak/' + rep_name + '' + chr(idx) + '.prm.' + date_str + '\n'
                    else:
                        script_str = script_str + 'cp /odc/dirprm/' + ogg_mess[7] + '.prm /odc/dirprm/bak/' + ogg_mess[7] + '.prm.' + date_str + '\n'
                    o7.append(ogg_mess[7])
                    
    script_str = script_str + '\n'     
    script_str = script_str + '\n/odc/ggsci\n'      
    o7 = []     
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if ogg_mess[7] not in o7:
                    if str(ogg_mess[7])[-2] == '-': 
                        for idx in range(begin_num, end_num):
                            script_str = script_str + 'stop ' + rep_name + '' + chr(idx) + '\n'
                    else:
                        script_str = script_str + 'stop ' + ogg_mess[7] + '\n'
                    o7.append(ogg_mess[7])
                    
    script_str = script_str + '\nexit\n'

    # 业务库查询scn_number
    script_str = script_str + '\n-- ODS库查询scn_number\n'
    script_str = script_str + 'ssh oracle@11.111.24.149\nsqlplus / as sysdba\nselect to_char(current_scn) from v$database;\n-- scn_number_2tck\nexit\n'
    
    # 导出dmp文件
    script_str = script_str + '\n-- 导出dmp文件\n'
    table_str = ''
    for t in table_list:
        table_str = table_str + t + ','
    table_str = table_str.strip(',')
    expdp = 'expdp \\"/ as sysdba \\" directory=dump dumpfile=expdp_2tck_scn_number_2tck_' + date_str + '_%U.dmp logfile=expdp_2tck_scn_number_2tck_' + date_str + '_.log tables=' + table_str + ' cluster=n parallel=8 compression=all flashback_scn=scn_number_2tck '
    script_str = script_str + expdp
    
    # scp到探查库
    script_str = script_str + '\n\n-- 传到探查库\n'
    script_str = script_str + 'scp -P 7859 /dbbak/dump/expdp_2tck_scn_number_2tck_' + date_str + '_*.dmp oracle@14.32.5.1:/localdisk/dump\n'

    # 探查库编辑rep配置文件
    script_str = script_str + '\n-- 探查库编辑rep配置文件\nssh -p 7859 oracle@14.32.5.1\n/odc/ggsci'
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if str(ogg_mess[7])[-2] == '-':
                    rep_name = ogg_mess[7].split('a-')[0]
                    begin_num = ord(str(ogg_mess[7])[-3])
                    end_num = ord(str(ogg_mess[7])[-1]) + 1
                    max_num = end_num - begin_num
                    
                    for idx in range(begin_num, end_num):
                        editrep = '\n\nedit param ' + rep_name + '' + chr(idx) + '\n'
                        editrep = editrep + '-- ' + date_str + '\n'
                        map_ = ''
                        for t in table_list:
                            if user == t.split('.')[0]:
                                map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_2tck' + '), filter(@range(' + str(idx - 96) + ', ' + str(max_num) + '));\n'
                        map_ = map_.strip('\n')
                        editrep = editrep + map_ + '\n'
                        script_str = script_str + editrep
                        
                else:
                    editrep = '\n\nedit param ' + ogg_mess[7] + '\n'
                    editrep = editrep + '-- ' + date_str + '\n'
                    map_ = ''
                    for t in table_list:
                        if user == t.split('.')[0]:
                            map_ = map_ + 'map ' + t + ', target ' + t + ', filter(@getenv("transaction","csn")>scn_number_2tck' + ');\n'
                    map_ = map_.strip('\n')
                    editrep = editrep + map_    
                    script_str = script_str + editrep
    script_str = script_str + '\n\nexit\n'
        
    # 导入探查库
    script_str = script_str + '\n-- 导入探查库\n'
    script_str = script_str + 'impdp \\"/ as sysdba \\" directory=oradump dumpfile=expdp_2tck_scn_number_2tck_' + date_str + '_%U.dmp logfile=expdp_2tck_scn_number_2tck_' + date_str + '_.log cluster=n parallel=8 table_exists_action=replace\n'
    script_str = script_str + '\n-- 如果表空间不存在\n'
    script_str = script_str + "create tablespace XXX datafile '+DATA22/' size autoextend off;\n"
    
    # 启动rep进程
    script_str = script_str + '\n-- 启动rep进程\n/odc/ggsci\n'
    o7 = []
    for user in user_list:
        ogg_mess = ''
        for ogg_mess_ in db:
            if user == ogg_mess_[0]:
                ogg_mess = ogg_mess_
                if ogg_mess[7] not in o7:
                    if str(ogg_mess[7])[-2] == '-':
                        rep_name = ogg_mess[7].split('a-')[0]
                        begin_num = ord(str(ogg_mess[7])[-3])
                        end_num = ord(str(ogg_mess[7])[-1]) + 1
                        for idx in range(begin_num, end_num):
                            script_str = script_str + 'start ' + rep_name + '' + chr(idx) + '\n'
                        script_str = script_str + '\n'   
                    else:
                        startrep = 'start ' + ogg_mess[7] + '\n'
                        script_str = script_str + startrep
                    o7.append(ogg_mess[7])
    script_str = script_str + '\nexit\n'
        
    Tools.echo(script_str, 'ogg' + date_str + '.txt', 'w')
    print(script_str)

    
if __name__ == '__main__':
    main()

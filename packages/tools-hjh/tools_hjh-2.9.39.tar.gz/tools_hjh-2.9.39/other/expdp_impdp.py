# coding:utf-8

from tools_hjh import Tools

date_str = Tools.locatdate().replace('-', '')

tables = '''
CRCDATA.PBC_PUBLIC_CUST_INFO           where 1=1
CRCDATA.PBC_CUST_INFO                  where 1=1
CRCDATA.PBC_ORG_LEGAL_PERSON_INFO      where 1=1
CRCDATA.PBC_BRANCH_INFO                where 1=1
CRCDATA.PBC_LOAN_WITHDRAW_LOG          where 1=1
CRCDATA.PBC_LOAN_INFO                  where 1=1
CRCDATA.PBC_LOAN_PRIN_BAL              where 1=1
CRCDATA.PBC_INBANK_DEPOSIT_TRANS_LOG   where 1=1
CRCDATA.PBC_INBANK_DEPOSIT_INFO        where 1=1
CRCDATA.PBC_INBANK_DEPOSIT_BAL         where 1=1
CRCDATA.PBC_INBANK_LOAN_TRANS_LOG      where 1=1
CRCDATA.PBC_INBANK_LOAN_INFO           where 1=1
CRCDATA.PBC_INBANK_LOAN_BAL            where 1=1
CRCDATA.PBC_FTP_DETAIL                 where 1=1
CRCDATA.PBC_RATE_EXRATE_REPORT         where 1=1
CRCDATA.PBC_RATE_CHECK_ERR_LOG         where 1=1
CRCDATA.PBC_RPT_ENT_CNY_FLR_RNG_NR01   where 1=1
CRCDATA.PBC_RPT_CNY_FLR_DDLN_STR_NR02  where 1=1
CRCDATA.PBC_RPT_CNY_FLR_RNG_NR03       where 1=1
CRCDATA.PBC_RPT_CNY_FXR_DDLN_STR_NR04  where 1=1
CRCDATA.PBC_RPT_CNY_FXR_RNG_NR05       where 1=1
CRCDATA.PBC_RPT_CNY_DSCR_LV_NR06       where 1=1
CRCDATA.PBC_RPT_MKT_OFR_R_STAT_NR07    where 1=1
CRCDATA.PBC_RPT_HSE_FLR_LV_NR11        where 1=1
CRCDATA.PBC_RPT_HSE_FLR_RNG_NR12       where 1=1
CRCDATA.PBC_RPT_HSE_FXR_LV_NR13        where 1=1
CRCDATA.PBC_RPT_HSE_FXR_RNG_NR14       where 1=1
CRCDATA.PBC_RPT_ARGM_R_MON_NR20        where 1=1
CRCDATA.PBC_RPT_FIN_IBK_DP_R_LV_NR21   where 1=1
CRCDATA.PBC_RPT_IBK_LOAN_R_NR22        where 1=1
CRCDATA.PBC_RPT_CNY_DP_R_AP_NR31       where 1=1
CRCDATA.PBC_RPT_USD_R_MON_NR51         where 1=1
CRCDATA.PBC_RPT_EUR_R_MON_NR52         where 1=1
CRCDATA.PBC_RPT_JPY_R_MON_NR53         where 1=1
CRCDATA.PBC_RPT_HKD_R_MON_NR54         where 1=1
'''


def main():
    script_str = ''

    script_str = script_str + '\n-- 目标端统计\n'
    for table_str in tables.strip().split('\n'):
        table_str = Tools.merge_spaces(table_str.strip())
        owner = table_str.split('.')[0]
        table = table_str.split('.')[1].split(' where ')[0]
        where = table_str.split('.')[1].split(' where ')[1]
        script_str = script_str + 'select count(1) from ' + table_str + ';\n'
        
    tables_ = ''
    querys_ = ''        
    script_str = script_str + '\n-- 导出语句\n'
    for table_str in tables.strip().split('\n'):
        table_str = Tools.merge_spaces(table_str.strip())
        owner = table_str.split('.')[0]
        table = table_str.split('.')[1].split(' where ')[0]
        tables_ = tables_ + ',' + owner + '.' + table
        where = table_str.split('.')[1].split(' where ')[1]
        querys_ = querys_ + ',' + "" + owner + "." + table + ':"where ' + where + '''"'''
    tables_ = tables_.strip(',')
    querys_ = querys_.strip(',')

    dumpfile = 'expdp_ds_' + date_str + '_%U.dmp'
    directory = 'dump'
    tables__ = '(' + tables_ + ')'
    query = '(' + querys_ + ')'
    
    script_str = script_str + 'vim txt.par' + '\n'
    script_str = script_str + 'dumpfile=' + dumpfile + '\n'
    script_str = script_str + 'directory=' + directory + '\n'
    script_str = script_str + 'tables=' + tables__ + '\n'
    script_str = script_str + 'query=' + query + '\n'
    script_str = script_str + 'cluster=' + 'n' + '\n'
    script_str = script_str + 'parallel=' + '8' + '\n'
    script_str = script_str + 'compression=' + 'all' + '\n'
    script_str = script_str + 'expdp \\"/ as sysdba \\" parfile=txt.par' + '\n'
        
    script_str = script_str + '\n-- 导入语句\n'
    script_str = script_str + 'impdp \\"/ as sysdba \\" directory=dump dumpfile=expdp_ds_' + date_str + '_%U.dmp logfile=impdp_ds_' + date_str + '_.log cluster=n parallel=8 table_exists_action=append\n'
        
    script_str = script_str + '\n-- 删除语句\n'
    for table_str in tables.strip().split('\n'):
        table_str = Tools.merge_spaces(table_str.strip())
        owner = table_str.split('.')[0]
        table = table_str.split('.')[1].split(' where ')[0]
        where = table_str.split('.')[1].split(' where ')[1]
        script_str = script_str + 'delete from ' + table_str + ';\n'
        
    script_str = script_str + '\n-- scp语句 64.3操作\n'
    script_str = script_str + 'scp oracle@11.111.28.107:/dbbak/dump/expdp_ds_' + date_str + '_*.dmp /tmp\n'
    script_str = script_str + 'scp /tmp/expdp_ds_' + date_str + '_*.dmp oracle@11.111.24.149:/dbbak/dump\n'
    script_str = script_str + 'scp -P 7859 /dbbak/dump/expdp_ds_' + date_str + '_*.dmp oracle@14.32.5.1:/localdisk/dump\n'

    print(script_str)

    
if __name__ == '__main__':
    main()

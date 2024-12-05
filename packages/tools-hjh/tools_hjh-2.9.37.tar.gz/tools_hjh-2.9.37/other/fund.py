# coding:utf-8
import sys
from tools_hjh import DBConn
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import Tools
from tools_hjh import HTTPTools
import json
import time
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from tools_hjh.Chrome import ChromePool
from _datetime import timedelta

stop_flag = False
page_num = None

date = Tools.locatdate()
log = Log('U:/MyFiles/MyPy/log/fund/' + date + '.log')

host = 'https://'

chrome_path = r'U:\MyApps\CentBrowser\App\chrome.exe'
chromedriver_path = r'U:\MyApps\CentBrowser\chromedriver.exe'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'text',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': 'x86;v=99, Windows;v=10, Surface Laptop Studio;v=1',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Referer':'http://fundf10.eastmoney.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'cookie':'qgqp_b_id=5b3011884880cd251f1bc065e16256ae; emshistory=%5B%22513100%22%5D; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; HAList=ty-103-NQ00Y-%u5C0F%u578B%u7EB3%u6307%u5F53%u6708%u8FDE%u7EED%2Cty-100-NDX100-%u7EB3%u65AF%u8FBE%u514B100%2Cty-133-USDCNH-%u7F8E%u5143%u79BB%u5CB8%u4EBA%u6C11%u5E01%2Cty-1-512690-%u9152ETF%2Cty-1-513100-%u7EB3%u6307ETF%2Cty-105-NVDA-%u82F1%u4F1F%u8FBE%2Cty-1-600900-%u957F%u6C5F%u7535%u529B%2Cty-1-000001-%u4E0A%u8BC1%u6307%u6570; st_si=04690614705089; st_asi=delete; EMFUND0=null; EMFUND7=07-18%2022%3A48%3A53@%23%24%u62DB%u5546%u4E2D%u8BC1%u767D%u9152%u6307%u6570%28LOF%29A@%23%24161725; EMFUND8=07-19%2002%3A43%3A47@%23%24%u6613%u65B9%u8FBE%u5929%u5929%u7406%u8D22%u8D27%u5E01A@%23%24000009; EMFUND9=07-29 10:05:57@#$%u534E%u590F%u6210%u957F%u6DF7%u5408@%23%24000001; st_pvi=99805886133314; st_sp=2024-04-24%2009%3A56%3A14; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fsh513100.html; st_sn=4; st_psi=20240729100557782-112200305282-3955411629'
}

try:
    sys_argv_1 = sys.argv[1]
except:
    sys_argv_1 = 'download'
try:
    sys_argv_2 = int(sys.argv[2])
except:
    sys_argv_2 = 60
try:
    sys_argv_3 = sys.argv[3]
except:
    sys_argv_3 = 32
    

def main(): 
    # db = DBConn('sqlite', db='U:/MyFiles/MyPy/data/fund.db')
    db = DBConn('sqlite', db='D:/fund.db')
    # db = DBConn('pgsql', host='localhost', port='5432', db='fund', username='HJH', password='hjh', poolsize=16)
    createDatabase(db, rebuild=False)
    
    if sys_argv_1 == 'download':
        get_fund_main(db, HTTPTools)
        get_a_stock_main(db, HTTPTools)
        chrome = ChromePool(1, chrome_path, chromedriver_path, is_display_picture=False, is_hidden=True)
        get_a_stock_index_main(db, chrome)
        chrome.close()
        get_fund_dv(db, HTTPTools, page_size=sys_argv_2)
        get_stock_dv(db, HTTPTools, start_date=str(datetime.date.today() - timedelta(days=sys_argv_2)).replace('-', ''))
        # get_stock_dv(db, HTTPTools, start_date='all')
    else: 
        get_by_text(db)
        get_val(db)
        get_hc(db)
        get_nh(db)


def createDatabase(db, rebuild=False):
    if rebuild:
        db.run('drop table if exists t_main')
        db.run('drop table if exists t_date_value')

    t_main = '''
        create table if not exists t_main(
            code char(9),
            name varchar(255),
            type varchar(255),
            primary key(code)
        )
    '''
    
    t_date_value = '''
        create table if not exists t_date_value(
            code char(9),
            date char(10),
            dwjz real,
            ljjz real,
            zf real,
            fh text,
            val real,
            hc real,
            hc1n real,
            hc3n real,
            nh1n real,
            nh3n real,
            nh5n real,
            primary key(code, date)
        )
    '''
    
    db.run(t_main)
    db.run(t_date_value)
    
    db.run('create index if not exists idx_val_code on t_date_value(code)')
    db.run('create index if not exists idx_val_date on t_date_value(date)')
    db.run('create index if not exists idx_zbd_val on t_date_value(val)')
    db.run('create index if not exists idx_zbd_hc on t_date_value(hc)')
    db.run('create index if not exists idx_zbd_nh5n on t_date_value(nh5n)')


def get_fund_main(db, rep):
    sql = 'insert or replace into t_main(code,name,type) values(?,?,?)'
    if db.dbtype == 'pgsql':
        sql = 'insert into t_main(code,name,type) values(?,?,?)'
    page = rep.get('http://fund.eastmoney.com/js/fundcode_search.js')
    page = page.encode('utf8')[3:].decode('utf8')
    page = page.replace('var r = ', '').replace(';', '')
    fund_list = json.loads(page)
    params = []
    for fund in fund_list:
        code = 'jj_' + fund[0]
        name = fund[2]
        type_ = fund[3]
        params.append((code, name, type_))
        log.info('get_fund_main', code, name, type_)
    num = db.run(sql, params)
    log.info('get_fund_main', num)

    
def get_a_stock_main(db, rep):
    sql = 'insert or replace into t_main(code,name,type) values(?,?,?)'
    if db.dbtype == 'pgsql':
        sql = 'insert into t_main(code,name,type) values(?,?,?)'
    timestamp = str(int(time.time() * 1000))
    url = 'https://93.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112403555256741608235_' + timestamp + '&pn=1&pz=6000&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f12&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&_=' + timestamp
    page = rep.get(url)
    page = page.split('"diff":')[1].split('}});')[0]
    stock_list = json.loads(page)
    params = []
    for stock in stock_list:
        code = 'cn_' + stock['f12']
        name = stock['f14']
        type_ = '中国A股'
        params.append((code, name, type_))
        log.info('get_a_stock_main', code, name, type_)
    num = db.run(sql, params)
    log.info('get_a_stock_main', num)

    
def get_a_stock_index_main(db, rep):
    sql = 'insert or replace into t_main(code,name,type) values(?,?,?)'
    if db.dbtype == 'pgsql':
        sql = 'insert into t_main(code,name,type) values(?,?,?)'
    url = 'https://q.stock.sohu.com/cn/zs.shtml'
    page = rep.get(url)
    bs = BeautifulSoup(page, features="lxml")
    trs = bs.find('tbody').find_all('tr')
    params = []
    for tr in trs:
        code = 'zs_' + tr.find('td', class_='e1').text
        name = tr.find('td', class_='e2').text
        type_ = '中国A股指数'
        params.append((code, name, type_))
        log.info('get_a_stock_index_main', code, name, type_)
    num = db.run(sql, params)
    log.info('get_a_stock_index_main', num)


def get_fund_dv(db, rep, page_size):
    vals_all = []
    codes = []
    if page_size == '' or page_size == -1 or page_size == 0 or page_size == None or page_size == 'all':
        page_size = 9999
            
    # sql1 = "insert or replace into t_date_value(code,date,dwjz,ljjz,zf,fh,val) values(?,?,?,?,?,?,?)"
    if page_size == 9999:
        sql = "insert into t_date_value(code,date,dwjz,ljjz,zf,fh,val) select ?,?,?,?,?,?,? where not exists(select 1 from t_date_value where code = ? and date = ?)"
    else:
        sql = "insert into t_date_value(code,date,dwjz,ljjz,zf,fh) select ?,?,?,?,?,? where not exists(select 1 from t_date_value where code = ? and date = ?)"

    def get_fund_dv_one(code, rep, page_size=9999, times=1):
        try:
            val = 1.0
            idx = 1
            timestamp = str(int(time.time() * 1000))
            url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18306743973867400965_1722217638986&fundCode=' + code.split('_')[1] + '&pageIndex=' + str(idx) + '&pageSize=' + str(page_size) + '&startDate=&endDate=&_=' + timestamp
            page = rep.get(url, headers=headers)
            page = page.replace('jQuery18306743973867400965_1722217638986', '').strip()
            page = page.split('"LSJZList":')[1].split(',"FundType"')[0]
            rss = json.loads(page)
            
            if page_size == 9999 and len(rss) > 0:
                exists_count = db.run('select count(1) from t_date_value where code = ?', (code,)).get_rows()[0][0]
                get_min_date = rss[-1]['FSRQ']
                get_max_date = rss[0]['FSRQ']
                try:
                    db_min_date = db.run('select min(date) from t_date_value where code = ?', (code,)).get_rows()[0][0]
                except:
                    db_min_date = '1949-10-01'
                if db_min_date == None:
                    db_min_date = '1949-10-01'
                try:
                    db_max_date = db.run('select max(date) from t_date_value where code = ?', (code,)).get_rows()[0][0]
                except:
                    db_max_date = '2999-01-01'
                if db_max_date == None:
                    db_max_date = '1949-10-01'
                                        
                if int(exists_count) == len(rss) and get_min_date == db_min_date and get_max_date == db_max_date:
                    log.info('get_fund_dv_one', code, 'exists', times)
                    return
                elif get_min_date < db_min_date and int(exists_count) > 0:
                    num = db.run('delete from t_date_value where code = ?', (code,))
                    log.info('get_fund_dv_one', code, 'delete', num, times)
                elif get_min_date == db_min_date and get_max_date > db_max_date:
                    num = len(rss) - int(exists_count)
                elif int(exists_count) == 0:
                    num = len(rss)
                elif get_min_date > db_min_date:
                    raise Exception('get_min_date_error')
                    
            if len(rss) == 0:
                return
            
            for rs in reversed(rss):
                date_ = rs['FSRQ']
                dwjz = rs['DWJZ']
                if dwjz == '':
                    dwjz = None
                ljjz = rs['LJJZ']
                if ljjz == '':
                    ljjz = None
                zf = rs['JZZZL']
                if zf == '':
                    zf = 0
                if page_size == 9999:
                    val = val * (1 + (float(zf) / 100))
                fh = rs['FHSP']
                if fh == '':
                    fh = None
                if page_size == 9999:
                    vals_all.append((code, date_, dwjz, ljjz, zf, fh, val, code, date_))
                else:
                    vals_all.append((code, date_, dwjz, ljjz, zf, fh, code, date_))

            codes.append(code)
            log.info('get_fund_dv_one', code, len(vals_all), times)
                    
        except Exception as _:
            if times <= 10:
                log.error('get_fund_dv_one', code, times, _)
                time.sleep(10)
                times = times + 1
                get_fund_dv_one(code, rep, page_size, times)
            else:
                log.error('get_fund_dv_one', code, times, _)
            
    get_code_sql = '''
        select code from t_main 
        where 1=1
        and type not in('货币型-普通货币')
        and code like 'jj_%'
        --and code = 'jj_000277'
        order by code
    '''
    
    funds = db.run(get_code_sql).get_rows()
    tp = ThreadPool(64)
    for fund in funds:
        if len(vals_all) <= 1000000:
            code = fund[0]
            # time.sleep(0.1)
            tp.run(get_fund_dv_one, (code, rep, page_size))
        else:
            tp.wait()
            log.info('get_fund_dv', 'begin', len(vals_all))
            num = db.run(sql, vals_all)
            log.info('get_fund_dv', num)
            vals_all.clear()
            codes.clear()
    tp.wait()
    num = db.run(sql, vals_all)
    log.info('get_fund_dv', len(codes), num)
    vals_all.clear()
    codes.clear()


def get_stock_dv(db, rep, start_date):
    vals_all = []
    codes = []
    if start_date == 'all':
        start_date = '19491001'
            
    if start_date == '19491001':
        sql = "insert into t_date_value(code,date,dwjz,ljjz,zf,fh,val) select ?,?,?,?,?,?,? where not exists(select 1 from t_date_value where code = ? and date = ?)"
    else:
        sql = "insert into t_date_value(code,date,dwjz,ljjz,zf,fh) select ?,?,?,?,?,? where not exists(select 1 from t_date_value where code = ? and date = ?)"

    def get_stock_dv_one(code, rep, start_date='19491001', times=1):
        try:
            val = 1.0
            today = Tools.locatdate().replace('-', '')
            url = 'https://q.stock.sohu.com/hisHq?code=' + code + '&start=' + start_date + '&end=' + today
            page = rep.get(url, headers=headers)
            js = json.loads(page)
            try:
                rss = js[0]["hq"]
            except:
                return
            
            if start_date == '19491001' and len(rss) > 0:
                exists_count = db.run('select count(1) from t_date_value where code = ?', (code,)).get_rows()[0][0]
                get_min_date = rss[-1][0]
                get_max_date = rss[0][0]
                try:
                    db_min_date = db.run('select min(date) from t_date_value where code = ?', (code,)).get_rows()[0][0]
                except:
                    db_min_date = '1949-10-01'
                if db_min_date == None:
                    db_min_date = '1949-10-01'
                try:
                    db_max_date = db.run('select max(date) from t_date_value where code = ?', (code,)).get_rows()[0][0]
                except:
                    db_max_date = '2999-01-01'
                if db_max_date == None:
                    db_max_date = '1949-10-01'
                    
                if int(exists_count) == len(rss) and get_min_date == db_min_date and get_max_date == db_max_date:
                    log.info('get_stock_dv_one', code, 'exists', times)
                    return
                elif get_min_date < db_min_date and int(exists_count) > 0:
                    num = db.run('delete from t_date_value where code = ?', (code,))
                    log.info('get_stock_dv_one', code, 'delete', num, times)
                elif get_min_date == db_min_date and get_max_date > db_max_date:
                    num = len(rss) - int(exists_count)
                elif int(exists_count) == 0:
                    num = len(rss)
                elif get_min_date > db_min_date:
                    raise Exception('get_min_date_error')
                
            if len(rss) == 0:
                return
            
            for rs in reversed(rss):
                date_ = rs[0]
                dwjz = rs[2]
                if dwjz == '':
                    dwjz = None
                ljjz = None
                zf = rs[4].strip('%')
                if zf == '':
                    zf = 0
                if start_date == '19491001':
                    val = val * (1 + (float(zf) / 100))
                fh = None
                if start_date == '19491001':
                    vals_all.append((code, date_, dwjz, ljjz, zf, fh, val, code, date_))
                else:
                    vals_all.append((code, date_, dwjz, ljjz, zf, fh, code, date_))
                    
            codes.append(code)
            log.info('get_stock_dv_one', code, len(vals_all), times)
               
        except Exception as _:
            if times <= 10:
                log.error('get_stock_dv_one', code, times, _)
                time.sleep(10)
                times = times + 1
                get_stock_dv_one(code, rep, start_date, times)
            else:
                log.error('get_stock_dv_one', code, times, _)
            
    get_code_sql = '''
        select code from t_main 
        where 1=1
        --and not exists(select 1 from t_date_value where t_date_value.code = t_main.code and t_date_value.date >= date('now','-1 day'))
        and (code like '12345' or code like 'zs_%')
        --and code = '000001_zs'
        --and code = '000001'
        order by code
    '''
    
    stocks = db.run(get_code_sql).get_rows()
    tp = ThreadPool(16)
    for stock in stocks:
        if len(vals_all) <= 1000000:
            code = stock[0]
            # time.sleep(0.1)
            tp.run(get_stock_dv_one, (code, rep, start_date))
        else:
            tp.wait()
            num = db.run(sql, vals_all)
            log.info('get_stock_dv', len(codes), num)
            vals_all.clear()
            codes.clear()
    tp.wait()
    num = db.run(sql, vals_all)
    log.info('get_stock_dv', len(codes), num)
    vals_all.clear()
    codes.clear()


def get_val(db):
    sql = 'update t_date_value set val = ? where code = ? and date = ?'
    vals = []

    def get_val_one(db, code):
        rss = db.run('select date,zf from t_date_value where code = ? and val is null order by date', (code,)).get_rows()
        num = 0            
        for rs in rss:
            date_ = rs[0]
            zf = rs[1]
            try:
                next_val = db.run('select val from t_date_value where code = ? and date < ? order by date desc limit 1', (code, date_)).get_rows()[0][0]
            except:
                next_val = 1
            val = float(next_val) * (1 + float(zf) / 100)
            
            if len(rss) == 1:
                vals.append((val, code, date_))
                log.info('get_val_one', code, len(vals))
            else:
                num = num + db.run(sql, (val, code, date_), wait=True)
                log.info('get_val_one', code, len(vals), num)

    tp = ThreadPool(64)
    funds = db.run("select DISTINCT code from t_date_value where val is null order by code").get_rows()
    for fund in funds:
        tp.run(get_val_one, (db, fund[0]))
    tp.wait()
    num = db.run(sql, vals)
    log.info('get_val', num)


def get_hc(db):
    codes = []
    rs_list = []        
    hc_sql = 'update t_date_value set hc = ?, hc1n = ?, hc3n = ? where code = ? and date = ?'

    def get_hc_one(db, code):
        rows = db.run('select date,val from t_date_value where hc is null and code = ?', (code,)).get_rows()
        for row in rows:
            date_now = row[0]
            date_1n_old = (datetime.datetime.strptime(date_now, '%Y-%m-%d') - relativedelta(years=1)).strftime('%Y-%m-%d')
            date_3n_old = (datetime.datetime.strptime(date_now, '%Y-%m-%d') - relativedelta(years=3)).strftime('%Y-%m-%d')
            val = row[1]
            max_val = db.run('select max(val) from t_date_value where date <= ? and code = ?', (date_now, code)).get_rows()[0][0]
            max_1n_val = db.run('select max(val) from t_date_value where date <= ? and date >= ? and code = ?', (date_now, date_1n_old, code)).get_rows()[0][0]
            max_3n_val = db.run('select max(val) from t_date_value where date <= ? and date >= ? and code = ?', (date_now, date_3n_old, code)).get_rows()[0][0]
            val = float(val)
            max_val = float(max_val)
            max_1n_val = float(max_1n_val)
            max_3n_val = float(max_3n_val)
            hc = round((max_val - val) / max_val * 100, 3)
            hc1n = round((max_1n_val - val) / max_1n_val * 100, 3)
            hc3n = round((max_3n_val - val) / max_3n_val * 100, 3)
            rs_list.append((hc, hc1n, hc3n, code, date_now))
        codes.append(code)
        log.info('get_hc_one', code, len(rows), len(rs_list))
    
    tp = ThreadPool(64)
    funds = db.run("select DISTINCT code from t_date_value where hc is null order by code").get_rows()
    for fund in funds:
        if len(rs_list) >= 1000000:
            tp.wait()
            num = db.run(hc_sql, rs_list)
            log.info('get_hc', num)
            rs_list.clear()
            codes.clear()
        else:
            tp.run(get_hc_one, (db, fund[0]))
    tp.wait()
    num = db.run(hc_sql, rs_list)
    log.info('get_hc', num)
    rs_list.clear()
    codes.clear()


def get_nh(db):
            
    codes = []
    rs_list = []        
    nh_sql = 'update t_date_value set nh1n = ?, nh3n = ?, nh5n = ? where code = ? and date = ?'

    def get_nh_one(db, code):
        rows = db.run('select date,val from t_date_value where (nh5n is null or nh5n = -1) and code = ?', (code,)).get_rows()
        for row in rows:
            date_now = row[0]
            date_future_1 = (datetime.datetime.strptime(date_now, '%Y-%m-%d') + relativedelta(years=1)).strftime('%Y-%m-%d')
            date_future_3 = (datetime.datetime.strptime(date_now, '%Y-%m-%d') + relativedelta(years=3)).strftime('%Y-%m-%d')
            date_future_5 = (datetime.datetime.strptime(date_now, '%Y-%m-%d') + relativedelta(years=5)).strftime('%Y-%m-%d')
            val = row[1]
            val = float(val)
            try:
                val_future_1 = db.run('select val from t_date_value where date >= ? and code = ? order by date limit 1', (date_future_1, code)).get_rows()[0][0]
                val_future_1 = float(val_future_1)
                hn1n = round((val_future_1 - val) / val * 100, 3)
            except:
                hn1n = -1
            try:
                val_future_3 = db.run('select val from t_date_value where date >= ? and code = ? order by date limit 1', (date_future_3, code)).get_rows()[0][0]
                val_future_3 = float(val_future_3)
                hn3n = round((val_future_3 - val) / val * 100 / 3, 3)
            except:
                hn3n = -1
            try:
                val_future_5 = db.run('select val from t_date_value where date >= ? and code = ? order by date limit 1', (date_future_5, code)).get_rows()[0][0]
                val_future_5 = float(val_future_5)
                hn5n = round((val_future_5 - val) / val * 100 / 5, 3)
            except:
                hn5n = -1
            
            rs_list.append((hn1n, hn3n, hn5n, code, date_now))
        codes.append(code)
        log.info('get_nh_one', code, len(rows), len(rs_list))
    
    tp = ThreadPool(16)
    funds = db.run("select DISTINCT code from t_date_value where nh5n is null order by code").get_rows()
    for fund in funds:
        if len(rs_list) >= 1000000:
            tp.wait()
            num = db.run(nh_sql, rs_list)
            log.info('get_nh', num)
            rs_list.clear()
            codes.clear()
        else:
            tp.run(get_nh_one, (db, fund[0]))
    tp.wait()
    num = db.run(nh_sql, rs_list)
    log.info('get_nh', num)
    rs_list.clear()
    codes.clear()
    
    
def get_by_text(db):
    sql = 'insert into t_date_value(code,date,dwjz,zf) select ?,?,?,? where not exists(select 1 from t_date_value where code = ? and date = ?)'
    params = []
    text = Tools.cat('D:/2.txt')
    code = 'NDX'
    for line in text.split('\n'):
        if '\t' in line:
            date_ = line.split('\t')[0]
            y = date_.split('/')[0]
            m = date_.split('/')[1]
            d = date_.split('/')[2]
            if len(m) == 1:
                m = '0' + m
            if len(d) == 1:
                d = '0' + d
            date_ = y + '-' + m + '-' + d
            dwjz = line.split('\t')[1].replace(',', '')
            zf = line.split('\t')[2].replace('%', '')
            params.append((code, date_, dwjz, zf, code, date_))
    num = db.run(sql, params)
    print(num)
    
    rows = db.run("select date,zf from t_date_value t where code = '" + code + "' order by date").get_rows()
    val = 1
    params.clear()
    for row in rows:
        date_ = row[0]
        val = val * (1 + float(row[1]) / 100)
        params.append((val, code, date_))
    db.run("update t_date_value set val = ? where code = ? and date = ?", params)
    

def find_name(db, name):
    sql = '''
        select replace(date,'-','/'),nh3n from t_date_value t where code = 'NDX' order by date
    '''
    rss = db.run(sql).get_rows_2()
    for rs in rss:
        print(rs)

    
if __name__ == '__main__':
    main()


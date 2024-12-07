# coding:utf-8
import sys
import gc
from tools_hjh import DBConn
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import Tools
from tools_hjh import HTTPTools
from bs4 import BeautifulSoup

stop_flag = False
page_num = None

date = Tools.locatdate()
log = Log('U:/MyFiles/MyPy/log/mmys/' + date + '.log')

host = 'https://www.mmys07.one'

chrome_path = r'U:\MyApps\CentBrowser\App\chrome.exe'
chromedriver_path = r'U:\MyApps\CentBrowser\chromedriver.exe'

try:
    sys_argv_1 = sys.argv[1]
except:
    sys_argv_1 = 'download'
try:
    sys_argv_2 = sys.argv[2]
except:
    sys_argv_2 = None
try:
    sys_argv_3 = sys.argv[3]
except:
    sys_argv_3 = 32
    

def main(): 
    db = DBConn('sqlite', db='U:/MyFiles/MyPy/data/mmys.db')
    createDatabase(db, rebuild=False)
    # get_main(db, '/category/3/8/page/PAGEIDX', 'youxi', HTTPTools)
    # get_main(db, '/category/3/10/page/PAGEIDX', 'donghua', HTTPTools)
    # get_main(db, '/category/3/4/page/PAGEIDX', 'lifan', HTTPTools)
    # get_main(db, '/category/3/5/page/PAGEIDX', 'shengyin', HTTPTools)
    get_youxi(db)
    # fenxi(db)

    
def createDatabase(db, rebuild=False):
    if rebuild:
        db.run('drop table if exists t_m')
        db.run('drop table if exists t_youxi')

    t_m = '''
        create table if not exists t_m(
            url text, 
            name text,
            uploader text,
            type text
        )
    '''
    
    t_youxi = '''
        create table if not exists t_youxi(
            url text, 
            name text,
            shetuan text,
            riqi text,
            gengxin text,
            nianling text,
            leixing text,
            xingshi text,
            yuyan text,
            biaoqian text,
            daxiao text,
            xilie text,
            zuozhe text,
            juqing text,
            chahua text,
            shengyou text,
            yinyue text,
            qita text,
            message text
        )
    '''
    
    db.run(t_m)
    db.run(t_youxi)
    db.run('create index if not exists idx_m_url on t_m(url)')
    db.run('create index if not exists idx_yx_url on t_youxi(url)')
    db.run('create index if not exists idx_yx_name on t_youxi(name)')

    
def get_main(db, firstPageUrl, type_, chrome):

    def get_main_one(idx, type_, db, times=1):
        pageurl = host + firstPageUrl.replace('PAGEIDX', str(idx))
        
        url = ''
        name = ''
        uploader = ''
        
        try:
            page = HTTPTools.get(pageurl)
            bs = BeautifulSoup(page, features="lxml")
            divs = bs.find_all('div', class_='post-info')
            insert_params = []
            for div in divs:
                try:
                    url = div.find('h2').find('a')['href'].strip()
                    if host not in url:
                        log.warning('get_main_one', url, 'host not in url')
                        return
                    url = url.replace(host, '')
                    name = div.find('h2').find('a').text.strip()
                    uploader = div.find('a', class_='post-list-meta-avatar').find('span').text.strip()
                except Exception as _:
                    print(idx, _)
                
                insert_param = (url, name, uploader, type_, url)
                insert_params.append(insert_param)
            
            if len(insert_params) == 0 and idx < page_num:
                raise Exception("insert_params size == 0")
                
            insert_sql = 'insert into t_m select ?,?,?,? where not exists(select 1 from t_m t where t.url = ?)'
            insert_num = db.run(insert_sql, insert_params, wait=True)
            
            if insert_num == 0:
                global stop_flag
                stop_flag = True
            
            log.info('get_main_one', pageurl, insert_num, len(insert_params), tp.get_running_num(), times)
        except Exception as _:
            if times <= 10:
                times = times + 1 
                get_main_one(idx, type_, db, times)
            else:
                log.error('get_main_one', pageurl, times, _)
    
    tp = ThreadPool(sys_argv_3)
    global page_num
    global stop_flag
    stop_flag = False
    if page_num is None:
        pageurl = host + firstPageUrl.replace('PAGEIDX', '1')
        page = chrome.get(pageurl)
        bs = BeautifulSoup(page, features="lxml")
        page_num = int(bs.find('div', class_='b2-pagenav post-nav box mg-t b2-radius')['data-max'])
    for idx in range(1, page_num + 1):
    # for idx in range(1394, 1401 + 1):
        if stop_flag:
            break
        else:
            tp.run(get_main_one, (idx, type_, db))
    tp.wait()

    
def get_youxi(db):
    get_url_sql = '''
        select url from t_m 
        where not exists(select 1 from t_youxi where t_m.url = t_youxi.url) 
        --and exists(select 1 from t_page where t_page.url = t_m.url)
        and (
            name like '[同人游戏]%'
            or name like '[手机游戏]%'
            or name like '[Gal]%'
        ) order by cast(replace(url,'https://www.mmys04.one/archives/','') as int) desc
    '''
    # get_page_sql = "select page from t_page where url = ?"
    insert_sql = "insert into t_youxi select ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? where not exists(select 1 from t_youxi where url = ?)"
    params = []
    
    def get_youxi_one(url, rep):
        
        def get_td(tr):
            td = ''
            if '<span>' in str(tr):
                spans = tr.find('td').find_all('span')
                for span in spans:
                    td = td + '丶' + span.text
            else:
                td = tr.find('td').text
            td = Tools.merge_spaces(td)
            td = td.replace('\n', ' ')
            td = td.replace('（', '(')
            td = td.replace('）', ')')
            td = td.strip('丶')
            td = td.strip()
            return td
        
        name = ''
        shetuan = ''
        riqi = ''
        gengxin = ''
        nianling = ''
        leixing = ''
        xingshi = ''
        yuyan = ''
        biaoqian = ''
        daxiao = ''
        xilie = ''
        zuozhe = ''
        juqing = ''
        chahua = ''
        shengyou = ''
        yinyue = ''
        qita = ''
        message = ''
                
        # page = db.run(get_page_sql, (url,)).get_rows()[0][0]
        page = rep.get(host + url)
        
        if '<title>WordPress &rsaquo; 错误</title>' in str(page):
            # db.run("delete from t_page where url = ?", (url,))
            log.error('get_youxi_one', url, 'page error')
            return
        
        bs = BeautifulSoup(page, features="lxml")
        try:
            if 'entry-header' in str(page):
                name = bs.find('header', class_='entry-header').find('h1').text.strip()
            else:
                name = bs.find('title').text.replace(' - 萌萌御所', '').strip()
        except:
            log.error('get_youxi_one', url, 'name is None')
            return
                
        try:
            message = bs.find('div', class_='content-excerpt').text.strip()
        except:
            pass
        
        if 'wp-block-table' not in str(page):
            log.error('get_youxi_one', url, 'table is None', name.split(']')[0] + ']')
            return
        
        table = bs.find('figure', class_='wp-block-table')
        tr_list = table.find_all('tr')
        for tr in tr_list:
            if '社团' in str(tr) or '商标' in str(tr):
                shetuan = get_td(tr)
            elif '日期' in str(tr):
                riqi = get_td(tr)
                riqi = riqi.split('日')[0].replace('年', '').replace('月', '')
            elif '更新' in str(tr):
                gengxin = get_td(tr)
                gengxin = gengxin.split('日')[0].replace('年', '').replace('月', '')
            elif '年龄' in str(tr):
                nianling = get_td(tr)
            elif '类型' in str(tr):
                leixing = get_td(tr)
            elif '形式' in str(tr):
                xingshi = get_td(tr)
            elif '语言' in str(tr):
                yuyan = get_td(tr)
            elif '标签' in str(tr):
                biaoqian = get_td(tr)
            elif '大小' in str(tr):
                daxiao = get_td(tr)
            elif '系列' in str(tr):
                xilie = get_td(tr)
            elif '作者' in str(tr):
                zuozhe = get_td(tr)
            elif '剧情' in str(tr):
                juqing = get_td(tr)
            elif '插画' in str(tr):
                chahua = get_td(tr)
            elif '声优' in str(tr):
                shengyou = get_td(tr)
            elif '音乐' in str(tr):
                yinyue = get_td(tr)
            elif '其他' in str(tr):
                qita = get_td(tr)
                
        if len(shetuan) > 0: 
            param = (url, name, shetuan, riqi, gengxin, nianling, leixing, xingshi, yuyan, biaoqian, daxiao, xilie, zuozhe, juqing, chahua, shengyou, yinyue, qita, message, url)        
            params.append(param)
            log.info('get_youxi_one', url, len(params), name.split(']')[0] + ']')
        else:
            log.warning('get_youxi_one', url, 'shetuan is null', name.split(']')[0] + ']')

    urls = db.run(get_url_sql).get_rows()
    tp = ThreadPool(32)
    for url_ in urls:
        if len(params) <= 200:
            url = url_[0]
            tp.run(get_youxi_one, (url, HTTPTools))
        else:
            tp.wait()
            num = db.run(insert_sql, params)
            log.info('get_youxi', 'insert', num)
            params.clear()
            gc.collect()
    tp.wait()
    num = db.run(insert_sql, params)
    log.info('get_youxi', 'insert', num)

    
def fenxi(db):
    get_url_sql = "select url from t_m where name like '[同人动画]%'"
    get_page_sql = "select page from t_page where url = ?"
    
    th_map = {}
    th_list = []
    
    def get_one(db, url, i):
        page = db.run(get_page_sql, (url,)).get_rows()[0][0]
        bs = BeautifulSoup(page, features="lxml")
        try:
            table = bs.find('figure', class_='wp-block-table')
            trs = table.find_all('tr')
        except Exception as _:
            log.error('fenxi', i, url, _)
            return
        
        for tr in trs:
            try:
                th = tr.find('th').text.strip()
                if th not in th_list:
                    th_list.append(th)
                    th_map[th] = 1
                else:
                    th_map[th] = th_map[th] + 1
            except Exception as _:
                pass
            
        log.info('fenxi', i, th_map)
    
    urls = db.run(get_url_sql).get_rows()
    tp = ThreadPool(64)
    i = 1
    for url_ in urls:
        url = url_[0]
        tp.run(get_one, (db, url, i), time_out=10)
        i = i + 1
    tp.wait()


def sql(db):
    sql = '''
        
    '''
    rss = db.run(sql).get_rows()
    for rs in rss:
        print(rs)

    
if __name__ == '__main__':
    main()


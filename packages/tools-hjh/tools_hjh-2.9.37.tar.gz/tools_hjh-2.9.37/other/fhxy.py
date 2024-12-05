# coding:utf-8
import sys
from tools_hjh import DBConn
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import Tools
from bs4 import BeautifulSoup
from tools_hjh.HTTPTools import HTTPTools

stop_flag = False
date = Tools.locatdate()
log = Log('U:/MyFiles/MyPy/log/fhxy/' + date + '.log')

host = 'https://fhxy-a.top'

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
    db = DBConn('sqlite', db='U:/MyFiles/MyPy/data/fhxy-a.db')
    createDatabase(db, rebuild=False)
    get_main(db, '/fhxyzy/page/PAGEIDX')
    get_main(db, '/ssyx/page/PAGEIDX/')
    get_main(db, '/zytg1/gal/page/PAGEIDX')
    get_e(db, HTTPTools)

    
def createDatabase(db, rebuild=False):
    if rebuild:
        db.run('drop table if exists t_m')
        db.run('drop table if exists t_e')

    t_m = '''
        create table if not exists t_m(
            url text, 
            name_ text,
            date text,
            views real,
            likes real
        )
    '''
    
    t_e = '''
        create table if not exists t_e(
            url text, 
            name_ text, 
            content text,
            tags text
        )
    '''
    db.run(t_m)
    db.run(t_e)
    db.run('create index if not exists idx_m_url on t_m(url)')
    db.run('create index if not exists idx_e_url on t_e(url)')

    
def get_main(db, firstPageUrl):

    def get_mian_one(idx, db, times=1):
        pageurl = host + firstPageUrl.replace('PAGEIDX', str(idx))
        
        url = ''
        name_ = ''
        date = ''
        views = ''
        likes = ''
        
        try:
            page = HTTPTools.get(pageurl, timeout=10)
            bs = BeautifulSoup(page, features="lxml")
            lis = bs.find_all('li', class_='post-list-item')
            insert_params = []
            update_params = []
            for li in lis:
                try:
                    url = li.find('div', class_='post-info').find('h2').find('a')['href'].strip()
                    if url.startswith('https://api.fh-xy.net/'):
                        url = url.replace('https://api.fh-xy.net/', 'https://fh-xy.net/')
                    name_ = li.find('div', class_='post-info').find('h2').find('a').text.strip()
                    date_ = li.find('time', class_='b2timeago')['datetime']
                    views = li.find('li', class_='post-list-meta-views').text.strip()
                    if 'k' in views:
                        views = float(views.rstrip('k')) * 1000
                    likes = li.find('li', class_='post-list-meta-like').text.strip()
                except Exception as _:
                    print(_)
                
                insert_param = (url, name_, date_, views, likes, url)
                insert_params.append(insert_param)
                
                update_param = (name_, date_, views, likes, url)
                update_params.append(update_param)
            
            insert_sql = 'insert into t_m select ?,?,?,?,? where not exists(select 1 from t_m t where t.url = ?)'
            insert_num = db.run(insert_sql, insert_params, wait=True)
            
            if insert_num == 0:
                global stop_flag
                stop_flag = True
            
            update_sql = 'update t_m set name_ = ?, date = ?, views = ?, likes = ? where url = ?'
            db.run(update_sql, update_params, wait=True)
            log.info('get_mian_one', pageurl, insert_num, len(insert_params), times)
        except Exception as _:
            if times <= 3:
                times = times + 1 
                get_mian_one(idx, db, times)
            else:
                log.error('get_mian_one', pageurl, 'error', _)
    
    tp = ThreadPool(sys_argv_3)
    global page_num
    global stop_flag
    stop_flag = False
    page_num = 99999
    for idx in range(1, page_num + 1):
        if stop_flag:
            break
        else:
            tp.run(get_mian_one, (idx, db))
    tp.wait()

    
def get_e(db, chrome, tpNum=sys_argv_3):
    params = []

    def get_e_one(url, name_, times=1):
        try:
            page = chrome.get(url)
            bs = BeautifulSoup(page, features="lxml")
            content = Tools.merge_spaces(bs.find('div', class_='entry-content').text.strip()).strip()
            tags = ''
            tag_spans = bs.find_all('span', class_='tag-text')
            for span in tag_spans:
                tags = tags + span.text + '、'
            tags = tags.strip('、')
                
            param = (url, name_, content, tags, url)
            params.append(param)
            
            log.info('get_e_one', url, len(params), tp.get_running_num(), times)
        except Exception as _:
            if times <= 5:
                times = times + 1 
                get_e_one(url, name_, times)
            else:
                log.error('get_e_one', url, 'error', _)
    
    tp = ThreadPool(tpNum)
    urls = db.run('select url,name_ from t_m where not exists(select 1 from t_e where t_e.url = t_m.url and t_e.name_ = t_m.name_) order by date desc').get_rows()
    sql = 'insert into t_e select ?,?,?,? where not exists(select 1 from t_e t where t.url = ?)'
    for url in urls:
        tp.run(get_e_one, (url[0], url[1],), time_out=10)
        if len(params) > 500:
            tp.wait()
            num = db.run(sql, params)
            log.info('get_e', num)
            params.clear()
    tp.wait()
    num = db.run(sql, params)
    log.info('get_e', num)


def sql(db):
    sql = '''
        select t.url,t.date,t.views
        from t_m t left join t_e e
        on t.url = e.url 
        where 1=1
        and e.content not like '%GPT%' and e.content not like '%AI%' and e.content not like '%机翻%' and e.content not like '%智能翻译%' and e.content not like '%云汉%' and e.content not like '%云翻%' and e.content not like '%生肉%' and e.content not like '%智能汉化%'
        and t.name_ not like '%GPT%' and t.name_ not like '%AI%' and t.name_ not like '%机翻%' and t.name_ not like '%智能翻译%' and t.name_ not like '%云汉%' and t.name_ not like '%云翻%' and t.name_ not like '%生肉%' and t.name_ not like '%智能汉化%'
        --and e.tags not like '%ADV%'
        --and e.content not like '%欧美%'
        and (
            e.tags like '%战斗H%' or e.tags like '%战斗h%' or e.tags like '%戰鬥H%' or e.tags like '%戰鬥h%' or e.tags like '%战斗エロ%' or e.tags like '%戰鬥エロ%'
            or e.content like '%战斗H%' or e.content like '%战斗h%' or e.content like '%戰鬥H%' or e.content like '%戰鬥h%' or e.content like '%战斗エロ%' or e.content like '%戰鬥エロ%'
        ) order by t.views desc;
    '''
    rss = db.run(sql).get_rows()
    for rs in rss:
        print(rs)

    
if __name__ == '__main__':
    main()


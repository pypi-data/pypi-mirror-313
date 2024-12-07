# coding:utf-8
import sys
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import Tools
from bs4 import BeautifulSoup
from tools_hjh import HTTPTools
import os
from tools_hjh import ChromePool

date = Tools.locatdate()
log = Log('U:/MyFiles/MyPy/log/sissy_game/' + date + '.log')

host = 'https://sissy.game'

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
    sys_argv_3 = 2
    

def main():
    req = ChromePool(sys_argv_3, chrome_path, chromedriver_path, is_display_picture=False, is_hidden=False)
    download('/page/PAGEIDX/', req)

    
def download(first_page_url, req):

    def download_one_page(idx, req):
        pageurl = host + first_page_url.replace('PAGEIDX', str(idx))
        page = req.get(pageurl)
        bs = BeautifulSoup(page, features="lxml")
        divs = bs.find_all('div', class_='single-post panel box-shadow-wrap-normal')
        for div in divs:
            name_ = div.find('h2', class_='m-t-none text-ellipsis index-post-title text-title').find('a').text
            date_ = div.find('div', class_='text-muted post-item-foot-icon text-ellipsis list-inline').find_all('li')[1].text
            date_ = date_.replace(' 年 ', '').replace(' 月 ', '').replace(' 日', '')
            try:
                pic_url = div.find('img', class_='img-full lazy')['src']
            except:
                pic_url = ''
            pic_name = date_ + '_' + name_ + '.jpg'
            pic_name = Tools.merge_spaces(pic_name)
            pic_name = pic_name.replace('/', ' ').replace('\\', ' ').replace(':', '：').replace('*', '·').replace('?', '？').replace('"', '\'').replace('<', '[').replace('>', ']').replace('|', ' ') 
            pic_name = pic_name.replace('＃', '#')
            pic_name = pic_name.replace('] ', ']').replace(' [', '[')
            pic_name = pic_name.replace('～ ', '～').replace(' ～', '～')
            pic_name = pic_name.replace('# ', '#').replace(' #', '#')
            pic_name = pic_name.replace('。 ', '。').replace(' 。', '。')
            pic_name = pic_name.replace('( ', '(').replace(' (', '(')
            pic_name = pic_name.replace('！ ', '！').replace(' ！', '！')
            pic_name = 'U:/MyFiles/MyPy/download/sissy_game/' + pic_name
            if 'uploads' in pic_url:
                try:
                    pic_size = HTTPTools.get_size(pic_url)
                    if not os.path.exists(pic_name):
                        HTTPTools.download(pic_url, pic_name)
                        log.info('download', idx, 'download', pic_name, pic_url)
                    elif os.path.exists(pic_name) and pic_size != os.path.getsize(pic_name):
                        HTTPTools.download(pic_url, pic_name, True)
                        log.info('download', idx, 'replace', pic_name, pic_url)
                    else:
                        log.info('download', idx, 'exists', pic_name, pic_url)
                except Exception as _:
                    log.error('download', idx, 'error', pic_name, pic_url, str(_))
        
    page = req.get(host)
    bs = BeautifulSoup(page, features="lxml")
    max_page = bs.find('ol', class_='page-navigator').find_all('li')[-2].text
    tp = ThreadPool(sys_argv_3)
    for idx in range(1, int(max_page) + 1):
        tp.run(download_one_page, (idx, req))
    tp.wait()
    
    
if __name__ == '__main__':
    main()


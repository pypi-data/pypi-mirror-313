# coding:utf-8
from tools_hjh.HTTPRequest import HTTPRequest
from math import ceil
from tools_hjh.Tools import mkdir, rm
from tools_hjh.ThreadPool import ThreadPool
import os

    
def main():
    headers = {
        'cookie':'cf_clearance=ZyXhlDX.MEsAT8edtS9fzDZpnwDpDBgN8jzhq4uzQHY-1714422048-1.0.1.1-gMVkjl718OqgU4CMIWop9tl4WCWpgYdT3aizn70Z0z905jYV.zSYdAwMg1OScze8BsMUQtkcdNJ3GtfT0m3ZMA; csrftoken=ZgclpVKZTiRpWHRhF0OOeTdSlU5odAJsyWq2a37iNNizZykV4w2XAhL9VOWW7hIT',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie':'',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://avbebe.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    # size = HTTPTools.get_size(url='https://v.avgigi.com/acg/watch/198910.mp4', headers=headers)
    # size = HTTPTools.download(url='https://www.bixiashuku.com/modules/article/txtarticle.php?id=87850', filepath='D:/1.txt', headers=headers, retry_until_success=True)
    size = HTTPTools.get(url='https://nhentai.net/')
    print(size)


class HTTPTools():
    
    @staticmethod
    def get_page(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, retry_until_success=False):
        text = ''
        if retry_until_success:
            try:
                req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
                text = req.get_text()
                req.close()
            except:
                HTTPTools.get_page(url, headers, data, proxies, encoding, timeout, stream, allow_redirects, verify, retry_until_success)
        else: 
            req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
            text = req.get_text()
            req.close()
        return text

    @staticmethod
    def get_content(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, retry_until_success=False):
        content = ''
        if retry_until_success:
            try:
                req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
                content = req.get_content()
                req.close()
            except:
                HTTPTools.get_content(url, headers, data, proxies, encoding, timeout, stream, allow_redirects, verify, retry_until_success)
        else: 
            req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
            content = req.get_content()
            req.close()
        return content
    
    @staticmethod
    def get(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, retry_until_success=False):
        return HTTPTools.get_page(url, headers, data, proxies, encoding, timeout, stream, allow_redirects, verify, retry_until_success)
    
    @staticmethod
    def get_size(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, retry_until_success=False):
        text = 0
        if retry_until_success:
            try:
                req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
                text = req.get_size()
                req.close()
            except:
                HTTPTools.get_page(url, headers, data, proxies, encoding, timeout, stream, allow_redirects, verify, retry_until_success)
        else: 
            req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
            text = req.get_size()
            req.close()
        return text
    
    @staticmethod
    def get_status_code(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, retry_until_success=False):
        text = ''
        if retry_until_success:
            try:
                req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
                text = req.get_status_code()
                req.close()
            except:
                HTTPTools.get_page(url, headers, data, proxies, encoding, timeout, stream, allow_redirects, verify, retry_until_success)
        else: 
            req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
            text = req.get_status_code()
            req.close()
        return text

    @staticmethod
    def download(url, filepath, replace=False, partsize=1024 * 1024, threadnum=1, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, retry_until_success=False):
        req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
        if threadnum == 1:
            if not retry_until_success:
                return req.download(filepath=filepath, replace=replace)
            else:
                return req.download_until_success(filepath=filepath, replace=replace)
        else:
            # 有问题，还没看出问题出在哪里QAQ
            tp = ThreadPool(threadnum)
            filesize = HTTPTools.get_size(url, headers, data, proxies, encoding, timeout, stream, allow_redirects, verify, retry_until_success=False)
            partnum = ceil(filesize / partsize)
            filepath = filepath.replace('\\', '/')
            path = filepath.rsplit('/', 1)[0] + '/'
            name = filepath.split('/')[-1]
            tmp_path = path + name + '_tmp/'
            if replace:
                rm(filepath)
            mkdir(tmp_path)
            downloaded_files = []
            for idx in range(partnum):
                begin = idx * partsize + 1
                if idx == partnum - 1:
                    end = filesize
                else:
                    end = begin + partsize - 1
                new_filepath = tmp_path + str(idx)
                downloaded_files.append(new_filepath)
                new_headers = headers.copy()
                new_headers['Range'] = f'bytes={begin}-{end}'
                if retry_until_success:
                    tp.run(HTTPTools.download, (url, new_filepath, True, 1024 * 1024, 1, new_headers, data, proxies, encoding, timeout, stream, allow_redirects, verify))
                else:
                    tp.run(HTTPTools.download_until_success, (url, new_filepath, True, 1024 * 1024, 1, new_headers, data, proxies, encoding, timeout, stream, allow_redirects, verify))
            tp.wait()
            
            size = 0
            filepath = open(filepath, 'wb')
            for downloaded_file in downloaded_files:
                if os.path.exists(downloaded_file):
                    f = open(downloaded_file, "rb")
                    tsfileRead = f.read()
                size = size + filepath.write(tsfileRead)
                f.close()
            filepath.close()
            rm(tmp_path)
            return size
        
    @staticmethod
    def N_m3u8DL_CLI(url, filepath, filename, theadnum=32, exe_path='N_m3u8DL-CLI_v3.0.2.exe', headers=''):
        cmd = exe_path + ' --workDir ' + filepath + ' --saveName "' + filename + '" --maxThreads ' + str(theadnum) + ' --enableDelAfterDone ' + '--headers "' + headers + '" ' + url
        os.popen('chcp 65001')
        os.system(cmd)

    
if __name__ == '__main__':
    main()

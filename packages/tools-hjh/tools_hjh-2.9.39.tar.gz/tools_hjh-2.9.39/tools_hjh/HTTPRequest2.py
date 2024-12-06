# coding:utf-8
import time
from tools_hjh.ThreadPool import ThreadPool
import requests
import os
from tools_hjh import Tools


def main():
    pass


class HTTPRequest2():
    """ 用户向网站提出请求的类 """

    def __init__(self, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False):
        self.headers = headers
        self.data = data
        self.proxies = proxies
        self.encoding = encoding
        self.timeout = timeout
        self.stream = stream
        self.allow_redirects = allow_redirects
        self.verify = verify
        self.response = None
        self.head = None
        self.cookies = None
        self.status = 0  # 未被占用
        
    def set_cookies(self, cookies):
        self.cookies = {}
        for cookie in cookies:
            self.cookies[cookie['name']] = cookie['value']
        
    def close(self):
        self.chrome.quit()
        
    def get(self, url):
        self.status = 1  # 被占用
        if self.data is None:
            self.response = requests.get(url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, timeout=self.timeout, stream=self.stream, allow_redirects=self.allow_redirects, verify=self.verify)
        else:
            self.response = requests.post(url, headers=self.headers, cookies=self.cookies, data=self.data, proxies=self.proxies, timeout=self.timeout, stream=self.stream, allow_redirects=self.allow_redirects, verify=self.verify)
        self.response.encoding = self.encoding
        self.status = 0
        return self.response.content
                
    def get_status(self):
        return self.status


class HTTPRequestPool():

    def __init__(self, maxSize, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False, cache=False):
        self.cache = cache
        self.maxSize = maxSize
        self.pool = []
        for _ in range(0, maxSize):
            self.pool.append(HTTPRequest2(headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify))
        self.openSize = 0
        
    def set_cookies(self, cookies):

        def set_one(http_request, cookies):
            http_request.set_cookies(cookies)

        tp = ThreadPool(self.maxSize)
        for http_request in self.pool:
            tp.run(set_one, (http_request, cookies))
        tp.wait()
        
    def get(self, url):
        while self.openSize == self.maxSize:
            time.sleep(0.2)
        for http_request in self.pool:
            if http_request.get_status() == 0:
                self.openSize = self.openSize + 1
                if self.cache:
                    url_split = url.split('/')
                    host = url_split[0] + '//' + url_split[2] + '/'
                    path_ = 'tmp/' + url.replace(host, '').rstrip('/')
                    if os.path.exists(path_):
                        text = Tools.cat(path_)
                    else:
                        text = http_request.get(url)
                        Tools.echo(text, path_)
                else:
                    text = http_request.get(url)
                self.openSize = self.openSize - 1
                return text
        time.sleep(0.2)
        return self.get(url)
    
    def close(self):
        while self.openSize > 0:
            time.sleep(0.2)
        for c in self.pool:
            c.close()


if __name__ == '__main__':
    main()

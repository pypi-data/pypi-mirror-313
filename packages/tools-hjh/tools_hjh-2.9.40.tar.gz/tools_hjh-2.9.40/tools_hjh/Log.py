# coding:utf-8
from tools_hjh.Tools import locattime, echo


def main():
    log = Log('test.log')
    log.info('a', '', 1)


class Log():
    """ 简单的日志类 """

    def __init__(self, filepath):
        self.filepath = filepath

    def info(self, *text):
        mess = ''
        for one in text:
            if one != '' and one is not None:
                mess = mess + str(one) + ', '
        mess = mess[:-2]
        print(str(locattime()) + ' ' + 'info : ' + mess)
        echo(str(locattime()) + ' ' + 'info : ' + mess, self.filepath)
        
    def warning(self, *text):
        mess = ''
        for one in text:
            if one != '' and one is not None:
                mess = mess + str(one) + ', '
        mess = mess[:-2]
        print(str(locattime()) + ' ' + 'warning : ' + mess)
        echo(str(locattime()) + ' ' + 'warning : ' + mess, self.filepath)
        
    def error(self, *text):
        mess = ''
        for one in text:
            if one != '' and one is not None:
                mess = mess + str(one) + ', '
        mess = mess[:-2]
        print(str(locattime()) + ' ' + 'error : ' + mess)
        echo(str(locattime()) + ' ' + 'error : ' + mess, self.filepath)
        
    def out(self, *text):
        mess = ''
        for one in text:
            if one != '' and one is not None:
                mess = mess + str(one) + ', '
        mess = mess[:-2]
        print(mess)
        echo(mess, self.filepath)

        
if __name__ == '__main__': 
    main()

# coding:utf-8
import paramiko
import os
import time
from tools_hjh.Tools import remove_leading_space


class SSHConn:
    """ 维护一个基于ssh协议的linux连接 """

    def __init__(self, host, port, username, password, wait_time=1):
        """ 给入连接信息初始化该连接，wait_time是连上后等待时间（等待系统初始化一些可能存在的东西），单位秒 """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.wait_time = wait_time
        
        self.transport = paramiko.Transport((host, int(port)))
        self.transport.connect(username=username, password=password)
        
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, username, password, timeout=3, allow_agent=False, look_for_keys=False)
        time.sleep(wait_time)
        self.shell = self.client.invoke_shell()

    def exec_command(self, cmd):
        """ 执行单一命令，返回结果 """
        cmd = remove_leading_space(cmd)
        stdout = self.client.exec_command(cmd)[1]
        return stdout.read().decode("UTF-8", errors='ignore').strip()

    def exec_script(self, script):
        """ 执行shell脚本，返回交互式shell内容 """
        mess = ''
        shell = self.client.invoke_shell()
        script = remove_leading_space(script)
        shell.send(script + '\n')
        shell.send('exit\n')
        while not shell.exit_status_ready():
            mess = mess + shell.recv(1024).decode('UTF-8', errors='ignore')
        shell.close()
        return mess
        
    def _download(self, src, dst):
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        sftp = paramiko.SFTPClient.from_transport(self.transport, 1024)
        filetype = self.exec_command("ls -ld " + src)[0]
        if filetype == '-':
            sftp.get(src, dst)
        elif filetype == 'd':
            for file in sftp.listdir(src):
                self._download(src + '/' + file, dst + '/' + file)
        sftp.close()

    def download(self, src, dst):
        """ 下载文件到本地，dst只能是一个目录，表示下载到该目录下 """
        if not os.path.exists(dst):
            os.makedirs(dst)
        sftp = paramiko.SFTPClient.from_transport(self.transport, 1024)
        filetype = self.exec_command("ls -ld " + src)[0]
        if filetype == '-':
            sftp.get(src, dst + '/' + src.split('/')[-1])
        elif filetype == 'd':
            self._download(src, dst)
        sftp.close()

    def close(self):
        try:
            self.shell.close()
        except:
            pass
        try:
            self.client.close()
        except:
            pass
        
    def __del__(self):
        self.close()
    
    def refresh(self):
        self.close()
        return SSHConn(self.host, self.port, self.username, self.password)

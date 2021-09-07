# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:31:52 2021

@author: huawei
"""

import paramiko
import stat
import datetime
import os
import time
from ftplib import FTP

parameters = {'aip':'192.168.6.99', 'aport':22, 
              'adir':'/weishuyuan/DTU30-A7/bin/', 'afile':'dtu30',
              'bdir':'/usr/local/dtu30', 'bfile':'dtu30'
              }


def ftp_connect():
     ftp = FTP()
     ftp.connect('192.168.151.126', 21)
     ftp.login('root', 'root')
     print(ftp.getwelcome())
     ftp.cwd(parameters['bdir'])
     return ftp;


def ssh_connect():
    scp = paramiko.SSHClient()
    scp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    scp = paramiko.Transport((parameters['aip'], parameters['aport']))
    print("Connecting To SFTP " + parameters['aip'])
    scp.connect(username = 'root', password = 'Zhwld@88888')
    scp.set_keepalive(3)
    sftp = paramiko.SFTPClient.from_transport(scp)
    return sftp


def check(sftp):
    for fd in sftp.listdir_attr(parameters['adir']):
        if not stat.S_ISDIR(fd.st_mode):
            if fd.filename == parameters['afile']:
                return True
    return False


def update(sftp, ftp):
    if check(sftp):
        n = datetime.datetime.now()
        
        print('Update ' + n.strftime('%Y-%m-%d %H:%M:%S.'))
    
        t = parameters['afile'] + n.strftime('%Y%m%d%H%M%S')
        a = parameters['adir'] + parameters['afile']
        b = parameters['bfile']
        
        sftp.get(a, t)
        with open(t, 'rb') as fp:
            ftp.storbinary(f'STOR {b}', fp, 1024)
        
        os.remove(t)
        sftp.remove(a)


if __name__=='__main__':
    sftp = ssh_connect()
    ftp = ftp_connect()
    while True:
        update(sftp, ftp)
        time.sleep(3)

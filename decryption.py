# -*- coding: utf-8 -*-

import os
import paramiko

parameters = {'ip':'192.168.6.99'}

def progress(a, b):
    if a == b:
        print('Finish.')

if __name__ == '__main__':
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(parameters['ip'], username = 'root', password = 'Zhwld@88888')
    sftp = client.open_sftp()

    for file_name in os.listdir('.'):
        file_names = os.path.splitext(file_name)
        if file_names[1] != '.py':
            sftp.put(file_name, f'/weishuyuan/decryption/{file_name}', progress)

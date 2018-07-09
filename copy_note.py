import os
import shutil
import time


rootdir = 'F:\\WSHY\\札记'

desdir = '札记'

if __name__ == '__main__':
    print('---==== 札记自动备份工具 ====---\n')
    
    desdir = desdir + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    
    for file_name in os.listdir(rootdir):
        sub_file_name = os.path.join(rootdir, file_name)
        if os.path.isdir(sub_file_name):
            if len(os.listdir(sub_file_name)) > 0:
                shutil.copytree(sub_file_name, os.path.join(desdir, file_name))
                shutil.rmtree(sub_file_name)
            else:
                os.rmdir(sub_file_name)
    
    

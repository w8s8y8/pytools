import codecs
import time
import os
import shutil
import re

version = '1.0.1'
name = '采集服务器测试工具'

release_dir = '../'
qt_path = 'C:/Qt/Qt5.6.3/5.6.3/mingw49_32/bin;C:/Qt/Qt5.6.3/Tools/mingw492_32/bin;'

def find_pro_file():
    for file_name in os.listdir('.'):
        file_names = os.path.splitext(file_name)
        if file_names[1] == '.pro':
            return file_name;
        
def findpro(lines, name):
    for line in lines:
        if re.search(name, line):
            return line.replace(name, '').replace('\n', '').replace('\r', '')

pro_file = find_pro_file()

lines = open(pro_file, 'r').readlines()
target = findpro(lines, 'TARGET = ')
rc_file = findpro(lines, 'RC_FILE = ')

print('Read git information.')
master = codecs.open('.git/logs/refs/heads/master', 'r', 'utf-8')
master = master.readlines()[-1]
master = master.split(' ')
v = master[1][0:6]
t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(int(master[4])))
v = t + v
print(v)

lines = open('git.rc', 'r').readlines()
fp = open(rc_file, 'w')
for s in lines:
    fp.write(s.replace('$V', v))
fp.close()

print('Building.')
os.environ['PATH'] = qt_path + os.environ['PATH']
if not os.path.exists('build'):
    os.mkdir('build')
os.chdir('build')
for line in os.popen('qmake.exe ../' + pro_file).readlines():
    print(line, end = '')
for line in os.popen('mingw32-make.exe -j3 release').readlines():
    print(line, end = '')

release_file = release_dir + '/' + name + '.exe'
build_file = 'release/' + target + '.exe'
if os.path.isfile(build_file):
    if os.path.isfile(release_file):
        os.remove(release_file)
    shutil.move(build_file, release_file)
    os.chdir('..')
    shutil.rmtree('build')
else:
    time.sleep(10)

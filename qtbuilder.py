import time
import os
import shutil
import re

version = '1.0.0'
name = 'BIN合并工具'

qt_path = 'D:/0/Qt/Qt5.15.2/5.15.2/mingw81_64/bin;D:/0/Qt/Qt5.15.2/Tools/mingw810_64/bin;'

def qt_deploy(dir_name):
    os.chdir(dir_name)
    with os.popen('windeployqt.exe --no-translations --no-system-d3d-compiler --no-angle --no-opengl-sw .'):
        pass
    for name in ['bearer', 'iconengines', 'imageformats', 'Qt5Svg.dll']:
        if os.path.isdir(name):
            shutil.rmtree(name)
        elif os.path.isfile(name):
            os.remove(name)
    os.chdir('..')


def find_pro_file():
    print('查找文件夹内的Qt工程文件...')
    for file_name in os.listdir('.'):
        file_names = os.path.splitext(file_name)
        if file_names[1] == '.pro':
            print(f'\t找到文件{file_name}.\n')
            return file_name


def find_line(lines, name):
    for line in lines:
        if re.search(name, line):
            return line.replace(name, '').replace('\n', '').replace('\r', '')


def find_target(pro_file):
    print(f'查找{pro_file}文件内的编译目标程序名...')
    with open(pro_file, 'r') as fp:
        lines = fp.readlines()
        target = find_line(lines, 'TARGET = ')
        print(f'\t找到编译目标程序名{target}.\n')
        return target


def find_rc_file(pro_file):
    print(f'查找{pro_file}文件内的RC文件名...')
    with open(pro_file, 'r') as fp:
        lines = fp.readlines()
        rc_file = find_line(lines, 'RC_FILE = ')
        print(f'\t找到RC文件名{rc_file}.\n')
        return rc_file


def git_version():
    print('读取git版本...')
    with os.popen('git log -1 --format="%h %ct"') as fp:
        v, t = fp.readlines()[0].rstrip().split(' ')
        v = v.upper()
        t1 = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime(int(t)))
        t2 = time.strftime("%Y%m%d", time.localtime(int(t)))
        print(f'\t{v} {t1} {t2}\n')
        return [v, t1, t2]


def generate_h_file(version):
    print('生成version.h.\n')
    with open('version.h', 'w') as fp:
        fp.write('#ifndef VERSION_H\n')
        fp.write('#define VERSION_H\n\n')
        fp.write('#define VERSION \"%s\"\n\n' % version)
        fp.write('#endif // VERSION_H\n')


def write_rc_file(rc_file, v, t):
    print('更改RC文件.\n')
    with open(rc_file, 'r') as r:
        lines = r.readlines()
        with open(rc_file, 'w') as fp:
            for line in lines:
                if 'ProductVersion' in line:
                    s = line.split(',')[0]
                    line = f'{s}, "{t} {v}"\n'
                fp.write(line)


def write_version(rc_file):
    v, t1, t2 = git_version()
    generate_h_file(f'{v} {t1}')
    write_rc_file(rc_file, v, t1)
    return t2


def build(pro_file, release_file, target):
    print(f'编译工程{pro_file}.\n')
    os.environ['PATH'] = qt_path + os.environ['PATH']
    if not os.path.exists('build'):
        os.mkdir('build')
    os.chdir('build')
    with os.popen(f'qmake.exe ../{pro_file}') as fp:
        for line in fp.readlines():
            print(line, end = '')
    with os.popen('mingw32-make.exe -j4 release') as fp:
        for line in fp.readlines():
            print(line, end = '')
        print('\n')
    os.chdir('..')
    build_file = f'build/release/{target}.exe'
    if os.path.isfile(build_file):
        print(f'生成文件{build_file}.\n')
        if os.path.isfile(release_file):
            os.remove(release_file)
        shutil.move(build_file, release_file)
    shutil.rmtree('build')


if __name__ == '__main__':
    pro_file = find_pro_file()
    target = find_target(pro_file)
    rc_file = find_rc_file(pro_file)
    release_dir = name + write_version(rc_file)

    print(f'创建文件夹[{release_dir}].\n')
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    release_file = f'{release_dir}/{name}.exe'
    build(pro_file, release_file, target)

    print('部署程序.')

    if os.path.isfile(release_file):
        print('\t部署Qt.')
        qt_deploy(release_dir)


        print('\t压缩成zip.')
        shutil.make_archive(release_dir, 'zip', '.', release_dir)
        print(f'\t删除文件夹[{release_dir}].')
        shutil.rmtree(release_dir)
    else:
        time.sleep(10)

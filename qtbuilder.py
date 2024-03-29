import time
import os
import shutil
import pathlib
import subprocess
import colorama


name = 'FTU文件传输工具'


qt_path = 'D:/0/Qt/Qt5.12.12/5.12.12/mingw73_64/bin;D:/0/Qt/Qt5.12.12/Tools/mingw730_64/bin;'


enigmavbconsole = 'C:/Program Files (x86)/Enigma Virtual Box/enigmavbconsole.exe'


def prompt(message):
    print(f'\033[1;32m{message}\033[0m')


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
    prompt('查找文件夹内的Qt工程文件...')
    file_name = list(pathlib.Path('.').rglob('*.pro'))[0].name
    prompt(f'\t找到文件{file_name}.\n')
    return file_name


def find_line(lines, key):
    for line in lines:
        if key in line:
            return line.replace(key, '').strip()


def find_target(pro_file):
    prompt(f'查找{pro_file}文件内的编译目标程序名...')
    with open(pro_file, 'r') as fp:
        lines = fp.readlines()
        target = find_line(lines, 'TARGET = ')
        if target is None:
            target = pro_file.replace('.pro', '')
        prompt(f'\t找到编译目标程序名{target}.\n')
        return target


def find_rc_file(pro_file):
    prompt(f'查找{pro_file}文件内的RC文件名...')
    with open(pro_file, 'r') as fp:
        lines = fp.readlines()
        rc_file = find_line(lines, 'RC_FILE = ')
        prompt(f'\t找到RC文件名{rc_file}.\n')
        return rc_file


def git_version():
    prompt('读取git版本...')
    with os.popen('git log -1 --format="%h %ct"') as fp:
        v, t = fp.readlines()[0].rstrip().split(' ')
        v = v.upper()
        t1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)))
        t2 = time.strftime("%Y%m%d", time.localtime(int(t)))
        prompt(f'\t{v} {t1} {t2}\n')
        return [v, t1, t2]


def generate_h_file(version):
    prompt('生成version.h.\n')
    with open('version.h', 'w') as fp:
        fp.write('#ifndef VERSION_H\n')
        fp.write('#define VERSION_H\n\n')
        fp.write('#define VERSION \"%s\"\n\n' % version)
        fp.write('#endif // VERSION_H\n')


def write_rc_file(rc_file, v, t):
    prompt('更改RC文件.\n')
    with open(rc_file, 'r') as r:
        lines = r.readlines()
    for line in lines:
        if 'ProductVersion' in line:
            s = line.split(',')[0]
            lines[lines.index(line)] = f'{s}, "{t} {v}"\n'
            break
    with open(rc_file, 'w') as fp:
        fp.writelines(lines)


def write_version(rc_file):
    v, t1, t2 = git_version()
    generate_h_file(f'{v} {t1}')
    write_rc_file(rc_file, v, t1)
    return t2


def command(cmdline, code='UTF-8'):
    last_line_not_empty = False
    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    while process.poll() is None:
        line = process.stdout.readline().strip().decode(code)
        line_not_empty = len(line) > 0
        if line_not_empty or last_line_not_empty:
            print(line)
        last_line_not_empty = line_not_empty


def build(pro_file, release_file, target):
    prompt(f'编译工程{pro_file}.\n')
    os.environ['PATH'] = qt_path + os.environ['PATH']
    if not os.path.exists('build'):
        os.mkdir('build')
    os.chdir('build')
    command(f'qmake.exe ../{pro_file}')
    command('mingw32-make.exe -j4 release')
    os.chdir('..')
    build_file = f'build/release/{target}.exe'
    if os.path.isfile(build_file):
        prompt(f'生成文件{build_file}.\n')
        if os.path.isfile(release_file):
            os.remove(release_file)
        shutil.move(build_file, release_file)
    shutil.rmtree('build')


if __name__ == '__main__':
    colorama.init(autoreset = True)

    pro_file = find_pro_file()
    target = find_target(pro_file)
    version = write_version(find_rc_file(pro_file))
    release_dir = 'release'

    exe = 'release.exe'

    prompt(f'创建文件夹[{release_dir}].\n')
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    release_file = f'{release_dir}/{exe}'
    build(pro_file, release_file, target)

    prompt('部署程序.')

    if os.path.isfile(release_file):
        prompt('\t部署Qt.\n')
        qt_deploy(release_dir)

        prompt('\tUPX压缩.\n')
        command(f'upx.exe --best {release_file}', 'GB2312')

        prompt('\t封包.\n')
        evbproject = list(pathlib.Path('.').rglob('*.evb'))[0].name
        command(f'{enigmavbconsole} {evbproject}')
        shutil.rmtree(release_dir)

        prompt('\t打包压缩应用程序.')
        release_zip_dir = name + version
        os.makedirs(release_zip_dir)
        shutil.move(f'{exe}', f'{release_zip_dir}/{name}.exe')
        shutil.make_archive(release_zip_dir, 'zip', '.', release_zip_dir)
        shutil.rmtree(release_zip_dir)

        prompt('结束.')

        time.sleep(3)
    else:
        time.sleep(10)

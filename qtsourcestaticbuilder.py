# -*- coding: utf-8 -*-

import subprocess
import glob2
import shutil
import os
import zipfile
import pathlib

# 最小配置
args = '-confirm-license -opensource -platform win32-g++ -release -no-opengl -make libs -nomake tools -nomake examples -nomake tests -skip qt3d -skip qtandroidextras -skip qtcanvas3d -skip qtconnectivity -skip qtdatavis3d -skip qtdeclarative -skip qtdoc -skip qtgamepad -skip qtcharts -skip qtgraphicaleffects -skip qtimageformats -skip qtlocation -skip qtmacextras -skip qtmultimedia -skip qtnetworkauth -skip qtpurchasing -skip qtquickcontrols -skip qtquickcontrols2 -skip qtscript -skip qtscxml -skip qtsensors -skip qtserialbus -skip qtspeech -skip qtsvg -skip qttools -skip qttranslations -skip qtvirtualkeyboard -skip qtwayland -skip qtwebchannel -skip qtwebengine -skip qtwebsockets -skip qtwebview -skip qtwinextras -skip qtx11extras -skip qtxmlpatterns -no-feature-texthtmlparser -no-feature-textodfwriter -no-feature-concurrent -no-feature-effects -no-feature-sharedmemory -no-feature-systemsemaphore -no-feature-im -no-feature-dom -no-feature-filesystemwatcher -no-feature-graphicsview -no-feature-graphicseffect -no-feature-sizegrip -no-feature-printpreviewwidget -no-feature-keysequenceedit -no-feature-colordialog -no-feature-fontdialog -no-feature-printpreviewdialog -no-feature-progressdialog -no-feature-errormessage -no-feature-wizard -no-feature-datawidgetmapper -no-feature-cups -no-feature-codecs -no-feature-big_codecs -no-feature-iconv -no-feature-networkproxy -no-feature-socks5 -no-feature-networkdiskcache -no-feature-bearermanagement -no-feature-mimetype -no-feature-undocommand -no-feature-undostack -no-feature-undogroup -no-feature-undoview -no-feature-statemachine -no-feature-gestures -no-feature-dbus -no-feature-sessionmanager -no-feature-topleveldomain -no-feature-sha3-fast -no-feature-imageformat_ppm -no-feature-imageformat_xbm -no-feature-freetype -no-feature-appstore-compliant -no-feature-process -no-feature-lcdnumber -qt-zlib -qt-libpng -qt-libjpeg -no-harfbuzz -skip remoteobjects -optimize-size -optimized-tools'

def run(cmdline):
    last_line_not_empty = False
    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    while process.poll() is None:
        line = process.stdout.readline().strip().decode('UTF-8')
        line_not_empty = len(line) > 0
        if line_not_empty or last_line_not_empty:
            print(line)
        last_line_not_empty = line_not_empty


if __name__ == '__main__':
    # 搜索文件名后缀为7z的文件,例如i686-8.1.0-release-posix-dwarf-rt_v6-rev0.7z
    mingw32 = glob2.glob('*.7z')[0]
    # 搜索文件名后缀为zip的文件,例如qt-everywhere-src-5.12.12.zip
    qt = glob2.glob('*.zip')[0]

    print(f'mingw32编译器压缩包:{mingw32}')
    print(f'Qt源码压缩包:{qt}')

    if not os.path.exists('Tools'):
        # 解压mingw32编译器,解压后目录名为mingw32
        run(f'\"C:\Program Files\WinRAR\WinRAR.exe\" x {mingw32}')
        # 创建Tools文件夹
        os.mkdir('Tools')
        # 将mingw32文件夹移动至Tools文件夹下
        shutil.move('mingw32', 'Tools/mingw810_64')

    # v1为Qt源码解压后的文件夹名,例如qt-everywhere-src-5.12.12
    v1 = qt.replace('.zip', '')
    # v为Qt的版本号,例如5.12.12
    v = v1.replace('qt-everywhere-src-', '')
    if not os.path.exists(v):
        # 创建Qt版本号为名称的文件夹,将生成后的文件放置在该处
        os.mkdir(v)
        with zipfile.ZipFile(qt, 'r') as z:
            z.extractall('.')

    # 创建build文件夹
    if not os.path.exists('build'):
        os.mkdir('build')

    # 将mingw32的路径声明为环境变量PATH
    cwd = pathlib.PurePosixPath(pathlib.Path.cwd())
    prefix = f'{cwd}/{v}'
    os.environ['PATH'] = f'{cwd}/Tools/mingw810_64/bin;' + os.environ['PATH']

    file_name = f'{v1}/qtbase/mkspecs/common/g++-win32.conf'
    with open(file_name, 'r') as r:
        lines = r.readlines()
    with open(file_name, 'w') as w:
        for line in lines:
            if 'QMAKE_LFLAGS_DLL        = -shared' in line:
                line = 'QMAKE_LFLAGS_DLL        = -static\n'
            w.write(line)

    file_name = f'{v1}/qtbase/mkspecs/common/gcc-base.conf'
    with open(file_name, 'r') as r:
        lines = r.readlines()
        print(lines)
    with open(file_name, 'w') as w:
        for line in lines:
            if 'QMAKE_LFLAGS           +=\n' in line:
                line = 'QMAKE_LFLAGS           += -static\n'
            w.write(line)

    # 配置Qt
    os.chdir('build')
    #run(f'{cwd}/{v1}/configure.bat -prefix {prefix} -shared {args}')
    run(f'{cwd}/{v1}/configure.bat -prefix {prefix} -static -static-runtime {args}')

    # 编译
    #run('mingw32-make')

    # 安装
    #run('mingw32-make install')

    # mkspecs\common\目录下的gcc-base.conf文件中的QMAKE_LFLAGS参数值改为-static并保存
    # mkspecs\common\目录下的g++-win32.conf文件中的QMAKE_LFLAGS_DLL参数值改为-static并保存

$source_dir='qt-everywhere-src-5.15.5'

$mingw32='D:/0/Qt/Qt5.15.5x/Tools/mingw810_64/bin'
$prefix='D:/0/Qt/Qt5.15.5x/5.15.5/mingw81_64'

$env:Path="$mingw32;$env:Path"

# 最小配置
$args = '-confirm-license -opensource -platform win32-g++ -release -static -static-runtime -no-opengl -make libs -nomake tools -nomake examples -nomake tests -skip qt3d -skip qtandroidextras -skip qtcanvas3d -skip qtdatavis3d -skip qtdeclarative -skip qtdoc -skip qtgamepad -skip qtcharts -skip qtgraphicaleffects -skip qtimageformats -skip qtlocation -skip qtmacextras -skip qtmultimedia -skip qtnetworkauth -skip qtpurchasing -skip qtquickcontrols -skip qtquickcontrols2 -skip qtscript -skip qtscxml -skip qtsensors -skip qtserialbus -skip qtspeech -skip qtsvg -skip qttools -skip qttranslations -skip qtvirtualkeyboard -skip qtwayland -skip qtwebchannel -skip qtwebengine -skip qtwebsockets -skip qtwebview -skip qtwinextras -skip qtx11extras -skip qtxmlpatterns -no-feature-texthtmlparser -no-feature-textodfwriter -no-feature-effects -no-feature-sharedmemory -no-feature-systemsemaphore -no-feature-im -no-feature-dom -no-feature-filesystemwatcher -no-feature-graphicsview -no-feature-graphicseffect -no-feature-sizegrip -no-feature-printpreviewwidget -no-feature-keysequenceedit -no-feature-colordialog -no-feature-fontdialog -no-feature-printpreviewdialog -no-feature-progressdialog -no-feature-errormessage -no-feature-wizard -no-feature-datawidgetmapper -no-feature-cups -no-feature-codecs -no-feature-big_codecs -no-feature-iconv -no-feature-networkproxy -no-feature-socks5 -no-feature-networkdiskcache -no-feature-bearermanagement -no-feature-mimetype -no-feature-undocommand -no-feature-undostack -no-feature-undogroup -no-feature-undoview -no-feature-statemachine -no-feature-gestures -no-feature-dbus -no-feature-sessionmanager -no-feature-topleveldomain -no-feature-sha3-fast -no-feature-imageformat_ppm -no-feature-imageformat_xbm -no-feature-freetype -no-feature-appstore-compliant -no-feature-process -no-feature-lcdnumber -qt-zlib -qt-libpng -qt-libjpeg -no-harfbuzz -skip remoteobjects -optimize-size -optimized-tools'

# 替换g++-win32.conf文件
$file_name=$source_dir + '/qtbase/mkspecs/common/g++-win32.conf'
$contents = Get-Content $file_name
if (!$contents.contains("QMAKE_LFLAGS_DLL        = -static"))
{
 $contents = $contents -replace 'QMAKE_LFLAGS_DLL        = -shared', 'QMAKE_LFLAGS_DLL        = -static'
$contents | Set-Content $file_name -Encoding Ascii
}

# 替换gcc-base.conf文件
$file_name=$source_dir + '/qtbase/mkspecs/common/gcc-base.conf'
$contents = Get-Content $file_name
if (!$contents.contains("QMAKE_LFLAGS           += -static"))
{
 $contents = $contents -replace "QMAKE_LFLAGS           \+\=", 'QMAKE_LFLAGS           += -static'
 $contents | Set-Content $file_name -Encoding Ascii 
}

# 创建build文件夹
$ebuild=Test-Path build
if (!$ebuild)
{
 mkdir build
}

# 切换到build文件夹
cd build

# 配置
$configure='../' + $source_dir + '/configure.bat -prefix ' + $prefix + ' ' + $args
Invoke-Expression $configure

# 若移动编译好的BIN
# 需改动plugins/platforms/windows/qwindows.prl内的绝对路径

# 增加qt.conf
# [Paths]
# Prefix=..
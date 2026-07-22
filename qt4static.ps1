$source_dir='qt-everywhere-opensource-src-4.8.7'

$mingw32='D:/0/Qt/mingw32/bin/'
$prefix='D:/0/Qt/4.8.7-static'

$env:Path="$mingw32;$env:Path"

# 配置
$args = '-opensource -confirm-license -release  -static -platform win32-g++ -iconv -qt-zlib -no-libtiff -qt-libpng -no-libmng -qt-libjpeg -no-openssl -no-opengl -no-webkit -no-qt3support -no-xmlpatterns -no-multimedia -no-script -no-scripttools -no-declarative -no-declarative-debug -no-sql-mysql  -no-sql-odbc -no-sql-psql -qt-sql-sqlite -no-phonon -no-style-motif -no-style-cde -no-style-cleanlooks -no-style-plastique -nomake tools -nomake examples -nomake demos -nomake docs -nomake translations'

# 替换g++-win32.conf文件
$file_name=$source_dir + '/mkspecs/win32-g++/qmake.conf'
$contents = Get-Content $file_name
if (!$contents.contains("QMAKE_LFLAGS_DLL        = -static"))
{
 $contents = $contents -replace 'QMAKE_LFLAGS_DLL        = -shared', 'QMAKE_LFLAGS_DLL        = -static'
$contents | Set-Content $file_name -Encoding Ascii
}

# 替换gcc-base.conf文件
$file_name=$source_dir + '/mkspecs/win32-g++/qmake.conf'
$contents = Get-Content $file_name
if (!$contents.contains("QMAKE_LFLAGS           += -static"))
{
 $contents = $contents -replace "QMAKE_LFLAGS           \+\=", 'QMAKE_LFLAGS           += -static'
 $contents | Set-Content $file_name -Encoding Ascii
}

# 切换到$source_dir文件夹
cd $source_dir

# 配置
$configure='./configure.exe -prefix ' + $prefix + ' ' + $args
Invoke-Expression $configure

# 若移动编译好的BIN
# 需改动plugins/platforms/windows/qwindows.prl内的绝对路径

# 增加qt.conf
# [Paths]
# Prefix=..
import time
import os
import shutil
import datetime
import struct
import lxml.etree
import pathlib
import subprocess
import glob2
import colorama

crc_length = 100 * 1024

IAR = '\"C:/Program Files (x86)/IAR Systems/Embedded Workbench 8.2/common/bin/IarBuild.exe\"'


def file_crc32(filename):
    with open(filename, 'rb') as fp:
        crc32 = 0xFFFFFFFF
        polynomial = 0x04C11DB7
        for data in struct.unpack('i' * int(crc_length / 4), fp.read(crc_length)):
            xbit = 1 << 31
            while xbit:
                if crc32 & 0x80000000:
                    crc32 = (crc32 << 1) & 0xFFFFFFFF
                    crc32 = (crc32 ^ polynomial) & 0xFFFFFFFF
                else:
                    crc32 = (crc32 << 1) & 0xFFFFFFFF
                if data & xbit:
                    crc32 = (crc32 ^ polynomial) & 0xFFFFFFFF
                xbit = (xbit >> 1) & 0xFFFFFFFF
        return '{:08X}'.format(crc32)


def build(project, start_time, output):
    print(f'\033[1;32m开始编译工程{project}:\033[0m')
    commandline = f'{IAR} {filename} -build {project} -parallel 8'
    last_line_not_empty = False
    process = subprocess.Popen(commandline, stdout=subprocess.PIPE)
    while process.poll() is None:
        line = process.stdout.readline().strip().decode('UTF-8')
        line_not_empty = len(line) > 0
        if line_not_empty or last_line_not_empty:
            print(line)
        last_line_not_empty = line_not_empty
    result = os.path.exists(output)
    if result:
        print('\033[1;32m编译消耗%d秒.\033[0m\n' % (time.time() - start_time))
    return result


def bin_merge(application, whole):
    files = glob2.glob('*Bootloader.bin')
    if files:
        with open(files[0], 'rb') as fp:
            bin = fp.read()
        with open(application, 'rb') as fp:
            bin += fp.read()
        count = len(bin) % 4
        if count > 0:
            count = 4 - count
            print(f'\033[1;32m补{count}字节.\033[0m')
            bin += bytearray([0xFF] * count)
        with open(whole, 'wb') as fp:
            fp.write(bin)
    else:
        print('\033[1;32m没有找到Bootloader,不用进行BIN合并.\033[0m')


if __name__ == '__main__':
    colorama.init(autoreset = True)

    ewp = list(pathlib.Path('.').rglob('*.ewp'))[0]
    dirname, filename = ewp.parent, ewp.name
    filename = f'{dirname}/{filename}'

    print(f'\033[1;32m工程文件:{filename}\033[0m')

    x = lxml.etree.parse(filename)

    project = x.xpath('/project/configuration/name')[0].text
    exepath = x.xpath('//name[text()="ExePath"]/parent::option/state')[0].text
    output = x.xpath('//name[text()="OOCOutputFile"]/parent::option/state')[0].text

    target = os.path.splitext(output)[0]
    output = f'{dirname}/{exepath}/{output}'

    print(f'\033[1;32m输出文件:{output}\033[0m')

    if build(project, time.time(), output):
        crc32 = file_crc32(output)
        now = datetime.datetime.now().strftime('%Y%m%dT%H%M')
        target = f'{target}-{now}-{crc32}.bin'
        shutil.copy(output, target)

        bin_merge(target, target.replace('.bin', '-ALL.bin'))

        print('\033[1;32m\n结束.\033[0m')

        time.sleep(3)
    else:
        time.sleep(10)

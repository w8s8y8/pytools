import time
import os
import shutil
import datetime
import struct
import lxml.etree
import re

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


def bin_merge(application, whole):
    for filename in os.listdir('.'):
        if re.search('.*Bootloader.bin', filename):
            print('BIN合并.')
            with open(whole, 'wb') as fp:
                with open(filename, 'rb') as fp2:
                    fp.write(fp2.read())
                with open(application, 'rb') as fp2:
                    application = fp2.read()
                    fp.write(application)
                    size = len(application) % 4
                    if size > 0:
                        print(f'补{size}字节.')
                        fp.write(bytearray([0xFF] * size))
            break
    else:
        print('没有找到Bootloader,不用进行BIN合并.')


if __name__ == '__main__':
    dirname = None
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if os.path.splitext(filename)[1] == '.ewp':
                dirname = root.replace('.\\', '')
                break
        if dirname:
            break

    filename = f'{dirname}/{filename}'

    print(f'工程文件:{filename}')

    x = lxml.etree.parse(filename)

    project = x.xpath('/project/configuration/name')[0].text
    exepath = x.xpath('//name[text()="ExePath"]/parent::option/state')[0].text
    output = x.xpath('//name[text()="OOCOutputFile"]/parent::option/state')[0].text

    target = os.path.splitext(output)[0]
    output = f'{dirname}/{exepath}/{output}'

    print(f'输出文件:{output}')

    print(f'开始编译工程{project}')
    start_time = time.time()
    with os.popen(f'{IAR} {filename} -build {project}') as fp:
        for line in fp.readlines():
            print(line, end='')

    if os.path.exists(output):
        elapse = time.time() - start_time
        print('编译消耗%d秒.\n' % elapse)

        crc32 = file_crc32(output)
        now = datetime.datetime.now().strftime('%Y%m%dT%H%M')
        target = f'{target}-{now}-{crc32}.bin'
        shutil.copy(output, target)

        bin_merge(target, target.replace('.bin', '-ALL.bin'))

        print('\n结束.')

        time.sleep(3)
    else:
        time.sleep(10)

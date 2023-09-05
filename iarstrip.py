import os
import shutil
import stat


iar_path = 'D:/0/IAR Systems/Embedded Workbench 9.2'


def remove_dir(path):
    path = f'{iar_path}/{path}'
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file_name in files:
                os.chmod(os.path.join(root, file_name), stat.S_IWRITE)
        shutil.rmtree(path)


def remove_dirs(path, expath):
    path = f'{iar_path}/{path}'
    for name in os.listdir(path):
        npath = f'{path}/{name}'
        if os.path.isdir(npath) and name not in expath:
            for root, dirs, files in os.walk(npath):
                for file_name in files:
                    os.chmod(os.path.join(root, file_name), stat.S_IWRITE)
            shutil.rmtree(npath)


if __name__ == '__main__':
    ex = ['ARM', 'Geehy', 'ArteryTek', 'GigaDevice', 'XHSC', 'ST']
    remove_dirs('arm/config/devices', ex)
    remove_dirs('arm/config/flashloader', ex)
    remove_dirs('arm/config/linker', ex)
    remove_dirs('arm/config/debugger', ex)

    ex = ['arm', 'c', 'cpp', 'Geehy', 'libcpp', 'ST']
    remove_dirs('arm/inc', ex)

    ex = ['CMSIS-DAP', 'Jlink', 'ST-Link']
    remove_dirs('arm/drivers', ex)

    remove_dir('common/CMSIS-Manager')

    ex = ['ArteryTek', 'GigaDevice', 'ST']
    remove_dirs('arm/src/flashloader', ex)

    remove_dir('arm/CMSIS')

    remove_dir('arm/bin/Nu-Link')
    remove_dir('arm/bin/pemicro')
    remove_dir('arm/bin/jet')
    remove_dir('arm/bin/renesas')

# -*- coding: utf-8 -*-

import xml
import shutil


target = 'Bootloader'

template = 'ZYX'


def eww_conversion():
    ewd = xml.etree.ElementTree.parse(f'{template}.eww')
    root = ewd.getroot()
    root.find('./project/path').text = f'$WS_DIR$\{target}.ewp'
    ewd.write(f'{target}.eww', encoding='iso-8859-1', xml_declaration=True, short_empty_elements=False)


if __name__ == '__main__':
    eww_conversion()
    for e in ['ewp', 'ewp', 'ewd']:
        shutil.copy(f'{template}.{e}', f'{target}.{e}')

# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import glob2

def node_set(node, path, value):
    node.find(path).text = value


def node_remove(node, path):
    n = node.find(path)
    parent = node.find(path + '/..')
    children = parent.findall('*')
    if children[-1] == n:
        children[-2].tail = n.tail
    parent.remove(n)


def ewp_conversion(source, destination):
    ewp = ET.parse(source)

    root = ewp.getroot()

    data = root.find('./configuration/settings/name[.=\'General\']/../data')
    node_set(data, './version', '34')
    node_set(data, './option/name[.=\'OGLastSavedByProductVersion\']/../state', '9.20.1.43525')
    node_set(data, './option/name[.=\'GBECoreSlave\']/../version', '31')
    node_set(data, './option/name[.=\'CoreVariant\']/../version', '31')
    node_set(data, './option/name[.=\'GFPUCoreSlave2\']/../version', '31')

    node_remove(data, './option/name[.=\'PointerAuthentication\']/..')
    node_remove(data, './option/name[.=\'FPU64\']/..')


    data = root.find('./configuration/settings/name[.=\'ILINK\']/../data')
    node_set(data, './version', '26')
    node_remove(data, './option/name[.=\'IlinkFpuProcessor\']/..')
    node_remove(data, './option/name[.=\'IlinkProcessor\']/..')

    ewp.write(destination, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)


def ewt_conversion(source, destination):
    ewt = ET.parse(source)

    root = ewt.getroot()

    settings = root.find('./configuration/settings/name[.=\'C-STAT\']/..')
    node_set(settings, './archiveVersion', '515')
    node_set(settings, './data/version', '515')
    node_set(settings, './data/cstat_settings/cstat_version', '2.3.2')

    node_remove(settings, './/check[@name=\'MISRAC2012-Rule-1.4_b\']')
    node_remove(settings, './/check[@name=\'MISRAC2012-Rule-1.4_a\']')
    node_remove(settings, './/check[@name=\'MISRAC2012-Rule-21.21\']')

    ewt.write(destination, encoding='UTF-8', xml_declaration=True, short_empty_elements=True)


def ewd_conversion(source, destination):
    ewd = ET.parse(source)

    root = ewd.getroot()

    data = root.find('./configuration/settings/name[.=\'C-SPY\']/../data')
    node_set(data, './option/name[.=\'OCLastSavedByProductVersion\']/../state', '9.20.1.43525')

    debuggerPlugins = root.find('.//debuggerPlugins')
    for plugin in debuggerPlugins.findall('.//plugin'):
        if 'uCOS-II' in plugin.find('.//file').text:
             debuggerPlugins.remove(plugin)

    ewd.write(destination, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)


if __name__ == '__main__':
    ewt = glob2.glob('*.ewt')[0]
    ewd = ewt.replace('.ewt', '.ewd')
    ewp = ewt.replace('.ewt', '.ewp')

    ewp_conversion(ewp, ewp)
    ewt_conversion(ewt, ewt)
    ewd_conversion(ewd, ewd)

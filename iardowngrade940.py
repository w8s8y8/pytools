# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import glob2

def node_set(node, path, value):
    node.find(path).text = value


def node_remove_last(node, path):
    n = node.find(path)
    parent = node.find(path + '/..')
    children = parent.findall('*')
    if children[-1] == n:
        children[-2].tail = n.tail
    parent.remove(n)


def node_find(node, vstring):
    tag, name, value = vstring.replace('=', '@').split('@')
    for n in node.findall(f'.//{tag}'):
        if name in n.attrib and n.attrib[name] == value:
            return n
    return None


def node_remove_one(node, parent, child):
    parent = node_find(node, parent)
    if parent is not None:
        tag, name, value = child.replace('=', '@').split('@')
        for n in parent.findall(f'.//{tag}'):
            if name in n.attrib and n.attrib[name] == value:
                n.tail = n.tail
                parent.remove(n)
                break


def ewp_conversion(source, destination):
    ewp = ET.parse(source)

    root = ewp.getroot()
    root.find('./fileVersion').text = '3'

    data = root.find('./configuration/settings/name[.="General"]/../data')
    node_set(data, './version', '35')
    node_set(data, './option/name[.="OGLastSavedByProductVersion"]/../state', '9.30.1.50052')
    node_set(data, './option/name[.="GBECoreSlave"]/../version', '32')
    node_set(data, './option/name[.="CoreVariant"]/../version', '32')
    node_set(data, './option/name[.="GFPUCoreSlave2"]/../version', '32')
    node_remove_last(data, './option/name[.="OG_32_64DeviceCoreSlave"]/..')

    data = root.find('./configuration/settings/name[.="ICCARM"]/../data')
    node_set(data, './version', '37')
    node_remove_last(data, './option/name[.="CCBranchTargetIdentification"]/..')
    node_remove_last(data, './option/name[.="CCPointerAutentiction"]/..')

    data = root.find('./configuration/settings/name[.="AARM"]/../data')
    node_set(data, './version', '11')
    node_remove_last(data, './option/name[.="A_32_64Device"]/..')

    data = root.find('./configuration/settings/name[.="BUILDACTION"]/..')
    node_set(data, './archiveVersion', '1')
    data = data.find('./data')
    data.text = data.tail + '        '
    e = data.makeelement('prebuild', {})
    e.tail = data.tail + '        '
    data.append(e)
    e = data.makeelement('postbuild', {})
    e.tail = data.tail + '    '
    data.append(e)

    ewp.write(destination, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)


def ewt_conversion(source, destination):
    ewt = ET.parse(source)

    root = ewt.getroot()
    root.find('./fileVersion').text = '3'

    settings = root.find('./configuration/settings/name[.="C-STAT"]/..')
    node_set(settings, './archiveVersion', '516')
    node_set(settings, './data/version', '516')
    node_set(settings, './data/cstat_settings/cstat_version', '2.4.1')

    node_remove_one(root, 'group@name=MISRAC2012-Rule-1', 'check@name=MISRAC2012-Rule-1.3_l')
    node_remove_one(root, 'group@name=CERT-ERR', 'check@name=CERT-ERR30-C_e')
    node_remove_one(root, 'group@name=MISRAC2012-Dir-4', 'check@name=MISRAC2012-Dir-4.13_a')
    node_remove_one(root, 'group@name=MISRAC2012-Rule-12', 'check@name=MISRAC2012-Rule-12.4')

    check = node_find(root, 'group@name=MISRAC2012-Rule-1')
    node1 = node_find(root, 'check@name=MISRAC2012-Rule-1.3_v')
    node2 = ET.Element("check")
    node2.attrib = {'enabled':'true', 'name':'MISRAC2012-Rule-1.3_w'}
    node2.tail = node1.tail
    check.insert(check.findall('*').index(node1) + 1, node2)

    ewt.write(destination, encoding='UTF-8', xml_declaration=True, short_empty_elements=True)


def ewd_conversion(source, destination):
    ewd = ET.parse(source)

    root = ewd.getroot()
    root.find('./fileVersion').text = '3'

    data = root.find('./configuration/settings/name[.="C-SPY"]/../data')
    node_set(data, './version', '32')
    node_set(data, './option/name[.="OCLastSavedByProductVersion"]/../state', '9.30.1.50052')
    node_remove_last(data, './option/name[.="AuthEnforce"]/..')
    node_remove_last(data, './option/name[.="AuthSdmExplicitLib"]/..')
    node_remove_last(data, './option/name[.="AuthSdmManifest"]/..')
    node_remove_last(data, './option/name[.="AuthSdmSelection"]/..')
    node_remove_last(data, './option/name[.="AuthEnable"]/..')
    node_remove_last(data, './option/name[.="C_32_64Device"]/..')
    node_remove_last(data, './option/name[.="OCOverrideSlavePath"]/..')
    node_remove_last(data, './option/name[.="OCOverrideSlave"]/..')

    # remove node settings/name[.="E2_ID"]
    configuration = root.find('./configuration')
    s = configuration.find('./settings/name[.="E2_ID"]/..')
    children = configuration.findall('*')
    index = children.index(s)
    configuration.remove(s)
    children[index].tail = children[index - 1].tail

    data = root.find('./configuration/settings/name[.="STLINK_ID"]/../data')
    node_set(data, './version', '7')
    data.find('./option/name[.="CCSTLinkProbeList"]/../version').text = '1'
    node_remove_last(data, './option/name[.="CCSTLinkTargetVoltage"]/..')
    node_remove_last(data, './option/name[.="CCSTLinkTargetVccEnable"]/..')

    data = root.find('./configuration/settings/name[.="XDS100_ID"]/../data')
    data.find('./option/name[.="CCXds100ResetList"]/../version').text = '0'

    ewd.write(destination, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)


if __name__ == '__main__':
    ewt = glob2.glob('*.ewt')[0]
    ewd = ewt.replace('.ewt', '.ewd')
    ewp = ewt.replace('.ewt', '.ewp')

    ewp_conversion(ewp, ewp)
    ewt_conversion(ewt, ewt)
    ewd_conversion(ewd, ewd)

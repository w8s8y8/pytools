# -*- coding: utf-8 -*-
"""
Created on Thu May 24 10:28:51 2018

@author: Administrator

将SVG接线图加入通讯中断的状态

"""

import xml.dom.minidom

doc = xml.dom.minidom.parse('D:/35kV主接线图.svg')

def setNewNode(newNode):
    for nc in newNode.childNodes:
        if nc.nodeType == nc.ELEMENT_NODE:
            if nc.nodeName == 'g':
                setNewNode(nc)
            else:
                if nc.hasAttribute('fill') and nc.getAttribute('fill') != 'none':
                    nc.setAttribute('fill', 'grey')
                if nc.hasAttribute('stroke'):
                    nc.setAttribute('stroke', 'grey')
                    
                    
def removeAttributeFromG(node):
    for nc in node.childNodes:
        if nc.nodeType == nc.ELEMENT_NODE:
            if nc.nodeName == 'g':
                if nc.hasAttribute('irealstate'):
                    nc.removeAttribute('irealstate')
                if nc.hasAttribute('style'):
                    nc.removeAttribute('style')
                removeAttributeFromG(nc)


def parser(node):
    node.setAttribute('irealstate', '-1')

    newNode = None
    for apc in node.childNodes:
        if apc.nodeType == apc.ELEMENT_NODE and apc.getAttribute('irealstate') == '0':
            newNode = apc.cloneNode(True)
            apc.setAttribute('style', 'display:none;')

    node.appendChild(newNode)
    
    newNode.setAttribute('irealstate', '-1')
    newNode.setAttribute('style', 'display:block;')
    setNewNode(newNode)
      
    for nc in node.childNodes:
        removeAttributeFromG(nc);

for g in doc.childNodes:
    for ap in g.childNodes:
        for ap in ap.childNodes:
            if ap.nodeType == ap.ELEMENT_NODE and ap.getAttribute('itemplatetype') == 'status':
                if ap.getAttribute('igraphtype') in ('circuitbreaker', 'handcart', 'groundedswitch'):
                    parser(ap)
                else:
                    print(ap.getAttribute('id'))
                    
doc.writexml(open('D:/manage/config/target/graphics/test.svg', 'w', encoding='utf-8'))
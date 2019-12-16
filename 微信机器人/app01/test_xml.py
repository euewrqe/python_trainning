import xml.sax
import xml.sax.handler

import xml.etree.ElementTree as ET
tree = ET.fromstring('''<?xml version="1.0" encoding="UTF-8"?><note><to>World</to><from>Linvo</from><heading>Hi</heading><body>Hello World!</body></note>''')
# root = tree.get_root()
print(dir(tree))
print(tree.tag)
tree = ET.parse("a.xml")
print(tree.getroot())


# class XMLHandler(xml.sax.handler.ContentHandler):
#     def __init__(self):
#         self.buffer = ""
#         self.mapping = {}
#
#     def startElement(self, name, attributes):
#         self.buffer = ""
#
#     def characters(self, data):
#         self.buffer += data
#
#     def endElement(self, name):
#         self.mapping[name] = self.buffer
#
#     def getDict(self):
#         return self.mapping
#
#
# data = '''''<?xml version="1.0" encoding="UTF-8"?><note><to>World</to><from>Linvo</from><heading>Hi</heading><body>Hello World!</body></note>'''
#
# xh = XMLHandler()
# xml.sax.parseString(data, xh)
# ret = xh.getDict()
#
# import pprint
#
# pprint.pprint(ret)
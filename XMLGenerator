import xml.dom.minidom as Dom

class XMLGenerator:

    def __init__(self, xmlname):
        self.doc = Dom.Document()
        self.xml_name = xmlname

    def createNode(self, node_name):
        return self.doc.createElement(node_name)

    def addNode(self, node, prev_node = None):
        cur_node = node
        if prev_node is not None:
            prev_node.appendChild(cur_node)
        else:
            self.doc.appendChild(cur_node)
        return cur_node

    def setNodeAttr(self, node, att_name, value):
        cur_node = node
        cur_node.setAttribute(att_name, value)

    def setNodeValue(self, cur_node, value):
        node_data = self.doc.createTextNode(value)
        cur_node.appendChild(node_data)

    def genXml(self):
        f = open(self.xml_name, "w")
        f.write(self.doc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8"))
        f.close()


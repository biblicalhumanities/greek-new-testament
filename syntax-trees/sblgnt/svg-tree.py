# http://www.petercollingridge.co.uk/book/export/html/437
# http://docs.python.org/2/library/xml.etree.elementtree.htm
# http://www.w3.org/TR/SVG/coords.html#ViewportSpace
# http://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html

# Could do a function for row() to avoid this global

row = 1

def graph(node, column):
    global row
    first = True;
    print node.attrib.get("Cat"), row, column, node.text
    for child in node:
        if first:
           first=False
        else:
           row = row + 1
        graph(child, column+1)

import xml.etree.ElementTree as ET
tree = ET.parse('10-ephesians.xml')
sblroot = tree.getroot()

width = 40
height = 30
text_column = 40

print tree
print sblroot
sentence = sblroot.find("Sentence")
print sentence.attrib.get("ID")

trees = sentence.find("Trees")
t = trees.find("Tree")
n = t.find("Node")

print n

graph(n, 1)

# svgtree = ET.Element("{http://www.w3.org/2000/svg}svg")
# print svgtree

# Strategy:
# 
# Grow from left to right UNTIl you hit a node with text in it.  Nodes
# like [verb GREEK] go on the right, as two boxes.
# (Analysis could go after that, if need be)

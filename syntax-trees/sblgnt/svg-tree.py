# http://www.petercollingridge.co.uk/book/export/html/437
# http://docs.python.org/2/library/xml.etree.elementtree.htm
# http://www.w3.org/TR/SVG/coords.html#ViewportSpace
# http://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html



#  Next attempt:  
# 
#  Place text in leftmost column
# 
#  Algorithm:
#  1. Dive down to text node, place it in the column
#  2. Ascend to analysis nodes, mark as 'visited' as you go (discard afterward)
#     compute 'just enough distance' for each node

from lxml import etree

width = 60  # 20 + 30  (x+25, x-5?)
height = 30

def row(add=0):
    row.counter = row.counter + add
    return row.counter

if "counter" not in row.__dict__: 
    row.counter = 1

def graph(svgroot, node, column, parent_row):

    print node.attrib.get("Cat"), row(), column, node.text

    svg_node = etree.SubElement( svgroot, "{http://www.w3.org/2000/svg}text")   
    svg_node.set('font-size', str(18))
    svg_node.set('fill', 'black')
    svg_node.set('x', str(width*column))
    svg_node.set('y', str(height*row()))
    svg_node.text = node.attrib.get("Cat")
    
    if node.text and not node.text.isspace():
        t =  etree.SubElement( svgroot, "{http://www.w3.org/2000/svg}text")
        t.set('font-size', str(24))
        t.set('fill', 'blue')
        t.set('x', str(width*14))
        t.set('y', str(height*row()))
        t.text = node.text

        l =  etree.SubElement( svgroot, "{http://www.w3.org/2000/svg}path")
        l.set('stroke', 'grey')
        l.set('stroke-dasharray', '10,10')
        d = "M %d %d L %d %d"  % (width*column+45, row()*height-5, width*14-20, row()*height-5, )
        l.set('d', d)

    print "row: %d, parent row: %d" % (row(), parent_row)

    if column > 1: 
        horiz = etree.SubElement( svgroot, "{http://www.w3.org/2000/svg}path") 
        horiz.set('stroke','black') 
        d = "M %d %d L %d %d"  % (width*column-20, row()*height-5, width*column-5, row()*height-5 )
        horiz.set('d', d)
        if node.getnext() == None:
            vert = etree.SubElement( svgroot, "{http://www.w3.org/2000/svg}path") 
            vert.set('stroke','black') 
            d = "M %d %d L %d %d"  % (width*column-20, row()*height-5, width*column-20, parent_row*height-5 )
            vert.set('d', d)

    r = row()
    for child in node:
        if child.getprevious() != None:
           row(1)
        graph(svgroot, child, column+1, r)


tree = etree.parse('10-ephesians.xml')
sblroot = tree.getroot()

sentence = sblroot.find("Sentence")

trees = sentence.find("Trees")
t = trees.find("Tree")
n = t.find("Node")

svgroot = etree.Element("{http://www.w3.org/2000/svg}svg")
svgtree = etree.ElementTree(svgroot)

graph(svgroot, n, 1, row())

svgtree.write('test.svg', xml_declaration=True, encoding='UTF-8')

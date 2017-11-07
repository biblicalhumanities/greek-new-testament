# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

#
# Script to transform Hebrew and Greek XML Syntax Trees from
# Global Bible Initiative into Emdros MQL.
#
# http://emdros.org/
#
# This works for all syntax trees published by the Global Bible Initiative,
# and emits both the MQL for the data part and an MQL schema derived
# from the data.
#
# Works with both Python2 and Python3.
#
# Usage:
#
# python GBITrees2MQL.py -o <MQL-output-file> <XML-input-file1> [<XML-input-file2> ...]
#
# Example:
#
# python GBITrees2MQL.py -o Nestle1904.mql /path/to/Nestle/XML/files/*.xml
#
# This will produce Nestle1904.mql (containing the data) and
# Nestle1904.schema.mql (containing the MQL schema).
#
#
# To import this into Emdros using the SQLite3 backend (-b 3):
#
# $ echo "CREATE DATABASE 'Nestle1904' GO" | mql -b 3
# $ mql -b 3 -d Nestle1904 Nestle1904.schema.mql
# $ mql -b 3 -d Nestle1904 Nestle1904.mql
#
# That's it.
#

#
# Written by Ulrik Sandborg-Petersen with help from Andi Wu.
#
# Ulrik can be contacted via the contact information available at:
#
# http://ulrikp.org/
#
#

#
# Placed under the MIT license by kind permission from
# Dr. Reinier de Blois of the United Bible Societies.
#
# LICENSE:
#
# Copyright (C) 2017 United Bible Societies
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sys
import xml.sax
import codecs
import re

if sys.version_info[0] == 2:
    bIsPython2 = True
else:
    bIsPython2 = False

Emdros_reserved_words_dict = {
    "Type" : "SubType",
}


bookNumber2Name_list = [
    "ZeroDummy", # To offset everything by 1
    # OT
    "GEN",
    "EXO",
    "LEV",
    "NUM",
    "DEU",
    "JOS",
    "JDG",
    "RUT",
    "1SA",
    "2SA",
    "1KI",
    "2KI",
    "1CH",
    "2CH",
    "EZR",
    "NEH",
    "EST",
    "JOB",
    "PSA",
    "PRO",
    "ECC",
    "SNG",
    "ISA",
    "JER",
    "LAM",
    "EZK",
    "DAN",
    "HOS",
    "JOL",
    "AMO",
    "OBA",
    "JON",
    "MIC",
    "NAM",
    "HAB",
    "ZEP",
    "HAG",
    "ZEC",
    "MAL",
    # NT
    "MAT",
    "MRK",
    "LUK",
    "JHN",
    "ACT",
    "ROM",
    "1CO",
    "2CO",
    "GAL",
    "EPH",
    "PHP",
    "COL",
    "1TH",
    "2TH",
    "1TI",
    "2TI",
    "TIT",
    "PHM",
    "HEB",
    "JAS",
    "1PE",
    "2PE",
    "1JN",
    "2JN",
    "3JN",
    "JUD",
    "REV",
]

MAX_MONAD = 2100000000 

########################################
##
## MQL string mangling
##
########################################
special_re = re.compile(r"[\n\t\"\\]")

special_dict = {
    '\n' : '\\n',
    '\t' : '\\t',
    '"' : '\\"',
    '\\' : '\\\\',
}

if bIsPython2:
    upper_bit_re = re.compile(r'[\x80-\xff]')
else:
    upper_bit_re = None

def special_sub(mo):
    c = mo.group(0)
    assert len(c) == 1
    return special_dict[c]

def upper_bit_sub(mo):
    c = mo.group(0)
    assert len(c) == 1
    return "\\x%02x" % ord(c)

def mangleMQLString(ustr):
    #if bIsPython2:
    #    tmpresult = special_re.sub(special_sub, ustr)

    #    return upper_bit_re.sub(upper_bit_sub, tmpresult.encode('utf-8'))
    #else:
    result = []
    tmpresult = special_re.sub(special_sub, ustr)
    for i, c in enumerate(tmpresult):
        if ord(c) >= 128:
            result.append("\\x%02x" % ord(c))
        else:
            result.append(c)
    return "".join(result)
                



def mse2string(mse):
    (f,l) = mse
    if f == l:
        return "%d" % f
    else:
        return "%d-%d" % (f, l)


def set2somString(som):
    result = []
    mlist = list(sorted(som))

    if len(mlist) == 0:
        return " { } "
    elif len(mlist) == 1:
        return " { %d } " % mlist[0]
    else:
        prev_start = mlist[0]
        prev_end = mlist[0]
        for i in range(1, len(mlist)):
            m = mlist[i]
            diff = m - prev_end
            if diff == 1:
                prev_end = m
            else:
                assert diff > 0
                result.append((prev_start, prev_end))
                prev_start = m
                prev_end = m

        prev_end = mlist[-1]
        result.append((prev_start, prev_end))

    return " { %s } " % ",".join([mse2string(mse) for mse in result])

def featureName2nonReservedWord(feature_name):
    if feature_name in Emdros_reserved_words_dict:
        return Emdros_reserved_words_dict[feature_name]
    else:
        return feature_name
        
    
class EmdrosObject:
    def __init__(self, object_type_name, id_d):
        self.object_type_name = object_type_name
        self.id_d = id_d # Emdros id_d
        self.features_string = {} # Emdros string-features
        self.features_nonstring = {}
        self.attributes = {} # Attributes that don't end up as Emdros features
        self.som = set()
        self.parent_id_d = 0 # Emdros parent id_d

    def addAttribute(self, key, value):
        self.attributes[key] = value

    def getAttribute(self, key):
        return self.attributes[key]

    def getFeatureNonString(self, key):
        return self.features_nonstring[key]

    def getFeatureString(self, key):
        return self.features_string[key]

    def addFeatureNonString(self, key, value):
        real_key = featureName2nonReservedWord(key)
        self.features_nonstring[real_key] = value

    def addFeatureString(self, key, value):
        real_key = featureName2nonReservedWord(key)
        self.features_string[real_key] = value

    def hasFeatureString(self, key):
        return key in self.features_string

    def getObjectTypeName(self):
        return self.object_type_name

    def getID_D(self):
        """Accessor function."""
        return self.id_d

    def getSOM(self):
        return self.som

    def getSOMFirst(self):
        return list(sorted(self.som))[0]

    def getSOMLast(self):
        return list(sorted(self.som))[-1]

    def addMonad(self, m):
        self.som.add(m)

    def addMSE(self, fm, lm):
        for m in range(fm, lm+1):
            self.som.add(m)

    def getMonadsType(self):
        if len(self.som) == 0:
            assert False, "Error: som is empty for object of type %s and id_d %d and string-features %s" % (self.getObjectTypeName(), self.getID_D(), repr(self.features_string.items()))
        elif len(self.som) == 1:
            return 0 # SINGLE MONAD OBJECTS
        else:
            som_string = set2somString(self.som)
            if "," in som_string:
                return 2 # MULTIPLE RANGE OBJECTS
            else:
                return 1 # SINGLE RANGE OBJECTS

    def getMQL(self, bEmitObjectTypeName):
        result = []
        result.append("CREATE OBJECT FROM MONADS=%sWITH ID_D=%d\n" % (set2somString(self.som), self.id_d))

        if bEmitObjectTypeName:
            result.append("[%s\n" % objectTypeName)
        else:
            result.append("[\n")

        for (key,value) in sorted(self.features_string.items()):
            result.append("%s:=\"%s\";\n" % (key,mangleMQLString(value)))
        for (key,value) in sorted(self.features_nonstring.items()):
            result.append("%s:=%s;\n" % (key, value))
        result.append("]")

        if bEmitObjectTypeName:
            result.append("GO")
        result.append("\n")

        return "".join(result)


def ConvertMorphId(morphId):
    (ch_vs,wiv_wp) = morphId[2:].split(",")
    ch = int(ch_vs.split(":")[0])
    vs = int(ch_vs.split(":")[1])
    wiv = int(wiv_wp.split(".")[0])
    wp = int(wiv_wp.split(".")[1])
    morphId_converted = int("%d%03d%03d%02d" % (ch,vs,wiv,wp))
    return morphId_converted

class GBIXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.curmonad = 1
        self.curid_d = 1

        self.schema = {} # OTN -> { "features" -" { feature-name -> type-string },
                         #          "monad_type" : string }

        self.books = {} # book-number -> { "first_monad" : integer, "last_monad", "integer", "chapters" : { # chapter-number -> { "first_monad": integer, "last_monad" : integer} }}

        self.clean()

    def clean(self):
        self.elemstack = []
        self.charstack = []

        self.terminals = {} # { Tree ID_D --> { morphId --> id_d } }

        self.objects = {} # { ObjectTypeName --> {id_d --> obj} }
        for otn in ["Sentences", "Sentence", "Trees", "Tree", "Node", "Word"]:
            self.objects[otn] = {}
        self.object_stack = []

        self.bigobjectpool = {} # id_d --> obj

        self.parent2children_dict = {} # parent_id_d --> [immediate_child_id_ds]

        self.nTreeID_D = None


    def getObject(self, id_d):
        return self.bigobjectpool[id_d]

    def startDocument(self):
        pass

    def endDocument(self):
        # Set terminal monads
        for treeID_D in sorted(self.terminals):
            for morphId in sorted(self.terminals[treeID_D]):
                id_d = self.terminals[treeID_D][morphId]
                obj = self.getObject(id_d)
                obj.addMonad(self.curmonad)
                self.curmonad += 1

        # Calculate self.parent2children_dict, used in the next step
        self.setParents()

        # Recursively calculate monads sets of all objects, except
        # the top-level "book" (element "Sentences")
        for id_d in sorted(self.objects["Sentences"]):
            self.addMonads(id_d)

        self.createBooksAndChapters()

        self.makeSchema()

    def createBooksAndChapters(self):
        for treeID_D in sorted(self.terminals):
            for morphId in sorted(self.terminals[treeID_D]):
                id_d = self.terminals[treeID_D][morphId]
                obj = self.getObject(id_d)
                m = obj.getSOMFirst()
                self.addMonadToBooksAndChapters(morphId, m)

    def addMonadToBooksAndChapters(self, morphId, m):
        bookNumber = int(morphId[0:2])
        chapterNumber = int(morphId[2:5])
        if bookNumber not in self.books:
            self.books.setdefault(bookNumber, {})
            self.books[bookNumber]["first_monad"] = MAX_MONAD
            self.books[bookNumber]["last_monad"] = 0
            self.books[bookNumber]["chapters"] = {}
        if chapterNumber not in self.books[bookNumber]["chapters"]:
            self.books[bookNumber]["chapters"].setdefault(chapterNumber, {})
            self.books[bookNumber]["chapters"][chapterNumber]["first_monad"] = MAX_MONAD
            self.books[bookNumber]["chapters"][chapterNumber]["last_monad"] = 0

        if self.books[bookNumber]["first_monad"] > m:
            self.books[bookNumber]["first_monad"] = m
        if self.books[bookNumber]["last_monad"] < m:
            self.books[bookNumber]["last_monad"] = m

        if self.books[bookNumber]["chapters"][chapterNumber]["first_monad"] > m:
            self.books[bookNumber]["chapters"][chapterNumber]["first_monad"] = m

        if self.books[bookNumber]["chapters"][chapterNumber]["last_monad"] < m:
            self.books[bookNumber]["chapters"][chapterNumber]["last_monad"] = m

        

    def makeSchema(self):
        for OTN in self.objects:
            self.schema.setdefault(OTN, {})
            self.schema[OTN].setdefault("features", {})
            monads_type = 0
            mydict = self.objects[OTN]
            for id_d in mydict:
                obj = mydict[id_d]

                for feature_name in obj.features_string:
                    self.schema[OTN]["features"][feature_name] = "string"
                for feature_name in obj.features_nonstring:
                    if feature_name == "parent":
                        self.schema[OTN]["features"][feature_name] = "id_d"
                    else:
                        self.schema[OTN]["features"][feature_name] = "integer"

                obj_monads_type = obj.getMonadsType()
                if obj_monads_type > monads_type:
                    monads_type = obj_monads_type
                

            self.schema[OTN].setdefault("monads_type", monads_type)

    def setParents(self):
        for OTN in ["Word", "Node", "Tree", "Trees", "Sentence"]:
            for id_d in self.objects[OTN]:
                obj = self.getObject(id_d)

                parent_id_d = obj.getFeatureNonString("parent")
                if parent_id_d not in self.parent2children_dict:
                    self.parent2children_dict[parent_id_d] = []
                self.parent2children_dict[parent_id_d].append(obj.getID_D())

    def getFirstLastMonadFromTreeId(self, nTreeID_D, first_monad, last_monad):
        for morphId in sorted(self.terminals[nTreeID_D]):
            id_d = self.terminals[nTreeID_D][morphId]
            obj = self.getObject(id_d)
            obj_first = obj.getSOMFirst()
            obj_last = obj.getSOMLast()

            if obj_first < first_monad:
                first_monad = obj_first

            if obj_last > last_monad:
                last_monad = obj_last

        return (first_monad, last_monad)

    def addMonads(self, id_d):
        obj_parent = self.getObject(id_d)

        if obj_parent.getObjectTypeName() == "Word":
            # base case of the recursion:
            # We have already set the SOM of all Words in self.endDocument()
            return
        else:
            id_d_parent = obj_parent.getID_D()

            for child_id_d in self.parent2children_dict[id_d_parent]:
                # Recurse
                self.addMonads(child_id_d)

                # Add child's SOM to parent's SOM
                child_obj = self.getObject(child_id_d)
                child_som = child_obj.getSOM()
                obj_parent.som = obj_parent.som.union(child_som)



    def createObject(self, objectTypeName):
        obj = EmdrosObject(objectTypeName, self.getNextID_D())

        self.objects[objectTypeName][obj.getID_D()] = obj

        self.bigobjectpool[obj.getID_D()] = obj

        return obj

    def handleObject(self, obj):
        if obj.getObjectTypeName() == "Word":
            if obj.hasFeatureString("morphId"):
                morphId = obj.getFeatureString("morphId")
            elif obj.hasFeatureString("nodeId"):
                morphId = obj.getFeatureString("nodeId")[0:11]
            self.terminals.setdefault(self.nTreeID_D, {})[morphId] = obj.getID_D()

    def getNextID_D(self):
        self.curid_d += 1
        return self.curid_d - 1

    def characters(self, data):
        self.charstack.append(data)

    def isTerminal(self, tag, attributes, parent_obj):
        if tag != "Node":
            return False
        else:
            if parent_obj.getObjectTypeName() != "Node":
                return False
            elif "Rule" not in attributes:
                # Terminal Nodes don't have the "Rule" attribute.
                # All non-terminal Nodes do.
                # As per conversation with Andi Wu on 2017-10-31.
                return True
            else:
                return False

    def attribIsNonString(self, tag, key):
        if tag != "Node":
            # All non-Node tags have only String features
            return False
        else:
            # tag == Node
            if key in set(["Start", "End", "Head"]):
                return True
            else:
                return False

    def startElement(self, tag, attributes):
        chars = "".join(self.charstack)
        del self.charstack
        self.charstack = []

        if tag == "Node":
            if self.isTerminal(tag, attributes, self.object_stack[-1]):
                obj = self.createObject("Word")
            else:
                obj = self.createObject("Node")
                
            for (key, value) in attributes.items():
                if self.attribIsNonString(tag, key):
                    obj.addFeatureNonString(key, value)
                else:
                    obj.addFeatureString(key, value)

            self.handleObject(obj)
        elif tag == "Tree":
            obj = self.createObject("Tree")
            self.nTreeID_D = obj.getID_D()
        elif tag == "Trees":
            obj = self.createObject("Trees")
        elif tag == "Sentence":
            obj = self.createObject("Sentence")
            obj.addFeatureString("ID", attributes["ID"])
        elif tag == "Sentences":
            obj = self.createObject("Sentences")
        else:
            raise Exception(("Error: Unknown start-tag '<" + tag + ">'").encode('utf-8'))

        # Set parent id_d
        if len(self.object_stack) > 0:
            obj.addFeatureNonString("parent", self.object_stack[-1].getID_D())
            
        self.object_stack.append(obj)
            
    def endElement(self, tag):
        chars = "".join(self.charstack)
        del self.charstack
        self.charstack = []

        obj = self.object_stack[-1]
        self.object_stack.pop()
        
        if tag == "Node":
            pass
        elif tag == "Tree":
            self.nTreeID_D = None
        elif tag == "Trees":
            pass
        elif tag == "Sentence":
            pass
        elif tag == "Sentences":
            pass
        else:
            raise Exception(("Error: Unknown start-tag '<" + tag + ">'").encode('utf-8'))


        
    def emitMQL(self, fout):
        bEmitObjectTypeName = False
        for objectTypeName in sorted(self.objects):
            result = []
            result.append("CREATE OBJECTS WITH OBJECT TYPE [%s]\n" % objectTypeName)
            for id_d in sorted(self.objects[objectTypeName]):
                obj = self.objects[objectTypeName][id_d]
                result.append(obj.getMQL(bEmitObjectTypeName))

            result.append("GO\n\n\n")

            uotdoc = "".join(result)
            if bIsPython2:
                fout.write(uotdoc.encode('utf-8'))
            else:
                fout.write(bytes(uotdoc, 'ascii'))



    def emit_schema(self, schema_fout):
        result = []
        
        for OTN in sorted(self.schema):
            monads_type_int = self.schema[OTN]["monads_type"]
            if monads_type_int == 0:
                monads_type = "WITH SINGLE MONAD OBJECTS"
            elif monads_type_int == 1:
                monads_type = "WITH SINGLE RANGE OBJECTS"
            elif monads_type_int == 2:
                monads_type = "WITH MULTIPLE RANGE OBJECTS"
            else:
                assert False, "Unknown monads_type_int = %d" % monads_type_int

            if OTN in ["Word", "Tree", "Trees", "Sentence"]:
                uniqueness_type = "HAVING UNIQUE FIRST MONADS\n"
            else:
                uniqueness_type = ""

            result.append("CREATE OBJECT TYPE\n")
            result.append(monads_type)
            result.append("\n")
            result.append(uniqueness_type)
            result.append("[")
            result.append(OTN)
            result.append("\n")
            for (feature_name, feature_type) in sorted(self.schema[OTN]["features"].items()):
                result.append("  ")
                result.append(feature_name)
                result.append(" : ")
                result.append(feature_type)
                result.append(";\n")
                

            result.append("]")
            result.append("\nGO\n\n")

        result.append("""
CREATE OBJECT TYPE
WITH SINGLE RANGE OBJECTS
HAVING UNIQUE FIRST MONADS
[Book
   code : STRING;
]
GO

CREATE OBJECT TYPE
WITH SINGLE RANGE OBJECTS
HAVING UNIQUE FIRST MONADS
[Chapter
   code : STRING;
   chapter : INTEGER;
]
GO

""")
            
        doc = "".join(result)

        if bIsPython2:
            schema_fout.write(doc.encode('ascii'))
        else:
            schema_fout.write(bytes(doc, 'ascii'))

    def emitBookChapterMQL(self, fout):
        self.objects = {}
        self.objects["Book"] = {}
        self.objects["Chapter"] = {}
        for bookNumber in sorted(self.books):
            obj = self.createObject("Book")
            code = bookNumber2Name_list[bookNumber]
            obj.addFeatureString("code", code)
            fm = self.books[bookNumber]["first_monad"]
            lm = self.books[bookNumber]["last_monad"]
            obj.addMSE(fm, lm)

            for chapterNumber in sorted(self.books[bookNumber]["chapters"]):
                chapter_obj = self.createObject("Chapter")
                chapter_obj.addFeatureString("code", code)
                chapter_obj.addFeatureNonString("chapter", chapterNumber)
                fm = self.books[bookNumber]["chapters"][chapterNumber]["first_monad"]
                lm = self.books[bookNumber]["chapters"][chapterNumber]["last_monad"]
                chapter_obj.addMSE(fm, lm)

        self.emitMQL(fout)
        
                
            


def doIt(out_filename, xml_file_name_list):
    XH = GBIXMLHandler()
    fout = open(out_filename, "wb")
    
    for xml_file_name in xml_file_name_list:
        sys.stderr.write("Now reading: %s\n" % xml_file_name)
        
        fin = open(xml_file_name, "r")
        xml.sax.parse(fin, XH)
        fin.close()

        XH.emitMQL(fout)

        sys.stderr.write("Done! next_monad = %d    next_id_d = %d\n" % (XH.curmonad, XH.curid_d))

        XH.clean()

    XH.emitBookChapterMQL(fout)
    fout.close()

    #
    # Emit schema
    #
    if ".mql" in out_filename:
        schema_file_name = out_filename.replace(".mql", ".schema.mql")
    else:
        schema_file_name = out_filename + ".schema.mql"
        
    schema_fout = open(schema_file_name, "wb")
    XH.emit_schema(schema_fout)
    schema_fout.close()
    

if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] != "-o":
        sys.stderr.write("\n\nUsage:\n    python GBITrees2MQL.py -o <MQL-outfile> <infile1> [<infile2> <infile3> ... ]\n\n")
        sys.exit(1)
    else:
        doIt(sys.argv[2], sys.argv[3:])
        sys.exit(0)


import os
from bs4 import BeautifulSoup
import bs4


from djangocms_site_importer.management.core.ElementParser import *
from djangocms_site_importer.management.core.HeadingParser  import *
from djangocms_site_importer.management.core.ParagraphParser import *
from djangocms_site_importer.management.core.SectionParser import *
from djangocms_site_importer.management.core.TextParser import *
from djangocms_site_importer.management.core.DivParser import *

class PageParser:
    element_list = []
    parser_list = [DivParser, HeadingParser, ParagraphParser, SectionParser, TextParser]
    parse_tree = []

    def __init__(self, filepath):
        self.element_list = []
        self.filepath = filepath

    
    def parseFile(self):
        with open(self.filepath) as fp:
                soup = BeautifulSoup(fp, "html.parser")

                if(soup is not None and soup.head is not None):
                    for child in soup.body:
                        #print("Child: " + str(child.name) + "   " + str(child))
                        self.parseSection(child, str(child.name))

    def parseSection(self, section, tag, parent=None):

        if(tag != None and tag != "None"):
            print("Parsing Tag")
            for p in self.parser_list:
                
                #print("THis: " + HeadingParser.getElementType())
                #print("tag: " + tag)

                #print("Does it start? " + str(tag.startswith(p.getElementType())))
                if(tag.startswith(p.getElementType())):
                    
                    print("Tag Starts with it " + p.getElementType())
                    # instantiate it
                    #print(p.getElementType())
                    parser_object = type(p)

                    klass = globals()[p.__name__]
                    instance = klass(section, tag)
                    #instance.print()

                    if(parent is None):
                        #print("Top")
                        self.parse_tree.append(instance)
                    else:
                        #print("Child of ")
                        #parent.print()
                        parent.children.append(instance)

                    for child in section:
                        #print("CHild Type:" + str(type(child)))
                        #print("=================================================")
                        #print(child)
                        #print("=================================================")
                        #if child != None and child.name != None:
                        if type(child) is not bs4.element.NavigableString:
                            print("Parsing  child  " + child.name)
                            #print("parsing child in section" + str(child))
                            #if(child.tag != "None"):
                            #print("Child Name: " + child.name)
                            #print("Child Tag: " + child.tag )
                            self.parseSection(child, child.name, parent=instance)

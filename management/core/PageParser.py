import os
from bs4 import BeautifulSoup
import bs4

from djangocms_site_importer.management.core.ElementParser import *
from djangocms_site_importer.management.core.HeadingParser  import *
from djangocms_site_importer.management.core.ParagraphParser import *
from djangocms_site_importer.management.core.SectionParser import *
from djangocms_site_importer.management.core.TextParser import *
from djangocms_site_importer.management.core.StrongParser import *
from djangocms_site_importer.management.core.DivParser import *
from djangocms_site_importer.management.core.olParser import *
from djangocms_site_importer.management.core.liParser import *
from djangocms_site_importer.management.core.iParser import *
from djangocms_site_importer.management.core.linkParser import *
from djangocms_site_importer.management.core.tableParser import *
from djangocms_site_importer.management.core.imageParser import *

class PageParser:
    element_list = []
    parser_list = [DivParser, 
                   HeadingParser, 
                   ParagraphParser, 
                   SectionParser, 
                   TextParser, 
                   StrongParser,
                   liParser,
                   olParser,                   
                   linkParser,
                   tableParser,
                   imageParser,
                   iParser]
    
    parse_tree = []
    

    def __init__(self, filepath):
        self.element_list = []
        self.filepath = filepath
        self.page_name = ""

    def checkChildValid(self, child):
        if(child is not None and child != "None" and child.name != None):
            return True
        else:
            return False
        
    def parseFile(self):
        with open(self.filepath) as fp:
            soup = BeautifulSoup(fp, "html.parser")

            if(soup is not None and soup.head is not None):

                # Extract Title
                self.page_name = soup.find_all('title')[0].string.split('|', 1)[0]
                new_page = self.createPage(self.page_name)
                                    
                if(new_page is not None):                        
                    page_placeholder = new_page.placeholders.all()[0]
                    self.processChildren(soup.body, new_page, parent_plugin=None)
                    

    def processChildren(self, children, page, parent_plugin=None):
        # Iterate over all items in 
        for child in children:

            #print("Process Children Child " + str(child))
            if(self.checkChildValid(child)):
                print("=======================================================================")
                print("Child: Name: " + str(child.name))

                from cms.api import add_plugin

                tag = child.name

                parser = None

                if(tag != None and tag != "None"):            
                    for p in self.parser_list:
                        if(tag.startswith(p.getElementType())):
                            
                            parser_object = type(p)

                            klass = globals()[p.__name__]
                            parser = klass(child, tag, self.filepath)

                            if(parser is not None):

                                print("Found parser: " + parser.ElementType)

                                page_top_placeholder = page.placeholders.all()[0]

                                new_plug = parser.createPlugin(page_top_placeholder, parent_plugin)

                                if(parser.allowChildren()):
                                    # Process children of the child
                                    self.processChildren(child, page, parent_plugin=new_plug)
                            break                                          
                                            
        
    def createPage(self, name):
        from cms.api import create_page
        new_page = create_page(name, language='en', template='bootstrap5.html')
        return new_page

    def getParser(self, section, tag):
        if(tag != None and tag != "None"):            
            for p in self.parser_list:
                if(tag.startswith(p.getElementType())):
                    
                    print("Tag Starts with it " + p.getElementType())                    
                    parser_object = type(p)

                    klass = globals()[p.__name__]
                    parserInstance = klass(section, tag)
                    return parserInstance
                else:
                    print("No Parser")
                    return None
        else:
            print("Error Getting parser")
            return None
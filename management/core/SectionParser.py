from djangocms_site_importer.management.core.ElementParser import *

class SectionParser(ElementParser):
    ElementType = "section"
    def __init__(self, element, tag, filepath):
        super().__init__(element, tag, filepath)
        self.ElementType = "section"

    def print(self, pre=""):
        #print("This is " + __name__)
        super(DivParser, self).print(pre)

    def getSectionName(self):
        return "section"
from djangocms_site_importer.management.core.TextParser import *

class ParagraphParser(TextParser):
    ElementType = "p"
    def __init__(self, element, tag, filepath):        
        super().__init__(element, tag, filepath)
        self.ElementType = "p"
        
    # def print(self, pre=""):
    #     super(ParagraphParser, self).print(pre)

    # def getPluginName(self):
    #     return "TextPlugin"
    
    # def getPluginBody(self):
    #     return self.element.get_text()
    
    # def createPlugin(self, parent, placeholder):
    #     from cms.api import add_plugin
        
    #     print("Attributes: " + self.getAttributesStr())
    #     body = "<" + self.tag + " " + self.getAttributesStr() + "> " + self.getPluginBody() + "</" + self.tag + ">"
    #     print("heADING BODY: " + body)
    #     add_plugin(parent, 
    #                self.getPluginName(), 
    #                'en', 
    #                body=body, 
    #                target=placeholder)
    
    # def export(self):
    #     pass
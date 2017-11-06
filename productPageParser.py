from HTMLParser import HTMLParser

class ProductPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #self.data = {}
        #self.inProductNameTag = False
        self.clean()

    def clean(self):
        self.data = {}
        self.inProductNameTag = False

    
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            name = attr[0]
            value = attr[1]
            if name == 'id' and value == 'dp-summary-see-all-reviews':
                for attr1 in attrs:
                    if attr1[0] == 'href':
                        #print attr1
                        self.data['reviewListLink'] = attr1[1]

        for attr in attrs:
            name = attr[0]
            value = attr[1]
            if name == 'id' and value == 'productTitle':
                self.inProductNameTag = True

    def handle_endtag(self, tag):
        if self.inProductNameTag:
            self.inProductNameTag = False

    def handle_data(self, data):
        if self.inProductNameTag:
            list = data.split("\n")
            list = [str for str in [str.strip() for str in list] if len(str) > 0]
            self.data['productTitle'] = list[0]



#class ProductPageParser:
#    def __init__(self):
#        self.data = {}
#
#    def feed(self, text):
#        self.data['reviewListLink'] = self.getAllPageLinkFromProdPage(text)
#
#
#    def getAllPageLinkFromProdPage(self, pageContent):
#        HTML_ID = 'dp-summary-see-all-reviews'
#        #HREF_REGEXP = "href=\".*\""
#
#        idIndex = pageContent.find(HTML_ID)
#        closeIndex = pageContent.find('>', idIndex)
#        #print idIndex, closeIndex
#        targetSubString = pageContent[idIndex:closeIndex]
#        #print targetSubString
#
#        beginIdx = targetSubString.find("href=")
#        #print beginIdx
#        return targetSubString[beginIdx + 6: -1]

#    f = open('./product.html')
#    lines = f.readlines()
#    f.close()
#    
#    str = "\n".join(lines)
#    
#    parser = ProductPageParser()
#    parser.feed(str)
#    
#    print parser.data

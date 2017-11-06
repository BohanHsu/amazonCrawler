from HTMLParser import HTMLParser

class ProductListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.clean()

    def clean(self):
        self.links = []
        self.data = {'links': self.links}
        self.inResultList = False
        self.resultListDepth = 0

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            name = attr[0]
            value = attr[1]
            if name == 'href' and value.find('https://www.amazon.com') >= 0:
                for attr1 in attrs:
                    if attr1[0] == 'title':
                        if self.inResultList:
                            #if value.find('gp') < 0 and value.find('dp') < 0:
                            #print value[23:25]
                            if len(value) > 23 and value[23:25] != 'dp':
                                self.links.append(value)

        for attr in attrs:
            name = attr[0]
            value = attr[1]
            if name == 'id' and value == 's-results-list-atf':
                #print 'maizi maozi'
                self.inResultList = True
                
        if self.inResultList:
            self.resultListDepth += 1
        
    def handle_endtag(self, tag):
        if self.inResultList:
            self.resultListDepth -= 1

        if self.inResultList and self.resultListDepth == 0:
            self.inResultList = False

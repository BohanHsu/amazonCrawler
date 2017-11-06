class UserPageParser:
    def __init__(self):
        self.clean()

    def clean(self):
        self.data = {}

    def feed(self, text):
        self.data['location'] = self.findLocation(text)
        self.data['username'] = self.findName(text)

    def findLocation(self, text):
        KEY_STRING = 'occupationLocationList'
        startIndex = text.find(KEY_STRING)
        if startIndex >= 0:
            endIndex = text.find(']', startIndex)
            startIndex = startIndex + 4 + len(KEY_STRING)
            locationString = text[startIndex:endIndex - 1]
            return ' '.join(locationString.split(','))
        else:
            return None

    def findName(self, text):
        KEY_STRING = 'nameHeaderData'
        startIndex = text.find(KEY_STRING)
        if startIndex > 0:
            startIndex = text.find('name', startIndex + 1)
            startIndex += 7
            endIndex = text.find('"', startIndex)
            return text[startIndex:endIndex]
        else:
            return None



        

#f = open('./userPage.html')
#lines = f.readlines()
#f.close()
#str = "\n".join(lines)
#
#parser = UserPageParser()
#parser.feed(str)
#print parser.data

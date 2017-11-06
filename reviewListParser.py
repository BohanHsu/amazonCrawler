from HTMLParser import HTMLParser

class ReviewListParser(HTMLParser):
    def __init__(self):
        self.clean()

    def clean(self):
        #super(ReviewListParser, self).__init__()
        HTMLParser.__init__(self)
        self.inReview = False
        self.depth = 0

        self.currentReviewId = None
        self.currentAuthorId = None

        self.data = {}
        self.reviews = {}
        self.users = {}
        self.data['reviews'] = self.reviews
        self.data['users'] = self.users

        self.inReviewDateTag = False

    def handle_starttag(self, tag, attrs):
        # find customer-review start
        for attr in attrs:
            name = attr[0]
            value = attr[1]
            if name == 'id' and value.find('customer_review') == 0:
                #print name, value
                self.currentReviewId = value[16:]
                #print self.currentReviewId
                if not self.currentReviewId in self.reviews:
                    self.inReview = True
                #else:
                    #print 'duplicate'

        # increase depth level of tag
        if self.inReview:
            self.depth += 1

        if self.inReview:
            # handle data
            reviewAuthorExist = False
            authorHref = None
            for attr in attrs:
                name = attr[0]
                value = attr[1]
                if name == 'data-hook' and value == 'review-author':
                    reviewAuthorExist = True

                if name == 'href':
                    authorHref = value

                # I found this author's link
                if reviewAuthorExist and not authorHref is None:
                    # I found one author's link
                    startIdx = authorHref.find('account')
                    startIdx += 8
                    endIdx = authorHref.find('/', startIdx)
                    #print authorHref
                    userId = authorHref[startIdx:endIdx]
                    #print 'userId =', userId
                    #print ''

                    if not self.currentReviewId in self.reviews:
                        self.reviews[self.currentReviewId] = {'userId': userId, 'userLink': authorHref}

                    if not userId in self.users:
                        self.users[userId] = True

                    reviewAuthorExist = False
                    authorHref = None
                    break

            # find review data
            if tag == 'span':
                for attr in attrs:
                    name = attr[0]
                    value = attr[1]
                    if name == 'class' and value.find('review-date') > 0:
                        self.inReviewDateTag = True



    def handle_endtag(self, tag):
        # descrese depth level of tag
        if self.inReview:
            self.depth -= 1

        # out of customer-review
        if self.depth == 0:
            self.inReview = False
            self.currentReviewId = None

        if self.inReviewDateTag:
            self.inReviewDateTag = False

    def handle_data(self, data):
        if self.inReviewDateTag:
            list = data.split(',')
            list = [str.strip() for str in list]
            list[0] = list[0][3:]
            data = ' '.join(list)
            self.reviews[self.currentReviewId]['reviewDate'] = data
        

# usage example:

#parser = ReviewListParser()
#f = open('./allReview.html')
#lines = f.readlines()
#f.close()
#str = "\n".join(lines)
#print HTMLParser
#parser.feed(str)
#print parser.reviews
#print parser.users.keys()
#print parser.data

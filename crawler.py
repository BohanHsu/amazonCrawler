from userPageParser import UserPageParser
from reviewListParser import ReviewListParser
from productPageParser import ProductPageParser
from pageDownloader import getHtmlContentByConnectionTypeSiteAndUrl

#amazonLink = "https://www.amazon.com/Coppertone-Water-Babies-Sunscreen-Lotion/dp/B00CXVOT74/ref=cm_cr_arp_d_product_top?ie=UTF8"

def only2016(review):
    dates = review['reviewDate'].split(' ')
    return int(dates[-1]) == 2016

class Crawler:
    def __init__(self, amazonLink, reviewFilter=None, test=False):
        # init varialbes
        self.test = test
        self.amazonLink = amazonLink
        self.pageDownloaderQueue = []
        self.productName = None
        self.reviewList = []
        self.ConnectionHttpType = None
        self.ConnectionHttpMethod = None
        self.ConnectionHttpSite = None
        self.userPageParser = UserPageParser()
        self.reviewListParser = ReviewListParser()
        self.productPageParser = ProductPageParser()
        self.reviewFilter = reviewFilter
        
        # parse the link
        parsedLink = self.linkParser(amazonLink)
        self.productUrl = parsedLink['url']
        self.ConnectionHttpType = parsedLink['type']
        self.ConnectionHttpMethod = parsedLink['method']
        self.ConnectionHttpSite = parsedLink['site']

        # parse product data
        self.productPageData = None
        self.getProductPageData()
        #print self.productPageData
        if ('productTitle' in self.productPageData):
            print 'Crawling: ', self.productPageData['productTitle']

        self.reviewData = {}
        self.userData = {}
        self.getReviewAndUser()

        

    def linkParser(self, link):
        list = link.split('/')
        list = [str for str in list if len(str) > 0]
        type = list[0][0:-1]
        method = 'GET'
        site = list[1]
        urlList = list[2:]
        url = "/" + '/'.join(urlList)
        return {'type': type, 'method': method, 'site': site, 'url': url}

    def getProductPageData(self):
        productPageDataString = getHtmlContentByConnectionTypeSiteAndUrl(self.ConnectionHttpType, self.ConnectionHttpMethod, self.ConnectionHttpSite, self.productUrl)
        self.productPageParser.feed(productPageDataString)
        self.productPageData = self.productPageParser.data
        self.productPageParser.clean()


    def getReviewAndUser(self):
        userToDownload = []
        pageNumber = 1
        if not 'reviewListLink' in self.productPageData:
            return

        curReviewPageUrl = self.addPageNumberToReviewListUrl(self.productPageData['reviewListLink'], pageNumber)
        #print "HTTP request:" + curReviewPageUrl
        curReviewPageContentString = getHtmlContentByConnectionTypeSiteAndUrl(self.ConnectionHttpType, self.ConnectionHttpMethod, self.ConnectionHttpSite, curReviewPageUrl)
        self.reviewListParser.feed(curReviewPageContentString)
        curReviewPageData = self.reviewListParser.data
        self.reviewListParser.clean()
        print 'Review Number in current page:', len(curReviewPageData['reviews'])

        i = 0
        while bool(curReviewPageData['reviews']) and (not self.test or i < 1) and i <= 100:
            i += 1
            # handle last downloaded page
            for reviewId in curReviewPageData['reviews']:
                if self.reviewFilter is None or self.reviewFilter(curReviewPageData['reviews'][reviewId]):
                    #print curReviewPageData['reviews'][reviewId]
                    self.reviewData[reviewId] = curReviewPageData['reviews'][reviewId]
                    userToDownload.append((curReviewPageData['reviews'][reviewId]['userId'], curReviewPageData['reviews'][reviewId]['userLink']))

            while len(userToDownload) > 0:
                user = userToDownload.pop(0)
                self.getUser(user)

            # download the next page
            pageNumber += 1
            curReviewPageUrl = self.addPageNumberToReviewListUrl(self.productPageData['reviewListLink'], pageNumber)
            #print "HTTP request:" + curReviewPageUrl
            curReviewPageContentString = getHtmlContentByConnectionTypeSiteAndUrl(self.ConnectionHttpType, self.ConnectionHttpMethod, self.ConnectionHttpSite, curReviewPageUrl)
            self.reviewListParser.feed(curReviewPageContentString)
            curReviewPageData = self.reviewListParser.data
            self.reviewListParser.clean()
            #print len(curReviewPageData['reviews'])
            print 'Review Number in current page:', len(curReviewPageData['reviews'])
            

        #print userToDownload

    def getUser(self, user):
        userId = user[0]
        userLink = user[1]
        print 'Crwaling User:', userId
        if not userId in self.userData:
            #print "HTTP request:" + userLink
            userPageContentString = getHtmlContentByConnectionTypeSiteAndUrl(self.ConnectionHttpType, self.ConnectionHttpMethod, self.ConnectionHttpSite, userLink)
            self.userPageParser.feed(userPageContentString)
            userData = self.userPageParser.data
            self.userPageParser.clean()
            userData['userLink'] = userLink
            self.userData[userId] = userData
            #print self.userData[userId]




    def addPageNumberToReviewListUrl(self, url, pageNum):
        return url + "&pageNumber=" + str(pageNum)




# test

#crawler = Crawler("https://www.amazon.com/Coppertone-Water-Babies-Sunscreen-Lotion/dp/B00CXVOT74/ref=cm_cr_arp_d_product_top?ie=UTF8")

#
#
#crawler = Crawler("https://www.amazon.com/Coppertone-Water-Babies-Sunscreen-Lotion/dp/B00CXVOT74/ref=cm_cr_arp_d_product_top?ie=UTF8", only2016)
#
#
#print crawler.reviewData
#print crawler.userData

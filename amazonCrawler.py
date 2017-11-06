from crawler import Crawler
from crawler import only2016
from fileWriter import writeLinesToFIle
import sys

def main():
    if len(sys.argv) < 2:
        print 'Usage: python amazomCrwaler.py {amazonLink}'
        return
    
    amazonLink = sys.argv[1]
    print 'Crawling:', amazonLink
    
    crawler = Crawler(amazonLink, only2016, False)

    result = handleCrawler(crawler)
    filename = "./result/" + getConnectedProductTitle(crawler) + ".csv"
    
    writeLinesToFIle(result, filename)
    print "Finish write to file:", filename

    
def handleCrawler(crawler):
    result = []
    result.append(crawler.amazonLink + "\n")
    if 'productTitle' in crawler.productPageData:
        result.append((crawler.productPageData['productTitle']).encode('utf-8').strip() + "\n")
    else:
        result.append("\n")

    result.append("reviewId, reviewDate, userId, userName, userLocation, userLink\n")

    for reviewId in crawler.reviewData:
        review = crawler.reviewData[reviewId]
        str = reviewId + ','

        if 'reviewDate' in review:
            reviewDate = review['reviewDate']
        else:
            reviewDate = ''
        str += (reviewDate + ',')

        if 'userId' in review:
            userId = review['userId']
            str += (userId + ',')
            if userId in crawler.userData:
                user = crawler.userData[userId]
                if 'username' in user:
                    str += (user['username'] + ',')
                else:
                    str += ','

                if 'location' in user:
                    str += (user['location'] + ',')
                else:
                    str += ','

                if 'userLink' in user:
                    str += (user['userLink'])

            else:
                str += ",,"
        else:
            str += ",,,"

        result.append(str.encode('utf-8').strip() + "\n")

    return result

def getConnectedProductTitle(crawler):
    title = crawler.productPageData['productTitle']
    list = title.split(' ')
    return "_".join(list)
    
    

main()

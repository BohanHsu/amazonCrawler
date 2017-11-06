from productListParser import ProductListParser
from pageDownloader import getHtmlContentByConnectionTypeSiteAndUrl
import sys

# coppertone template
#COPPERTONE_URL_TEMPLATE = "/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Acoppertone&page={}&keywords=coppertone&ie=UTF8&qid=1509839407"
# neutrogena template
#NEUTROGENA_URL_TEMPALTE = "/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Aneutrogena&page={}&keywords=neutrogena&ie=UTF8&qid=1509845011"



# exmaple
#coppertoneURL = COPPERTONE_URL_TEMPLATE.format(1)



def main():
    if len(sys.argv) < 2:
        print 'Usage: python productListCrawler.py {pattern}'
        print 'Please refer to python file for pattern detail'
        return
    
    pattern = sys.argv[1]

    # limit
    PAGE_LIMIT = 20
    print sys.argv
    if len(sys.argv) >= 3:
        print 'mazo', sys.argv
        PAGE_LIMIT = int(sys.argv[2])

    print "PAGE_LIMIT=", PAGE_LIMIT

    
    parser = ProductListParser()
    
    pageNumber = 1
    coppertoneLinkList = []
    while pageNumber <= PAGE_LIMIT:
        #url = COPPERTONE_URL_TEMPLATE.format(pageNumber)
        url = pattern.format(pageNumber)
        productListPageContentString = getHtmlContentByConnectionTypeSiteAndUrl('https', 'GET', 'www.amazon.com', url)
        parser.feed(productListPageContentString)
        print len(parser.data['links'])
        for link in parser.data['links']:
            coppertoneLinkList.append(link)
            #print link
        
        parser.clean()
    
        pageNumber += 1
    
    print "==" * 50
    for link in coppertoneLinkList:
        print link

main()

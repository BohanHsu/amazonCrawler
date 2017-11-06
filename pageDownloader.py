import httplib
import re
import random
import time


# type: "http" / "https"
# method: "GET"
# site: "www.amazon.com"
# url: "/Coppertone-Water-Babies-Sunscreen-Lotion/dp/B00CXVOT74/ref=sr_1_1_sspa?ie=UTF8&qid=1509762546&sr=8-1-spons&keywords=coppertone%2Bsunscreen&th=1"
def getHtmlContentByConnectionTypeSiteAndUrl(type, method, site, url):
    waitTime = random.randint(2,4)
    print "Wait for", waitTime, "seconds."
    time.sleep(waitTime)
    return getHtmlContentByConnectionTypeSiteAndUrlNoWait(type, method, site, url)

def getHtmlContentByConnectionTypeSiteAndUrlNoWait(type, method, site, url):
    print "HTTP: url =", url
    conn = None

    if type == 'http':
        conn = httplib.HTTPConnection(site)
    elif type == 'https':
        conn = httplib.HTTPSConnection(site)
    
    conn.request(method, url)
    resp = conn.getresponse()
    
    data = resp.read()
    return data.decode('utf-8')






#str = getHtmlContentByConnectionTypeSiteAndUrl('https', 'GET', 'www.amazon.com', '/Coppertone-Water-Babies-Sunscreen-Lotion/dp/B00CXVOT74/ref=sr_1_1_sspa?ie=UTF8&qid=1509762546&sr=8-1-spons&keywords=coppertone%2Bsunscreen&th=1')
#allReviewUrl = getAllPageLinkFromProdPage(str)

#str = getHtmlContentByConnectionTypeSiteAndUrl('https', 'GET', 'www.amazon.com', allReviewUrl)
#print str

#https://www.amazon.com/gp/profile/amzn1.account.AEWED2AD7KE2BZXHAVW53FUKUNNA/ref=cm_cr_arp_d_pdp?ie=UTF8
#"https://www.amazon.com/Coppertone-Sunscreen-Lotion-Spectrum-Ounces/dp/B074W9WQ47/ref=sr_1_6_a_it?ie=UTF8&qid=1509839407&sr=8-6&keywords=coppertone"

#str = getHtmlContentByConnectionTypeSiteAndUrlNoWait('https', 'GET', 'www.amazon.com', '/Coppertone-Sunscreen-Lotion-Spectrum-Ounces/dp/B074W9WQ47/ref=sr_1_6_a_it?ie=UTF8&qid=1509839407&sr=8-6&keywords=coppertone')
#print str


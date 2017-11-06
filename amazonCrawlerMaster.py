import subprocess
import os
import time
import sys

def getAllLinks(link):
    #if len(sys.argv) < 2:
    #f = open('./coppertone_links_target.txt')
    f = open(link)
    lines = f.readlines()
    f.close()
    return lines


def numOfPythonProcess():
    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'python'), stdin=ps.stdout)
    ps.wait()
    lines = output.split("\n")
    lines = [line for line in lines if len(line) > 0]
    return len(lines) - 1



def driving():

    if len(sys.argv) < 2:
        print "Usage: python amazonCrawlerMaster.py {filePath}"

    path = sys.argv[1]

    lines = getAllLinks(path)

    lines = [line for line in lines if len(line) > 0]

    if len(lines) == 0:
        print "No Link found from", path
        return

    while len(lines) > 0:
        nopp = numOfPythonProcess()
        if nopp > 1:
            print 'Number of python process:', nopp, ', wait for 15 seconds'
            time.sleep(15)
        else:
            link = lines.pop(0)
            crawlALink(link)
            print "??" * 50
            print 'Created a new task, Remain task after this:', len(lines)
            print "??" * 50
            
def crawlALink(link):
    os.system('python amazonCrawler.py ' + link)

#lk = 'https://www.amazon.com/Coppertone-Waterbabies-Lotion-Fluid-Ounce/dp/B0012AOMEW/ref=sr_1_3_a_it/134-0057925-9790720?ie=UTF8&qid=1509910361&sr=8-3&keywords=coppertone'
#crawlALink(lk)

driving()

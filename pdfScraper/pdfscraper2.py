import urllib # will use scrapy instead later
import json
import os, glob
import pdfminer
import slate
import time # temporary solution to prevent calling parsepdf() before download finishes
import subprocess

def readJSON():
    with open("feedexport-20.json") as jsonfile:
        data = json.load(jsonfile)
        for i in range(len(data)):
            try:
                if data[i][u'pdf']:
                    title = str(data[i][u'title'])[3:-2]
                    url = str(data[i][u'pdf'])
                    # xmlid = str(data[i][u'id'])
                print "\n" + str(i + 1) + ") Title: " + title
                download(title, url) #, xmlid)
            except KeyError:
                pass
    print "File should be closed now, waiting to finish downloads...\n"
    # time.sleep(20)
    # print "Slept 20 secs, calling parsepdf()...\n"
    parsepdf()


def download(title, url): #, xmlid):
    file = urllib.urlretrieve(url, "./PDFs/" + title + ".pdf")
    print "Downloading: " + title + ".pdf\n"

def parsepdf():
    print "parsepdf() was called...\n"
    os.chdir("./PDFs")
    for pdf in glob.glob("*.pdf"):
        pdftitle = pdf[:-4] + ".txt"

        print "Reading:" + pdf
        proc = subprocess.Popen(['pdf2txt.py', '-m 8', pdf], stdout=subprocess.PIPE)
        output = proc.stdout.read()

        print "Writing: " + pdftitle + "\n"

        savepath = "/home/edric/scraper/pdfScraper/Text/"
        filepath = os.path.join(savepath, pdftitle)
        with open(filepath, 'w') as textfile:
            textfile.write(output)

    print "\n                     ============[PROGRAM FINISHED]============\n"







# Calling pdf2txt.py script from pdfminer; only thing that works // scratch that



def main():
    readJSON()
    # parsepdf()

main()

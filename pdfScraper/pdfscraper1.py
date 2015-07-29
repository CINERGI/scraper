import urllib # will use scrapy instead later
import json
import os, glob
# import pdfminer    doesn't work -.-
import slate
import time # temporary solution to prevent calling parsepdf() before download finishes
from PyPDF2 import PdfFileReader

# !!!!!!!!!!!!!!! MAJOR ISSUE: slate library doesn't work! Error message:

# Traceback (most recent call last):
#  File "<stdin>", line 2, in <module>
#  File "build/bdist.linux-x86_64/egg/slate/slate.py", line 52, in __init__
#  File "build/bdist.linux-x86_64/egg/slate/slate.py", line 36, in process_page
# AttributeError: 'cStringIO.StringO' object has no attribute 'buf'


def readJSON():
    with open("feedexport-3.json") as jsonfile:
        data = json.load(jsonfile)
        for i in range(len(data)):
            if data[i][u'pdf']:
                title = str(data[i][u'title'])[3:-2]
                url = str(data[i][u'pdf'])
                # xmlid = str(data[i][u'id'])
            print "\n" + str(i + 1) + ") Read this title from JSON: " + title
            download(title, url) #, xmlid)
    print "=====>> File should be closed now, waiting to finish downloads...\n\n"
    time.sleep(20)
    print "=====>> Slept 20 secs, calling parsepdf()...\n\n"
    parsepdf()


def download(title, url): #, xmlid):
    file = urllib.urlretrieve(url, "./PDFs/" + title + ".pdf")
    # file = urllib.URLopener()
    # file.retrieve(url, "./PDFs/" + title + ".pdf")
    print "... Downloading: " + title + ".pdf\n"

def parsepdf():
    os.chdir("./PDFs")
    for pdf in glob.glob("*.pdf"):

        # print pdf
        # print "\n"

        try:
            # with open(pdf) as f:
            #    text = slate.PDF(f)
            # output = str.join(text)
            inputpdf = PdfFileReader(open(pdf, "rb"), strict = False)
            output = inputpdf.extractText()
            pdftitle = pdf[:-4] + ".txt"
            print "Writing: " + pdftitle + "\n"
            with open(pdftitle) as textfile:
                textfile.write(output)
        except AttributeError:
            pass

    print "              =======>>>   FINISHED   <<<======="







# Calling pdf2txt.py script from pdfminer; only thing that works // scratch that



def main():
    readJSON()
    # parsepdf()

main()

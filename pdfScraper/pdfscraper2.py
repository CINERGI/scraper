import urllib # will use scrapy instead later
import json
import os, glob
# import pdfminer // Outdated and not working; instead call shell tool
# import slate // Not working
# import time  // No longer needed; urlretrieve pauses itself until dl finishes
import subprocess

def readJSON():
    with open("feedexport-20.json") as jsonfile:
        data = json.load(jsonfile)
        for i in range(len(data)):
            try:
                if data[i][u'pdf']:
                    title = str(data[i][u'title'])[3:-2]
                    url = str(data[i][u'pdf'])
                    # xmlid = str(data[i][u'id']) // may implement later
                print "\n" + str(i + 1) + ") TITLE: " + title
                download(title, url) #, xmlid)
            except KeyError:
                pass
    print "File should be closed now, waiting to finish downloads...\n"
    # time.sleep(20) // No longer needed; urlretrieve waits until dl finishes
    # print "Slept 20 secs, calling parsepdf()...\n"
    parsepdf()


def download(title, url): #, xmlid):
    file = urllib.urlretrieve(url, "./PDFs/" + title + ".pdf")
    print "DOWNLOADED: " + title + ".pdf\n"

def parsepdf():
    print "parsepdf() was called...\n"
    os.chdir("./PDFs")
    for pdf in glob.glob("*.pdf"):
        filename = pdf[:-4] + ".txt"

        print "READING: " + pdf
        proc = subprocess.Popen(['pdf2txt.py', '-m 8', pdf], stdout=subprocess.PIPE)
        output = proc.stdout.read()

        print "WRITING: " + filename + "\n"

        savepath = "/home/edric/scraper/pdfScraper/Text/"
        filepath = os.path.join(savepath, filename)
        with open(filepath, 'w') as f:
            f.write(output)

    print "\n                  ============[PARSING FINISHED]============\n"

# TO DO: extract abstract/intro from txt. Problem is variations in formatting.
# See ./Text/ folder for examples of quirks of the pdf scraper
# Issues: random(?) newlines, Unicode form feed characters

def main():
    readJSON()

main()

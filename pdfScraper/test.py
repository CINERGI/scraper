import urllib

testfile = urllib.URLopener()
testfile.retrieve("http://pubs.usgs.gov/bul/0520i/report.pdf", "THE RAMPART AND HOT SPRINGS REGIONS.pdf")

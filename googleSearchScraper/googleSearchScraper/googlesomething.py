import mechanize

br = mechanize.Browser()

br.set_handle_robots(False)

br. addheaders = [("User-agent", "Chrome/43.0.2357.130")]

q = raw_input("enter the keyword::")

qe=""

alert = ""
for i in range(0, len(q)):
  if q[i] ==" ":
    qe+="+"
  else:
    qe+=q[i]

counter = 0

for i in range(0,9):
  google_url = br.open("https://www.google.com/search?q=" + qe + "&amp;start=" + str(counter))
  search_keyword = google_url.read()
  if "http://www.thetaranights.com" in search_keyword:
    alert = "found"
    break
  counter+=10

if alert == "found":
  print "Found at page:: ",i+1
else:
  print "not found"

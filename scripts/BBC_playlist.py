import requests

plsdir = "/home/pi/radio/"       #set the directory

#list the BBC pls files here:
stations = {
    'BBC1'      : 'http://www.bbc.co.uk/radio/listen/live/r1_aaclca.pls',
    'BBC2'      : 'http://www.bbc.co.uk/radio/listen/live/r2_aaclca.pls',
    'BBC3'      : 'http://www.bbc.co.uk/radio/listen/live/r3_aaclca.pls',
    'BBC4'      : 'http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls',
    'BBC4Extra' : 'http://www.bbc.co.uk/radio/listen/live/r4x_aaclca.pls',
    'BBC5LiveSX': 'http://www.bbc.co.uk/radio/listen/live/r5lsp_aaclca.pls',
    'BBC6Music' : 'http://www.bbc.co.uk/radio/listen/live/r6_aaclca.pls',
}

def fetch_stream(url):
    #what we're looking for
    search='File1='
    r = requests.get(url)
    if r.status_code == 200:
        for line in r.text.splitlines():
            if search in line:
                return line.lstrip(search)


#file = open (plsdir + "bbc.pls", "w+") #opens the file, +w creates it if it doesn't exist
def generate():
    for (name,url) in stations.iteritems():
        file = open(plsdir + name + '.m3u','w+')
        file.write('#EXTM3U\n')
        file.write('\n')
        file.write('#EXTINF:-1, %s\n' % name)
        file.write(fetch_stream(url) + '\n')
        file.close()

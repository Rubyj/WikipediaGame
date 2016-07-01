from bs4 import BeautifulSoup
import urllib2
import re

#Gets all the links for a given URL of a valid wikipedia article
def getLinks(url):
    linkList = []
    html = urllib2.urlopen(url)
    bsObj = BeautifulSoup(html)
    # filter out the content we need using the appropriate selectors and filters
    for link in bsObj.find("div", {"id":"mw-content-text"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            # build the appropriate wikipedia URL
            linkList.append("http://en.wikipedia.org" + link.attrs['href'])
    return linkList

#Run the BFS search from start wiki article (URL) to end wiki article (URL)
def bfs(start, end):
    visited_sites = []
    #This is necesarry so that the first article we hit is not just "Special:Random"
    response = urllib2.urlopen(start)
    start = response.geturl()

    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])

    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        # do not try and visit the node if we have already
        if not node in visited_sites:
            visited_sites.append(node)
            try:
                links = getLinks(node)
                for link in links:
                    new_path = list(path)
                    new_path.append(link)
                    queue.append(new_path)
                    if link == end:
                        return new_path
            except:
                pass

# run the algorithm
print bfs("http://en.wikipedia.org/wiki/Special:Random", "http://en.wikipedia.org/wiki/Adolf_Hitler")

import csv 
import requests 
import xml.etree.ElementTree as ET 

def getImage(image_url, image_name):

    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)

###############
# get URL's
def parseXML(xmlfile): 
  
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
    newsitems = [] 
  
    # iterate news items 
    for item in root.findall('./channel/item'): 
        # empty news dictionary 
        news = {} 
        # iterate child elements of item 
        for child in item: 
            # special checking for namespace object content:media 
            if child.tag == '{http://search.yahoo.com/mrss/}content': 
                news['media'] = child.attrib['url'] 
            else: 
                news[child.tag] = child.text.encode('utf8')  
        # append news dictionary to news items list 
        newsitems.append(news)    
    # return news items list 
    return newsitems 

def main(): 
    # load rss from web to update existing xml file 
    #loadRSS() 

    # parse xml file 
    dataFile = 'data/first_100k.json'
    items = parseXML(dataFile) 
  
    # store news items in a csv file 
    #savetoCSV(newsitems, 'topnews.csv') 
    # save image
    data_dir = 'data/images/'
    image_url = 'http://2.americanart.si.edu/images/1970/1970.154_1a.jpg'
    image_name = data_dir + image_url.rsplit('/', 1)[1]
    print(image_url, image_name)
    getImage(image_url, image_name)
      
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 
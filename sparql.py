import os
import wget
import time
import logging
from lxml import etree
from SPARQLWrapper import SPARQLWrapper

# save location...............
imagePath = "data/images/"
logFilePath = "data/"

#logging
logFile = logFilePath + time.strftime("%Y%m%d-%H%M%S") + ".log"
logging.basicConfig(filename=logFile,level=logging.INFO)

# sparql
offset = 0          # absolute location
limit = 500         # batch size
maxOffset = 10000     # last absolute location
sparqlHost  = "https://triplydb.com/smithsonian/american-art-museum/sparql/american-art-museum"
ns = {'sparql' : 'http://www.w3.org/2005/sparql-results#'}

while offset < maxOffset :
    # query the smithsonian with sparql
    try :
        queryString = "SELECT ?sub WHERE {{?sub ?pred ?obj .}} order by desc(?sub) LIMIT {} OFFSET {}".format(limit,offset)
        offset = offset + limit
        sparql = SPARQLWrapper(sparqlHost)
        sparql.setQuery(queryString)
        response = sparql.query().response
        print("\nQuerystring: {}".format(queryString))
        logging.warn(queryString)
    except(Exception) :
        print("Error on SPARQL : " + queryString)
        break
    
    ## parse with etree
    try :
        root = etree.parse(response).getroot()
        urls = root.findall('.//sparql:uri', ns)
        # temp save
        #my_tree = etree.ElementTree(root)
        #with open('./filename', 'wb') as f:
        #    f.write(etree.tostring(my_tree))
    except(Exception) :
        print("Error parsing XML")

    # iterate over images and save
    for img_uri in urls:
        try :
            uri = img_uri.text
            filename = imagePath + uri.rsplit('/', 1)[1]
            
            if os.path.isfile(filename) :
                print("Skipping: {}".format(filename))
            else :
                wget.download(uri, filename)
                print("\nURI retrieved: {} File saved: {}".format(uri,filename))
            # record Uri
            logging.info(uri)
        except(Exception) :
            print(("Error saving uri: {} file {}").format(uri,filename))
            continue





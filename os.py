import requests
import json
#from opensextant.xlayer import XlayerClient
url = "http://localhost:8787/xlayer/rest/control"

class Annotations(object):
    TAXON_TYPES = ["Person.", "nationality.", "Org."]
    def __init__(self, data):
        status = data.get("response", {}).get("status")
        if status != "ok":
            raise ValueError("Invalid Annotations: Received status: "+str(status))
        
        if data.get("response", {}).get("numfound", 0) == 0:
            raise ValueError("No Annotations found in text")

        self._annons = []
        self.__process(data.get("annotations", []))
    
    def __process(self, data):
        for anon in data:
            self._annons.append(anon)
    
    def Types(self):
        """List all the unique Taxonimies in the code"""
        taxons = set()
        for a in self._annons:
            if a.get("type") == "taxon":
                taxons.add(a.get("taxon", "").split(".")[0])
                continue
            taxons.add(a.get("type"))
        return list(taxons)
    
    def Coordinates(self):
        for a in self._annons:
            if "feat_class" in a:
                yield a

class XLayer(object):
    TAXON_TYPES = ["person", ""]
    def __init__(self, url):
        url = url.rstrip("/")
        if url.endswith("/control"):
            url = "/".join(url.split("/")[:-1])
        elif url.endswith("/xlayer"):
            url += "/rest"
        elif url.endswith("/rest"):
            pass
        else:
            url += "/xlayer/rest"
        print(url)
        self._url = url
    
    def ping(self):
        result = requests.get(self._url + "/control/ping")
        return result.json().get("status") == "OK"
    
    def process(self, data):
        data = {"text": data}
        result = requests.post(self._url + "/process", data=json.dumps(data))
        result = result.json()
        return Annotations(result)
        

client = XLayer(url)

print(client.ping())
with open("test.txt") as fil:
    data = client.process(fil.read())

print(data.Types())

for i in data.Coordinates():
    print(i)
    input()
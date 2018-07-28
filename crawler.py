
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Crawler():
    base_url = ""
    http = ""
    base = ""
    depth = 5
    content_regex = ""
    keywords = [] # sayfada aranacak kelimeler
    allowed_subdomains = []
    except_extensions = []
    content_class=""
    scanned_links = []

    allow_subdomain = False
    headers = {
            'User-Agent': 'My User Agent 1.0',
        }

    def __init__(self,base_url):
        ## Url kontrolü yap
        self.base_url = base_url
        self.http = base_url.split("/")[0]
        self.base = base_url.split("/")[2]
    
    def parse(self):
        if self.base_url != "":
            links = (self.travel(self.base_url,[],5))
            results = []
            for link in links:
                response = requests.get(link,headers=self.headers,verify=False)
                parsed_html = BeautifulSoup(response.text,"lxml")
                parsed_body = parsed_html.body
                prettified = parsed_body.prettify()
                res = []
                is_found = 0
                for keyword in self.keywords:
                    is_found = str(prettified).find(keyword)
                if(is_found>0):
                    founded = re.findall(self.content_regex,prettified,re.S|re.I|re.UNICODE)
                    if len(founded)>0:
                        results.append(re.sub(r"\n+","\n",BeautifulSoup(founded[0],"lxml").get_text()))
            return results
    
    def travel(self,link,scanned=[],depth=depth):
        if link not in scanned and link[-4:] not in self.except_extensions:
            scanned.append(link)
            #print(link)
            #print(depth)
            if depth > 0:
                urls = self.get_links_from_page(link)
                for url in urls:
                    self.travel(url,scanned,depth-1)
        return scanned

    def get_links_from_page(self,url):
        links = []
        try:
            response = requests.get(url,headers=self.headers,verify=False)
            #print(response.text)
            regex_link = "<[ ]*a[^<>]+href=[\"']+([a-zA-Z0-9:\/\.\-%üıöğçşÜİÖĞÇŞ]+)[\"']+"
            results = re.findall(regex_link,response.text,re.I)
            for result in results:
                temp = ""
                if(len(result)>1 and result[0]=="/" and  result[1]=="/"):
                    temp = (result.replace("//",self.http))
                elif(result[0]=="/"):
                    temp = (self.base_url+result[1:])
                else:
                    temp = (result)
                if (temp not in links and temp != self.base_url)or temp in self.allowed_subdomains:
                    if self.allow_subdomain== False and temp.find(self.base_url)==0:
                        links.append(temp)
                    elif self.allow_subdomain == True:
                        matched = re.match('(http|https):\/\/([a-zA-Z_-]+\.)+'+self.base+'[a-zA-Z0-9\/\.\-%üıöğçşÜİÖĞÇŞ]+',temp)
                        #print(matched)
                        if matched != None:
                            links.append(matched.group(0))

            return (links)
        except requests.exceptions.ConnectionError:
            return links
        
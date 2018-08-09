# -*- coding: utf-8 -*-
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from queue import Queue
import threading
import time

class Crawler():
    debug_mode = False
    url = ''
    base_url = ''
    thread_count=4
    queue = None
    visited = None
    limit = 0
    data = None
    data_regex = None
    # for now  we suppose urls will be normal
    def __init__(self,url,thread_count=4,limit = 100,data_regex=None,debug_mode=False):
        if url[-1:]!="/":
            url +="/"
        Crawler.url = url
        Crawler.thread_count = thread_count 
        Crawler.queue = Queue()
        Crawler.visited = set()
        Crawler.limit = limit
        Crawler.data = set()
        Crawler.data_regex = data_regex
        Crawler.debug_mode = debug_mode
    
    def parse(self):
        if self.url[0:4]!="http":
            print("[!] Please set a protocol for url"+self.url)
            return []
        if Crawler.debug_mode:
            print("Parsing started.")
        Crawler.visited.add(self.url)
        for i in Crawler.normalize_links(Crawler.get_links(self.url),Crawler.url):
            if i not in Crawler.visited:
                if i[-4:] in [".jpg",".png",".gif",".exe",".pdf"]:
                    continue
                self.queue.put(i)
                
        #names = ["herro"]
        names = ["herro","ceymi","merro","minik"]
        workers = []
        for name in names:
            w = self.Worker(name)
            w.setDaemon(True)
            w.start()
            workers.append(w)

        for worker in workers:
            worker.join()
        
        return Crawler.data

    @staticmethod
    def get_base_url(url):
        return (url.split("://")[1]).replace("www.","").replace("/","")

    @staticmethod
    def normalize_links(link_list,url):
        normalized_links = []
        for link in link_list:
            if len(link)>1:
                link = link.lower()
                temp = ""
                if link[0:2]=="//":
                    temp = link.replace("//",url.split("://")[0]+"://")
                elif link[0]=="/" :
                    temp = url+link[1:]
                elif link[0:4]!="http":
                    temp = url + link
                else:
                    temp = link

                if temp not in normalized_links and temp != url :
                    matched = re.search('^(http|https):\/\/(www\.|www2\.)*'+Crawler.get_base_url(url)+'.+',temp)
                    if matched != None:
                        normalized_links.append(temp)
                    
        return normalized_links

    @staticmethod
    def get_links(url):
        try:
            if Crawler.debug_mode:
                print("Looking to "+url)
            response = requests.get(url,verify=False,timeout=5)
            regex_link = "<[ ]*a[^<>]+href=[\"']?([^\"'\#]+)[\"']?"
            results = re.findall(regex_link,response.text,re.I)

            if Crawler.data_regex != None:
                datas = re.findall(Crawler.data_regex,response.text,re.I)
                for data in datas:
                    Crawler.data.add(data)

        except :
            print("Error happened")
            return []
        return results

    class Worker(threading.Thread):
        worker_name = ""
        lock = None
        def __init__(self,name):
            threading.Thread.__init__(self)
            self.worker_name = name          
            self.lock = threading.Lock()
        
        def run(self):
            if Crawler.debug_mode:
                print(self.worker_name + " started to working..")
            while Crawler.queue.empty() == False :
                
                if len(Crawler.visited) > Crawler.limit:
                    break
                link = Crawler.queue.get()
                if link in Crawler.visited:
                    continue
                if Crawler.debug_mode:
                    print(" Visited: "+str(len(Crawler.visited)))
                Crawler.visited.add(link)
                

                links = Crawler.normalize_links(Crawler.get_links(link),Crawler.url)
                for i in links:
                    if Crawler.base_url in i :
                        if i not in Crawler.visited: 
                            if i[-4:] in [".jpg",".png",".gif",".exe",".pdf"]:
                                continue
                            Crawler.queue.put(i)
                       
            if Crawler.debug_mode:
                print(self.worker_name + " finished its job.")
            #Crawler.queue.task_done()

            

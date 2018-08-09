# pycrawler
This repo presents Crawler class. Crawler class can go to any domain or/and it's subdomains and it returns requested data. Crawler uses DFS algorithm. If you use this class and you get an error please let me know.

### Example Usage
```
import crawler

site = "http://www.targetsite.com/"
c = Crawler(site,limit=50,data_regex="search_regex",debug_mode=False)
```

__limit__: Queue limit
__data_regex__:  This variable indicates what content will be searched. 

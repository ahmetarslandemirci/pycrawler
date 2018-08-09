# pycrawler
This repo presents Crawler class. Crawler class can go to any domain and it returns requested data. 
### Example Usage
```
import crawler

site = "http://www.targetsite.com/"
c = Crawler(site,limit=50,data_regex="search_regex",debug_mode=False)
```

__limit__: Queue limit
__data_regex__:  This variable indicates what content will be searched. 

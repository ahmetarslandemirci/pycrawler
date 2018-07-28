# pycrawler
This repo presents Crawler class. Crawler class can go to any domain or/and it's subdomains and it returns requested data. Crawler uses DFS algorithm. If you use this class and you get an error please let me know.

### Example Usage
```
import crawler
import re

c = crawler.Crawler("http://yoururl.com")
c.keywords = ["word1"]
c.except_extensions = [".pdf"] 
c.depth = 1
c.content_regex = "<div>(.+)<\\div>"
c.allow_subdomain = False

for result in c.parse():
    print(result)
```

__keywords__: This defines the words that crawler will search for on the page.
__except_extensions__:  Crawler will not follow these extensions.
__depth__: Maximum depth
__content_regex__: This field indicates exactly where the words are to be searched. 
__allow_subdomain__: If it is not True, crawler will not follow subdomains.

# scpscraper

A small scraper powered by Python and BeautifulSoup to scrape contents of the [SCP Wiki](http://www.scp-wiki.net).

It tries its best to scrape the page for a single SCP to return the following output:
```js
{
    "content": {
        "Description": "...",
        "Item #": "SCP-002",
        "Object Class": "Euclid",
        "Reference": "...",
        "Special Containment Procedures": "..."
    },
    "discussion": "http://www.scp-wiki.net/forum/t-76632/scp-002",
    "id": 2,
    "image": {
        "caption": "SCP-002 in its containment area",
        "src": "http://scp-wiki.wdfiles.com/local--files/scp-002/800px-SCP002.jpg"
    },
    "last_edited": 1409940932,
    "name": "The \"Living\" Room",
    "rating": 327,
    "revision": 45,
    "tags": [
        "alive",
        "euclid",
        "featured",
        "scp",
        "structure",
        "transfiguration"
    ]
}
```

It's quick to fail though, expect lots of errors.

There's also a small Flask server included that throws the above content back as JSON on `127.0.0.1:8080/scp/<id>`.
Why? 'cause.

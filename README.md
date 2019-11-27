# NTHU Crawler

NTHU Crawler is a python crawler module dedicated to crawling NTHU's school website data which is related to student affairs.

[![release](https://img.shields.io/badge/release-v1.0.1-blue.svg)](https://github.com/music1353/NTHU-Crawler) [![Python](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)



## Requirements

> Environment：Python 3.7

> Support Database：MongoDB 4.0

- pymongo
- pyquery



## Features

* Multi-threaded architecture to perform crawler tasks.
* Use queue as a buffer mechanism for data crawled from the crawler.
* Compare crawled data and stop crawling.



## Get Started

Clone or Download the project, and put nthu_crawler to your module folder.



## How it works

There are some concept words you need to know before browsing this document

* **subject**：Students may ask about topic categories for school affairs.
* **site**：The website structure type of the NTHU website. Respectively website type need different crawler algorithm to complete the mission.

* **store**：The queue temporarily used to store the data crawl from the NTHU Crawler



1. There are several subjects that we defined before

   ~~~python
   SUBJECT_DICT = {
       'event': {
           'subject': 'event',
           'bow': ['活動']
       }, 
       'speech': {
           'subject': 'speech',
           'bow': ['演講', '講座']
       }
   }
   ~~~

   * subject：Students may ask about topic categories for school affairs
   * bow：Possible words in title

2. Use `add_mission` method to add crawl mission that respectively type of site. You need to pass two arguments - site type and URL of the website you want to crawler.

   ~~~python
   crawler.add_mission('site_type', 'url')
   ~~~

3. Start to run the crawler! The data will put into the store.

4. Use `save` method can save data to mongo from store.



## Examples

* Add crawler mission and Start!

  ~~~python
  import nthu_crawler
  
  # instance of nthu crawler, it will default connect to local mongodb
  crawler = nthu_crawler.Crawler()
  
  # add mission to Crawler
  crawler.add_mission('billboard', 'http://bulletin.web.nthu.edu.tw/files/40-1912-5084-1.php?Lang=zh-tw')
  
  # run missions
  crawler.run()
  ~~~

* View data in store

  ~~~python
  # view the specific subject data which in store
  crawler.show_store('speech')
  
  # view all store of subject
  crawler.show_size()
  ~~~

* Save data to mongo

  ~~~python
  crawler.save()
  ~~~




## Connect to your own Mongo Server

The nthu crawler provide `connect_db`, `set_db_name` and `set_collect_name` methods.

Following is the example

~~~python
# connect to your own mongo server
crawler.connect_db('MONGO_URI')

# set database name and collect name is that you want to save the data
crawler.set_db_name('DB_NAME')
crawler.set_collect_name('COLLECT_NAME')
~~~



## License

2019, Ching-Hsuan Su 蘇靖軒
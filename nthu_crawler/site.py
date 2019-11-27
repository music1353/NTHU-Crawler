'''Implement crawler classes to crawl respectively structure type of NTHU website.'''

import time
from pyquery import PyQuery
from nthu_crawler.subject import SUBJECT_DICT
from nthu_crawler.store import SUBJECT_QUEUE_DICT


class Site:
    '''Parent class of different site's class'''

    def form(self, timestamp, date, title, url):
        '''Unified format of return data:
            data_result = {
                'timestamp': timestamp,
                'date': date,
                'title': title,
                'url': url
            }
        '''

        return_form = {
            'timestamp': timestamp,
            'date': date,
            'title': title,
            'url': url
        }
        return return_form
    
    def classify(self, text):
        '''classify the title is belong to which subject.
            Input: str title
            Output: str The subject of the title
        '''
        
        flag = False # whether has key word
        subject = '' # subject of title
        
        for subject_key in SUBJECT_DICT.keys():
            obj = SUBJECT_DICT[subject_key]
            for bow in obj['bow']:
                if bow in text:
                    flag = True
                    subject = obj['subject']
        
        if flag == True:
            return subject
        else:
            return None;

    def store(self, timestamp, date, title, url):
        '''store records to queue'''

        # 分到不同subject的queue
        subject = self.classify(title)
        if subject:
            SUBJECT_QUEUE_DICT[subject]['store'].put(self.form(timestamp, date, title, url))



class Billboard(Site):
    '''清華公佈欄'''

    def re_date(self, text):
        chars = "[] "
        for c in chars:
            text = text.replace(c, '')
        return text

    def go(self, url):
        dom = PyQuery(url=url, encoding="utf-8")
        events = dom('.h5').items()

        for item in events:
            # timestamp
            t = time.time()
            timestamp = int(t)
            
            # date
            date = item('.date').text()
            date = self.re_date(date)
            
            # name & url
            url_dom = item('a')
            title = url_dom.text()
            url = url_dom.attr.href

            self.store(timestamp, date, title, url)
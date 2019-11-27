'''The Craweler design for crawling the data from NTHU website.
    - Version: 1.0.1
    - Author: Ching-Hsuan Su (Jenson) on 2019/11/25.
    - Requirements:
        pyquery
        pymonogo
    - Support Site:
        Billboard
'''

# set SUBJECT_QUEUE_DICT
import queue
from nthu_crawler.crawler import Crawler
from nthu_crawler.store import SUBJECT_QUEUE_DICT
from nthu_crawler.subject import SUBJECT_DICT


for subject_key in SUBJECT_DICT.keys():
    q = queue.Queue()
    q_dict = {
        'subject': subject_key,
        'store': q
    }
    SUBJECT_QUEUE_DICT[subject_key] = q_dict
    print('complete set', subject_key, 'queue')
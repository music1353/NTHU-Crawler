'''the main crawler class for running crawler mission'''

import time
import threading
import pymongo
import copy
from nthu_crawler.site import Billboard
from nthu_crawler.subject import SUBJECT_DICT
from nthu_crawler.store import SUBJECT_QUEUE_DICT

class Crawler:
    def __init__(self):
        self._mission = [] # crawler mission
        
        # connect to mongo
        DB_NAME = 'nthu_db'
        COLLECT_NAME = 'data'
        try:
            self._client = pymongo.MongoClient()
            self._db_name = DB_NAME
            self._collect_name = COLLECT_NAME
            print('connect to localhost mongodb success')
        except:
            raise Warning("local doesn't running mongo, can use connect_db method to connect your mongo server")

    def connect_db(self, MONGO_URI):
        self._client = pymongo.MongoClient(MONGO_URI)
        print('connect to', MONGO_URI, 'success')

    def set_db_name(self, db_name):
        self._db_name = db_name
    
    def set_collect_name(self, collect_name):
        self._collect_name = collect_name

    def show_mission(self):
        for mission in self._mission:
            print(mission)

    def add_mission(self, source, url):
        if source == 'billboard':
            # self._mission.append(billboard(url))
            mission_dict = {
                'site': Billboard(),
                'url': url
            }
            self._mission.append(mission_dict)

    def run(self):
        threads = []
        for mission in self._mission:
            t = threading.Thread(target=mission['site'].go(mission['url']))
            threads.append(t)
            
        for t in threads:
            print(t, 'thread start !')
            t.start()
            
        for t in threads:
            t.join()

    def show_store(self, subject=None):
        if subject is None:
            print(SUBJECT_QUEUE_DICT)
        else:
            q = SUBJECT_QUEUE_DICT[subject]['store']
            records = []
            for item in list(q.queue):
                records.append(item)

            print(records)
    
    def show_size(self, subject=None):
        if subject is None:
            for subject_name in SUBJECT_DICT.keys():
                q = SUBJECT_QUEUE_DICT[subject_name]['store']
                print(subject_name, 'size:', q.qsize())
        else:
            subject = SUBJECT_QUEUE_DICT[subject]
            q = subject['store']
            print(subject, 'size:', q.qsize())

    def save(self):
        db = self._client[self._db_name]
        collect = db[self._collect_name]
        
        for subject in SUBJECT_DICT.keys():
            # if the subject is not exist, create one
            doc = collect.find_one({'subject': subject}, {'_id': False})
            if doc is None:
                subject_doc = {
                    'subject': subject,
                    'data': []
                }
                collect.insert_one(subject_doc)

            # last record
            try:
                last_record = doc['data'][0]
                last_record_title = last_record['title']
            except:
                last_record_title = ''
            
            # take out data from queue, then save data to doc which is it belongs to
            q = SUBJECT_QUEUE_DICT[subject]['store']
            if not q.empty():
                try:
                    data = []
                    while(not q.empty()):
                        record = q.get()
                        
                        if record['title'] == last_record_title: # there has duplicate record in db
                            break
                        else:
                            data.append(record)
                    
                    collect.find_one_and_update({'subject': subject}, {'$push': {'data': {'$each': data, '$position': 0}}}, {'_id': False})
                        
                    print('store', subject, 'to mongo complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
                except Exception as error:
                    print('Error: store '+ subject +' to mongo error')
                    print('Error Message:', error)
            else:
                print("The", subject, "doesn't have data in queue")

            q.queue.clear()
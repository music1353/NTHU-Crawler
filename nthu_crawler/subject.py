'''The subject of the title.
    Supported Subject: event, speech
'''

# just set subject in the SUBJECT_DICT, then can drive the crawler to crawl different subjects
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
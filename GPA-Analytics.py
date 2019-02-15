import os
import pickle

from ScrapLinks import SaveLinks
from ScrapResults import SaveResults
from ProgressBar import printProgressBar

time = SaveLinks()

count = 1
if os.path.exists('./Data/'+time+'/result_links.pkl'):
    links = pickle.load(open('./Data/'+time+'/result_links.pkl', 'rb'))
    total_links = len(links)

    for link in links.values():
        SaveResults(link)
        printProgressBar(count, total_links, prefix = 'Progress:', suffix = 'Complete', length = 50)
        count += 1

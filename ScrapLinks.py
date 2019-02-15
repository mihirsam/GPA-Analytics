from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import os
import pickle

def SaveLinks():
    try:
        # get url of result and time
        # eg. 'https://results.smu.edu.in/smit/results_grade_selection.php?exam=41'
        # eg. NOV/DEC-2018

        link = input("Enter Link : ")
        time = input("Enter Time : ")

        # get html data
        pre = 'https://results.smu.edu.in/smit/'
        uClient = uReq(link)
        result_html = uClient.read()
        uClient.close()
        print("Recieved HTML!")

        # parse data
        result_soup = soup(result_html, "html.parser")
        containers = result_soup.findAll("a")
        print("Data Parsed!")

        # save links to a dict
        result_links = dict()
        flag = 0

        for item in result_soup.findAll('a', attrs={'href': re.compile("^results")}):
            result_links[flag] = pre+item.get('href')
            flag += 1
        print("Data saved to dict!")

        if os.path.isdir(os.getcwd()+'\\Data\\'+time):
            with open('.\\Data\\'+time+'\\result_links.pkl', 'wb') as f:
                pickle.dump(result_links, f)
        else:
            try:
                path = os.getcwd()+'\\Data\\'+time
                os.mkdir(path)
                with open('.\\Data\\'+time+'\\result_links.pkl', 'wb') as f:
                    pickle.dump(result_links, f)

            except:
                print("Pickle File Creation Failed!")

        print("File Saved!\n\nStarting Scrapping : \n\n")
        return time

    except Exception as e:
        print("Error in getting links!")

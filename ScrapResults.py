from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import numpy as np
import os
import pickle

def SaveResults(link):
    # getting html
    try:
        uClient = uReq(link)
        result_html = uClient.read()
        uClient.close()

        #parsing html
        result_soup = soup(result_html, "html.parser")
        containers = result_soup.find("div", attrs={'style' : 'font-family:courier'})

        # adding content to list
        data = []
        count = 2
        for container in containers:
            if count % 2 == 0:
                data.append(container)
                count += 1
            else:
                count += 1

        # cleaning data
        cleaned_data = []
        count = 0
        for item in data:
            string = item.strip('\r')
            string = string.replace(u'\xa0', u' ')
            string = string.strip('\n')
            string = string.strip('\t')
            string = ' '.join(string.split())
            #print(string)
            cleaned_data.append(string)

        #making data dict
        data_dict = {}
        count = 0
        for item in cleaned_data:
            temp_list = item.replace(' ', ',').split(',')
            new_list = [i.strip(' ') for i in temp_list]
            if new_list != ['']:
                data_dict[count] = new_list
                count += 1
            else:
                pass

        #creating information dict
        subdict = {}
        months = [x.upper() for x in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
         'Jan', 'Feb', 'Mar', 'Apr', 'Nov', 'Dec', 'Aug']]
        years = list(str(x) for x in range(1990, 2050))
        types = ['SUPP', 'EXTRA', 'BACK', 'MAKE']


        for value in data_dict.values():
            if 'GRADE SHEET' in ' '.join(value):

                time_temp = []
                for item in months:
                    if item in ' '.join(value).replace('/', ' ').replace('(', ' ').replace(')', ' ').replace('-', ' '):
                        time_temp.append(item)
                    else:
                        pass

                if len(time_temp) == 0:
                    time_temp.append('EXTRA')

                subdict['Time'] = '-'.join(time_temp)
                subdict['Type'] = None

                for year in years:
                    if year in ' '.join(value).replace('/', ' ').replace('(', ' ').replace(')', ' ').replace('-', ' '):
                        subdict['Year'] = year

                for item in types:
                    if item in ' '.join(value).replace('/', ' ').replace('(', ' ').replace(')', ' ').replace('-', ' '):
                        subdict['Type'] = item

                if subdict['Type'] == None:
                    subdict['Type'] = 'NORMAL'

                subdict['Dir'] = '-'.join([subdict['Time'], subdict['Year']])

            elif len(value) >= 2 and value[1] == 'Code':
                subdict_name = value[3].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_') + '_dict'
                subdict['Code'] = value[3]

                if subdict['Type'] == 'NORMAL':
                    filename = value[3].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_')+'.csv'
                elif subdict['Type'] == 'BACK':
                    filename = value[3].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_')+'-Backlog.csv'
                elif subdict['Type'] == 'SUPP':
                    filename = value[3].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_')+'-Backlog.csv'
                elif subdict['Type'] == 'MAKE':
                    filename = value[3].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_')+'-Backlog.csv'
                elif subdict['Type'] == 'EXTRA':
                    filename = value[3].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_')+'-Backlog.csv'
                else:
                    pass

            elif len(value) >= 2 and value[1] == 'Title':
                length = len(value)
                temp = []
                for i in range(3, len(value)):
                    temp.append(value[i])

                subdict['Title'] = ' '.join(temp)

            elif len(value) >= 4 and value[1] == 'Credit':
                subdict['Credit'] = value[3]

            elif len(value) >= 7 and value[4] == 'E':
                subdict['Cutoff_E'] = value[6]

            elif len(value) >= 7 and value[4] == 'D':
                subdict['Cutoff_D'] = value[6]

            elif len(value) >= 7 and value[4] == 'C':
                subdict['Cutoff_C'] = value[6]

            elif len(value) >= 7 and value[4] == 'B':
                subdict['Cutoff_B'] = value[6]

            elif len(value) >= 7 and value[4] == 'A':
                subdict['Cutoff_A'] = value[6]

            elif len(value) >= 7 and value[4] == 'S':
                subdict['Cutoff_S'] = value[6]

            elif len(value) >= 5 and value[2] == 'Absentees':
                subdict['Absentees'] = value[4]

            elif len(value) >= 5 and value[2] == 'Malpractices':
                subdict['Malpractices'] = value[4]

            elif len(value) >= 5 and value[2] == 'Detentions':
                subdict['Detentions'] = value[4]

            elif len(value) >= 5 and value[2] == 'NA':
                subdict['NA'] = value[4]

            elif len(value) >= 6 and value[3] == 'appeared':
                subdict['appeared'] = value[5]

            elif len(value) >= 10 and 'S' in value[0] and 'A:' in value[2]:
                subdict['Cutoff_S'] = value[0][2:]
                subdict['Cutoff_A'] = value[3][0:2]
                subdict['Cutoff_B'] = value[6][0:2]
                subdict['Cutoff_C'] = value[9][0:2]
                subdict['Cutoff_D'] = value[11][2:4]
                subdict['Cutoff_E'] = value[13][2:4]

            else:
                pass

        for key in subdict:
            subdict[key] = subdict[key].replace('/', '_').replace('(', '_').replace(')', '_').replace('-', '_')

        info = ['Time', 'Year', 'Dir', 'Type', 'Code', 'Title', 'Credit', 'Cutoff_E', 'Cutoff_S', 'Cutoff_D', 'Cutoff_C', 'Cutoff_B', 'Cutoff_A', 'Absentees', 'Malpractices', 'Detentions', 'NA', 'appeared']

        for item in info:
            if item in subdict.keys():
                pass
            else:
                subdict[item] = 0

        exec('{} = {}' .format(subdict_name, subdict))
        #exec('print({})' .format(subdict_name))

        extra_info = [subdict['Time'], subdict['Year'], subdict['Type'], subdict['Code'], subdict['Credit'], subdict['Title'], subdict['Cutoff_S'], subdict['Cutoff_A'], subdict['Cutoff_B'], subdict['Cutoff_C'], subdict['Cutoff_D'], subdict['Cutoff_E'], subdict['Dir'], subdict['Absentees'], subdict['Malpractices'], subdict['Detentions'], subdict['NA'], subdict['appeared']]

        # data cleaning v2.0
        cleaned_dict = {}
        count = 0

        #for key in range(10, len(data_dict) - 14):
        for key in range(len(data_dict)):
            if len(data_dict[key]) >= 5:
                if data_dict[key][4].replace('(', ',').split(',')[0] in ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'I', 'P', 'DT', 'MP', 'PASS', 's', 'a', 'b', 'c', 'd', 'e', 'f', 'i', 'p', 'dt', 'na', 'mp', 'pass'] and data_dict[key][0] != 'Lower':
                    cleaned_dict[count] = data_dict[key][0:5] + extra_info
                    count += 1

        #making dataframe
        df = pd.DataFrame(cleaned_dict).transpose()
        df.columns = ['Reg_No', 'Internal', 'External', 'Total', 'Grade', 'Time', 'Year', 'Type', 'Code', 'Credit', 'Title', 'Cut-Off-S', 'Cut-Off-A', 'Cut-Off-B', 'Cut-Off-C', 'Cut-Off-D', 'Cut-Off-E', 'Directory', 'Absentees', 'Malpractices', 'Detentions', 'NA', 'appeared']


        while(True):
            if os.path.isdir(os.getcwd()+'\\Data\\'+subdict['Dir']):
                df.to_csv(os.getcwd()+'\\Data\\'+subdict['Dir']+'\\'+filename, index = False, encoding='utf-8')
                if subdict['Type'] == 'NORMAL':
                    with open(os.getcwd()+'\\Data\\'+subdict['Dir']+'\\'+subdict['Code']+'.pkl', 'wb') as f:
                        exec('pickle.dump({}, f)' .format(subdict_name))
                elif subdict['Type'] == 'BACK-LOG-PAPER':
                    with open(os.getcwd()+'\\Data\\'+subdict['Dir']+'\\'+subdict['Code']+'-Backlog.pkl', 'wb') as f:
                        exec('pickle.dump({}, f)' .format(subdict_name))
                else:
                    pass

                break

            else:
                try:
                    path = os.getcwd()+'\\Data\\'+subdict['Dir']
                    os.mkdir(path)

                except:
                    printf("Error in saving file!")

        while(True):
            rel_path = 'Data\MainDatabase.csv'
            path = os.path.join(os.getcwd(), rel_path)
            if os.path.exists(path):
                with open(path, 'a') as f:
                    df.to_csv(f, index=False, header=False)
                    f.close()
                break

            else:
                with open(path, "w") as f:
                    f.close()

        #print('Completed'+subdict['Code'])
    #print("\nResult Saved : "+subdict['Code']+"\t\tType : "+subdict['Type'])

    except Exception as e:
        print(e)
        print(link)

import os
import glob
import pandas as pd
import pathlib 
from pprint import pprint


path = pathlib.Path(__file__).parent.absolute()
os.chdir(path)

all_filenames = glob.glob('*.csv')


def head_cread() -> dict:
    '''Show headers'''
    
    head_list = []
    for i in all_filenames:
        data = pd.read_csv(i, warn_bad_lines=False, error_bad_lines=False, delimiter=';')
        for y in data.head(0):
            if y not in head_list:
                head_list.append(y)
            else:
                pass
    enum = enumerate(head_list[1:], start=1)
    head_dict = dict((i,j) for i,j in enum)
    
    return head_dict





'''fetch required columns'''
col_list = ['DATE']
dict_head = head_cread()

pprint(dict_head)
input_list = list(map(int,input('Выберете номера нужных заголовков: ').strip().split()))

for i in input_list:
    col_list.append(dict_head[i])





'''data cleaning'''
for i in all_filenames:
    data = pd.read_csv(i, error_bad_lines=False, delimiter=';', usecols=lambda x: x in col_list)
    df = pd.DataFrame(data)
    try:
        df['DATE'] = pd.to_datetime(df['DATE'], format='%d.%m.%Y %H:%M:%S')
    except:
        pass
    #df = df.round(2)
    #df[:2].to_csv('C:\\Users\\Admin\\Desktop\\test\\new\\output'+i, sep=';', index=False)
    df.to_csv('output'+i, sep=';', index=False)





'''Data connection'''
files = glob.glob('output*.csv')

combined = pd.read_csv(files[0], delimiter=';')

for file in files[1:]:
    data_file = pd.read_csv(file, delimiter=';')
    combined = combined.merge(data_file, how='outer')

"""combined = pd.read_csv(files[0], delimiter=';')
for file in files[1:]:
    data_file = pd.read_csv(file, delimiter=';')
    combined = combined.append(data_file, on='DATE')

"""
    
#(combined.sort_values('DATE')).to_csv("combined.csv", index=False, sep=';')
#df = df.drop_duplicates(subset=['DATE'], keep='first')
combined.to_csv("combined.csv", index=False, sep=';')


for file in files:
    os.remove(file)
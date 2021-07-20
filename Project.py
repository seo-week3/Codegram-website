import requests
import json
import pandas as pd
import os
from sqlalchemy import create_engine
import string

def remove(string):
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)
        t = string.translate(translator)
        return t
        
def get_API_data(choice):    
    
        secret = '	I68I7hy1Rpww0cGWAVjtsoi7dO5fxg'
        personal_use_script = 'E2xxiNzl8utDycr7e_dGIg'


        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth('E2xxiNzl8utDycr7e_dGIg', 'I68I7hy1Rpww0cGWAVjtsoi7dO5fxg')

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': 'dpbolat19',
                'password': 'Codegram101!'}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value

        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        response = requests.get('https://oauth.reddit.com/r/'+ choice + '/hot', headers=headers)
        
        df = pd.DataFrame()  # initialize dataframe
        # loop through each post retrieved from GET request
        for post in response.json()['data']['children'][2:12]:
            # append relevant data to dataframe
            #clean = re.sub(r"[^. 0-9a-z]", "", post['data']['selftext'], re.IGNORECASE)
            df = df.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': remove(post['data']['selftext']),
                'author_fullname':post['data']['author_fullname']
            }, ignore_index=True) 
        return df
            
        
def createdb(name):
    df = get_API_data(name)
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' + 'Codegram' + ';"')
    #create_engine('mysql+mysqldb:///mydb?charset=utf8&use_unicode=1')
    engine = create_engine('mysql://root:codio@localhost/Codegram?charset=utf8mb4&use_unicode=1')
    with engine.connect() as con:
            con.execute('ALTER DATABASE Codegram COLLATE = "utf8mb4_unicode_ci";')
    df.to_sql(name, con=engine, if_exists='replace', index=False)
    return df

def savedb():
    os.system("mysqldump -u root -pcodio Codegram > Codegram.sql")


def loaddb():
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' +
              'Codegram' + ';"')
    os.system("mysql -u root -pcodio Codegram < Codegram.sql")


def loadDataset(name, update=False):
    engine = create_engine('mysql://root:codio@localhost/' + 'Codegram')
    loaddb()
    df = pd.read_sql_table(name, con=engine)
    return df

def Update_db(name, new_data):
    df = loadDataset(name)
    
    
    
        
option_1 = "cscareerquestions"   
option_2 = "csMajors"
option_3 = "csinterviewproblems"
option_4 = 'DataScienceJobs'
option_5 = 'cscareers'
option_6 = 'datasciencecareers'

DB_list = [option_1, option_2, option_3, option_4, option_5, option_6]
for i in DB_list:
        createdb(i)       
savedb()

#print(db.head())

    




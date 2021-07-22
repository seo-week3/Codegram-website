import requests
import json
import pandas as pd
import os
from sqlalchemy import create_engine
import string

engine = create_engine(
    'mysql://root:codio@localhost/Codegram?charset=utf8mb4&use_unicode=1')


def remove(string):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    t = string.translate(translator)
    return t


def get_API_data(choice):

    secret = '	I68I7hy1Rpww0cGWAVjtsoi7dO5fxg'
    personal_use_script = 'E2xxiNzl8utDycr7e_dGIg'

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to
    # 'token'
    auth = requests.auth.HTTPBasicAuth(
        'E2xxiNzl8utDycr7e_dGIg',
        'I68I7hy1Rpww0cGWAVjtsoi7dO5fxg')

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

    # while the token is valid (~2 hours) we just add headers=headers to our
    # requests
    response = requests.get(
        'https://oauth.reddit.com/r/' +
        choice +
        '/hot',
        headers=headers)

    df = pd.DataFrame()  # initialize dataframe
    # loop through each post retrieved from GET request
    index = 0
    for post in response.json()['data']['children'][2:13]:
        index += 1
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': remove(post['data']['selftext']),
            'author_fullname': post['data']['author_fullname']
        }, ignore_index=True)
    # print(str(df.iloc[0][0]), str(df.iloc[0][1]), str(df.iloc[0][3]))
    return df


def createdb(name):
    df = get_API_data(name)
    os.system(
        'mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' +
        'Codegram' +
        ';"')
    with engine.connect() as con:
        con.execute('ALTER DATABASE Codegram COLLATE = "utf8mb4_unicode_ci";')
    df.to_sql(name, con=engine, if_exists='replace', index=False)
#     with engine.connect() as con:
#             con.execute(
# #             """ALTER TABLE Codegram.csMajors
# #             ADD user_id INT NOT NULL AUTO_INCREMENT primary key;""")
# #        con.execute(
#             """ALTER TABLE Codegram.datasciencecareers
#             ADD user_id INT NOT NULL AUTO_INCREMENT primary key;""")
# #         con.execute(
# #             """ALTER TABLE Codegram.cscareerquestions
# #             ADD user_id INT NOT NULL AUTO_INCREMENT primary key;""")
# #         con.execute(
# #             """ALTER TABLE Codegram.csinterviewproblems
# #             ADD user_id INT NOT NULL AUTO_INCREMENT primary key;""")
# #         con.execute(
# #             """ALTER TABLE Codegram.DataScienceJobs
# #             ADD user_id INT NOT NULL AUTO_INCREMENT primary key;""")
# #         con.execute(
#              """ALTER TABLE Codegram.softwaredevelopment
#              ADD user_id INT NOT NULL AUTO_INCREMENT primary key;""")
    return df


def savedb():
    os.system("mysqldump -u root -pcodio Codegram > Codegram.sql")


def loaddb():
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' +
              'Codegram' + ';"')
    os.system("mysql -u root -pcodio Codegram < Codegram.sql")


def loadDataset(name, update=False):
    loaddb()
    df = pd.read_sql_table(name, con=engine)
    return df


def Update_db(name, new_data):
    # os.system('mysql -u root -pcodio -e
    # "CREATE DATABASE IF NOT EXISTS ' + 'Codegram' + ';"')
    df = loadDataset(name)
    with engine.connect() as con:
        con.execute(
            'INSERT INTO Codegram.' +
            name +
            ' (subreddit, title, selftext, author_fullname) VALUES ' +
            str(new_data) +
            ';')
    print('success')
    # savedb()
    # df.to_sql(name, con=engine, if_exists='replace', index=False)


def move_comment_up(df):
    idx = df.index.tolist()
    idx.pop(len(df.index) - 1)
    df = df.reindex([len(df.index) - 1] + idx)
    print(df)
    return (df)


option_1 = "cscareerquestions"
option_2 = "csMajors"
option_3 = "csinterviewproblems"
option_4 = 'DataScienceJobs'
option_5 = 'softwaredevelopment'
option_6 = 'datasciencecareers'

# DB_list = [option_5]
# for i in DB_list:
#         createdb(i)
# createdb(option_5)
# savedb()

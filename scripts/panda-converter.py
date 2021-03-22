# import libraries that we will use
import pandas as pd 
import sys, glob, json,csv
from bs4 import BeautifulSoup

def get_conversation_data(conversation,f_type,headers=False):   
    columns = ['id','type','commentor.id', 'commentor.name', 'mention.sgid', 'mention.name','mention.id', 'content.text']
    convo = pd.DataFrame(columns=columns) 
    for index, row in conversation.iterrows():
        soup = BeautifulSoup(row['content'], 'html5lib')
        attachments = soup.find_all('bc-attachment')
        for attachment in attachments:
            if(attachment['content-type'] == "application/vnd.basecamp.mention"):
                convo = pd.concat([convo, pd.DataFrame(data={'id':[conversation.loc[index].at['id']],'type':f_type,'commentor.id':[conversation.loc[index].at['creator.id']],'commentor.name':conversation.loc[index].at['creator.name'], 'mention.sgid':attachment['sgid'], 'mention.name': attachment.img['alt'], 'mention.id':attachment.img['data-avatar-for-person-id'], 'content.text':"\""+soup.text.replace("\n", "")})])

            #else:
            #    convo = pd.concat([convo, pd.DataFrame(data={'commentor.id':[conversation.loc[index].at['creator.id']],'commentor.name':conversation.loc[index].at['creator.name'],'mention.sgid':"",'mention.name':"",'mention.id':"",'content.text':"\""+soup.text.replace("\n", "")})])
    if(headers):
        convo.to_csv("mentions.csv",mode='a',index=False,header=True)
    else:
        convo.to_csv("mentions.csv",mode='a',index=False, header=False)

# put in the path to the files
PATH = '/Users/bowens3/Downloads/LASG_IU DataViz project data/'
# array of the different file types
file_types = ['projects','people','messageboards','comments']
headers=True
# loop through the file types
for f_type in file_types:
    # list all of the json files of that type
    arr = glob.glob(PATH+"*_"+f_type+".json")
    # create an empty data frame to use to concat with
    df = pd.DataFrame()
    # loop through all of the files
    for f in arr:
        # open the fiel
        inputFile = open(f) #open json file
        # load it as json data
        data = json.load(inputFile)
        # normalize, or flatten, the json data
        df2 = pd.json_normalize(data)
        if(f_type in ['messageboards','comments']):
            get_conversation_data(df2,f_type,headers)
            headers=False
        if('content' in list(df2)):
            df2.drop(columns=['content'],inplace=True)
        # concatenate the two data frames together
        df = pd.concat([df,df2]) 
        


    # Once done with all of the files
    # save the whole data frame to a csv file
    df.to_csv(f_type+".csv",index=False)







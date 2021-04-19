# import libraries that we will use
import glob
import json
import os
from django.conf import settings


import pandas as pd
from bs4 import BeautifulSoup


def merge_people(path):
    # open the people file in pandas
    people_df = pd.read_csv(path + '/csv/' + 'people.csv', encoding='utf8')
    # make all of the names the same text format
    people_df['name'] = people_df['name'].str.title()
    # group by the name and count how many there are
    grouped_people = people_df.groupby(by=['name'], as_index=False).count()
    # drop all of the groups that aren't duplicates
    duplicates = grouped_people.where(grouped_people['id'] > 1).dropna()
    # loop through and add the ids together and multiply by 10 so we don't collide with already existing ids
    # the id solution isn't going to be good in the long term but for right now we should be fine
    for i in duplicates.index:
        matches = people_df[people_df['name'] == duplicates['name'][i]]['id']
        new_id = matches.sum() * 10
        for j in matches.index:
            # add a new column called old_id so we can match in other files later
            people_df.loc[j, 'old_id'] = people_df.loc[j, 'id']
            people_df.loc[j, 'id'] = new_id

     # if we wanted to we can drop the duplicate names but since we have to find the duplicates
    # in the other files it isn't the best option at this time
    # people_df.drop_duplicates(subset=['name'], inplace=True)

    # write the merged people to a csv
    people_df.to_csv(path + '/csv/' + 'merged_people.csv', header=True, index=False)


def update_people_ids(path):
    # files that contain the duplicate people ids that we need to update
    files = ['messageboards.csv', 'comments.csv', 'comments_and_mentions.csv']
    # open up the merged people file
    merged_people = pd.read_csv(path + '/csv/' + 'merged_people.csv')
    # find all of the merged people in the file
    duplicates = merged_people.where(pd.notna(merged_people['old_id']) == True).dropna(how='all')

    # loop through all of the files
    for f in files:
        # open in pandas
        file_df = pd.read_csv(path + '/csv/' + f, encoding='utf8')
        # for every duplicate person
        for dup in duplicates.index:
            # find the id of them in the files and update them to the new id that was created
            if (f == 'comments_and_mentions.csv'):
                matches = file_df.where(file_df['commentor.id'] == duplicates['old_id'][dup]).dropna(how='all')
                for match in matches.index:
                    file_df.loc[match, 'commentor.id'] = duplicates.loc[dup, 'id']
                matches = file_df.where(file_df['mention.id'] == duplicates['old_id'][dup]).dropna(how='all')
                for match in matches.index:
                    file_df.loc[match, 'mention.id'] = duplicates.loc[dup, 'id']
            else:
                matches = file_df.where(file_df['creator.id'] == duplicates['old_id'][dup]).dropna(how='all')
                for match in matches.index:
                    file_df.loc[match, 'creator.id'] = duplicates.loc[dup, 'id']
        # then save the file
        file_df.to_csv(path + '/csv/' + f, index=False)


def count_interactions():
    path = settings.MEDIA_ROOT
    projects_df = pd.read_csv(path + '/csv/' + 'projects.csv', encoding='utf8')
    comments_and_mentions_df = pd.read_csv(path + '/csv/' + 'comments_and_mentions.csv', encoding='utf8')
    for project in projects_df['id']:
        interaction = comments_and_mentions_df.where(
            comments_and_mentions_df['project.id'] == project).dropna().groupby(
            ['commentor.id', 'commentor.name', 'mention.id', 'mention.name']).size().reset_index().rename(
            columns={0: 'count'}).sort_values(by=['count'], ascending=False)
        interaction.to_csv(path + '/csv/' + str(project) + "_interactions.csv", index=False)


def get_conversation_data(path, conversation, f_type, headers=False):
    # column array for the comments and message board
    columns = ['id', 'type', 'project.id', 'project.name', 'commentor.id', 'commentor.name', 'mention.sgid',
               'mention.name', 'mention.id', 'content.text']
    #
    convo = pd.DataFrame(columns=columns)
    for index, row in conversation.iterrows():
        soup = BeautifulSoup(row['content'], 'html5lib')
        attachments = soup.find_all('bc-attachment')
        for attachment in attachments:
            if attachment['content-type'] == "application/vnd.basecamp.mention":
                convo = pd.concat([convo, pd.DataFrame(data={'id': [conversation.loc[index].at['id']], 'type': f_type,
                                                             'project.id': [conversation.loc[index].at['bucket.id']],
                                                             'project.name': [
                                                                 conversation.loc[index].at['bucket.name']],
                                                             'commentor.id': [conversation.loc[index].at['creator.id']],
                                                             'commentor.name': conversation.loc[index].at[
                                                                 'creator.name'], 'mention.sgid': attachment['sgid'],
                                                             'mention.name': attachment.img['alt'],
                                                             'mention.id': attachment.img['data-avatar-for-person-id'],
                                                             'content.text': "\"" + soup.text.replace("\n", "")})])

            else:
                convo = pd.concat([convo, pd.DataFrame(data={'project.id': [conversation.loc[index].at['bucket.id']],
                                                             'project.name': [
                                                                 conversation.loc[index].at['bucket.name']],
                                                             'commentor.id': [conversation.loc[index].at['creator.id']],
                                                             'commentor.name': conversation.loc[index].at[
                                                                 'creator.name'], 'mention.sgid': "",
                                                             'mention.name': "", 'mention.id': "",
                                                             'content.text': "\"" + soup.text.replace("\n", "")})])
                break
    if headers:
        convo.to_csv(path + "/csv/" + "comments_and_mentions.csv", mode='a', index=False, header=True)
    else:
        convo.to_csv(path + "/csv/" + "comments_and_mentions.csv", mode='a', index=False, header=False)


def output_csv(path):
    # put in the path to the files
    PATH = path
    # array of the different file types
    file_types = ['projects', 'people', 'messageboards', 'comments']
    headers = True
    # loop through the file types
    for f_type in file_types:
        # list all of the json files of that type
        arr = glob.glob(PATH + '/json/' + "*_" + f_type + ".json")
        # create an empty data frame to use to concat with
        df = pd.DataFrame()
        # loop through all of the files
        for f in arr:
            # open the fiel
            inputFile = open(f, encoding="utf8")  # open json file
            # load it as json data
            data = json.load(inputFile)
            # normalize, or flatten, the json data
            df2 = pd.json_normalize(data)
            if f_type in ['messageboards', 'comments']:
                get_conversation_data(path, df2, f_type, headers)
                headers = False
            if 'content' in list(df2):
                df2.drop(columns=['content'], inplace=True)
            # concatenate the two data frames together
            df = pd.concat([df, df2])

        # Once done with all of the files
        # save the whole data frame to a csv file
        df.to_csv(PATH + "/csv/" + f_type + ".csv", index=False)

    merge_people(path)
    update_people_ids(path)
    count_interactions()

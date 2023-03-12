import openai
import pandas as pd
import os

def get_bulletpoints(link):
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Extract 3 to 5 brief ( up to 8 words ) bulletpoints but with no indexing that can pass as tasks from the following link:" + str(link)},
    ])
    message = response.choices[0]['message']
    bulletpoints = message['content'].splitlines()
    
    return bulletpoints

def get_hours(bulletpoints):
    hourlist = []
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": 'Give me a simple non-indexed list that only contains time values in hours that add up to 8 hours for the following tasks,please do not include the tasks and put every entry in the list on a different line and it should not contain the word "hours" ' + str(bulletpoints)},
    ])
    message = response.choices[0]['message']
    hourlist = message['content']
    hourlist = hourlist.replace('hours', '')
    hourlist = hourlist.replace('hour', '')
    hourlist = hourlist.replace('-', '')
    hourlist = hourlist.replace(' ', '')
    return hourlist.splitlines()
    

def create_output(template,bulletpoints,hourlist):
    output_df = pd.concat([template, bulletpoints], axis = 1, sort = False)
    output_df = pd.concat([output_df, hourlist], axis = 1, sort = False)
    output_df['Description/Planning'] = output_df['Column1']
    output_df['Est Hours'] = output_df['Column2']
    output_df['Actual Hours'] = output_df['Est Hours']
    output_df['Diff'] = 0
    output_df['Task'] = 'Max 4 hours tasks'
    output_df['Actual Hours'] = output_df['Actual Hours'].astype(float)
    output_df['Est Hours'] = output_df['Est Hours'].astype(float)
    output_df = output_df[['Date', 'Status', 'Task' ,'Description/Planning','Task Type','Most suited ILO', 'Est Hours',
             'Actual Hours','Diff','Evidence link','Task reflection / notes']]
    output_df = output_df.reset_index(drop=True)
    print(output_df)
    return output_df





    
import openai
import pandas as pd
from update_api_key import update_api_key
global listhehe
listhehe= []
openai.api_key = ""
model_engine = "gpt-3.5-turbo"
    
def get_bulletpoints(link):
    global listhehe
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Extract 3 to 5 brief ( up to 8 words ) bulletpoints but with no indexing that can pass as tasks from the following link: " + str(link)},
    ])
    message = response.choices[0]['message']
    prompt = message['content']
    listhehe = message['content'].splitlines()
    return prompt

def get_hours(prompt):
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": 'Give me a simple non-indexed list that only contains time values in hours that add up to 8 hours for the following tasks,please do not include the tasks and put every entry in the list on a different line and also do not include the word "hours"' + str(prompt)},
    ])
    message = response.choices[0]['message']
    hourlist = message['content']
    return hourlist


if openai.api_key == "":
    openai.api_key = update_api_key()

link = input('Please provide link you want to generate worklog for:\n')
prompt = get_bulletpoints(link) #TODO: prompt for link

template = ['Date', 'Status', 'Task' ,'Description/Planning','Task Type','Most suited ILO', 'Est Hours',
             'Actual Hours','Diff','Evidence link','Task reflection / notes']
df = pd.DataFrame(columns = template)

df = df.append(pd.DataFrame(listhehe, columns=['Description/Planning']), ignore_index=True)
    
hourlist = get_hours(prompt)
hourlist = hourlist.splitlines()

listhehe_df = pd.DataFrame()
listhehe_df["Description/Planning"] = listhehe
hourlist_df = pd.DataFrame()
hourlist_df['Est Hours'] = hourlist

listhehe_df.reset_index(drop = True, inplace = True)
hourlist_df.reset_index(drop = True, inplace = True)

""" listhehe_df['Task Description/Planning'] = listhehe_df['Task Description/Planning'].str.replace('\n', '')
hourlist_df['Est Hours'] = hourlist_df['Est Hours'].str.replace('\n', '') """

yes = pd.concat([df, listhehe_df], axis = 1, sort = False).drop_duplicates()
yes = pd.concat([yes, hourlist_df], axis = 1, sort = False).drop_duplicates()

yes = yes.loc[:,~yes.columns.duplicated()]

yes['Est Hours'] = hourlist_df['Est Hours']
#yes['Actual Hours'] = hourlist_df['Est Hours']
#yes['Diff'] = 0
yes['Task'] = 'Max 4 hours tasks'

yes['Actual Hours'] = yes['Actual Hours'].astype(float)
yes['Est Hours'] = yes['Est Hours'].astype(float)

yes = yes.reset_index(drop=True)

yes.to_excel('../LazyData_Save.xlsx', index=False )
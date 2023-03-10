import openai
import pandas as pd
global listhehe
listhehe= []
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"

def get_bulletpoints(link):
    global listhehe
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Extract 3 to 5 brief ( up to 8 words ) bulletpoints but with no indexing that can pass as tasks from the following link:" + str(link)},
    ])
    message = response.choices[0]['message']
    prompt = message['content']
    listhehe = message['content'].splitlines()
    return prompt

prompt = get_bulletpoints('https://adsai.buas.nl/Study%20Content/DeepLearning/12.%20CNN%20day%202.html')
print(listhehe)

template = ['Date', 'Status', 'Task' ,'Description/Planning','Task Type','Most suited ILO', 'Est Hours',
             'Actual Hours','Diff','Evidence link','Task reflection / notes']
df = pd.DataFrame(columns = template)

df = df.append(pd.DataFrame(listhehe, columns=['Description/Planning']), ignore_index=True)

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
yes['Actual Hours'] = hourlist_df['Est Hours']
yes['Diff'] = 0
yes['Task'] = 'Max 4 hours tasks'

yes['Actual Hours'] = yes['Actual Hours'].astype(float)
yes['Est Hours'] = yes['Est Hours'].astype(float)

yes = yes.reset_index(drop=True)

yes.to_excel('C:/Users/bogda/Documents/GitHub/LazyLogger/LazyData_Save2.xlsx', index= False )
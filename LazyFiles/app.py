# Importing necessary modules
import openai
import pandas as pd
import functions
import numpy as np

def run_logger(key,link, daynumber):
    # Defining Api Key and model engine
    openai.api_key = key
    model_engine = "gpt-3.5-turbo"

    # Initializing a template df for the formatting of the output
    template = ['Date', 'Status', 'Task' ,'Description/Planning','Task Type','Most suited ILO', 'Est Hours',
             'Actual Hours','Diff','Evidence link','Task reflection / notes']
    template_df = pd.DataFrame(columns = template)

    #Getting bulletpoints from link
    bulletpoints = functions.get_bulletpoints(link)

    #Getting hourlist from bulletpoints
    hourlist = functions.get_hours(bulletpoints)

    #Creating dataframes from the two lists
    hourlist_df = pd.DataFrame()
    hourlist_df['Column2'] = hourlist
    
    bulletpoints_df = pd.DataFrame()
    bulletpoints_df["Column1"] = bulletpoints
    

    #Resetting index for appending
    bulletpoints_df.reset_index(drop = True, inplace = True)
    hourlist_df.reset_index(drop = True, inplace = True)

    #Creating output dataframe
    output_df = functions.create_output(template_df,bulletpoints_df,hourlist_df)

    #Getting file path for output folder
    
    print(output_df)
    #Saving to excel
    output_df.to_excel('./OutputDay' + str(daynumber + 1) + '.xlsx', index= False)

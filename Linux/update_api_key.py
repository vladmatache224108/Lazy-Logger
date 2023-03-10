def update_api_key():
    f=open('app.py','r')
    text = f.readlines()
    f.close()

    fw=open('app.py', 'w')
    for line in text:
        if 'openai.api_key = ""' in line:
            api_key = str(input("please provide openai api key:\n"))
            line = line.replace('""', '"' + api_key + '"')
        fw.write(line)
    fw.close()
    return api_key
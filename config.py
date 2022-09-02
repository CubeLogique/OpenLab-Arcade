import json

with open('settings.json', 'r') as file:
 
    # Reading from json file
    data = json.load(file)
    
print(type(data))

Languages = data['Languages']
French = Languages['French']
print(French[0])
English = Languages['English']
print(English[0])

with open('settings.json', 'r+') as f:
    data = json.load(f)
    data["ChoosenLanguage"] = "English"
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()


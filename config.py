import json

def read_saved_language():
    
    with open('settings.json', 'r') as file:
        
        data = json.load(file)
        return data['ChoosenLanguage']

def read_language(language,number):

    with open('settings.json', 'r') as file:
        
        data = json.load(file)
        
    Languages = data['Languages']
    
    if language == "fr":
        fr = Languages['fr']
        return fr[number]
    if language == "en":
        en = Languages['en']
        return en[number]

def save_language(language):
    with open('settings.json', 'r+') as f:
        data = json.load(f)
        if language == "fr":
            data["ChoosenLanguage"] = "fr"
        if language == "en":
            data["ChoosenLanguage"] = "en"
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
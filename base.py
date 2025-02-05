import json

import requests
from mlphon import PhoneticAnalyser
from tqdm import tqdm

mlphon = PhoneticAnalyser()

def get_morphological_analysis(word):
    
    url = f"https://morph.smc.org.in/api/analyse?text={word}"
    response = requests.get(url)
      
    if response.status_code == 200:
        return response.json()  
    else:
        return None  

def process_words(words):
    result = []
    
    for word in tqdm(words):
        word_analysis = {}
        
        ipa_representation = mlphon.grapheme_to_phoneme(word)
        word_analysis['word'] = word
        word_analysis['ipa'] = ipa_representation

        morphology = get_morphological_analysis(word)
        if morphology:
            analysis_result = morphology.get("result", {}).get(word, [])
            if analysis_result:                
                sorted_morphemes = sorted(analysis_result, key=lambda x: x.get('weight', float('inf')))
                word_analysis['morphology'] = sorted_morphemes[0]  
            else:
                word_analysis['morphology'] = 'No morphemes found'
        else:
            word_analysis['morphology'] = 'Error retrieving data'

        result.append(word_analysis)
    
    with open('analysis_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.readlines()
    return [word.strip() for word in words[:100000]] #<-- HERE

words = read_words_from_file('malayalam_words.txt')
print(len(words))   
process_words(words)

print("Analysis written to 'analysis_results.json'.")

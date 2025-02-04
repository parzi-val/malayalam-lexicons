import json
from mlphon import PhoneticAnalyser
import requests
from tqdm import tqdm

# Initialize analyzers
mlphon = PhoneticAnalyser()

def get_morphological_analysis(word):
    # API URL
    url = f"https://morph.smc.org.in/api/analyse?text={word}"

    # Send the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the response as JSON
    else:
        return None  # Return None if there was an error with the request

def process_words(words):
    result = []
    
    for word in tqdm(words):
        word_analysis = {}
        
        # Phonetic Analysis (Grapheme to Phoneme)
        ipa_representation = mlphon.grapheme_to_phoneme(word)
        word_analysis['word'] = word
        word_analysis['ipa'] = ipa_representation

        # Morphological Analysis using the API
        morphology = get_morphological_analysis(word)
        if morphology:
            # Extract the results
            analysis_result = morphology.get("result", {}).get(word, [])
            if analysis_result:
                # Sort by weight to find the one with the least weight
                sorted_morphemes = sorted(analysis_result, key=lambda x: x.get('weight', float('inf')))
                word_analysis['morphology'] = sorted_morphemes[0]  # Take the one with the least weight
            else:
                word_analysis['morphology'] = 'No morphemes found'
        else:
            word_analysis['morphology'] = 'Error retrieving data'

        result.append(word_analysis)

    # Convert the result to JSON and write to a file
    with open('analysis_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

# List of words to analyze
def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.readlines()
    # Clean up and return the first 100 words as a list
    return [word.strip() for word in words[:10000]]

words = read_words_from_file('malayalam_words.txt')
print(len(words))   
# Call the function to process the words
process_words(words)

print("Analysis written to 'analysis_results.json'.")

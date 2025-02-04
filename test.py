import os
import re
from tqdm import tqdm 

# Define the base directory
base_dir = "corpus/text/ml-wiki"
output_file = "malayalam_words.txt"
seen_words = set()  # To track unique words and avoid duplicates

# Function to extract words from a file
def extract_words(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    # Remove <doc> tags and metadata
    clean_text = re.sub(r"<doc.*?>|</doc>", "", data)  # Remove <doc> tags
    clean_text = re.sub(r"https?://\S+", "", clean_text)  # Remove URLs
    clean_text = re.sub(r"[^\u0D00-\u0D7F\s]", "", clean_text)  # Keep only Malayalam characters

    # Tokenize words (splitting by spaces & newlines)
    words = set(clean_text.split())  # Use set to remove duplicates
    return words

# Traverse directories and process files
for root, _, files in os.walk(base_dir):
    for file in tqdm(files):
        file_path = os.path.join(root, file)
        words = extract_words(file_path)
        seen_words.update(words)

# Save unique words to a file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(seen_words))

print(f"Extracted {len(seen_words)} unique words and saved to {output_file}.")

import json
import aiohttp
import asyncio
from mlphon import PhoneticAnalyser
from tqdm.asyncio import tqdm  # Async progress bar

# Initialize phonetic analyzer
mlphon = PhoneticAnalyser()

API_URL = "https://morph.smc.org.in/api/analyse?text={}"
CONCURRENT_REQUESTS = 10  # Limit to avoid overwhelming the API


async def get_morphological_analysis(session, word, semaphore):
    """Fetch morphological analysis for a word asynchronously."""
    url = API_URL.format(word)

    async with semaphore:  # Limit concurrent requests
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result", {}).get(word, [])
                return None
        except Exception as e:
            print(f"Error fetching {word}: {e}")
            return None


async def process_word(word, session, semaphore):
    """Process a single word asynchronously."""
    word_analysis = {}

    # Phonetic Analysis
    ipa_representation = mlphon.grapheme_to_phoneme(word)
    word_analysis["word"] = word
    word_analysis["ipa"] = ipa_representation

    # Morphological Analysis
    morphology = await get_morphological_analysis(session, word, semaphore)
    if morphology:
        # Pick the result with the least weight
        sorted_morphemes = sorted(morphology, key=lambda x: x.get("weight", float("inf")))
        word_analysis["morphology"] = sorted_morphemes[0] if sorted_morphemes else "No morphemes found"
    else:
        word_analysis["morphology"] = "Error retrieving data"

    return word_analysis


async def process_words(words):
    """Process words concurrently with async requests."""
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)  # Limit concurrent requests
    async with aiohttp.ClientSession() as session:
        tasks = [process_word(word, session, semaphore) for word in tqdm(words, desc="Processing words")]
        results = await asyncio.gather(*tasks)  # Run tasks concurrently

    # Save results to JSON
    with open("analysis_results.json", "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


def read_words_from_file(file_path, limit=100000):
    """Read words from file and return as a list."""
    with open(file_path, "r", encoding="utf-8") as file:
        words = [line.strip() for line in file.readlines()]
    return words[:limit]


# Run the async event loop
if __name__ == "__main__":
    words = read_words_from_file("malayalam_words.txt", limit=100)
    print(f"Processing {len(words)} words...")
    asyncio.run(process_words(words))
    print("Analysis written to 'analysis_results.json'.")

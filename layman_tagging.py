import json
from tqdm import tqdm

# Mapping from detailed POS tags to layman-friendly categories.
pos_to_layman = {
    # Nouns & Nominal Categories
    "n": "Noun",
    "np": "Noun",
    "n-v-compound": "Noun",
    "masculine": "Noun Modifier",
    "feminine": "Noun Modifier",
    "neutral": "Noun Modifier",
    "pl": "Noun Modifier",
    "ablative": "Case Marker",
    "accusative": "Case Marker",
    "dative": "Case Marker",
    "genitive": "Case Marker",
    "locative": "Case Marker",
    "allative": "Case Marker",
    "instrumental": "Case Marker",
    "perlative": "Case Marker",
    "vocative": "Case Marker",
    "sociative": "Case Marker",
    "cardinal": "Numeral",
    "ordinal": "Numeral",
    "ones": "Numeral",
    "tens": "Numeral",
    "hundreds": "Numeral",
    "thousands": "Numeral",
    "lakhs": "Numeral",
    "crores": "Numeral",
    "half": "Numeral",
    "zero": "Numeral",
    "quantifier": "Quantifier",
    "qn": "Question",

    # Pronouns & Related Words
    "prn": "Pronoun",
    "dem": "Pronoun/Determiner",
    "interrogative": "Interrogative",

    # Verbs & Verb-Related Features
    "v": "Verb",
    "abilitative-mood": "Verb (Mood)",
    "compulsive-mood": "Verb (Mood)",
    "compulsive-mood-neg": "Verb (Mood)",
    "conditional-mood": "Verb (Mood)",
    "desiderative-mood": "Verb (Mood)",
    "imperative-mood": "Verb (Mood)",
    "optative-mood": "Verb (Mood)",
    "permissive-mood": "Verb (Mood)",
    "precative-mood": "Verb (Mood)",
    "promissive-mood": "Verb (Mood)",
    "purposive-mood": "Verb (Mood)",
    "quotative-mood": "Verb (Mood)",
    "satisfactive-mood": "Verb (Mood)",
    "past": "Verb (Tense)",
    "present": "Verb (Tense)",
    "future": "Verb (Tense)",
    "causative-voice": "Verb (Voice)",
    "passive-voice": "Verb (Voice)",
    "cont-perfect-aspect": "Verb (Aspect)",
    "cont-perfect-aspect-neg": "Verb (Aspect)",
    "simple-perfect-aspect": "Verb (Aspect)",
    "simple-perfect-aspect-neg": "Verb (Aspect)",
    "remote-perfect-aspect": "Verb (Aspect)",
    "remote-perfect-aspect-neg": "Verb (Aspect)",
    "iterative-aspect": "Verb (Aspect)",
    "iterative-future-aspect": "Verb (Aspect)",
    "iterative-past-aspect": "Verb (Aspect)",
    "iterative-present-aspect": "Verb (Aspect)",
    "emphatic-iterative-future-aspect": "Verb (Aspect)",
    "emphatic-iterative-past-aspect": "Verb (Aspect)",
    "habitual-aspect": "Verb (Aspect)",
    "cvb-adv-part-absolute": "Verb (Adverbial Participle)",
    "cvb-adv-part-conditional": "Verb (Adverbial Participle)",
    "cvb-adv-part-future": "Verb (Adverbial Participle)",
    "cvb-adv-part-past": "Verb (Adverbial Participle)",
    "cvb-adv-part-past-simul": "Verb (Adverbial Participle)",
    "cvb-adv-part-simul": "Verb (Adverbial Participle)",

    # Adjectives & Adverbs
    "adj": "Adjective",
    "adv": "Adverb",
    "adv-clause-rp-past": "Adverbial Clause",
    "adv-clause-rp-past-neg": "Adverbial Clause",
    "adv-clause-rp-present": "Adverbial Clause",
    "adv-clause-rp-present-neg": "Adverbial Clause",
    "indeclinable": "Indeclinable",

    # Conjunctions, Postpositions & Related Function Words
    "cnj": "Conjunction",
    "coordinative": "Conjunction",
    "concessive": "Conjunction",
    "postp": "Postposition",

    # Miscellaneous / Other Categories
    "aff": "Affirmative",
    "deriv": "Derviative",
    "eng": "English",
    "fw": "Foreign/Language",
    "sanskrit": "Sanskrit orig.",
    "neg": "Negation"
}

def classify_pos(pos_tags):
    """
    Given a list of detailed POS tags, return a list of unique layman categories.
    If a tag is not in our mapping, it's classified as 'Other'.
    """
    layman_categories = set()
    for tag in pos_tags:
        category = pos_to_layman.get(tag, "Other")
        layman_categories.add(category)
    return list(layman_categories)

def process_json(json_path, output_path):
    # Load JSON data from file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each entry in the data
    for entry in tqdm(data, desc="Processing entries"):
        morphology = entry.get("morphology", {})
        # Initialize an empty set for POS tags from all morphemes
        detailed_pos_tags = set()
        
        if morphology != 'No morphemes found':
            morphemes_list = morphology.get("morphemes", [])
            for morpheme in morphemes_list:
                pos_list = morpheme.get("pos", [])
                for pos in pos_list:
                    detailed_pos_tags.add(pos)
                    
        # Classify the collected POS tags into layman categories
        entry["layman"] = classify_pos(list(detailed_pos_tags))
        
    # Write the updated data back to a new JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Processed data has been saved to {output_path}")

if __name__ == "__main__":
    input_json = "lexicons.json"  # Input JSON file
    output_json = "lexicons_with_layman.json"  # Output JSON file
    process_json(input_json, output_json)

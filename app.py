import streamlit as st
import pandas as pd
import json
from tqdm import tqdm


st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    /* Adjust the top padding of the main container */
    .block-container {
        padding-top: 1rem;  /* Adjust as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Malayalam Lexicon Explorer")
# Custom CSS for top padding


# Load JSON data from local file (the new JSON with "layman" attribute)
@st.cache_data
def load_data():
    with open("lexicons_with_layman.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Build DataFrame from JSON data
def json_to_dataframe(data):
    records = []
    for entry in tqdm(data, desc="Building records"):
        word = entry.get("word", "")
        ipa = ", ".join(entry.get("ipa", []))
        morphemes = entry.get("morphology", {})
        if morphemes == 'No morphemes found':
            root = "unk"
            pos = "unk"
            weight = "unk"
        else:
            weight = morphemes.get("weight", "")
            morphemes_list = morphemes.get("morphemes", [])
            if morphemes_list:
                root = morphemes_list[0].get("root", "")
                pos = ", ".join(morphemes_list[0].get("pos", []))
            else:
                root, pos = "unk", "unk"
        # Join the layman categories list into a string for display/filtering
        layman = ", ".join(entry.get("layman", []))
        records.append({
            "Word": word,
            "IPA": ipa,
            "Root": root,
            "POS": pos,
            "Weight": weight,
            "Layman": layman
        })
    df = pd.DataFrame(records)
    return df

# Load the new JSON data
data = load_data()

# Extract unique layman categories from the data
unique_layman = set()
for entry in data:
    for cat in entry.get("layman", []):
        unique_layman.add(cat)
layman_options = sorted(unique_layman)
layman_options.insert(0, "All")  # Insert "All" as the first option

# Show limited options initially
num_shown = 10  # Number of categories to show initially
show_all = st.toggle("Show More Categories", value=False)

if not show_all:
    layman_display = layman_options[:num_shown]  # Show first 10
else:
    layman_display = layman_options  # Show all if toggled

# Pills for filtering by layman category
selected_filter = st.pills(
    options=layman_display,
    label="Filter by Layman Category",
)

# Build the DataFrame from data
df = json_to_dataframe(data)

# If a specific layman category is selected (other than "All"), filter the DataFrame.
if selected_filter and selected_filter != "All":
    # We filter by checking if the selected filter appears in the "Layman" column.
    df = df[df["Layman"].str.contains(selected_filter)]

# Pagination setup
page_size = 100
total_pages = len(df) // page_size + (1 if len(df) % page_size else 0)
page = st.number_input("Page", min_value=1, max_value=total_pages, step=1, value=1)
st.text(f"Total pages: {total_pages}")
start_idx = (page - 1) * page_size
end_idx = start_idx + page_size

# Display the paginated table
st.dataframe(df.iloc[start_idx:end_idx].drop(columns=["Weight","Layman"]), 
             height=600, 
             use_container_width=True,
             column_config={
                "IPA":st.column_config.TextColumn(help="International Phonetic Alphabet"),
                "POS":st.column_config.ListColumn(
                "Parts of Speech",
                help="Parts of speech tags.",
                width="medium"
                ),

             }
        )

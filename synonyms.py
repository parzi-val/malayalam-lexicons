from dotenv import load_dotenv
import os
import google.generativeai as genai
import textwrap
load_dotenv()



class SynonymsAndTranslation:
    def __init__(self):
        api_key = os.getenv("GENAI_KEY")
        genai.configure(api_key=api_key)

        synonym = genai.protos.Schema(
            type=genai.protos.Type.STRING
        )
        synonyms = genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=synonym
        )
        extract = genai.protos.FunctionDeclaration(
            name="add_to_database",
            description=textwrap.dedent("""\
            Adds entities to the database.
            """),
            parameters = genai.protos.Schema(
                type= genai.protos.Type.OBJECT,
                properties= {
                    'unknown': genai.protos.Schema(
                        type=genai.protos.Type.BOOLEAN
                    ),
                    'synonyms': synonyms,
                    'meaning': genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    )
                }
            )
        )
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest",tools=[extract],
                                    system_instruction="You are an expert linguist. Your task is to either translate or provide with synonyms.")
        
    def extract(self,word):
        result= self.model.generate_content(f"Analyse the word {word},IF YOU DONT UNDERSTAND IS SIMPLY RETURN TRUE FOR UNKNOWN else return the meaning in ENGLISH. If the word is not a proper noun, return 3 synonyms in MALAYALAM. else return 0.")
        fc = result.candidates[0].content.parts[0].function_call
        print(result)
        data = type(fc).to_dict(fc)
        print(data)
        return data["args"] if "args" in data else None


if __name__ == "__main__":
    synonyms = SynonymsAndTranslation()
    print(synonyms.extract("വേലുനായ്ക്കരെ"))

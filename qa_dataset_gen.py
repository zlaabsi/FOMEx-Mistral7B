import os
from openai import OpenAI
import json

#from dotenv import load_dotenv  

# Load environment variables from .env file
#load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Initialiser le client OpenAI avec la clé 

client = OpenAI(api_key = OPENAI_API_KEY)

# Initialiser DuckDuckGo Search
#search = DuckDuckGoSearchRun()

def gen_val_qa_pairs(topic, num_pairs):
    questions = []

    for _ in range(num_pairs):
        # Générer une question et une réponse
        prompt = f"""Create a very complex and challenging question and answer dataset 
        in JSON about this topic: {topic}.
        The purpose of this QA dataset is to fine-tune a large language model"""

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # Remplacer par le modèle souhaité
            #response_format={ "type": "json_object" },
            messages=[{"role": "user", "content": prompt}]
        )
        # Accéder correctement au contenu du message
        if chat_completion.choices:
            message = chat_completion.choices[0].message
            if message.content:
                qa_pair = message.content.strip()
                questions.append(qa_pair)  # Ajouter la paire question-réponse générée
            else:
                questions.append("No content found in message.")

    return questions


topic = "machine learning"
qa_dataset = gen_val_qa_pairs(topic, 1)
#(qa_dataset)

# Enregistrer le dataset dans un fichier JSON
file_name = 'qa_dataset.json'
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(qa_dataset, file, ensure_ascii=False)

print(f"Le dataset a été enregistré dans {file_name}.")


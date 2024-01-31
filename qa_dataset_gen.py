import os
from openai import OpenAI
import pandas as pd
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
    qa_pairs = []

    for _ in range(num_pairs):
        # Générer une question
        prompt_question = f"Generate a complex question about {topic}."
        response_question = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_question}]
        )
        question = response_question.choices[0].message.content.strip()

        # Générer une réponse à la question
        prompt_answer = f"Answer the following question in detail: {question}"
        response_answer = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_answer}]
        )
        answer = response_answer.choices[0].message.content.strip()

        qa_pairs.append({"question": question, "answer": answer})

    return qa_pairs

# Génération des paires question-réponse
topic = "machine learning"
qa_pairs = gen_val_qa_pairs(topic, 5)  # Générer 5 paires pour l'exemple

# Conversion en DataFrame pandas
qa_df = pd.DataFrame(qa_pairs)

# Affichage du DataFrame
print(qa_df)

# Enregistrement du DataFrame dans un fichier CSV, si nécessaire
#qa_df.to_csv('qa_dataset.csv', index=False)

# Enregistrer le dataset dans un fichier JSON
#file_name = 'qa_dataset.json'
#with open(file_name, 'w', encoding='utf-8') as file:
#    json.dump(qa_dataset, file, ensure_ascii=False)

#print(f"Le dataset a été enregistré dans {file_name}.")


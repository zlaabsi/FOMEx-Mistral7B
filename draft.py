

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun


llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)


----
# First, update the import statement for DuckDuckGoSearchRun based on the deprecation warning
from langchain_community.tools import DuckDuckGoSearchRun

# Next, adjust the OpenAI API call based on the new version
import openai
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Initialize DuckDuckGo Search
search = DuckDuckGoSearchRun()

def gen_val_qa_pairs(topic, num_pairs):
    questions = []
    answers = []

    for _ in range(num_pairs):
        # Generate question
        prompt = f"""Create a very complex and challenging question and answer dataset 
        in JSON about this topic: {topic}.
        The purpose of this QA dataset is to fine-tune a large language model"""
        response = openai.Completion.create(
            engine="davinci",  # Replace with your desired model, e.g., "text-davinci-004"
            prompt=prompt,
            max_tokens=50,  # Response length
            temperature=0,  # Adjust for creativity
            top_p=1,  # Control response diversity
            frequency_penalty=0,  # Fine-tune word frequency
            presence_penalty=0  # Fine-tune word presence
        )
        question = response.choices[0].text.strip()

        # Validate answer with DuckDuckGo search
        results = search.run(question)
        validated_answer = "Sample process to extract and validate answer"

        questions.append(question)
        answers.append(validated_answer)

    return questions, answers

topic = "machine learning"
qa_dataset = gen_val_qa_pairs(topic, 500)

# This script addresses the issues in your original script.
# Remember to replace "davinci" with the specific model name you want to use, such as "text-davinci-004". 
# The "Sample process to extract and validate answer" should be replaced with your own logic for processing the search results.

#-----------------------------------------------
import os
from openai import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialiser le client OpenAI avec la clé API
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialiser DuckDuckGo Search
search = DuckDuckGoSearchRun()

def gen_val_qa_pairs(topic, num_pairs):
    questions = []
    answers = []

    for _ in range(num_pairs):
        # Générer une question
        prompt = f"""Create a very complex and challenging question and answer dataset 
        in JSON about this topic: {topic}.
        The purpose of this QA dataset is to fine-tune a large language model"""

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Remplacer par le modèle souhaité
            messages=[{"role": "user", "content": prompt}]
        )
        question = chat_completion.choices[0].message['content'].strip()

        # Valider la réponse avec une recherche DuckDuckGo
        results = search.run(question)
        validated_answer = "Processus d'extraction et de validation de la réponse à partir des résultats de recherche"

        questions.append(question)
        answers.append(validated_answer)

    return questions, answers

topic = "machine learning"
qa_dataset = gen_val_qa_pairs(topic, 500)


#----------------------
   # Accéder correctement au contenu du message
        if chat_completion.choices:
            message = chat_completion.choices[0].message
            if message.content:
                questions = message.content.strip('\n', 1)
                questions.append(questions)  # Ajouter la paire question-réponse générée
            else:
                questions.append("No content found in message.")

    return questions

#---------

def gen_val_qa_pairs(topic, num_pairs):
    qa_pairs = []

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
            content = chat_completion.choices[0].message.content.strip()
            question, answer = content.split('\n', 1)
            qa_pairs.append({"question": question, "answer": answer})

    return qa_pairs


topic = "machine learning"
qa_dataset = gen_val_qa_pairs(topic, 1)

df = pd.DataFrame(qa_dataset)

print(df)


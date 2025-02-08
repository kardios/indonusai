import streamlit as st
import requests
import os
import time
import telebot
from openai import OpenAI
from st_copy_to_clipboard import st_copy_to_clipboard

# Set up Telegram Bot
recipient_user_id = os.environ['RECIPIENT_USER_ID']
bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

# Retrieve the API key from the environment variables
client_openai = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

friendli_url = "https://api.friendli.ai/dedicated/v1/chat/completions"
friendli_model = os.environ['FRIENDLI_MODEL_CODE']
friendli_token = os.environ['FRIENDLI_TOKEN_CODE']

st.set_page_config(page_title="Indochina and Nusantara AI", page_icon=":earth_asia:")
st.write("**Indochina and Nusantara AI** :earth_asia:")
st.image("sea-satellite-map.jpg")
Instruct_Option = st.selectbox("What would you like to do?", ('Bullet Point Summary', 'Comprehensive Evaluation', 'Cultural Nuances', 'Customise Instruction'))

if Instruct_Option == "Bullet Point Summary":
  instruction = "You are an expert in Southeast Asian languages and excellent at summarizing information. Your task is to read the text in the <input> tags and produce an English language summary. Identify the main ideas and key details, and condense them into concise bullet points. Recognize the overall structure of the text and create bullet points that reflect this structure. For the presentation of the output, start by identifying what language the input is in, followed by the bullet points. Present the points in a clear and organised way, and do not provide any titles."
elif Instruct_Option == "Comprehensive evaluation":
  instruction = "You will read the input I provide. Comprehensively evaluate the input across four dimensions.\n\nSummary: Provide a concise overview capturing the main ideas and key details of the text.\n\nBalance: Assess whether the text presents multiple viewpoints, and identify any biased, missing, or opposing perspectives.\n\nSignificance: Explain why the content of the text is important in a broader context, and discuss how it relates to larger trends or issues.\n\nImplications: Highlight the potential outcomes or consequences stemming from the findings or arguments in the text."
elif Instruct_Option == "Cultural Nuances":
  instruction = "Analyze the vernacular text provided below and identify the cultural nuances it reflects. Present your output in bullet points."
elif Instruct_Option == "Customise Instruction":
  instruction = "You are my reading assistant. You will read the input I provide." + st.text_input("Customise your own unique prompt:", "Identify the language used and rate the quality of the language upon 10.")

input_text = st.text_area("Enter the vernacular input source and click **Let\'s Go :rocket:**")
if st.button("Let\'s Go! :rocket:") and input_text.strip() != "":
  with st.spinner("Running AI Model..."):
    start = time.time()
    prompt = instruction + "\n\n" + input_text
    payload = {"messages": [{"content": "You are a helpful and informative assistant.", "role": "system"},
                            {"content": instruction + "\n\n" + input_text, "role": "user"}],
               "model": friendli_model}
    headers = {"Authorization": f"Bearer {friendli_token}", "Content-Type": "application/json"}
    response = requests.request("POST", friendli_url, json=payload, headers=headers)
    response_json = response.json()
    output_text = response_json["choices"][0]["message"]["content"]            
    end = time.time()

    with st.expander("Output", expanded = True):
      st.write(output_text)
      st_copy_to_clipboard(output_text)
  

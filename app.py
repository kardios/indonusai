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
friendli_model = os.environ['FRIENDLI_MODEL']
friendli_token = os.environ['FRIENDLI_TOKEN']

st.set_page_config(page_title="Indochina and Nusantara AI", page_icon=":earth_asia:")
st.write("**Indochina and Nusantara AI** :earth_asia:")
#st.image("sea-satellite-map.jpg")
Instruct_Option = st.selectbox("What would you like to do?", ('Bullet Point Summary', 'Comprehensive Evaluation', 'Cultural Nuances', 'Customise Instruction'))

if Instruct_Option == "Bullet Point Summary":
  instruction = "You are an expert in Southeast Asian languages and excellent at summarizing information. Your task is to read the text in the <input> tags and produce an English language summary. Identify the main ideas and key details, and condense them into concise bullet points. Recognize the overall structure of the text and create bullet points that reflect this structure. For the presentation of the output, start by identifying what language the input is in, followed by the bullet points. Present the points in a clear and organised way, and do not provide any titles."

elif Instruct_Option == "Comprehensive Evaluation":
  instruction = "You will read the input I provide in the <input> tags. Comprehensively evaluate the input across four dimensions.\n\nSummary: Provide a concise overview capturing the main ideas and key details of the text.\n\nBalance: Assess whether the text presents multiple viewpoints, and identify any biased, missing, or opposing perspectives.\n\nSignificance: Explain why the content of the text is important in a broader context, and discuss how it relates to larger trends or issues.\n\nImplications: Highlight the potential outcomes or consequences stemming from the findings or arguments in the text."

elif Instruct_Option == "Cultural Nuances":
  instruction = """### CONTEXT
You are a renowned expert in Southeast Asian history, culture, and society. Your role is to provide detailed insights into a vernacular language text.
### TASK
Analyze the vernacular text provided within the `<input>` tags by following these steps:
- **Identify Cultural References:** Detect idiomatic expressions, slang, or colloquial language that allude to specific cultural practices, beliefs, or traditions.
- **Examine Contextual Nuances:** Assess how historical, social, or regional influences are reflected in the text.
- **Highlight Linguistic Choices:** Note any specific word choices or phrases that reveal aspects of cultural identity or traditional influences.
### OUTPUT
Present your findings as a series of clear, concise bullet points, with each point describing a distinct cultural nuance or reference."""

elif Instruct_Option == "Customise Instruction":
  instruction = "You are my reading assistant. You will read the input I provide in the <input> tags." + st.text_input("Customise your own unique prompt:", "Identify the language used and rate the quality of the language upon 10.")

input_text = st.text_area("Enter the vernacular input source and click **Let\'s Go :rocket:**")
if st.button("Let\'s Go! :rocket:") and input_text.strip() != "":
  with st.spinner("Running AI Model..."):

    prompt = instruction + "\n\n<input>\n\n" + input_text + "</input>"
    combined_output = "\n\n"
    
    start = time.time()
    payload = {"messages": [{"content": "You are a helpful and informative assistant. Your output is always in English language.", "role": "system"},
                            {"content": prompt, "role": "user"}],
               "model": friendli_model,
               "max_tokens": 8192,
               "temperature": 0,
               "top_p": 0.8}
    headers = {"Authorization": f"Bearer {friendli_token}", "Content-Type": "application/json"}
    response = requests.request("POST", friendli_url, json=payload, headers=headers)
    response_json = response.json()
    output_text = response_json["choices"][0]["message"]["content"]      
    combined_output = combined_output + "<answer_sea-lion>\n\n" + output_text + "\n\n</answer_sea-lion>\n\n"
    end = time.time()

    #with st.expander("Response", expanded = False):
    #  st.write(response.text)

    with st.expander("Output - gemma2-9b-cpt-sea-lionv3-instruct", expanded = True):
      st.write(output_text)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(output_text)

    start = time.time()
    response = client_openai.chat.completions.create(model="gpt-4o-2024-11-20", messages=[{"role": "system", "content": "You are a helpful and informative assistant. Your output is always in English language."},
                                                                                          {"role": "user", "content": prompt}], temperature=0)
    output_text = response.choices[0].message.content
    combined_output = combined_output + "<answer_gpt-4o>\n\n" + output_text + "\n\n</answer_gpt-4o>\n\n"
    end = time.time()
    with st.expander("Output - gpt-4o-2024-11-20", expanded = True):
      st.write(output_text)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(output_text)

    st_copy_to_clipboard(combined_output)

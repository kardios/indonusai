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
Instruct_Option = st.selectbox("What are your instructions?", ('Bullet Point Summary', 'Comprehensive Evaluation', 'Identify Nuances', 'Custom'))

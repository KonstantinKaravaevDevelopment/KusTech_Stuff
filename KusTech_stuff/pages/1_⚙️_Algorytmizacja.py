import requests
from PIL import Image
import os

import streamlit as st
from streamlit_lottie import st_lottie

#Dodajemy Icone
file_path = os.path.join("images", "Icon_webpage.png")
ikonka = Image.open(file_path)

st.set_page_config(
    page_title='Kompetencje',
    page_icon=ikonka,
    layout='wide',
    
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_rocket = load_lottieurl('https://lottie.host/c6a39c47-7387-4b0b-b7a3-1b2e9c4d9f13/8mLeR8dPTh.json')

with st.container():
    st.header('Will be soon!')
    st.subheader('Projekt zostanie dodany  we wrzesniu.')
    st.write("---")
    st_lottie(lottie_rocket, height=400, key='coding')
